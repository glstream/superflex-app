<template>
  <a-layout class="layout">
    <AppHeader />
    <a-layout-content style="padding: 0 100px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item><a href="/userName">Home</a></a-breadcrumb-item>
        <a-breadcrumb-item>Ranks</a-breadcrumb-item>
      </a-breadcrumb>
      <h1>{{ source }} Rankings</h1>
      <div style="padding-bottom: 25px">
        <a-dropdown-button @click="handleButtonClick" class="dropdown-button">
          {{ source }}
          <template #overlay>
            <a-menu @click="handleMenuClick">
              <a-menu-item key="sf">
                <UserOutlined />
                <img style="padding-right: 5px" class="dropdown-img" :src="sfLogo" />SuperFlex
              </a-menu-item>
              <a-menu-item key="ktc">
                <UserOutlined />
                <img style="padding-right: 5px" class="dropdown-img" :src="ktcLogo" />KeepTradeCut
              </a-menu-item>
              <a-menu-item key="dp">
                <UserOutlined />
                <img style="padding-right: 5px" class="dropdown-img" :src="dpLogo" />
                DynastyProcess
              </a-menu-item>
              <a-menu-item key="fc">
                <UserOutlined />
                <img style="padding-right: 5px" class="dropdown-img" :src="fcLogo" />
                FantasyCalc
              </a-menu-item>
            </a-menu>
          </template>
        </a-dropdown-button>
        <div style="float: right">
          <a-switch
            size="large"
            v-model:checked="state.checked1"
            checked-children="Superflex"
            un-checked-children="OneQB"
          />
        </div>
      </div>

      <a-table
        :columns="playerColumns"
        :data-source="filteredData"
        :loading="isLoading"
        :expand-column-width="100"
        :pagination="{ pageSize: 75 }"
        :scroll="{ x: '850px' }"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'pos_rank'">
            <span>
              <a-tag :style="getPositionTag(record._position)">{{ record.pos_rank }}</a-tag>
            </span>
          </template>
        </template>
      </a-table>
    </a-layout-content>
    <AppFooter />
  </a-layout>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'

import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

// 3rd Party imports
import axios from 'axios'
import { message, Spin, Column, Empty, MenuProps } from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

const platform = ref('sf')
const ranksData = ref([{}])
const isLoading = ref(false)
const source = ref('SuperFlex')
const sfLogo = ref('src/assets/sourceLogos/sf.png')
const ktcLogo = ref('src/assets/sourceLogos/ktc.png')
const dpLogo = ref('src/assets/sourceLogos/dp.png')
const fcLogo = ref('src/assets/sourceLogos/fc.png')

const state = reactive({
  checked1: true
})

interface Column {
  title: string
  dataIndex: string
  key: string
}

const playerColumns: Column[] = [
  {
    title: 'Rank',
    dataIndex: 'rank',
    key: 'rank',
    width: 100,
    sorter: {
      compare: (a, b) => a.rank - b.rank,
      multiple: 1
    }
  },
  {
    title: 'Position',
    dataIndex: '_position',
    key: '_position',
    width: 100
  },
  {
    title: 'Player',
    dataIndex: 'player_full_name',
    key: 'player_full_name',
    width: 250
  },
  {
    title: 'Pos Rank',
    dataIndex: 'pos_rank',
    key: 'pos_rank',
    width: 100
  },
  {
    title: 'Team',
    dataIndex: 'team',
    key: 'team',
    width: 100
  },
  {
    title: 'Age',
    dataIndex: 'age',
    key: 'age',
    width: 100,
    sorter: {
      compare: (a, b) => a.age - b.age,
      multiple: 1
    }
  },
  {
    title: 'Value',
    dataIndex: 'value',
    key: 'value',
    width: 100
  }
]

onMounted(() => {
  fetchRanks(platform.value)
})

const filteredData = computed(() => {
  return ranksData.value.filter((item) => {
    return state.checked1 ? item._rank_type === 'sf_value' : item._rank_type === 'one_qb_value'
  })
})

const handleMenuClick: MenuProps['onClick'] = (e) => {
  console.log(e.key)
  const platform = e.key
  try {
    fetchRanks(platform)
  } catch {
    console.log('error loading leagues')
  } finally {
    switch (e.key) {
      case 'sf':
        source.value = 'SuperFlex'
        logoSource.value = 'src/assets/sourceLogos/sf.png'
        break
      case 'dp':
        source.value = 'DynastyProcess'
        logoSource.value = 'src/assets/sourceLogos/dp.png'
        break
      case 'ktc':
        source.value = 'KeepTradeCut'
        logoSource.value = 'src/assets/sourceLogos/ktc.png'
        break
      case 'fc':
        source.value = 'FantasyCalc'
        logoSource.value = 'src/assets/sourceLogos/fc.png'
        break
      default:
        source.value = 'sf'
        logoSource.value = 'src/assets/sourceLogos/sf.png'
    }
  }
}
function getPositionTag(position) {
  switch (position) {
    case 'QB':
      return {
        color: 'rgb(39, 125, 161)',
        background: 'rgb(39, 125, 161, .15)',
        'border-color': 'rgb(39, 125, 161)'
      }
    case 'RB':
      return {
        color: 'rgb(144, 190, 109)',
        background: 'rgb(144, 190, 109, .15)',
        'border-color': 'rgb(144, 190, 109)'
      }
    case 'WR':
      return {
        color: 'rgb(67, 170, 139)',
        background: 'rgb(67, 170, 139, .15)',
        'border-color': 'rgb(67, 170, 139)'
      }
    case 'TE':
      return {
        color: 'rgb(249, 132, 74)',
        background: 'rgb(249, 132, 74, .15)',
        'border-color': 'rgb(249, 132, 74)'
      }
    case 'PICKS':
      return {
        color: 'rgb(143, 145, 146)',
        background: 'rgb(143, 145, 146, .15)',
        'border-color': 'rgb(143, 145, 146)'
      }
    default:
      return {}
  }
}

async function fetchRanks(platform: string) {
  isLoading.value = true
  try {
    const response = await axios.get('http://127.0.0.1:8000/ranks', {
      params: {
        platform
      }
    })
    console.log('Pulling Player Values...')
    ranksData.value = response.data
    console.log(ranksData.value)
  } catch (error) {
    console.log('There was an error pulling values...')
  } finally {
    isLoading.value = false
  }
}
</script>
<style scoped>
.table-section {
  display: flex;
  justify-content: center;
  max-width: 850;
}
.dropdown-img {
  width: 24px;
  height: 20px;
  vertical-align: middle;
  border-radius: 3px;
}
</style>
