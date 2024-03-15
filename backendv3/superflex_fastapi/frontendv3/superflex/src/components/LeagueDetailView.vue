<template>
  <div class="league-info-container">
    <a-spin :spinning="isLoading">
      <div v-if="data && data.length > 0">
        <h2>League Details</h2>
        <ul>
          <li>League ID: {{ data.leagueId }}</li>
          <li>Platform: {{ data.platform }}</li>
          <!-- Add more details as needed -->
        </ul>
      </div>
      <div v-else>
        <h2>No League Data Found</h2>
      </div>
    </a-spin>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { message, Spin } from 'ant-design-vue'

const data = ref<any>(null) // Consider defining a more specific type or interface for your data
const isLoading = ref(false)
const route = useRoute()

onMounted(() => {
  const leagueId = route.params.leagueId as string
  const platform = route.params.platform as string
  if (leagueId && platform) {
    fetchData(leagueId, platform)
  }
})

async function fetchData(leagueId: string, platform: string) {
  isLoading.value = true
  try {
    const response = await axios.get(`http://127.0.0.1:8000/league`, {
      params: { league_id: leagueId, platform: platform }
    })
    data.value = response.data // Update this line based on the structure of your actual data
  } catch (error) {
    console.error('There was an error fetching the leagues data:', error)
    message.error('Failed to fetch league data.')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.league-info-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  background: #fff;
}
</style>
