import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/leagues/:leagueYear/:userName',
      name: 'LeaguesApp',
      component: () => import('../components/LeaguesApp.vue')
    },
    {
      path: '/userName',
      name: 'EnterUsername',
      component: () => import('../components/EnterUsername.vue')
    },
    {
      path: '/leagueview/:userName/:userId/:leagueId/:leagueName/:leagueSetting/:leagueYear/:leagueStarters/:leagueSize/:leagueType',
      component: () => import('../components/LeagueView.vue')
    },
    {
      path: '/league/:leagueId/:platform',
      component: () => import('../components/LeagueDetailView.vue')
    }
  ]
})

export default router
