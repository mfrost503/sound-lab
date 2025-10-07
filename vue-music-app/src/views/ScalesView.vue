<template>
  <div class="view-container">
    <ScaleGenerator @scale-generated="onScaleGenerated" />
    <ScaleDisplay :scale="scale" :note="note" :scaleType="scaleType" :octave="octave" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import ScaleGenerator from '../components/ScaleGenerator.vue';
import ScaleDisplay from '../components/ScaleDisplay.vue';

const scale = ref<string[]>([]);
const note = ref('');
const scaleType = ref('');
const octave = ref(4);

const onScaleGenerated = (data: { scale: string[], note: string, scaleType: string, octave: number }) => {
  scale.value = data.scale;
  note.value = data.note;
  scaleType.value = data.scaleType;
  octave.value = data.octave;
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
