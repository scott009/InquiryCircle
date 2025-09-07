import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../components/dashboard/Dashboard.vue')
    },
    {
      path: '/test-jitsi',
      name: 'test-jitsi',
      component: () => import('../views/JitsiTest.vue')
    }
  ]
})

export default router