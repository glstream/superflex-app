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
      path: '/leagueview/:userName/:userId/:leagueId/:leagueName/:leagueSetting/:leagueYear/:leagueStarters/:leagueSize/:leagueType/:guid/:rosterType/:avatar',
      component: () => import('../components/LeagueView.vue')
    },
    {
      path: '/league/:leagueId/:platform/:rankType/:guid/:leagueYear/:userName/:leagueName/:rosterType/:userId/:avatar',
      component: () => import('../components/LeagueDetailView.vue')
    },
    {
      path: '/ranks',
      component: () => import('../components/RanksView.vue')
    }
  ]
})

export default router
