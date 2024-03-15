<template>
  <a-layout class="layout">
    <AppHeader />

    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item><a href="/userName">Home</a></a-breadcrumb-item>
        <a-breadcrumb-item>Leagues</a-breadcrumb-item>
      </a-breadcrumb>

      <!-- Table to display league summary -->
      <a-table :columns="columns" :data-source="data" :loading="isLoading" table-layout="fixed">
        <!-- Custom cell template for league names with click handler -->
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'league_name'">
            <a @click.prevent="handleClick(record)">
              {{ record.league_name }}
            </a>
          </template>
        </template>
        <!-- Expanded row template for detailed league information -->
        <template #expandedRowRender="{ record }">
          <div class="expanded-row-content">
            <div
              style="
                display: flex;
                justify-content: start;
                gap: 20px;
                overflow-y: auto;
                max-height: 300px;
              "
            >
              <a-card title="Dynasty Ranks" :bordered="false" style="width: 400px">
                <a-collapse style="min-width: 320px" accordion>
                  <a-collapse-panel
                    key="1"
                    :header="`KeepTradeCut: ` + addOrdinalSuffix(record.ktc_power_rank)"
                  >
                    QB<a-badge :count="addOrdinalSuffix(record.ktc_power_rank)" /> RB<a-badge
                      :count="addOrdinalSuffix(record.ktc_power_rank)"
                    />
                    WR<a-badge :count="addOrdinalSuffix(record.ktc_power_rank)" /> TE<a-badge
                      :count="addOrdinalSuffix(record.ktc_power_rank)"
                    />
                    Picks<a-badge :count="addOrdinalSuffix(record.ktc_power_rank)" />
                  </a-collapse-panel>
                  <a-collapse-panel
                    key="2"
                    :header="`Superflex: ` + addOrdinalSuffix(record.sf_power_rank)"
                  >
                    QB<a-badge :count="addOrdinalSuffix(record.sf_power_rank)" /> RB<a-badge
                      :count="addOrdinalSuffix(record.sf_power_rank)"
                    />
                    WR<a-badge :count="addOrdinalSuffix(record.sf_power_rank)" /> TE<a-badge
                      :count="addOrdinalSuffix(record.sf_power_rank)"
                    />
                    Picks<a-badge :count="addOrdinalSuffix(record.sf_power_rank)" />
                  </a-collapse-panel>
                  <a-collapse-panel
                    key="3"
                    :header="`FantasyCalc: ` + addOrdinalSuffix(record.fc_power_rank)"
                  >
                    QB<a-badge :count="addOrdinalSuffix(record.fc_power_rank)" /> RB<a-badge
                      :count="addOrdinalSuffix(record.fc_power_rank)"
                    />
                    WR<a-badge :count="addOrdinalSuffix(record.fc_power_rank)" /> TE<a-badge
                      :count="addOrdinalSuffix(record.fc_power_rank)"
                    />
                    Picks<a-badge :count="addOrdinalSuffix(record.fc_power_rank)" />
                  </a-collapse-panel>
                  <a-collapse-panel
                    key="4"
                    :header="`Dynasty Process: ` + addOrdinalSuffix(record.dp_power_rank)"
                  >
                    QB<a-badge :count="addOrdinalSuffix(record.dp_power_rank)" /> RB<a-badge
                      :count="addOrdinalSuffix(record.ktc_power_rank)"
                    />
                    WR<a-badge :count="addOrdinalSuffix(record.dp_power_rank)" /> TE<a-badge
                      :count="addOrdinalSuffix(record.ktc_power_rank)"
                    />
                  </a-collapse-panel>
                </a-collapse>
              </a-card>
              <a-card title="Contender Ranks" :bordered="false" style="width: 400px">
                <a-collapse style="min-width: 320px" accordion>
                  <a-collapse-panel
                    key="1"
                    :header="`ESPN: ` + addOrdinalSuffix(record.espn_contender_rank)"
                  >
                    QB<a-badge :count="addOrdinalSuffix(record.espn_contender_rank)" /> RB<a-badge
                      :count="addOrdinalSuffix(record.espn_contender_rank)"
                    />
                    WR<a-badge :count="addOrdinalSuffix(record.espn_contender_rank)" /> TE<a-badge
                      :count="addOrdinalSuffix(record.espn_contender_rank)"
                    />
                  </a-collapse-panel>
                  <a-collapse-panel
                    key="2"
                    :header="`NFL: ` + addOrdinalSuffix(record.nfl_contender_rank)"
                  >
                    QB<a-badge :count="addOrdinalSuffix(record.nfl_contender_rank)" /> RB<a-badge
                      :count="addOrdinalSuffix(record.nfl_contender_rank)"
                    />
                    WR<a-badge :count="addOrdinalSuffix(record.nfl_contender_rank)" /> TE<a-badge
                      :count="addOrdinalSuffix(record.nfl_contender_rank)"
                    />
                  </a-collapse-panel>
                  <a-collapse-panel
                    key="3"
                    :header="`CBS: ` + addOrdinalSuffix(record.cbs_contender_rank)"
                  >
                    QB<a-badge :count="addOrdinalSuffix(record.cbs_contender_rank)" /> RB<a-badge
                      :count="addOrdinalSuffix(record.cbs_contender_rank)"
                    />
                    WR<a-badge :count="addOrdinalSuffix(record.cbs_contender_rank)" /> TE<a-badge
                      :count="addOrdinalSuffix(record.cbs_contender_rank)"
                    />
                  </a-collapse-panel>
                  <a-collapse-panel
                    key="4"
                    :header="`FantasyCalc: ` + addOrdinalSuffix(record.fc_contender_rank)"
                  >
                    QB<a-badge :count="addOrdinalSuffix(record.fc_contender_rank)" /> RB<a-badge
                      :count="addOrdinalSuffix(record.fc_contender_rank)"
                    />
                    WR<a-badge :count="addOrdinalSuffix(record.fc_contender_rank)" /> TE<a-badge
                      :count="addOrdinalSuffix(record.fc_contender_rank)"
                    />
                  </a-collapse-panel>
                </a-collapse>
              </a-card>
            </div>
          </div>
        </template>
        <template #expandColumnTitle> </template>
      </a-table>
    </a-layout-content>

    <a-layout-footer style="text-align: center">
      LeagueView ©2024 Created using Ant Design Vue
    </a-layout-footer>
  </a-layout>
