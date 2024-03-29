<template>
  <a-layout class="layout">
    <AppHeader />
    <a-layout-content style="padding: 0 100px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item><a href="/username">Home</a></a-breadcrumb-item>
        <a-breadcrumb-item>Trade Calculator</a-breadcrumb-item>
      </a-breadcrumb>
      <div class="trade-calculator">
        <a-row align="middle" justify="space-between">
          <a-col :span="8">
            <a-switch
              size="large"
              v-model:checked="state.checked1"
              checked-children="Superflex"
              un-checked-children="OneQB"
            />
          </a-col>
          <a-col :span="12" :push="6" style="padding-bottom: 8px">
            <a-dropdown-button @click="handleButtonClick">
              {{ source }}
              <template #overlay>
                <a-menu @click="handleMenuClick">
                  <a-menu-item key="sf">
                    <UserOutlined />
                    <img style="padding-right: 5px" class="dropdown-img" :src="sfLogo" />SuperFlex
                  </a-menu-item>
                  <a-menu-item key="ktc">
                    <UserOutlined />
                    <img
                      style="padding-right: 5px"
                      class="dropdown-img"
                      :src="ktcLogo"
                    />KeepTradeCut
                  </a-menu-item>
                  <a-menu-item key="dp">
                    <UserOutlined />
                    <img
                      style="padding-right: 5px"
                      class="dropdown-img"
                      :src="dpLogo"
                    />DynastyProcess
                  </a-menu-item>
                  <a-menu-item key="fc">
                    <UserOutlined />
                    <img style="padding-right: 5px" class="dropdown-img" :src="fcLogo" />
                    FantasyCalc
                  </a-menu-item>
                </a-menu>
              </template>
            </a-dropdown-button>
          </a-col>
        </a-row>
        <a-row :gutter="16" class="teams">
          <a-col :span="12">
            <a-card>
              <h3>Team A gets...</h3>
              <a-input-search placeholder="Search for a player" />
              <div class="total-pieces">0 Total Assets</div>
            </a-card>
          </a-col>
          <a-col :span="12">
            <a-card>
              <h3>Team B gets...</h3>
              <a-input-search placeholder="Search for a player" />
              <div class="total-pieces">0 Total Assets</div>
            </a-card>
          </a-col>
        </a-row>
        <div class="actions">
          <a-space :size="48">
            <a-button type="primary">Copy Trade URL</a-button>
            <a-button danger>Clear Calculator</a-button>
          </a-space>
        </div>
      </div>
      <a-auto-complete
        v-model:value="value"
        :options="options"
        style="width: 200px"
        placeholder="Player A..."
        @select="onSelect"
        @search="onSearch"
      />
      <AppFooter />
    </a-layout-content>
  </a-layout>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'

import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

// 3rd Party imports
import axios from 'axios'
import { message, Spin, Column, Empty, MenuProps } from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

interface MockVal {
  value: string
}
const mockVal = (str: string, repeat = 1): MockVal => {
  return {
    value: str.repeat(repeat)
  }
}
const value = ref('')
const options = ref<MockVal[]>([])
const onSearch = (searchText: string) => {
  console.log('searchText', searchText)
  if (!searchText) {
    options.value = []
  } else {
    // Filter based on the switch state and remove duplicates
    const filteredData = ranksData.value
      .filter((item) => {
        // Filter by mode based on the switch state (Superflex or OneQB)
        const mode = state.checked1 ? 'sf_value' : 'one_qb_value' // Adjust these values based on your actual data
        return item._rank_type === mode
      })
      .filter(
        (item, index, self) =>
          index === self.findIndex((t) => t.player_full_name === item.player_full_name)
      )

    // Further filter based on the searchText
    options.value = filteredData
      .filter((item) => item.player_full_name.toLowerCase().includes(searchText.toLowerCase()))
      .map((item) => ({
        value: item.player_full_name
      }))
  }
}
const onSelect = (value: string) => {
  console.log('onSelect', value)
}
watch(value, () => {
  console.log(value)
  console.log('value', value.value)
})

const isLoading = ref(false)
const ranksData = ref([{}])
const source = ref('SuperFlex')
const platform = ref('sf')

const sfLogo = ref('src/assets/sourceLogos/sf.png')
const ktcLogo = ref('src/assets/sourceLogos/ktc.png')
const dpLogo = ref('src/assets/sourceLogos/dp.png')
const fcLogo = ref('src/assets/sourceLogos/fc.png')

const state = reactive({
  checked1: true
})

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

onMounted(() => {
  fetchRanks(platform.value)
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
        break
      case 'dp':
        source.value = 'DynastyProcess'
        break
      case 'ktc':
        source.value = 'KeepTradeCut'
        break
      case 'fc':
        source.value = 'FantasyCalc'
        break
      default:
        source.value = 'sf'
    }
  }
}
</script>

<style scoped>
.trade-calculator {
  padding: 24px;
  background: #fff;
  border-radius: 2px;
}

.switches {
  margin-bottom: 24px;
  text-align: left;
}

.team-box {
  padding: 16px;
  background: #f0f2f5;
  border-radius: 2px;
}

.team-box h3 {
  margin-bottom: 16px;
}

.total-pieces {
  margin-top: 16px;
  text-align: center;
  font-weight: bold;
}

.actions {
  margin-top: 24px;
  text-align: center;
}

.dropdown-img {
  width: 24px;
  height: 20px;
  vertical-align: middle;
  border-radius: 3px;
}
</style>
