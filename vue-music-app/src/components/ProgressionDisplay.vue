<template>
  <div class="progression-display" v-if="progression.length">
    <div class="header">
      <button @click="playProgression" :disabled="isPlaying" class="play-progression-button">Play Progression</button>
      <select v-model="selectedSpeed">
        <option v-for="speed in speeds" :key="speed.name" :value="speed">{{ speed.name }}</option>
      </select>
    </div>
    <div class="chords-container">
      <div class="chord" v-for="(chord, index) in progression" :key="index" @click="playChord(chord, index, props.octave)" :class="{ playing: playingIndex === index }">
        {{ chord }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue';

const props = defineProps({
  progression: {
    type: Array as () => string[],
    required: true,
  },
  octave: {
    type: Number,
    default: 4,
  },
});

const speeds = [
  { name: 'Quarter', plays: 1, gap: 1000 },
  { name: 'Eighth', plays: 2, gap: 500 },
  { name: 'Sixteenth', plays: 4, gap: 250 },
];

const selectedSpeed = ref(speeds[0]);
const playingIndex = ref<number | null>(null);
const isPlaying = ref(false);

const soundFileMapping: { [key: string]: string } = {
  'C#': 'Db',
  'D#': 'Eb',
  'F#': 'Gb',
  'G#': 'Ab',
  'A#': 'Bb',
};

const noteToValueMap: { [key: string]: number } = {
  'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
};

const playChord = async (chordName: string, index: number, initialOctave: number) => {
  const chordRegex = /^([A-G][b#]?)(.*)$/;
  const match = chordName.match(chordRegex);

  if (!match) {
    console.error("Invalid chord name format:", chordName);
    return;
  }

  let rootNote = match[1];
  let chordType = match[2] || 'major'; // Default to major if no suffix

  // Handle cases where chordType might be just 'm' for minor
  if (chordType === 'm') {
    chordType = 'minor';
  }

  try {
    const response = await fetch(`http://localhost:8000/chord/${chordType}/${rootNote}`);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch chord');
    }
    const data = await response.json();
    const chordNotes = data.chord;

    if (!chordNotes.length) return;

    const audioElements = chordNotes.map((note: string) => {
      const soundFileNote = soundFileMapping[note] || note;
      return new Audio(`/sounds/${soundFileNote}${initialOctave}.mp3`);
    });

    audioElements.forEach(audio => {
      audio.currentTime = 0;
      audio.play();
    });

    playingIndex.value = index;
    setTimeout(() => {
      playingIndex.value = null;
    }, 300);
  } catch (err: any) {
    console.error("Error playing chord:", err);
  }
};

const playChordWithRepetitions = async (chordName: string, index: number, plays: number, gap: number, initialOctave: number) => {
  let repetition = 0;
  const play = async () => {
    if (repetition < plays) {
      await playChord(chordName, index, initialOctave);
      repetition++;
      setTimeout(play, gap);
    }
  };
  play();
};

const playProgression = () => {
  isPlaying.value = true;
  let progressionIndex = 0;

  const playNextChordInProgression = async () => {
    if (progressionIndex < props.progression.length) {
      const chordName = props.progression[progressionIndex];
      const { plays, gap } = selectedSpeed.value;
      
      await playChordWithRepetitions(chordName, progressionIndex, plays, gap, props.octave);
      progressionIndex++;

      setTimeout(playNextChordInProgression, plays * gap);
    } else {
      // Add a delay before setting isPlaying to false to allow the last chord to finish.
      setTimeout(() => {
        isPlaying.value = false;
      }, selectedSpeed.value.plays * selectedSpeed.value.gap);
    }
  };

  playNextChordInProgression();
};

</script>

<style scoped>
.progression-display {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.header {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 20px;
}

.chords-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chord {
  padding: 20px 30px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: box-shadow 0.1s ease-in-out;
  font-size: 1.5rem;
  font-weight: bold;
}

.chord.playing {
  box-shadow: 0 0 10px 5px rgba(173, 216, 230, 0.7);
}

.play-progression-button {
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
