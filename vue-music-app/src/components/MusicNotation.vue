<template>
  <div class="music-notation" v-if="scale.length">
    <h3>{{ note }} {{ scaleType }} Scale - Sheet Music</h3>
    <div id="notation-div"></div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, computed, onMounted, watch } from 'vue';

declare const ABCJS: any;

const props = defineProps({
  scale: {
    type: Array as () => string[],
    required: true,
  },
  note: {
    type: String,
    required: true,
  },
  scaleType: {
    type: String,
    required: true,
  },
});

const notation = computed(() => {
  if (!props.scale.length) {
    return '';
  }

  let abcString = `X:1\nM:4/4\nK:C\n`;

  const notes = props.scale.map((note, index) => {
    let abcNote = note.replace('b', '_').replace('#', '^');
    if (index === props.scale.length - 1) {
        return abcNote.toLowerCase();
    }
    return abcNote;
  }).join(' ');

  abcString += notes;

  return abcString;
});

const renderNotation = () => {
  if (typeof ABCJS !== 'undefined') {
    ABCJS.renderAbc("notation-div", notation.value);
  }
};

const waitForAbcjs = (callback: () => void) => {
  const interval = setInterval(() => {
    if (typeof ABCJS !== 'undefined') {
      clearInterval(interval);
      callback();
    }
  }, 100);
};

onMounted(() => {
  waitForAbcjs(renderNotation);
});

watch(notation, () => {
  waitForAbcjs(renderNotation);
});

</script>

<style scoped>
.music-notation {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  width: 75vw;
}
</style>