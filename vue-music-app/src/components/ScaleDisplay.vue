<template>
  <div class="scale-display" v-if="scale.length">
    <div class="header">
      <h3>{{ note }} {{ scaleType }} Scale:</h3>
      <button @click="playScale" :disabled="isPlaying" class="play-scale-button">Play Scale</button>
    </div>
    <div class="notes-container">
      <div class="bouncing-ball" ref="bouncingBall" v-show="isBallVisible"></div>
      <div class="note" v-for="(note, index) in scale" :key="index" @click="playSound(note, index)" :class="{ playing: playingIndex === index }" :ref="el => { if (el) noteElements[index] = el }">
        {{ note }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref, watch } from 'vue';

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
  octave: {
    type: Number,
    required: true,
  },
});

const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const noteMapping: { [key: string]: string } = {
    'Db': 'C#',
    'Eb': 'D#',
    'Gb': 'F#',
    'Ab': 'G#',
    'Bb': 'A#',
};

const soundFileMapping: { [key: string]: string } = {
  'C#': 'Db',
  'D#': 'Eb',
  'F#': 'Gb',
  'G#': 'Ab',
  'A#': 'Bb',
};

const getNoteValue = (note: string) => {
    const mappedNote = noteMapping[note] || note;
    return notes.indexOf(mappedNote);
};

const playingIndex = ref<number | null>(null);
const isPlaying = ref(false);
const isBallVisible = ref(false);
const audioCache = ref<HTMLAudioElement[]>([]);
const noteElements = ref<HTMLDivElement[]>([]);
const bouncingBall = ref<HTMLDivElement | null>(null);

watch(() => [props.scale, props.octave], ([newScale, newOctave]) => {
  let currentOctave = newOctave as number;
  let previousNoteValue = -1;

  audioCache.value = newScale.map((note, index) => {
    const noteValue = getNoteValue(note);
    if (index > 0 && noteValue < previousNoteValue) {
      currentOctave++;
    }
    const soundFileNote = soundFileMapping[note] || note;
    const octave = currentOctave;
    previousNoteValue = noteValue;
    return new Audio(`/sounds/${soundFileNote}${octave}.mp3`);
  });
}, { immediate: true, deep: true });


const playSound = (note: string, index: number, moveBall: boolean = true) => {
  const audio = audioCache.value[index];
  if (audio) {
    audio.currentTime = 0;
    audio.play();
  }

  playingIndex.value = index;
  setTimeout(() => {
    playingIndex.value = null;
  }, 300);

  if (moveBall) {
    // Move the ball
    if (bouncingBall.value && noteElements.value[index]) {
      const noteElement = noteElements.value[index] as HTMLDivElement;
      const noteRect = noteElement.getBoundingClientRect();
      const containerRect = noteElement.parentElement!.getBoundingClientRect();
      const endX = noteRect.left - containerRect.left + noteRect.width / 2 - 10;
      const endY = noteRect.top - containerRect.top - 30;

      const startX = bouncingBall.value.offsetLeft;
      const startY = bouncingBall.value.offsetTop;

      let startTime: number | null = null;
      const duration = 150; // ms

      const animate = (timestamp: number) => {
        if (!startTime) startTime = timestamp;
        const progress = timestamp - startTime;
        const t = Math.min(progress / duration, 1);

        const currentX = startX + (endX - startX) * t;
        const currentY = startY + (endY - startY) * t + Math.sin(t * Math.PI) * -20; // Simple sine wave (inverted)

        if (bouncingBall.value) {
          bouncingBall.value.style.left = `${currentX}px`;
          bouncingBall.value.style.top = `${currentY}px`;
        }

        if (progress < duration) {
          requestAnimationFrame(animate);
        }
      };

      requestAnimationFrame(animate);
    }
  }
};

const playScale = () => {
  isBallVisible.value = true;
  isPlaying.value = true;
  // Play scale up
  props.scale.forEach((note, index) => {
    setTimeout(() => {
      playSound(note, index, index !== 0);
    }, index * 300);
  });

  // Play scale down
  const reversedScale = props.scale.slice(0, -1).reverse();
  reversedScale.forEach((note, index) => {
    setTimeout(() => {
      const originalIndex = props.scale.length - 2 - index;
      playSound(note, originalIndex);
    }, (props.scale.length + index) * 300);
  });

  const totalDuration = (props.scale.length + reversedScale.length) * 300;
  setTimeout(() => {
    isPlaying.value = false;
    isBallVisible.value = false;
  }, totalDuration);
};
</script>

<style scoped>
.scale-display {
  
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 50px;
}

.notes-container {
  position: relative;
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



.bouncing-ball {
  position: absolute;
  width: 20px;
  height: 20px;
  background: linear-gradient(to right, #ff69b4, #8a2be2); /* Pink to Purple Gradient */
  border-radius: 50%;
  top: -30px;
  left: -10px;
}

.play-scale-button {
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