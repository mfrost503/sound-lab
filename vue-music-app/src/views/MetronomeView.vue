<template>
  <div class="metronome-view">
    <h1>Metronome</h1>
    <div class="controls">
      <div class="control-group">
        <label for="bpm">BPM:</label>
        <div class="bpm-display">
          <button @click="decrementBpm" class="bpm-button">-</button>
          <input type="number" id="bpm-input" v-model.number="bpm" min="40" max="240" class="bpm-value-input" />
          <button @click="incrementBpm" class="bpm-button">+</button>
        </div>
      </div>
      <div class="control-group">
        <label>Time Signature:</label>
        <div class="time-signature-display">
          <select id="time-signature-numerator" v-model.number="timeSignatureNumerator" class="time-signature-select">
            <option v-for="n in 12" :key="n" :value="n">{{ n }}</option>
          </select>
          <span class="time-signature-separator">/</span>
          <select id="time-signature-denominator" v-model.number="timeSignatureDenominator" class="time-signature-select">
            <option value="4">4</option>
            <option value="8">8</option>
            <option value="16">16</option>
          </select>
        </div>
      </div>
      <button @click="toggleMetronome" class="metronome-button">
        <div v-if="!isRunning" class="play-icon"></div>
        <div v-else class="stop-icon"></div>
      </button>
    </div>
    <div class="beat-indicators">
      <div
        v-for="n in timeSignatureNumerator"
        :key="n"
        class="beat-indicator"
        :class="{ active: n - 1 === currentBeat }"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const bpm = ref(80);
const timeSignatureNumerator = ref(4);
const timeSignatureDenominator = ref(4);
const isRunning = ref(false);
let intervalId: number | null = null;
const currentBeat = ref(-1); // -1 means no beat is active

const click1 = new Audio('/sounds/metronome_high.mp3'); // Assuming you have these sound files
const click2 = new Audio('/sounds/metronome_low.mp3');

const playClick = () => {
  currentBeat.value = (currentBeat.value + 1) % timeSignatureNumerator.value;
  if (currentBeat.value === 0) {
    click1.currentTime = 0;
    click1.play();
  } else {
    click2.currentTime = 0;
    click2.play();
  }
};

const startMetronome = () => {
  if (intervalId !== null) return;
  isRunning.value = true;
  currentBeat.value = -1; // Reset beat count
  const interval = (60 / bpm.value) * 1000;
  playClick(); // Play first beat immediately
  intervalId = setInterval(playClick, interval);
};

const stopMetronome = () => {
  if (intervalId !== null) {
    clearInterval(intervalId);
    intervalId = null;
  }
  isRunning.value = false;
  currentBeat.value = -1; // Reset beat indicator
};

const toggleMetronome = () => {
  if (isRunning.value) {
    stopMetronome();
  } else {
    startMetronome();
  }
};

const incrementBpm = () => {
  if (bpm.value < 240) {
    bpm.value++;
  }
};

const decrementBpm = () => {
  if (bpm.value > 40) {
    bpm.value--;
  }
};

watch(bpm, () => {
  if (isRunning.value) {
    stopMetronome();
    startMetronome();
  }
});

watch(timeSignatureNumerator, () => {
  if (isRunning.value) {
    stopMetronome();
    startMetronome();
  }
});

// Stop metronome when component is unmounted
import { onUnmounted } from 'vue';
onUnmounted(() => {
  stopMetronome();
});
</script>

<style scoped>
.metronome-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 2rem;
  gap: 20px;
}

.controls {
  display: flex;
  flex-direction: column;
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

.bpm-display {
  display: flex;
  align-items: center;
  gap: 10px;
}

.bpm-value-input {
  font-size: 3rem;
  font-weight: bold;
  color: #333;
  border: none;
  background-color: transparent;
  width: 80px; /* Adjust width as needed */
  text-align: center;
  -moz-appearance: textfield; /* Firefox */
}

.bpm-value-input::-webkit-outer-spin-button,
.bpm-value-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.bpm-button {
  background: linear-gradient(to right, #ff69b4, #8a2be2); /* Pink to Purple Gradient */
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 15px;
  font-size: 1.5rem;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.time-signature-display {
  display: flex;
  align-items: center;
  gap: 5px;
}

.time-signature-select {
  appearance: none; /* Remove default dropdown arrow */
  background: linear-gradient(to right, #ff69b4, #8a2be2); /* Pink to Purple Gradient */
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.time-signature-separator {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.metronome-button {
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
  width: 80px; /* Fixed width for the button */
  height: 40px; /* Fixed height for the button */
  display: flex;
  justify-content: center;
  align-items: center;
}

.play-icon {
  width: 0;
  height: 0;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  border-left: 15px solid white; /* White triangle */
}

.stop-icon {
  width: 15px;
  height: 15px;
  background-color: white; /* White square */
}

.beat-indicators {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.beat-indicator {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #ccc;
  transition: background-color 0.1s ease-in-out;
}

.beat-indicator.active {
  background: linear-gradient(to right, #ff69b4, #8a2be2); /* Pink to Purple Gradient */
}
</style>
