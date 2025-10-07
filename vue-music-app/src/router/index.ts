import { createRouter, createWebHistory } from 'vue-router'
import ScalesView from '../views/ScalesView.vue'
import ChordsView from '../views/ChordsView.vue'
import ProgressionsView from '../views/ProgressionsView.vue'
import MetronomeView from '../views/MetronomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/scales',
    },
    {
      path: '/scales',
      name: 'scales',
      component: ScalesView,
    },
    {
      path: '/chords',
      name: 'chords',
      component: ChordsView,
    },
    {
      path: '/progressions',
      name: 'progressions',
      component: ProgressionsView,
    },
    {
      path: '/metronome',
      name: 'metronome',
      component: MetronomeView,
    },
  ],
})

export default router
