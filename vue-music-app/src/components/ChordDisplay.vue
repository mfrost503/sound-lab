<template>
  <div class="chord-display" v-if="chord.length">
    <div class="header">
      <h3>{{ note }} {{ formattedChordType }} Chord</h3>
      <button @click="playChord" :disabled="isPlaying" class="play-chord-button">Play Chord</button>
    </div>
    <div class="notes-container">
      <div class="note" v-for="(note, index) in chord" :key="index" @click="playNote(note, index)" :class="{ playing: playingIndex === index }">
        {{ note }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref, watch, computed } from 'vue';

const props = defineProps({
  chord: {
    type: Array as () => string[],
    required: true,
  },
  note: {
    type: String,
    required: true,
  },
  chordType: {
    type: String,
    required: true,
  },
  octave: {
    type: Number,
    required: true,
  },
});

const formattedChordType = computed(() => {
  if (!props.chordType) return '';
  return props.chordType.charAt(0).toUpperCase() + props.chordType.slice(1);
});

const soundFileMapping: { [key: string]: string } = {
  'C#': 'Db',
  'D#': 'Eb',
  'F#': 'Gb',
  'G#': 'Ab',
  'A#': 'Bb',
};

const playingIndex = ref<number | null>(null);
const isPlaying = ref(false);
const audioCache = ref<HTMLAudioElement[]>([]);

watch(() => [props.chord, props.octave], ([newChord, newOctave]) => {
  audioCache.value = newChord.map(note => {
    const soundFileNote = soundFileMapping[note] || note;
    return new Audio(`/sounds/${soundFileNote}${newOctave}.mp3`);
  });
}, { immediate: true, deep: true });

const playNote = (note: string, index: number) => {
  const audio = audioCache.value[index];
  if (audio) {
    audio.currentTime = 0;
    audio.play();
  }

  playingIndex.value = index;
  setTimeout(() => {
    playingIndex.value = null;
  }, 300);
};

const playChord = () => {
  isPlaying.value = true;
  audioCache.value.forEach(audio => {
    audio.currentTime = 0;
    audio.play();
  });

  // Set a timeout to reset the isPlaying flag
  setTimeout(() => {
    isPlaying.value = false;
  }, 1000); // Adjust timeout as needed
};
</script>

<style scoped>
.chord-display {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 20px;
}

.notes-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.note {
  padding: 10px 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: box-shadow 0.1s ease-in-out;
}

.note.playing {
  box-shadow: 0 0 10px 5px rgba(173, 216, 230, 0.7);
}



.play-chord-button {
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
</style>