</template>
<script lang="ts" setup>
// Vue Imports
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
// 3rd Party imports
import axios from 'axios'
// UTILS imports
import { addOrdinalSuffix } from '../utils/suffix'
import AppHeader from '@/components/AppHeader.vue'

const columns = [
  { title: 'Name', dataIndex: 'league_name', key: 'league_name', width: 300 },
  { title: 'Type', dataIndex: 'league_type', key: 'league_type', width: 150 },
  { title: 'Size', dataIndex: 'total_rosters', key: 'total_rosters', width: 100 },
  { title: 'Roster', dataIndex: 'sf_check', key: 'sf_check', width: 150 },
  { title: 'Starters', dataIndex: 'starter_cnt', key: 'starter_cnt', width: 100 }
]

// configs
const activeKey = ref([])
// Assuming 'data' is the property used as the data source for your table
const data = ref([])
const route = useRoute()
const isLoading = ref(false)
const router = useRouter() // Use the useRouter composable to get access to the router instance
const userName = route.params.userName as string

onMounted(() => {
  const userName = route.params.userName as string
  const leagueYear = route.params.leagueYear as string
  if (leagueYear && userName) {
    fetchData(leagueYear, userName)
  }
})

async function fetchData(leagueYear: string, userName: string) {
  isLoading.value = true
  try {
    const response = await axios.get('http://127.0.0.1:8000/leagues', {
      params: {
        league_year: leagueYear,
        user_name: userName
      }
    })
    data.value = response.data // Assuming the server response format matches your table data format
    console.log(data.value)
  } catch (error) {
    console.error('There was an error fetching the leagues data:', error)
  } finally {
    isLoading.value = false
  }
}

// Function to handle click event
const handleClick = (record) => {
  console.log(record) // Do something with the record
  // For example, navigate to another route, open a modal, etc.

  const url = `/leagueview/${encodeURIComponent(userName)}/${encodeURIComponent(record.user_id)}/${encodeURIComponent(record.league_id)}/${encodeURIComponent(record.league_name)}/${encodeURIComponent(record.sf_check)}/${record.league_year}/${record.starter_cnt}/${record.total_rosters}/${record.league_type}/`

  router.push(url)
}
</script>
<style>
/* Additional styles for layout */
.layout {
  min-height: 100vh;
  min-width: 1000px;
}
.expanded-row-content {
  display: flex;
  justify-content: start;
  gap: 20px;
  overflow-y: auto;
  max-height: 300px;
}
/* Add custom styles for expanded row content if necessary */
.ant-table-expanded-row > td {
  overflow: hidden; /* Adjust as needed for your content */
}
</style>
