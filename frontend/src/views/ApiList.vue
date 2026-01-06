<template>
  <div>
    <h2>API 列表</h2>
    <div v-if="loading">加载中...</div>
    <div v-else class="api-list">
      <div v-for="api in apis" :key="api.id" class="card api-item">
        <div class="api-info">
          <h3>{{ api.name }}</h3>
          <p>{{ api.description }}</p>
          <span class="method-badge" :class="api.method.toLowerCase()">{{ api.method }}</span>
        </div>
        <button class="detail-btn" @click.stop="goToDetail(api.id)">显示详情</button>
      </div>
    </div>
    
    <!-- Admin/Demo purpose: Add API form -->
    <div class="card" style="margin-top: 2rem;">
      <h3>添加新 API (测试用)</h3>
      <form @submit.prevent="createApi">
        <input v-model="newApi.name" placeholder="名称" required />
        <input v-model="newApi.url" placeholder="URL" required />
        <select v-model="newApi.method" style="margin-bottom: 1rem; padding: 0.5rem; width: 100%;">
          <option>GET</option>
          <option>POST</option>
          <option>PUT</option>
          <option>DELETE</option>
        </select>
        <input v-model="newApi.description" placeholder="描述" />
        <textarea v-model="newApi.detail" placeholder="详情 JSON/文本" style="width: 100%; height: 100px; margin-bottom: 1rem;"></textarea>
        <button type="submit">添加 API</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const apis = ref([]);
const loading = ref(true);
const router = useRouter();

const newApi = ref({
  name: '',
  url: '',
  method: 'GET',
  description: '',
  detail: ''
});

const fetchApis = async () => {
  try {
    const response = await api.get('/apis');
    apis.value = response.data;
  } catch (err) {
    console.error('Failed to fetch APIs', err);
    if (err.response && err.response.status === 401) {
        router.push('/login');
    }
  } finally {
    loading.value = false;
  }
};

const goToDetail = (id) => {
  router.push(`/apis/${id}`);
};

const createApi = async () => {
  try {
    await api.post('/apis', newApi.value);
    newApi.value = { name: '', url: '', method: 'GET', description: '', detail: '' };
    fetchApis();
  } catch (err) {
    alert('Failed to create API');
  }
};

onMounted(() => {
  fetchApis();
});
</script>

<style scoped>
.api-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.api-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.api-card:hover {
  transform: translateY(-2px);
  border: 1px solid var(--primary-color);
}

.method-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
  color: white;
}

.get { background-color: #61affe; }
.post { background-color: #49cc90; }
.put { background-color: #fca130; }
.delete { background-color: #f93e3e; }
</style>
