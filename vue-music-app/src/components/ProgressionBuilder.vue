<template>
  <div class="progression-builder">
    <h2>Build Your Progression</h2>
    <div class="chord-selector">
      <select v-model="selectedNote">
        <option v-for="n in notes" :key="n" :value="n">{{ n }}</option>
      </select>
      <select v-model="selectedChordType">
        <option v-for="ct in chordTypes" :key="ct.value" :value="ct.value">{{ ct.text }}</option>
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

const notes = ['Ab', 'A', 'A#', 'Bb', 'B', 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#'];
const chordTypes = [
  { text: 'Major', value: 'major' },
  { text: 'Minor', value: 'minor' },
  { text: 'Major 7th', value: 'major7' },
  { text: 'Minor 7th', value: 'minor7' },
  { text: 'Major 9th', value: 'major9' },
  { text: 'Minor 9th', value: 'minor9' },
  { text: 'Add 9', value: 'add9' },
  { text: 'Major 11th', value: 'major11' },
  { text: 'Minor 11th', value: 'minor11' },
  { text: 'sus4', value: 'sus4' },
  { text: 'sus2', value: 'sus2' },
  { text: 'dim', value: 'dim' },
  { text: 'aug', value: 'aug' },
];

const selectedNote = ref('C');
const selectedChordType = ref('major');
const builtProgression = ref<string[]>([]);

const emit = defineEmits(['progression-updated']);

const addChordToProgression = () => {
  const chordName = `${selectedNote.value}${selectedChordType.value === 'major' ? '' : selectedChordType.value}`;
  builtProgression.value.push(chordName);
  emit('progression-updated', builtProgression.value);
};

const removeChordFromProgression = (index: number) => {
  builtProgression.value.splice(index, 1);
  emit('progression-updated', builtProgression.value);
};

const clearProgression = () => {
  builtProgression.value = [];
  emit('progression-updated', builtProgression.value);
};

watch(builtProgression, (newVal) => {
  emit('progression-updated', newVal);
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
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

.chord-selector button:hover {
  background-color: #0056b3;
}

.current-progression h3 {
  margin-top: 0;
  margin-bottom: 10px;
}

.progression-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
  min-height: 40px; /* Ensure visibility even when empty */
  border: 1px dashed #eee;
  padding: 10px;
  border-radius: 5px;
}

.built-chord {
  background-color: #e9ecef;
  padding: 8px 12px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.built-chord button {
  background: none;
  border: none;
  color: #dc3545;
  font-weight: bold;
  cursor: pointer;
  padding: 0 5px;
}

.clear-progression-button {
  background-color: #dc3545;
  color: white;
  padding: 8px 12px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.clear-progression-button:hover {
  background-color: #c82333;
}
</style>
