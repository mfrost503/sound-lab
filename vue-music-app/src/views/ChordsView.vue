<template>
  <div class="view-container">
    <ChordGenerator @chord-generated="onChordGenerated" />
    <ChordDisplay :chord="chord" :note="chordNote" :chordType="chordType" :octave="chordOctave" />
    <ChordDetector />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import ChordGenerator from '../components/ChordGenerator.vue';
import ChordDisplay from '../components/ChordDisplay.vue';
import ChordDetector from '../components/ChordDetector.vue';

const chord = ref<string[]>([]);
const chordNote = ref('');
const chordType = ref('');
const chordOctave = ref(4);

const onChordGenerated = (data: { chord: string[], note: string, chordType: string, octave: number }) => {
  chord.value = data.chord;
  chordNote.value = data.note;
  chordType.value = data.chordType;
  chordOctave.value = data.octave;
};
</script>

<style scoped>
.view-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 2rem;
  gap: 20px;
}
</style>
