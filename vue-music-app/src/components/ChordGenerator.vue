<template>
  <div class="chord-generator">
    <h2>Chord Generator</h2>
    <div>
      <label for="note">Note:</label>
      <select id="note" v-model="note">
        <option v-for="n in notes" :key="n" :value="n">{{ n }}</option>
      </select>
    </div>
    <div>
      <label for="chord-type">Chord Type:</label>
      <select id="chord-type" v-model="chordType">
        <option value="major">Major</option>
        <option value="minor">Minor</option>
        <option value="major7">Major 7th</option>
        <option value="minor7">Minor 7th</option>
        <option value="major9">Major 9th</option>
        <option value="minor9">Minor 9th</option>
        <option value="add9">Add 9</option>
        <option value="major11">Major 11th</option>
        <option value="minor11">Minor 11th</option>
        <option value="sus4">sus4</option>
        <option value="sus2">sus2</option>
        <option value="dim">dim</option>
        <option value="aug">aug</option>
      </select>
    </div>
    <div>
      <label for="octave">Octave:</label>
      <select id="octave" v-model="octave">
        <option v-for="o in 7" :key="o" :value="o">{{ o }}</option>
      </select>
    </div>
    <div v-if="error">
      <p style="color: red;">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, watch } from 'vue';

const note = ref('C');
const notes = ['A', 'A#', 'Bb', 'B', 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab'];
const chordType = ref('major');
const octave = ref(4);
const error = ref('');

const emit = defineEmits(['chord-generated']);

const getChord = async () => {
  if (!note.value || !chordType.value) {
    // Don't show an error, just clear the display
    error.value = '';
    emit('chord-generated', { chord: [], note: '', chordType: '', octave: 4 });
    return;
  }
  try {
    const response = await fetch(`http://localhost:8000/chord/${chordType.value}/${note.value}`);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch chord');
    }
    const data = await response.json();
    emit('chord-generated', { ...data, octave: octave.value });
    error.value = '';
  } catch (err: any) {
    emit('chord-generated', { chord: [], note: '', chordType: '', octave: 4 });
    error.value = err.message;
  }
};

watch([note, chordType, octave], getChord, { immediate: true });
</script>

<style scoped>
.chord-generator {
  border: 1px solid black;
  padding: 20px;
  border-radius: 10px;
}
div {
  margin-bottom: 10px;
}
</style>
