<template>
  <div class="card" style="max-width: 400px; margin: 2rem auto;">
    <h2 style="text-align: center;">登录</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label>用户名</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label>密码</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit" style="width: 100%;">登录</button>
      <p v-if="error" style="color: red; text-align: center;">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const username = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();

const handleLogin = async () => {
  try {
    const formData = new FormData();
    formData.append('username', username.value);
    formData.append('password', password.value);
    
    const response = await axios.post('http://localhost:8000/auth/token', formData);
    localStorage.setItem('token', response.data.access_token);
    
    // Dispatch event to update App.vue state
    window.dispatchEvent(new Event('login-success'));
    
    router.push('/apis');
  } catch (err) {
    error.value = 'Invalid username or password';
    console.error(err);
  }
};
</script>
