<template>
  <a-layout class="layout">
    <AppHeader />

    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item><a href="/userName">Home</a></a-breadcrumb-item>
        <a-breadcrumb-item>Leagues</a-breadcrumb-item>
      </a-breadcrumb>

      <div style="display: flex; justify-content: left">
        <a-table
          :columns="columns"
          :data-source="data"
          :loading="isLoading"
          :expand-column-width="100"
          style="max-width: 850px"
        >
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
                <div class="expanded-row-content">
                  <a-card title="Dynasty Ranks" :bordered="false" class="rank-card">
                    <ul class="rank-list">
                      <li class="rank-item">
                        <div class="rank-name">Keep Trade Cut</div>
                        <div class="rank-tags">
                          <a-tooltip title="Overall">
                            <a-tag>{{ addOrdinalSuffix(record.ktc_power_rank) }}</a-tag>
                          </a-tooltip>
                          <a-tooltip title="Starters">
                            <a-tag>{{ addOrdinalSuffix(record.ktc_power_rank) }}</a-tag>
                          </a-tooltip>
                        </div>
                        <span class="action-buttons">
                          <a-button
                            type="primary"
                            size="small"
                            class="league-load-buttons"
                            @click="
                              insertLeagueDetails(record, { platform: 'ktc', rankType: 'power' })
                            "
                            >Details</a-button
                          >
                          <a-button type="default" size="small">↻</a-button>
                        </span>
                      </li>
                      <li class="rank-item">
                        <div class="rank-name">Superflex</div>
                        <div class="rank-tags">
                          <a-tooltip title="Overall">
                            <a-tag>{{ addOrdinalSuffix(record.ktc_power_rank) }}</a-tag>
                          </a-tooltip>
                          <a-tooltip title="Starters">
                            <a-tag>{{ addOrdinalSuffix(record.ktc_power_rank) }}</a-tag>
                          </a-tooltip>
                        </div>
                        <span class="action-buttons">
                          <a-button type="primary" size="small" class="league-load-buttons"
                            >Details</a-button
                          >
                          <a-button type="default" size="small">↻</a-button>
                        </span>
                      </li>
                      <li class="rank-item">
                        <div class="rank-name">DynastyProcess</div>
                        <div class="rank-tags">
                          <a-tooltip title="Overall">
                            <a-tag>{{ addOrdinalSuffix(record.dp_power_rank) }}</a-tag>
                          </a-tooltip>
                          <a-tooltip title="Starters">
                            <a-tag>{{ addOrdinalSuffix(record.dp_power_rank) }}</a-tag>
                          </a-tooltip>
                        </div>

                        <span class="action-buttons">
                          <a-button type="primary" size="small" class="league-load-buttons"
                            >Details</a-button
                          >
                          <a-button type="default" size="small">↻</a-button>
                        </span>
                      </li>
                      <li class="rank-item">
                        <div class="rank-name">FantasyCalc</div>
                        <div class="rank-tags">
                          <a-tooltip title="Overall">
                            <a-tag>{{ addOrdinalSuffix(record.fc_power_rank) }}</a-tag>
                          </a-tooltip>
                          <a-tooltip title="Starters">
                            <a-tag>{{ addOrdinalSuffix(record.fc_power_rank) }}</a-tag>
                          </a-tooltip>
                        </div>

                        <span class="action-buttons">
                          <a-button type="primary" size="small" class="league-load-buttons"
                            >Details</a-button
                          >
                          <a-button type="default" size="small">↻</a-button>
                        </span>
                      </li>
                    </ul>
                  </a-card>
                </div>
                <a-card title="Contender Ranks" :bordered="false" class="rank-card">
                  <ul class="rank-list">
                    <li class="rank-item">
                      <div class="rank-name">ESPN</div>
                      <div class="rank-tags">
                        <a-tooltip title="Overall">
                          <a-tag>{{ addOrdinalSuffix(record.espn_contender_rank) }}</a-tag>
                        </a-tooltip>
                        <a-tooltip title="Starters">
                          <a-tag>{{ addOrdinalSuffix(record.espn_contender_rank) }}</a-tag>
                        </a-tooltip>
                      </div>
                      <span class="action-buttons">
                        <a-button type="primary" size="small" class="league-load-buttons"
                          >Details</a-button
                        >
                        <a-button type="default" size="small">↻</a-button>
                      </span>
                    </li>
                    <li class="rank-item">
                      <div class="rank-name">NFL</div>
                      <div class="rank-tags">
                        <a-tooltip title="Overall">
                          <a-tag>{{ addOrdinalSuffix(record.nfl_contender_rank) }}</a-tag>
                        </a-tooltip>
                        <a-tooltip title="Starters">
                          <a-tag>{{ addOrdinalSuffix(record.nfl_contender_rank) }}</a-tag>
                        </a-tooltip>
                      </div>
                      <span class="action-buttons">
                        <a-button type="primary" size="small" class="league-load-buttons"
                          >Details</a-button
                        >
                        <a-button type="default" size="small">↻</a-button>
                      </span>
                    </li>
                    <li class="rank-item">
                      <div class="rank-name">CBS</div>
                      <div class="rank-tags">
                        <a-tooltip title="Overall">
                          <a-tag>{{ addOrdinalSuffix(record.cbs_contender_rank) }}</a-tag>
                        </a-tooltip>
                        <a-tooltip title="Starters">
                          <a-tag>{{ addOrdinalSuffix(record.cbs_contender_rank) }}</a-tag>
                        </a-tooltip>
                      </div>
                      <span class="action-buttons">
                        <a-button type="primary" size="small" class="league-load-buttons"
                          >Details</a-button
                        >
                        <a-button type="default" size="small">↻</a-button>
                      </span>
                    </li>
                    <li class="rank-item">
                      <div class="rank-name">FantasyCalc</div>
                      <div class="rank-tags">
                        <a-tooltip title="Overall">
                          <a-tag>{{ addOrdinalSuffix(record.fc_contender_rank) }}</a-tag>
                        </a-tooltip>
                        <a-tooltip title="Starters">
                          <a-tag>{{ addOrdinalSuffix(record.fc_contender_rank) }}</a-tag>
                        </a-tooltip>
                      </div>
                      <span class="action-buttons">
                        <a-button type="primary" size="small" class="league-load-buttons"
                          >Details</a-button
                        >
                        <a-button type="default" size="small">↻</a-button>
                      </span>
                    </li>
                  </ul>
                </a-card>
              </div>
            </div>
          </template>
          <template #expandColumnTitle> </template>
        </a-table>
      </div>
    </a-layout-content>

    <AppFooter />
  </a-layout>
