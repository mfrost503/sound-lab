<template>
  <div class="view-container">
    <h1>Chord Progressions</h1>
    <div class="controls">
      <div class="progression-mode-tabs">
        <button
          :class="{ active: progressionMode === 'generated' }"
          @click="progressionMode = 'generated'"
        >
          Generated Progressions
        </button>
        <button
          :class="{ active: progressionMode === 'custom' }"
          @click="progressionMode = 'custom'"
        >
          Custom Progression
        </button>
      </div>

      <div v-if="progressionMode === 'generated'" class="generated-controls">
        <div class="control-group">
          <label for="key-select">Select a Key:</label>
          <select id="key-select" v-model="selectedKey" @change="generateProgressions">
            <option v-for="key in keys" :key="key" :value="key">{{ key }}</option>
          </select>
        </div>
        <div class="control-group">
          <label for="progression-select">Select a Progression:</label>
          <select id="progression-select" v-model="selectedProgressionName">
            <option v-for="progression in progressions" :key="progression.name" :value="progression.name">{{ progression.name }}</option>
          </select>
        </div>
      </div>

      <div v-else-if="progressionMode === 'custom'" class="custom-controls">
        <ProgressionBuilder @progression-updated="handleBuiltProgression" />
      </div>
    </div>
    <ProgressionDisplay v-if="displayedProgression" :progression="displayedProgression" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import ProgressionDisplay from '../components/ProgressionDisplay.vue';
import ProgressionBuilder from '../components/ProgressionBuilder.vue';

const keys = ['Ab', 'A', 'A#', 'Bb', 'B', 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#'];
const selectedKey = ref('C');
const progressions = ref<{ name: string; progression: string[] }[]>([]);
const selectedProgressionName = ref('I-V-vi-IV');
const userBuiltProgression = ref<string[]>([]);
const progressionMode = ref('generated'); // 'generated' or 'custom'

const getScale = (key: string, scaleType: 'major' | 'minor') => {
  const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  const flatToSharp: { [key: string]: string } = {
    'Ab': 'G#',
    'Bb': 'A#',
    'Db': 'C#',
    'Eb': 'D#',
    'Gb': 'F#',
  };
  const normalizedKey = flatToSharp[key] || key;
  const majorIntervals = [0, 2, 4, 5, 7, 9, 11];
  const minorIntervals = [0, 2, 3, 5, 7, 8, 10];
  const intervals = scaleType === 'major' ? majorIntervals : minorIntervals;
  const startIndex = notes.indexOf(normalizedKey);
  if (startIndex === -1) return [];

  const scale = intervals.map(interval => notes[(startIndex + interval) % 12]);
  return scale;
};

const generateProgressions = () => {
  const sharpToFlat: { [key: string]: string } = {
    'G#': 'Ab',
    'A#': 'Bb',
    'C#': 'Db',
    'D#': 'Eb',
    'F#': 'Gb',
  };
  const flatKeys = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb'];
  const isFlatKey = flatKeys.includes(selectedKey.value);

  let majorScale = getScale(selectedKey.value, 'major');
  if (majorScale.length === 0) return;

  if (isFlatKey) {
    majorScale = majorScale.map(note => sharpToFlat[note] || note);
  }

  const I = majorScale[0];
  const ii = majorScale[1] + 'm';
  const IV = majorScale[3];
  const V = majorScale[4];
  const vi = majorScale[5] + 'm';

  progressions.value = [
    { name: 'I-V-vi-IV', progression: [I, V, vi, IV] },
    { name: 'I-IV-V', progression: [I, IV, V] },
    { name: 'vi-IV-I-V', progression: [vi, IV, I, V] },
    { name: 'I-vi-IV-V', progression: [I, vi, IV, V] },
    { name: 'ii-V-I', progression: [ii, V, I] },
  ];
};

const handleBuiltProgression = (progression: string[]) => {
  userBuiltProgression.value = progression;
};

const displayedProgression = computed(() => {
  if (progressionMode.value === 'custom') {
    return userBuiltProgression.value;
  } else {
    const found = progressions.value.find(p => p.name === selectedProgressionName.value);
    return found ? found.progression : [];
  }
});

watch(progressionMode, (newMode) => {
  if (newMode === 'generated') {
    generateProgressions();
  }
});

generateProgressions();
</script>

<style scoped>
.view-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 2rem;
  gap: 20px;
}

.controls {
  display: flex;
  flex-direction: column; /* Stack the control groups */
  gap: 15px;
  align-items: center;
}

.control-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

label {
  font-weight: bold;
}

.generated-controls, .custom-controls {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: center;
  width: 100%;
}

.progression-mode-tabs {
  display: flex;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  overflow: hidden;
}

.progression-mode-tabs button {
  padding: 10px 15px;
  border: none;
  background-color: #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}

.progression-mode-tabs button.active {
  background-color: #007bff;
  color: white;
}

.progression-mode-tabs button:not(.active):hover {
  background-color: #e2e6ea;
}
</style>
