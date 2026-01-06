<template>
  <div v-if="apiData" class="card">
    <div style="margin-bottom: 1rem;">
        <button @click="$router.back()" style="background: transparent; color: var(--text-color); padding-left: 0;">&larr; 返回</button>
    </div>
    <h1>{{ apiData.name }}</h1>
    <div class="badge-container">
        <span class="method-badge" :class="apiData.method.toLowerCase()">{{ apiData.method }}</span>
        <span class="url">{{ apiData.url }}</span>
    </div>
    
    <div class="section">
        <h3>描述</h3>
        <p>{{ apiData.description }}</p>
    </div>

    <!-- 参数输入区域 -->
    <div class="section" v-if="parsedDetail.params && parsedDetail.params.length > 0">
        <h3>输入参数</h3>
        <div v-for="param in parsedDetail.params" :key="param.name" class="param-input">
            <label>{{ param.name }} <span v-if="param.required" style="color: red">*</span></label>
            <input v-model="inputParams[param.name]" :placeholder="param.description || param.type" />
        </div>
    </div>

    <div class="section" v-if="parsedDetail.body">
        <h3>Request Body (JSON)</h3>
        <textarea v-model="inputBody" placeholder="输入 JSON 格式的请求体" style="width: 100%; height: 100px;"></textarea>
    </div>

    <div class="section">
        <button @click="callApi" :disabled="calling">
            {{ calling ? '调用中...' : '调用 API' }}
        </button>
    </div>

    <!-- 调用结果 -->
    <div class="section" v-if="apiResult">
        <h3>调用结果</h3>
        <div :class="['result-box', apiResult.status === 'success' ? 'success' : 'error']">
            <pre>{{ apiResult.data }}</pre>
        </div>
    </div>

    <div class="section">
        <h3>元数据详情</h3>
        <pre>{{ apiData.detail }}</pre>
    </div>
  </div>
  <div v-else>加载中...</div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import api from '../api';

const route = useRoute();
const apiData = ref(null);
const parsedDetail = ref({});
const inputParams = ref({});
const inputBody = ref('');
const calling = ref(false);
const apiResult = ref(null);

onMounted(async () => {
  try {
    const response = await api.get(`/apis/${route.params.id}`);
    apiData.value = response.data;
    try {
        parsedDetail.value = JSON.parse(apiData.value.detail || '{}');
        // 初始化 params
        if (parsedDetail.value.params) {
            parsedDetail.value.params.forEach(p => {
                inputParams.value[p.name] = '';
            });
        }
    } catch (e) {
        console.error("Failed to parse detail JSON", e);
        parsedDetail.value = {};
    }
  } catch (err) {
    console.error('Failed to fetch API detail', err);
  }
});

const callApi = async () => {
    calling.value = true;
    apiResult.value = null;
    
    try {
        let url = apiData.value.url;
        const queryParams = {};
        
        // 处理 URL 参数和 Query 参数
        if (parsedDetail.value.params) {
            parsedDetail.value.params.forEach(p => {
                const val = inputParams.value[p.name];
                if (p.type === 'path') {
                    url = url.replace(`{${p.name}}`, val);
                } else {
                    if (val) queryParams[p.name] = val;
                }
            });
        }

        const config = {
            method: apiData.value.method,
            url: url,
            params: queryParams,
        };

        if (['POST', 'PUT'].includes(apiData.value.method.toUpperCase()) && inputBody.value) {
            try {
                config.data = JSON.parse(inputBody.value);
            } catch (e) {
                alert('Request Body 必须是合法的 JSON');
                calling.value = false;
                return;
            }
        }

        const response = await api(config);
        apiResult.value = {
            status: 'success',
            data: response.data
        };
    } catch (err) {
        apiResult.value = {
            status: 'error',
            data: err.response ? err.response.data : err.message
        };
    } finally {
        calling.value = false;
    }
};
</script>

<style scoped>
.badge-container {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
}
.method-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: bold;
  color: white;
}
.url {
    font-family: monospace;
    background: #f0f0f0;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
}
.section {
    margin-top: 2rem;
}
.get { background-color: #61affe; }
.post { background-color: #49cc90; }
.put { background-color: #fca130; }
.delete { background-color: #f93e3e; }
pre {
    background: #f1f5f9;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
}
.param-input {
    margin-bottom: 1rem;
}
.param-input label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
}
.result-box {
    padding: 1rem;
    border-radius: 4px;
}
.result-box.success {
    border: 1px solid #49cc90;
    background-color: #f0fdf4;
}
.result-box.error {
    border: 1px solid #f93e3e;
    background-color: #fef2f2;
}
</style>