</template>
<script lang="ts" setup>
// Vue Imports
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
// 3rd Party imports
import axios from 'axios'

// UTILS imports
import { addOrdinalSuffix } from '../utils/suffix'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import type { TableColumnType, TableProps } from 'ant-design-vue'

type TableDataType = {
  key: number
  league_name: string
  league_type: string
  total_rosters: number
  roster_type: string
  starter_cnt: number
}

const columns = [
  { title: 'Name', dataIndex: 'league_name', key: 'league_name', width: 300 },
  {
    title: 'Type',
    dataIndex: 'league_type',
    key: 'league_type',
    width: 150,
    filters: [
      {
        text: 'Redraft',
        value: 'Redraft'
      },
      {
        text: 'Keeper',
        value: 'Keeper'
      },
      {
        text: 'Dynasty',
        value: 'Dynasty'
      }
    ],
    onFilter: (value: string, record: TableDataType) => record.league_type.indexOf(value) === 0,
    sorter: (a: TableDataType, b: TableDataType) => a.league_type.length - b.league_type.length,
    sortDirections: ['descend']
  },
  {
    title: 'Size',
    dataIndex: 'total_rosters',
    key: 'total_rosters',
    width: 100,
    sorter: {
      compare: (a, b) => a.total_rosters - b.total_rosters,
      multiple: 1
    }
  },
  {
    title: 'Roster',
    dataIndex: 'roster_type',
    key: 'roster_type',
    width: 150,
    filters: [
      {
        text: 'SingleQB',
        value: 'SingleQB'
      },
      {
        text: 'Superflex',
        value: 'Superflex'
      }
    ],
    onFilter: (value: string, record: TableDataType) => record.roster_type.indexOf(value) === 0,
    sorter: (a: TableDataType, b: TableDataType) => a.roster_type.length - b.roster_type.length,
    sortDirections: ['descend']
  },
  {
    title: 'Starters',
    dataIndex: 'starter_cnt',
    key: 'starter_cnt',
    width: 100,
    sorter: {
      compare: (a, b) => a.starter_cnt - b.starter_cnt,
      multiple: 2
    }
  }
]

