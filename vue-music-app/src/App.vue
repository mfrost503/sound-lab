<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <h1>Sound Lab</h1>
    <nav>
      <RouterLink to="/scales">Scales</RouterLink>
      <RouterLink to="/chords">Chords</RouterLink>
      <RouterLink to="/progressions">Progressions</RouterLink>
      <RouterLink to="/metronome">Metronome</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  background: linear-gradient(to right, #ff69b4, #8a2be2);
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: space-between; /* Changed from flex-start */
  width: 100%;
  padding: 0 2rem; /* Adjusted padding */
  border-bottom: 1px solid #a0a0a0; /* Mid-gray border */
}

header h1 {
  color: white;
  font-size: 2rem;
}

nav {
  display: flex;
  gap: 1rem;
}

nav a {
  color: white;
  text-decoration: none;
  font-size: 1.2rem;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background-color 0.3s;
}

nav a.router-link-exact-active {
  border: 2px solid white;
  background-color: rgba(255, 255, 255, 0.2);
}
</style>