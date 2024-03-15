<!-- src/components/AppHeader.vue -->
<template>
  <a-layout-header>
    <div class="logo" :style="{ backgroundImage: 'url(' + logoImg + ')' }"></div>
    <a-menu theme="dark" mode="horizontal" :default-selected-keys="['1']">
      <a-menu-item key="1"><router-link to="/username">Home</router-link></a-menu-item>
      <!-- Add more menu items as needed -->
    </a-menu>
  </a-layout-header>
</template>

<script setup>
import { ref } from 'vue'
import logoImg from '@/assets/logo_small.png' // Adjust the path as necessary
</script>

<style scoped>
.logo {
  float: left;
  width: 120px; /* Adjust as needed */
  height: 31px; /* Adjust as needed */
  margin: 16px 24px 16px 0;
  background-size: contain; /* Ensure the logo fits well */
  background-position: center;
  background-repeat: no-repeat;
  background-color: transparent;
}
</style>