// configs
const activeKey = ref([])
// Assuming 'data' is the property used as the data source for your table
const data = ref([])
const route = useRoute()
const isLoading = ref(false)
const router = useRouter() // Use the useRouter composable to get access to the router instance

const userName = route.params.userName as string
const leagueYear = route.params.leagueYear
const guid = route.params.guid as string
const leagueName = route.params.leagueName as string

const leagueInfo = reactive({
  userName: userName,
  leagueYear: leagueYear,
  guid: guid as string
})

onMounted(() => {
  const userName = route.params.userName as string
  const leagueYear = route.params.leagueYear as string
  const guid = route.params.guid as string
  if (leagueYear && userName && guid) {
    fetchData(leagueYear, userName, guid)
  }
})

async function fetchData(leagueYear: string, userName: string, guid: string) {
  isLoading.value = true
  try {
    const response = await axios.get('http://127.0.0.1:8000/leagues', {
      params: {
        league_year: leagueYear,
        user_name: userName,
        guid: guid
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

const insertLeagueDetails = async (record, metadata) => {
  console.log('trying insert rosters')
  console.log(record)
  console.log(guid)
  console.log(leagueYear)
  try {
    const userResponse = await axios.get('http://127.0.0.1:8000/get_user', {
      params: {
        user_name: userName
      }
    })
    console.log(userResponse)
    const userId = userResponse.data.user_id

    // const response = await axios.post('http://127.0.0.1:8000/roster', {
    //   league_id: record.league_id,
    //   user_id: userId,
    //   guid: guid,
    //   league_year: leagueYear
    // })

    router.push(
      `/league/${record.league_id}/${metadata.platform}/${metadata.rankType}/${guid}/${leagueYear}/${userName}/${record.league_name}/${record.roster_type}/${userId}`
    )

    console.log('Sending to League details')
  } catch (error) {
    console.error('Failed to load league details:', error)
    // Optionally, update leagueDetails to indicate an error or show an error message
  } finally {
    console.log('complete')
  }
}

// Function to handle click event
const handleClick = (record) => {
  console.log(record) // Do something with the record
  // For example, navigate to another route, open a modal, etc.

  const url = `/leagueview/${encodeURIComponent(userName)}/${encodeURIComponent(record.user_id)}/${encodeURIComponent(record.league_id)}/${encodeURIComponent(record.league_name)}/${encodeURIComponent(record.sf_check)}/${record.league_year}/${record.starter_cnt}/${record.total_rosters}/${record.league_type}/${record.session_id}/${record.roster_type}`

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

.rank-card {
  width: 400px;
}

.rank-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.rank-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.league-load-buttons {
  margin-right: 25px;
}
.site-layout-content {
  min-height: 280px;
  padding: 24px;
  background: #fff;
}
.rank-name {
  flex: 1; /* Allows this element to grow and shrink as needed */
  min-width: 0; /* Prevents the element from overflowing */
  white-space: nowrap; /* Prevents text from wrapping */
}

.rank-tags {
  display: flex;
  gap: 8px; /* Adjust the space between tags */
}
</style>
