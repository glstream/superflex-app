<template>
  <a-layout class="layout" style="max-width: 1400px">
    <AppHeader />
    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item><a href="/username">Home</a></a-breadcrumb-item>
        <a-breadcrumb-item><a :href="leaguesUrl">Leagues</a></a-breadcrumb-item>
        <a-breadcrumb-item>League Details</a-breadcrumb-item>
      </a-breadcrumb>
      <a-avatar-group
        maxCount="12"
        maxPopoverPlacement="bottom"
        maxPopoverTrigger="hover"
        :max-count="12"
      >
        <div v-for="user in summaryData" :key="user.user_id">
          <div
            v-if="user.user_id === leagueInfo.userId"
            style="position: relative; display: inline-block"
          >
            <a-tooltip
              :title="`${addOrdinalSuffix(user.total_rank)} ${user.display_name}`"
              placement="top"
            >
              <a
                :href="`https://sleeper.com/leagues/${leagueInfo.leagueId}/league`"
                target="_blank"
              >
                <a-avatar
                  :src="`https://sleepercdn.com/avatars/thumbs/${user.avatar}`"
                  maxPopoverTrigger="hover"
                  :size="45"
                  style="border: 2px solid gold"
                />
              </a>
            </a-tooltip>
            <span class="badge-label">
              {{ addOrdinalSuffix(user.total_rank) }}
            </span>
          </div>

          <div v-else>
            <a-tooltip
              :title="`${addOrdinalSuffix(user.total_rank)} ${user.display_name}`"
              placement="top"
            >
              <a
                :href="`https://sleeper.com/leagues/${leagueInfo.leagueId}/league`"
                target="_blank"
              >
                <a-avatar
                  :src="`https://sleepercdn.com/avatars/thumbs/${user.avatar}`"
                  maxPopoverTrigger="hover"
                />
              </a>
            </a-tooltip>
          </div>
        </div>
      </a-avatar-group>
      <div style="display: flex; align-items: center; justify-content: space-between">
        <h2>
          {{ leagueInfo.leagueName }} &bull; {{ leagueInfo.platform }}
          {{ leagueInfo.rankType }} Rankings
        </h2>
        <a-button @click="insertLeagueDetials(leagueInfo.leagueId)" type="primary">
          Load League
        </a-button>
      </div>
      <a-spin tip="Loading..." :spinning="summaryIsLoading">
        <TabView>
          <TabPanel header="Overall">
            <div class="main-content" style="display: flex; flex-wrap: wrap">
              <div class="progress-bars-section">
                <div v-for="user in summaryData" :key="user.user_id" class="user-progress">
                  <h3>{{ user.display_name }} &bull; {{ addOrdinalSuffix(user.total_rank) }}</h3>
                  <div class="progress-container">
                    <a-progress
                      :percent="100"
                      :strokeColor="getProgressColor('Total')"
                      strokeWidth="25"
                      :show-info="false"
                    />

                    <a-progress
                      :percent="
                        user.qb_percent +
                        user.rb_percent +
                        user.wr_percent +
                        user.te_percent +
                        user.picks_percent
                      "
                      :strokeColor="getProgressColor('Picks')"
                      strokeWidth="25"
                      class="overlay-progress"
                      :show-info="false"
                    />
                    <a-tooltip title="Total Progress Tooltip">
                      <a-progress
                        :percent="
                          user.qb_percent + user.rb_percent + user.wr_percent + user.te_percent
                        "
                        :strokeColor="getProgressColor('TE')"
                        strokeWidth="25"
                        class="overlay-progress"
                        :show-info="false"
                      />
                    </a-tooltip>

                    <a-progress
                      :percent="user.qb_percent + user.rb_percent + user.wr_percent"
                      :strokeColor="getProgressColor('WR')"
                      strokeWidth="25"
                      class="overlay-progress"
                      :show-info="false"
                    />

                    <a-progress
                      :percent="user.qb_percent + user.rb_percent"
                      :strokeColor="getProgressColor('RB')"
                      strokeWidth="25"
                      class="overlay-progress"
                      :show-info="false"
                    />

                    <a-tooltip
                      :title="`QB: ${user.qb_sum.toLocaleString()}
          RB: ${user.rb_sum.toLocaleString()}
          WR: ${user.wr_sum.toLocaleString()}
          TE: ${user.te_sum.toLocaleString()}
          Picks: ${user.picks_sum.toLocaleString()}
          `"
                      :overlayStyle="{ maxWidth: '95px' }"
                      ><a-progress
                        :percent="user.qb_percent"
                        :strokeColor="getProgressColor('QB')"
                        strokeWidth="25"
                        class="overlay-progress"
                        :show-info="false"
                      />
                    </a-tooltip>
                  </div>
                </div>
              </div>
              <div class="table-section" style="flex: 2; min-width: 300px">
                <a-table
                  :columns="columns"
                  :dataSource="summaryData"
                  row-key="user_id"
                  :pagination="{ pageSize: 20 }"
                  :expand-column-width="100"
                  style="max-width: 850px"
                >
                  <template #expandedRowRender="{ record }">
                    Team Composition:
                    <div class="card">
                      <MeterGroup :value="formatGaugeData(record)" />
                    </div>
                  </template>
                  <template v-slot:totalValueTooltip="{ record }">
                    <a-tooltip
                      color="blue"
                      :title="`Total Value: ${record.total_value.toLocaleString()}`"
                      ><span>{{ record.total_rank_display }}</span>
                    </a-tooltip>
                  </template>
                  <template v-slot:qbValueTooltip="{ record }">
                    <a-tooltip
                      color="blue"
                      :overlayStyle="{ maxWidth: '130px' }"
                      :title="`QB Value: ${record.qb_sum.toLocaleString()} 
              QB Avg. ${record.qb_average.toLocaleString()}`"
                      ><span>{{ record.qb_rank_display }}</span>
                    </a-tooltip>
                  </template>
                  <template v-slot:rbValueTooltip="{ record }">
                    <a-tooltip
                      color="blue"
                      :overlayStyle="{ maxWidth: '130px' }"
                      :title="`RB Value: ${record.rb_sum.toLocaleString()} 
              RB Avg. ${record.rb_average.toLocaleString()}`"
                      ><span>{{ record.rb_rank_display }}</span>
                    </a-tooltip>
                  </template>
                  <template v-slot:wrValueTooltip="{ record }">
                    <a-tooltip
                      color="blue"
                      :overlayStyle="{ maxWidth: '130px' }"
                      :title="`WR Value: ${record.wr_sum.toLocaleString()} 
              WR Avg. ${record.wr_average.toLocaleString()}`"
                      ><span>{{ record.wr_rank_display }}</span>
                    </a-tooltip>
                  </template>
                  <template v-slot:teValueTooltip="{ record }">
                    <a-tooltip
                      color="blue"
                      :overlayStyle="{ maxWidth: '130px' }"
                      :title="`TE Value: ${record.te_sum.toLocaleString()} 
              TE Avg. ${record.te_average.toLocaleString()}`"
                      ><span>{{ record.te_rank_display }}</span>
                    </a-tooltip>
                  </template>
                  <template v-slot:picksValueTooltip="{ record }">
                    <a-tooltip
                      color="blue"
                      :title="`Picks Value: ${record.picks_sum.toLocaleString()}`"
                      ><span>{{ record.picks_rank_display }}</span>
                    </a-tooltip>
                  </template>
                  <template v-slot:benchValueTooltip="{ record }">
                    <a-tooltip
                      color="blue"
                      :overlayStyle="{ maxWidth: '150px' }"
                      :title="`Bench Value: ${record.bench_sum.toLocaleString()} 
              Bench Avg. ${record.bench_average.toLocaleString()}`"
                      ><span>{{ record.bench_rank_display }}</span>
                    </a-tooltip>
                  </template>
                </a-table>
              </div>
            </div>
          </TabPanel>
          <TabPanel header="Starters">
            <a-table
              :data-source="summaryData"
              :columns="starterColumns"
              :pagination="{ pageSize: 20 }"
              style="max-width: 1100px"
              row-key="user_id"
              ><template #expandedRowRender="{ record }">
                <div>
                  <a-row gutter="16">
                    <a-col :span="6">
                      <a-card
                        :title="`Quarterbacks ${addOrdinalSuffix(record.qb_starter_rank)}`"
                        bordered
                      >
                        <div v-for="player in getStarters(record.user_id)" :key="player.sleeper_id">
                          <p v-if="player.player_position === 'QB'">
                            {{ player.full_name }} &bull; {{ player.player_value.toLocaleString() }}
                          </p>
                        </div>
                      </a-card>
                    </a-col>

                    <a-col :span="6">
                      <a-card
                        :title="`Running Backs ${addOrdinalSuffix(record.rb_starter_rank)}`"
                        bordered
                      >
                        <div v-for="player in getStarters(record.user_id)" :key="player.sleeper_id">
                          <p v-if="player.player_position === 'RB'">
                            {{ player.full_name }} &bull; {{ player.player_value.toLocaleString() }}
                          </p>
                        </div>
                      </a-card>
                    </a-col>

                    <a-col :span="6">
                      <a-card
                        :title="`Winde Receivers ${addOrdinalSuffix(record.wr_starter_rank)}`"
                        bordered
                      >
                        <div v-for="player in getStarters(record.user_id)" :key="player.sleeper_id">
                          <p v-if="player.player_position === 'WR'">
                            {{ player.full_name }} &bull; {{ player.player_value.toLocaleString() }}
                          </p>
                        </div>
                      </a-card>
                    </a-col>

                    <a-col :span="6">
                      <a-card
                        :title="`Tight Ends ${addOrdinalSuffix(record.te_starter_rank)}`"
                        bordered
                      >
                        <div v-for="player in getStarters(record.user_id)" :key="player.sleeper_id">
                          <p v-if="player.player_position === 'TE'">
                            {{ player.full_name }} &bull; {{ player.player_value.toLocaleString() }}
                          </p>
                        </div>
                      </a-card>
                    </a-col>
                  </a-row>
                </div>
              </template>
              <template v-slot:starterValueTooltip="{ record }">
                <a-tooltip
                  color="blue"
                  :title="`Starters: ${record.starters_sum?.toLocaleString()}`"
                  ><span>{{ record.starters_rank_display }}</span>
                </a-tooltip>
              </template>
              <template v-slot:qbStarterValueTooltip="{ record }">
                <a-tooltip color="blue" :title="`QB: ${record.qb_starter_sum?.toLocaleString()}`"
                  ><span>{{ record.qb_starter_rank_display }}</span>
                </a-tooltip>
              </template>
              <template v-slot:rbStarterValueTooltip="{ record }">
                <a-tooltip color="blue" :title="`RB: ${record.rb_starter_sum?.toLocaleString()}`"
                  ><span>{{ record.rb_starter_rank_display }}</span>
                </a-tooltip>
              </template>
              <template v-slot:wrStarterValueTooltip="{ record }">
                <a-tooltip color="blue" :title="`WR: ${record.wr_starter_sum?.toLocaleString()}`"
                  ><span>{{ record.wr_starter_rank_display }}</span>
                </a-tooltip>
              </template>
              <template v-slot:teStarterValueTooltip="{ record }">
                <a-tooltip color="blue" :title="`TE: ${record.te_starter_sum?.toLocaleString()}`"
                  ><span>{{ record.te_starter_rank_display }}</span>
                </a-tooltip>
              </template>
            </a-table>

            {{ summaryData }}
          </TabPanel>
          <TabPanel header="All Players">
            <a-row :gutter="{ sm: 16 }">
              <a-col
                v-for="manager in summaryData"
                :key="manager.user_id"
                xs="{24}"
                sm="{12}"
                md="{8}"
                lg="{6}"
                style="min-width: 300px; max-width: 325px"
              >
                <a-card
                  :title="`${manager.display_name} &bull; ${addOrdinalSuffix(manager.total_rank)} Overall`"
                >
                  <div v-for="player in getPlayers(manager.user_id)">
                    <div v-if="player.player_position === 'QB'">
                      <a-tag color="blue">{{ player.player_position }}</a-tag>
                      {{ player.full_name }} &bull; {{ player.player_value.toLocaleString() }}
                    </div>
                    <div v-if="player.player_position === 'RB'">
                      <a-tag color="green">{{ player.player_position }}</a-tag>
                      {{ player.full_name }} &bull; {{ player.player_value.toLocaleString() }}
                    </div>
                    <div v-if="player.player_position === 'WR'">
                      <a-tag color="cyan">{{ player.player_position }}</a-tag>
                      {{ player.full_name }} &bull; {{ player.player_value.toLocaleString() }}
                    </div>
                    <div v-if="player.player_position === 'TE'">
                      <a-tag color="orange">{{ player.player_position }}</a-tag>
                      {{ player.full_name }} &bull; {{ player.player_value.toLocaleString() }}
                    </div>
                    <div v-if="player.player_position === 'PICKS'">
                      <a-tag>{{ player.player_position }}</a-tag>
                      {{ player.full_name }} &bull; {{ player.player_value.toLocaleString() }}
                    </div>
                  </div>
                </a-card>
              </a-col>
            </a-row>
            <li>{{ detailData }}</li>
          </TabPanel>
          <TabPanel header="Manager View">
            <div class="progress-bars-section">
              <div v-if="leagueOwnerData">
                <h3>
                  {{ leagueOwnerData.display_name }} &bull; Overall
                  {{ addOrdinalSuffix(leagueOwnerData.total_rank) }} &bull; Starters
                  {{ addOrdinalSuffix(leagueOwnerData.starters_rank) }}
                </h3>
                <h4>Overall Positional Values</h4>
                <div class="progress-container">
                  <div>
                    <span>Picks</span>
                    <span style="float: right"> Max</span>
                    <a-tooltip
                      :title="`${addOrdinalSuffix(leagueOwnerData.picks_rank)} ${leagueOwnerData.picks_sum?.toLocaleString()}`"
                      ><a-progress
                        :percent="
                          (leagueOwnerData.picks_sum / leagueOwnerData.picks_max_value) * 100
                        "
                        :strokeColor="getProgressColor('Picks')"
                        strokeWidth="15"
                        :format="
                          (percent) => `${leagueOwnerData.picks_max_value?.toLocaleString()}`
                        "
                      />
                    </a-tooltip>
                  </div>
                  <span>TE</span>
                  <a-tooltip
                    :title="`${addOrdinalSuffix(leagueOwnerData.te_rank)} ${leagueOwnerData.te_sum?.toLocaleString()}`"
                    ><a-progress
                      :percent="(leagueOwnerData.te_sum / leagueOwnerData.te_max_value) * 100"
                      :strokeColor="getProgressColor('TE')"
                      strokeWidth="15"
                      :format="(percent) => `${leagueOwnerData.te_max_value?.toLocaleString()}`"
                    />
                  </a-tooltip>
                  <span>WR</span>
                  <a-tooltip
                    :title="`${addOrdinalSuffix(leagueOwnerData.wr_rank)} ${leagueOwnerData.wr_sum?.toLocaleString()}`"
                    ><a-progress
                      :percent="(leagueOwnerData.wr_sum / leagueOwnerData.wr_max_value) * 100"
                      :strokeColor="getProgressColor('WR')"
                      strokeWidth="15"
                      :format="(percent) => `${leagueOwnerData.wr_max_value?.toLocaleString()}`"
                    />
                  </a-tooltip>
                  <span>RB</span>
                  <a-tooltip
                    :title="`${addOrdinalSuffix(leagueOwnerData.rb_rank)} ${leagueOwnerData.rb_sum?.toLocaleString()}`"
                    ><a-progress
                      :percent="(leagueOwnerData.rb_sum / leagueOwnerData.rb_max_value) * 100"
                      :strokeColor="getProgressColor('RB')"
                      strokeWidth="15"
                      :format="(percent) => `${leagueOwnerData.rb_max_value?.toLocaleString()}`"
                    />
                  </a-tooltip>
                  <span>QB</span>
                  <a-tooltip
                    :title="`${addOrdinalSuffix(leagueOwnerData.qb_rank)} ${leagueOwnerData.qb_sum?.toLocaleString()}`"
                    ><a-progress
                      :percent="(leagueOwnerData.qb_sum / leagueOwnerData.qb_max_value) * 100"
                      :strokeColor="getProgressColor('QB')"
                      strokeWidth="15"
                      :format="(percent) => `${leagueOwnerData.qb_max_value?.toLocaleString()}`"
                    />
                  </a-tooltip>
                </div>
              </div>
            </div>
          </TabPanel>
          <TabPanel header="single Manager"> {{ singleManagerData }} ///// {{ data }}</TabPanel>
          <TabPanel header="Best Available"></TabPanel>
        </TabView>
      </a-spin>
    </a-layout-content>
    <AppFooter />
  </a-layout>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { message, Spin, Column } from 'ant-design-vue'
import MeterGroup from 'primevue/metergroup'
import Card from 'primevue/card'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'

import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import { UserOutlined, AntDesignOutlined } from '@ant-design/icons-vue'

import { addOrdinalSuffix } from '../utils/suffix'
import { getCellStyle } from '../utils/colorTable'

const route = useRoute()

const leagueName = route.params.leagueName
const leagueYear = route.params.leagueYear
const leagueId = route.params.leagueId
const userName = route.params.userName
const guid = route.params.guid
const platform = route.params.platform
const rankType = route.params.rankType
const userId = route.params.userId
const rosterType = route.params.rosterType

// Sample league information
const leagueInfo = reactive({
  leagueName: leagueName as string,
  leagueId: leagueId as string,
  userName: userName,
  leagueYear: leagueYear,
  guid: guid as string,
  rankType: rankType as string,
  platform: platform as string,
  userId: userId as string,
  rosterType: rosterType as string
})

const summaryData = ref([])
const detailData = ref([{}])
const singleManagerData = ref(null)

const leaguesUrl = `/leagues/${leagueYear}/${userName}/${guid}`

const isLoading = ref(false)
const summaryIsLoading = ref(false)
const detailIsLoading = ref(false)

const selection = ref({})
function formatGaugeData(record) {
  // Assuming 'record' has a property 'usedSpace' you want to display
  return [
    {
      label: `QB: ${record.qb_sum.toLocaleString()}`,
      color: 'rgb(39, 125, 161)',
      value: record.qb_percent,
      total: record.qb_value
    },
    {
      label: `RB: ${record.rb_sum.toLocaleString()}`,
      color: 'rgb(144, 190, 109)',
      value: record.rb_percent
    },
    {
      label: `WR: ${record.wr_sum.toLocaleString()}`,
      color: 'rgb(67, 170, 139)',
      value: record.wr_percent
    },
    {
      label: `TE: ${record.te_sum.toLocaleString()}`,
      color: 'rgb(249, 132, 74)',
      value: record.te_percent
    },
    {
      label: `Picks: ${record.picks_sum.toLocaleString()}`,
      color: 'rgba(189, 195, 199, 0.6)',
      value: record.picks_percent
    }
  ]
}

const starterColumns: Column[] = [
  {
    title: '',
    dataIndex: 'display_name',
    key: 'display_name',
    align: 'center'
  },
  {
    title: 'Starters',
    dataIndex: 'starters_rank_display',
    key: 'starters_rank_display',
    align: 'center',
    slots: { customRender: 'starterValueTooltip' },
    customCell: (record: any) => ({
      style: getCellStyle(record.starters_rank)
    }),
    sorter: {
      compare: (a, b) => a.starters_rank - b.starters_rank,
      multiple: 2
    }
  },

  {
    title: 'QB',
    dataIndex: 'qb_starter_rank_display',
    key: 'qb_starter_rank',
    align: 'center',
    slots: { customRender: 'qbStarterValueTooltip' },
    customCell: (record: any) => ({
      style: getCellStyle(record.qb_starter_rank)
    }),
    sorter: {
      compare: (a, b) => a.qb_starter_rank - b.qb_starter_rank,
      multiple: 1
    }
  },
  {
    title: 'RB',
    dataIndex: 'rb_starter_rank_display',
    key: 'rb_starter_rank',
    align: 'center',
    slots: { customRender: 'rbStarterValueTooltip' },
    customCell: (record: any) => ({
      style: getCellStyle(record.rb_starter_rank)
    }),
    sorter: {
      compare: (a, b) => a.rb_starter_rank - b.rb_starter_rank,
      multiple: 1
    }
  },
  {
    title: 'WR',
    dataIndex: 'wr_starter_rank_display',
    key: 'wr_starter_rank',
    align: 'center',
    slots: { customRender: 'wrStarterValueTooltip' },
    customCell: (record: any) => ({
      style: getCellStyle(record.wr_starter_rank)
    }),
    sorter: {
      compare: (a, b) => a.wr_starter_rank - b.wr_starter_rank,
      multiple: 1
    }
  },
  {
    title: 'TE',
    dataIndex: 'te_starter_rank_display',
    key: 'te_starter_rank',
    align: 'center',
    slots: { customRender: 'teStarterValueTooltip' },
    customCell: (record: any) => ({
      style: getCellStyle(record.te_starter_rank)
    }),
    sorter: {
      compare: (a, b) => a.te_starter_rank - b.te_starter_rank,
      multiple: 1
    }
  }
]
const columns: Column[] = [
  {
    title: '',
    dataIndex: 'display_name',
    key: 'display_name',
    align: 'center'
  },
  {
    title: 'Overall',
    dataIndex: 'total_rank_display',
    key: 'total_rank_display',
    align: 'center',
    slots: { customRender: 'totalValueTooltip' },
    customCell: (record: any) => ({
      style: getCellStyle(record.total_rank)
    }),
    sorter: {
      compare: (a, b) => a.total_rank - b.total_rank,
      multiple: 10
    }
  },
  {
    title: 'QB',
    dataIndex: 'qb_rank',
    key: 'qb_rank',
    align: 'center',
    slots: { customRender: 'qbValueTooltip' },
    customCell: (record: any) => ({
      style: getCellStyle(record.qb_rank)
    }),
    sorter: {
      compare: (a, b) => a.qb_rank - b.qb_rank,
      multiple: 4
    }
  },
  {
    title: 'RB',
    dataIndex: 'rb_rank',
    key: 'rb_rank',
    align: 'center',
    slots: { customRender: 'rbValueTooltip' },
    customCell: (record: any) => ({
      style: getCellStyle(record.rb_rank)
    }),
    sorter: {
      compare: (a, b) => a.rb_rank - b.rb_rank,
      multiple: 5
    }
  },
  {
    title: 'WR',
    dataIndex: 'wr_rank',
    key: 'wr_rank',
    align: 'center',
    slots: { customRender: 'wrValueTooltip' },
    customCell: (record: any) => ({
      style: getCellStyle(record.wr_rank)
    }),
    sorter: {
      compare: (a, b) => a.wr_rank - b.wr_rank,
      multiple: 6
    }
  },
  {
    title: 'TE',
    dataIndex: 'te_rank',
    key: 'te_rank',
    align: 'center',
    slots: { customRender: 'teValueTooltip' },
    customCell: (record: any) => ({
      style: getCellStyle(record.te_rank)
    }),
    sorter: {
      compare: (a, b) => a.te_rank - b.te_rank,
      multiple: 7
    }
  },
  {
    title: 'Picks',
    dataIndex: 'picks_rank',
    key: 'picks_rank',
    align: 'center',
    slots: { customRender: 'picksValueTooltip' },
    customCell: (record: any) => ({
      style: getCellStyle(record.picks_rank)
    }),
    sorter: {
      compare: (a, b) => a.picks_rank - b.picks_rank,
      multiple: 8
    }
  },
  {
    title: 'Bench',
    dataIndex: 'bench_rank',
    key: 'bench_rank',
    align: 'center',
    slots: { customRender: 'benchValueTooltip' },
    customCell: (record: any) => ({
      style: getCellStyle(record.bench_rank)
    }),
    sorter: {
      compare: (a, b) => a.bench_rank - b.bench_rank,
      multiple: 3
    }
  }
  // Add more columns as needed
]

onMounted(() => {
  const leagueId = route.params.leagueId as string
  const platform = route.params.platform as string
  const rankType = route.params.rankType as string
  const guid = route.params.guid as string
  const rosterType = route.params.rosterType as string
  const userId = route.params.userId as string
  if (leagueId && platform && rankType && guid && userId) {
    fetchSummaryData(leagueId, platform, rankType, guid, rosterType)
    fetchDetailData(leagueId, platform, rankType, guid, rosterType)
  }
})

function getProgressColor(position: string): string {
  if (position === 'QB') {
    return 'rgb(39, 125, 161)'
  } else if (position === 'RB') {
    return 'rgb(144, 190, 109)'
  } else if (position === 'WR') {
    return 'rgb(67, 170, 139)'
  } else if (position === 'TE') {
    return 'rgb(249, 132, 74)'
  } else if (position === 'Picks') {
    return 'rgba(189, 195, 199, 0.6)'
  } else {
    return '#fff'
  }
}

const getStarters = (userId) => {
  const interimData = detailData.value
    .filter((item) => item.user_id === userId)
    .filter((item) => item.fantasy_designation === 'STARTER')
    .filter((item) => item.player_position != 'PICKS')
  return interimData
}

const getPlayers = (userId) => {
  const interimData = detailData.value.filter((item) => item.user_id === userId)
  return interimData
}

const insertLeagueDetials = async (values: any) => {
  isLoading.value = true
  detailIsLoading.value = true
  summaryIsLoading.value = true
  console.log('trying insert rosters')
  console.log(leagueId)
  console.log(userId)
  console.log(guid)
  console.log(leagueYear)
  try {
    const response = await axios.post('http://127.0.0.1:8000/roster', {
      league_id: leagueInfo.leagueId,
      user_id: leagueInfo.userId,
      guid: leagueInfo.guid,
      league_year: leagueInfo.leagueYear
    })

    console.log('Rosters loading...')
  } catch (error) {
    console.error('Error loading rosters', error)
    // Optionally, update leagueDetails to indicate an error or show an error message
  } finally {
    isLoading.value = false // Update loading state
    fetchSummaryData(
      leagueInfo.leagueId,
      leagueInfo.platform,
      leagueInfo.rankType,
      leagueInfo.guid,
      leagueInfo.rosterType
    )
    fetchDetailData(
      leagueInfo.leagueId,
      leagueInfo.platform,
      leagueInfo.rankType,
      leagueInfo.guid,
      leagueInfo.rosterType
    )
  }
}
async function fetchSummaryData(
  leagueId: string,
  platform: string,
  rankType: string,
  guid: string,
  rosterType: string
) {
  summaryIsLoading.value = true
  try {
    const response = await axios.get(`http://127.0.0.1:8000/league`, {
      params: {
        league_id: leagueId,
        platform: platform,
        rank_type: rankType,
        guid: guid,
        roster_type: rosterType
      }
    })

    const rawData = response.data
    const maxTotalValue = Math.max(...rawData.map((item) => item.total_value))
    // summaryData.value = response.data // Update this line based on the structure of your actual data
    summaryData.value = response.data.map((item) => {
      return {
        ...item,
        total_rank_display: addOrdinalSuffix(item.total_rank),
        starters_rank_display: addOrdinalSuffix(item.starters_rank),
        qb_rank_display: addOrdinalSuffix(item.qb_rank),
        rb_rank_display: addOrdinalSuffix(item.rb_rank),
        wr_rank_display: addOrdinalSuffix(item.wr_rank),
        te_rank_display: addOrdinalSuffix(item.te_rank),
        qb_starter_rank_display: addOrdinalSuffix(item.qb_starter_rank),
        rb_starter_rank_display: addOrdinalSuffix(item.rb_starter_rank),
        wr_starter_rank_display: addOrdinalSuffix(item.wr_starter_rank),
        te_starter_rank_display: addOrdinalSuffix(item.te_starter_rank),
        picks_rank_display: addOrdinalSuffix(item.picks_rank),
        bench_rank_display: addOrdinalSuffix(item.bench_rank),
        total_percent: (item.total_value / maxTotalValue) * 100,
        qb_percent: (item.qb_sum / maxTotalValue) * 100,
        rb_percent: (item.rb_sum / maxTotalValue) * 100,
        wr_percent: (item.wr_sum / maxTotalValue) * 100,
        te_percent: (item.te_sum / maxTotalValue) * 100,
        picks_percent: (item.picks_sum / maxTotalValue) * 100
      }
    })
  } catch (error) {
    console.error('There was an error fetching the leagues summary data:', error)
    message.error('Failed to fetch league summary data.')
  } finally {
    summaryIsLoading.value = false
  }
}

