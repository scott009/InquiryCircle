import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../components/dashboard/Dashboard.vue')
    },
    {
      path: '/tests',
      name: 'tests',
      component: () => import('../views/Tests.vue')
    },
    {
      path: '/test-jitsi',
      name: 'test-jitsi',
      component: () => import('../views/JitsiTest.vue')
    },
    {
      path: '/test-api',
      name: 'test-api',
      component: () => import('../views/ApiTest.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../components/auth/LoginForm.vue')
    },
    {
      path: '/administration',
      name: 'administration',
      component: () => import('../views/Administration.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/circle/:id',
      name: 'circle-view',
      component: () => import('../components/circles/CircleView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/meeting',
      name: 'meeting',
      component: () => import('../views/VideoTestDemo.vue')
    },
    {
      path: '/facmeet',
      name: 'facmeet',
      component: () => import('../views/FacilitatorMeeting.vue')
    },
    {
      path: '/facpanel',
      name: 'facpanel',
      component: () => import('../views/FacilitatorPanel.vue')
    },
    {
      path: '/circle-manager-demo',
      name: 'circle-manager-demo',
      component: () => import('../views/CircleManagerDemo.vue')
    }
  ]
})

// Navigation guards
router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()

  // Try to restore session if not authenticated
  if (!authStore.isAuthenticated) {
    authStore.restoreSession()
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      // Redirect to login if not authenticated
      next({ name: 'login', query: { redirect: to.fullPath } })
      return
    }

    // Check role-based access
    if (to.meta.role && authStore.userRole !== to.meta.role) {
      // Redirect to administration for any authenticated user
      next({ name: 'administration' })
      return
    }
  }

  // If already authenticated and going to login, redirect to administration
  if (to.name === 'login' && authStore.isAuthenticated) {
    next({ name: 'administration' })
    return
  }

  next()
})

export default router