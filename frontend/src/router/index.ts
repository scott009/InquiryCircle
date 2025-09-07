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
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../components/dashboard/FacilitatorDashboard.vue'),
      meta: { requiresAuth: true, role: 'facilitator' }
    },
    {
      path: '/circles',
      name: 'circles',
      component: () => import('../components/circles/CirclesList.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
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
      // Redirect to appropriate dashboard based on role
      if (authStore.isFacilitator) {
        next({ name: 'dashboard' })
      } else {
        next({ name: 'circles' })
      }
      return
    }
  }

  // If already authenticated and going to login, redirect to appropriate dashboard
  if (to.name === 'login' && authStore.isAuthenticated) {
    if (authStore.isFacilitator) {
      next({ name: 'dashboard' })
    } else {
      next({ name: 'circles' })
    }
    return
  }

  next()
})

export default router