const leagueOwnerData = computed(() => {
  const ownerData = summaryData.value
    .map(({ total_value, ...rest }) => rest)
    .find((item) => item.user_id === userId)
  const leagueSize = summaryData.value.reduce((max, item) => Math.max(max, item.total_rank), 0)
  const qbMaxValue = summaryData.value.reduce((max, item) => Math.max(max, item.qb_sum), 0)
  const rbMaxValue = summaryData.value.reduce((max, item) => Math.max(max, item.rb_sum), 0)
  const wrMaxValue = summaryData.value.reduce((max, item) => Math.max(max, item.wr_sum), 0)
  const teMaxValue = summaryData.value.reduce((max, item) => Math.max(max, item.te_sum), 0)
  const picksMaxValue = summaryData.value.reduce((max, item) => Math.max(max, item.picks_sum), 0)

  // Extract qb_sum values and sort them
  const qbSums = summaryData.value.map((item) => item.qb_sum).sort((a, b) => a - b)
  // Calculate the median of qb_sum
  let qbMedian
  const mid = Math.floor(qbSums.length / 2)
  if (qbSums.length % 2 === 0) {
    qbMedian = (qbSums[mid - 1] + qbSums[mid]) / 2
  } else {
    qbMedian = qbSums[mid]
  }

  return {
    ...ownerData,
    league_size: leagueSize,
    qb_max_value: qbMaxValue,
    rb_max_value: rbMaxValue,
    wr_max_value: wrMaxValue,
    te_max_value: teMaxValue,
    picks_max_value: picksMaxValue,
    qb_median: qbMedian
  }
})

