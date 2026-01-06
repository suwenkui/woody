<template>
  <div>
    <nav class="nav">
      <div class="logo">
        <router-link to="/" style="font-size: 1.5rem; font-weight: bold; color: var(--primary-color);">Woody API</router-link>
      </div>
      <div class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/apis">API 列表</router-link>
        <span v-if="!isLoggedIn">
          <router-link to="/login">登录</router-link>
          <router-link to="/register">注册</router-link>
        </span>
        <span v-else>
          <a href="#" @click.prevent="logout">退出</a>
        </span>
      </div>
    </nav>
    <div class="container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isLoggedIn = ref(false);

const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem('token');
};

const logout = () => {
  localStorage.removeItem('token');
  isLoggedIn.value = false;
  router.push('/login');
};

// Listen for storage changes (to update UI across tabs or after login)
// Also check on mount
onMounted(() => {
  checkLoginStatus();
  window.addEventListener('storage', checkLoginStatus);
  // Custom event for login update within the same tab
  window.addEventListener('login-success', checkLoginStatus);
});
</script>
