<template>
  <div class="min-h-screen bg-gray-100">
    <router-view v-if="initialized"></router-view>
    <div v-else class="flex justify-center items-center min-h-screen">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      initialized: false
    }
  },
  created() {
    // Check if user is registered
    const userInfo = localStorage.getItem('userInfo');
    const currentPath = this.$route.path;
    
    // If user is not registered and not already on registration page,
    // redirect to registration
    if (!userInfo && currentPath !== '/register') {
      this.$router.push('/register');
    } else if (userInfo && currentPath === '/register') {
      // If user is registered and on registration page,
      // redirect to main page
      this.$router.push('/main');
    }
    
    this.initialized = true;
  }
}
</script>

<style>
  @import url('./assets/tailwind.css');
  @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700&display=swap');

  :root {
    font-family: 'Heebo', sans-serif;
  }
</style>
