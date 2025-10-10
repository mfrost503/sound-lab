<template>
  <div class="progression-builder">
    <h2>Build Your Progression</h2>
    <div class="chord-selector">
      <select v-model="selectedKey">
        <option v-for="k in keys" :key="k" :value="k">{{ k }}</option>
      </select>
      <select v-model="selectedRomanNumeral">
        <option v-for="rn in romanNumerals" :key="rn" :value="rn">{{ rn }}</option>
      </select>
      <select v-model.number="selectedOctave">
        <option v-for="o in 7" :key="o" :value="o">{{ o }}</option>
      </select>
      <button @click="addChordToProgression">Add Chord</button>
    </div>

    <div class="current-progression">
      <h3>Current Progression:</h3>
      <div class="progression-list">
        <div v-for="(chord, index) in builtProgression" :key="index" class="built-chord">
          {{ chord }}
          <button @click="removeChordFromProgression(index)">x</button>
        </div>
      </div>
      <button @click="clearProgression" v-if="builtProgression.length">Clear Progression</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, watch } from 'vue';

const keys = ['Ab', 'A', 'A#', 'Bb', 'B', 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#'];
const romanNumerals = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii'];

const selectedKey = ref('C');
const selectedRomanNumeral = ref('I');
const selectedOctave = ref(4);
const builtProgression = ref<string[]>([]);

const emit = defineEmits(['progression-updated']);

const getScaleNotes = async (key: string) => {
  try {
    const encodedKey = encodeURIComponent(key);
    const response = await fetch(`http://localhost:8000/scale/major/${encodedKey}`);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch scale');
    }
    const data = await response.json();
    return data.scale;
  } catch (err) {
    console.error("Error fetching scale notes:", err);
    return [];
  }
};

const addChordToProgression = async () => {
  const scaleNotes = await getScaleNotes(selectedKey.value);
  if (scaleNotes.length === 0) return;

  let chordName = '';
  switch (selectedRomanNumeral.value) {
    case 'I':
      chordName = scaleNotes[0];
      break;
    case 'ii':
      chordName = scaleNotes[1] + 'm';
      break;
    case 'iii':
      chordName = scaleNotes[2] + 'm';
      break;
    case 'IV':
      chordName = scaleNotes[3];
      break;
    case 'V':
      chordName = scaleNotes[4];
      break;
    case 'vi':
      chordName = scaleNotes[5] + 'm';
      break;
    case 'vii':
      chordName = scaleNotes[6] + 'dim'; // Assuming diminished for vii
      break;
  }
  if (chordName) {
    builtProgression.value.push(chordName);
    emit('progression-updated', { progression: builtProgression.value, octave: selectedOctave.value });
  }
};

const removeChordFromProgression = (index: number) => {
  builtProgression.value.splice(index, 1);
  emit('progression-updated', { progression: builtProgression.value, octave: selectedOctave.value });
};

const clearProgression = () => {
  builtProgression.value = [];
  emit('progression-updated', { progression: builtProgression.value, octave: selectedOctave.value });
};

watch([builtProgression, selectedOctave], ([newProgression, newOctave]) => {
  emit('progression-updated', { progression: newProgression, octave: newOctave });
}, { deep: true });

</script>

<style scoped>
.progression-builder {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chord-selector {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  align-items: center;
}

.chord-selector select, .chord-selector button {
  padding: 8px 12px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.chord-selector button {
  background: linear-gradient(to right, #ff69b4, #8a2be2); /* Pink to Purple Gradient */
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chord-selector button:hover {
  opacity: 0.9;
}

.built-chord button {
  background: linear-gradient(to right, #ff69b4, #8a2be2); /* Pink to Purple Gradient */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  border: none;
  font-weight: bold;
  cursor: pointer;
  padding: 0 5px;
}

.clear-progression-button {
  background: linear-gradient(to right, #ff69b4, #8a2be2); /* Pink to Purple Gradient */
  color: white;
  padding: 8px 12px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.clear-progression-button:hover {
  opacity: 0.9;
}
</style>