const starterData = computed(() => {
  return detailData.value.filter((item) => item.fantasy_designation === 'STARTER')
})

async function fetchDetailData(
  leagueId: string,
  platform: string,
  rankType: string,
  guid: string,
  rosterType: string
) {
  detailIsLoading.value = true
  try {
    const response = await axios.get(`http://127.0.0.1:8000/league_detail`, {
      params: {
        league_id: leagueId,
        platform: platform,
        rank_type: rankType,
        guid: guid,
        roster_type: rosterType
      }
    })
    detailData.value = response.data // Update this line based on the structure of your actual data
  } catch (error) {
    console.error('There was an error fetching the leagues detail data:', error)
    message.error('Failed to fetch league detail data.')
  } finally {
    detailIsLoading.value = false
  }
}
</script>

<style scoped>
table {
  border-collapse: collapse;
}
.league-info-container {
  max-width: 1000px;
  margin: 20px auto;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  background: #fff;
}
/* Target the table rows in the table body */
.ant-table-tbody > tr {
  border-bottom: 1px solid white; /* Adds a white line between rows */
}

/* Target the cells in the table body */
.ant-table-tbody > tr > td {
  color: white; /* Makes the font color white */
}

/* If you also want to style the header */
.ant-table-thead > tr > th {
  color: white; /* Makes the font color white in the header */
  border-bottom: 2px solid white; /* Adds a white line below the header */
}
.user-progress {
  margin-bottom: 20px;
  width: 350px;
  height: 50px;
  transform: scale(0.8);
  transform-origin: top left;
  margin: 10px;
}

.progress-container {
  position: relative;
}
.median-line {
  bottom: 200; /* Position it at the bottom of the container */
  width: 20px; /* or the thickness you want for the line */
  background-color: red; /* or any color for the median line */
}
.overlay-progress {
  position: absolute;
  left: 0;
  top: 0;
  margin-bottom: 10px;
}
.badge-label {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translate(-50%, 0%);
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 0 4px;
  border-radius: 10px;
}
/* Responsive styles */
@media (min-width: 992px) {
  .main-content {
    flex-direction: row; /* Set flex direction to row for larger screens */
  }
  .progress-bars-section {
    max-width: 35%;
  }
  .table-section {
    max-width: 60%; /* Limit width of table section */
  }
}

@media (max-width: 991px) {
  .main-content {
    flex-direction: column; /* Stack vertically on smaller screens */
  }
  .progress-bars-section,
  .table-section {
    max-width: 100%; /* Full width for smaller screens */
  }
}
</style>
