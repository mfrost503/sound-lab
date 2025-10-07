<template>
  <div class="scale-generator">
    <h2>Scale Generator</h2>
    <div>
      <label for="note">Note:</label>
      <select id="note" v-model="note">
        <option value=""></option>
        <option v-for="n in notes" :key="n" :value="n">{{ n }}</option>
      </select>
    </div>
    <div>
      <label for="scale-type">Scale Type:</label>
      <select id="scale-type" v-model="scaleType">
        <option value="major">Major</option>
        <option value="dorian">Dorian</option>
        <option value="phrygian">Phrygian</option>
        <option value="lydian">Lydian</option>
        <option value="mixolydian">Mixolydian</option>
        <option value="minor">Minor</option>
        <option value="locrian">Locrian</option>
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
const scaleType = ref('major');
const octave = ref(4);
const error = ref('');

const emit = defineEmits(['scale-generated']);

const getScale = async () => {
  if (!note.value || !scaleType.value) {
    // Don't show an error, just clear the display
    error.value = '';
    emit('scale-generated', { scale: [], note: '', scaleType: '', octave: 4 });
    return;
  }
  try {
    const response = await fetch(`http://localhost:8000/scale/${scaleType.value}/${note.value}`);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch scale');
    }
    const data = await response.json();
    emit('scale-generated', { ...data, octave: octave.value });
    error.value = '';
  } catch (err: any) {
    emit('scale-generated', { scale: [], note: '', scaleType: '', octave: 4 });
    error.value = err.message;
  }
};

watch([note, scaleType, octave], getScale, { immediate: true });
</script>

<style scoped>
.scale-generator {
  border: 1px solid black;
  padding: 20px;
  border-radius: 10px;
}
div {
  margin-bottom: 10px;
}
</style>