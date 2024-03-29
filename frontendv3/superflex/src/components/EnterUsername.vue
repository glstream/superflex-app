<template>
  <a-layout class="layout">
    <AppHeader />

    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item><a href="/username">Home</a></a-breadcrumb-item>
      </a-breadcrumb>
      <div class="form-container">
        <a-form
          :model="formState"
          name="basic"
          :label-col="{ span: 8 }"
          :wrapper-col="{ span: 16 }"
          autocomplete="off"
          @finish="onFinish"
          @finishFailed="onFinishFailed"
          class="form-style"
        >
          <a-form-item
            label="Username"
            name="userName"
            :rules="[{ required: true, message: 'Please input your userName!' }]"
          >
            <a-input v-model:value="formState.userName" />
          </a-form-item>
          <!-- League Year Dropdown -->
          <a-form-item
            label="League Year:"
            name="leagueYear"
            :rules="[{ required: true, message: 'Please select a league year!' }]"
          >
            <a-select v-model:value="formState.leagueYear" placeholder="Select a year">
              <a-select-option value="2023">2023</a-select-option>
              <a-select-option value="2022">2022</a-select-option>
              <a-select-option value="2021">2021</a-select-option>
              <!-- Add more years as needed -->
            </a-select>
          </a-form-item>

          <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
            <a-button type="primary" html-type="submit">Submit</a-button>
          </a-form-item>
        </a-form>
      </div>
    </a-layout-content>
    <AppFooter />
  </a-layout>
</template>
<script lang="ts" setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

// Site tags
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

// 3rd Part Utils
import axios from 'axios'

// Custom Utils
import { useGuid } from '../utils/guid'

const router = useRouter()

interface FormState {
  userName: string
  leagueYear: string
}

const formState = reactive<FormState>({
  userName: '',
  leagueYear: '2024'
})

const onFinish = async (values: any) => {
  try {
    const { getOrCreateGUID } = useGuid()
    const userGuid = getOrCreateGUID()

    console.log('User GUID:', userGuid)
    // Make a POST request to your backend server
    await axios.post('http://127.0.0.1:8000/user_details', {
      league_year: formState.leagueYear,
      user_name: formState.userName,
      guid: userGuid
    })
    console.log('Username submission successful')
    console.log(formState.userName)

    // Redirect to the /leagues endpoint
    router.push(`/leagues/${formState.leagueYear}/${formState.userName}/${userGuid}`)
  } catch (error) {
    router.push(`/leagues/${formState.userName}`)
    console.error('Failed to submit userName:', error)
    onFinishFailed(error)
  }
}

const onFinishFailed = (errorInfo: any) => {
  console.log('Failed:', errorInfo)
}
</script>
<style>
/* Basic styling */
.layout {
  min-height: 100vh;
  min-width: 1000px;
}
.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 65vh; /* Make it full height of the viewport */
}

.form-style {
  width: 100%;
  max-width: 400px; /* Adjust based on your preference */
  padding: 25px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Optional: Adds some shadow for better visuals */
  background-color: white; /* Ensure the form background is white */
}
</style>
