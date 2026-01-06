<template>
  <div class="card" style="max-width: 400px; margin: 2rem auto;">
    <h2 style="text-align: center;">注册</h2>
    <form @submit.prevent="handleRegister">
      <div>
        <label>用户名</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label>密码</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit" style="width: 100%;">注册</button>
      <p v-if="error" style="color: red; text-align: center;">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const username = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();

const handleRegister = async () => {
  try {
    await api.post('/auth/register', {
      username: username.value,
      password: password.value
    });
    alert('注册成功！请登录。');
    router.push('/login');
  } catch (err) {
    error.value = err.response?.data?.detail || '注册失败';
  }
};
</script>
