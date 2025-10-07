<template>
  <div class="chord-detector">
    <h2>Chord Detector</h2>
    <button @click="toggleDetection" :class="{ 'start-button': !isDetecting, 'stop-button': isDetecting }">
      {{ isDetecting ? 'Stop Detection' : 'Start Detection' }}
    </button>
    <p v-if="isDetecting">Listening for chords...</p>
    <p v-if="detectedChord">Detected: {{ detectedChord }}</p>
    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue';

const isDetecting = ref(false);
const detectedChord = ref('');
const error = ref('');

let audioContext: AudioContext | null = null;
let analyser: AnalyserNode | null = null;
let microphone: MediaStreamAudioSourceNode | null = null;
let scriptProcessor: ScriptProcessorNode | null = null;

const toggleDetection = async () => {
  if (isDetecting.value) {
    stopDetection();
  } else {
    startDetection();
  }
};

const startDetection = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    microphone = audioContext.createMediaStreamSource(stream);
    scriptProcessor = audioContext.createScriptProcessor(2048, 1, 1); // Buffer size, input channels, output channels

    analyser.smoothingTimeConstant = 0.8;
    analyser.fftSize = 1024;

    microphone.connect(analyser);
    analyser.connect(scriptProcessor);
    scriptProcessor.connect(audioContext.destination);

    scriptProcessor.onaudioprocess = () => {
      const bufferLength = analyser!.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);
      analyser!.getByteFrequencyData(dataArray);

      // Basic pitch detection (very rudimentary, needs a proper algorithm)
      let maxVolume = 0;
      let maxIndex = -1;
      for (let i = 0; i < bufferLength; i++) {
        if (dataArray[i] > maxVolume) {
          maxVolume = dataArray[i];
          maxIndex = i;
        }
      }

      if (maxIndex > -1 && maxVolume > 100) { // Simple threshold
        const nyquist = audioContext!.sampleRate / 2;
        const frequency = maxIndex * nyquist / bufferLength;
        // This is a very basic frequency to note conversion, needs refinement
        const note = frequencyToNote(frequency);
        detectedChord.value = note; // For now, just display the note
      } else {
        detectedChord.value = '';
      }
    };

    isDetecting.value = true;
    error.value = '';
  } catch (err: any) {
    error.value = 'Error accessing microphone: ' + err.message;
    console.error(err);
  }
};

const stopDetection = () => {
  isDetecting.value = false;
  detectedChord.value = '';
  if (microphone) {
    microphone.disconnect();
    microphone.mediaStream.getTracks().forEach(track => track.stop());
  }
  if (analyser) analyser.disconnect();
  if (scriptProcessor) scriptProcessor.disconnect();
  if (audioContext) audioContext.close();
  audioContext = null;
  analyser = null;
  microphone = null;
  scriptProcessor = null;
};

const frequencyToNote = (frequency: number): string => {
  const A4 = 440;
  const C0 = A4 * Math.pow(2, -4.75);
  const noteStrings = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  const semitone = 12 * Math.log2(frequency / C0);
  const noteIndex = Math.round(semitone) % 12;
  const octave = Math.floor(semitone / 12);
  return noteStrings[noteIndex] + octave;
};

onUnmounted(() => {
  stopDetection();
});
</script>

<style scoped>
.chord-detector {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
  text-align: center;
}

.start-button {
  background: linear-gradient(to right, #ff69b4, #8a2be2); /* Pink to Purple Gradient */
  color: white;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
  border: 2px solid black;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  font-size: 1.2rem;
}

.stop-button {
  background-color: #f44336; /* Red */
  color: white;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
  border: 2px solid black;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  font-size: 1.2rem;
}
</style>
