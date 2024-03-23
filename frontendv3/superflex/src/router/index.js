import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/leagues/:leagueYear/:userName/:guid',
      name: 'LeaguesApp',
      component: () => import('../components/LeaguesApp.vue')
    },
    {
      path: '/userName',
      name: 'EnterUsername',
      component: () => import('../components/EnterUsername.vue')
    },
    {
      path: '/leagueview/:userName/:userId/:leagueId/:leagueName/:leagueSetting/:leagueYear/:leagueStarters/:leagueSize/:leagueType/:guid/:rosterType',
      component: () => import('../components/LeagueView.vue')
    },
    {
      path: '/league/:leagueId/:platform/:rankType/:guid/:leagueYear/:userName/:leagueName/:rosterType/:userId',
      component: () => import('../components/LeagueDetailView.vue')
    }
  ]
})

export default router
