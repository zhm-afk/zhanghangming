<template>
  <div class="api-test">
    <h2>API 连接测试</h2>
    
    <el-card class="test-card">
      <template #header>
        <div class="card-header">
          <span>通义千问 API 测试</span>
        </div>
      </template>
      
      <div class="input-section">
        <el-input
          v-model="apiKey"
          placeholder="输入 API Key"
          type="password"
          show-password
          clearable
        />
        
        <el-input
          v-model="prompt"
          type="textarea"
          :rows="3"
          placeholder="输入测试问题"
          class="mt-3"
        />
        
        <div class="mt-3">
          <el-button type="primary" @click="testApi" :loading="loading">
            测试 API 连接
          </el-button>
          <el-button @click="clearResult">
            清除结果
          </el-button>
        </div>
      </div>
      
      <div v-if="result" class="result-section">
        <h3>测试结果</h3>
        <pre>{{ result }}</pre>
      </div>
      
      <div v-if="error" class="error-section">
        <h3>错误信息</h3>
        <pre>{{ error }}</pre>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const apiKey = ref('')
const prompt = ref('你好，请做一个自我介绍')
const result = ref('')
const error = ref('')
const loading = ref(false)

const testApi = async () => {
  if (!apiKey.value) {
    ElMessage.warning('请输入 API Key')
    return
  }
  
  if (!prompt.value.trim()) {
    ElMessage.warning('请输入测试问题')
    return
  }
  
  loading.value = true
  result.value = ''
  error.value = ''
  
  try {
    const response = await fetch('https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey.value}`
      },
      body: JSON.stringify({
        model: 'qwen-turbo',
        input: {
          messages: [
            { role: 'system', content: '你是一个有帮助的AI助手' },
            { role: 'user', content: prompt.value }
          ]
        }
      })
    })
    
    const responseData = await response.json()
    result.value = JSON.stringify(responseData, null, 2)
    
    if (!response.ok) {
      error.value = `错误状态码: ${response.status}\n${JSON.stringify(responseData, null, 2)}`
    }
  } catch (err) {
    console.error('API 测试错误:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const clearResult = () => {
  result.value = ''
  error.value = ''
}

// 自动从本地存储加载 API Key
if (localStorage.getItem('dashscope_api_key')) {
  apiKey.value = localStorage.getItem('dashscope_api_key')
}
</script>

<style scoped>
.api-test {
  padding: 20px;
}

.test-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.input-section {
  margin-bottom: 20px;
}

.mt-3 {
  margin-top: 12px;
}

.result-section, .error-section {
  margin-top: 20px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
  overflow: auto;
}

.result-section pre, .error-section pre {
  white-space: pre-wrap;
  word-break: break-word;
}

.error-section {
  background-color: #fff8f8;
  color: #d81e06;
}
</style> 