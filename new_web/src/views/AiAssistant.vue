<template>
  <div class="ai-assistant">
    <!-- 保持原有模板结构不变 -->
    <div class="chat-container">
      <div class="chat-messages" ref="messageContainer">
        <div v-for="(message, index) in messages" :key="index" 
             :class="['message', message.role === 'user' ? 'user-message' : 'ai-message']">
          <div class="message-content">{{ message.content }}</div>
        </div>
      </div>
      <div class="chat-input">
        <el-input
          v-model="userInput"
          type="textarea"
          :rows="3"
          placeholder="请输入您的问题..."
          @keyup.enter.ctrl="sendMessage"
          :disabled="loading"
        />
        <el-button type="primary" @click="sendMessage" :loading="loading">
          发送
        </el-button>
      </div>
    </div>
    
    <!-- API Key 设置对话框 -->
    <el-dialog v-model="showApiKeyDialog" title="设置 API Key" width="500px">
      <el-form>
        <el-form-item label="通义千问 API Key">
          <el-input v-model="tempApiKey" placeholder="请输入您的通义千问 API Key" />
        </el-form-item>
        <p class="api-key-help">
          API Key 将保存在浏览器本地存储中，仅用于当前会话。刷新页面后仍然可用。
        </p>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showApiKeyDialog = false">取消</el-button>
          <el-button type="primary" @click="saveApiKey">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 环境变量配置
let apiKey = import.meta.env.VITE_DASHSCOPE_API_KEY || ''
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api'

// API Key 设置相关
const showApiKeyDialog = ref(false)
const tempApiKey = ref('')

// 检查本地存储中是否有保存的 API Key
const checkApiKey = () => {
  const savedApiKey = localStorage.getItem('dashscope_api_key')
  if (savedApiKey) {
    apiKey = savedApiKey
    console.log('从本地存储加载 API Key')
  }
  
  // 如果没有 API Key，显示设置对话框
  if (!apiKey) {
    showApiKeyDialog.value = true
  }
}

// 保存 API Key 到本地存储
const saveApiKey = () => {
  if (tempApiKey.value) {
    localStorage.setItem('dashscope_api_key', tempApiKey.value)
    apiKey = tempApiKey.value
    showApiKeyDialog.value = false
    ElMessage.success('API Key 已保存')
  } else {
    ElMessage.error('请输入有效的 API Key')
  }
}

// 添加环境变量检查
console.log('API Key 状态:', apiKey ? '已加载' : '未加载')
console.log('API Base URL:', apiBaseUrl)

// 响应式数据
const messages = ref([])
const userInput = ref('')
const loading = ref(false)
const messageContainer = ref(null)
const currentStreamMessage = ref('')

// 流式数据处理
const handleStream = (data) => {
  try {
    const parsedData = JSON.parse(data)
    if (parsedData.output?.text) {
      currentStreamMessage.value += parsedData.output.text
      
      // 更新最后一条AI消息或新增
      const lastMsg = messages.value[messages.value.length - 1]
      if (lastMsg?.role === 'assistant') {
        lastMsg.content = currentStreamMessage.value
      } else {
        messages.value.push({ 
          role: 'assistant', 
          content: currentStreamMessage.value 
        })
      }
      
      // 自动滚动到底部
      scrollToBottom()
    }
  } catch (e) {
    console.error('消息解析错误:', e)
  }
}

// 发送消息（完整修改版）
const sendMessage = async () => {
  if (!userInput.value.trim() || loading.value) return
  
  // 检查 API Key
  if (!apiKey) {
    showApiKeyDialog.value = true
    return
  }
  
  // 添加用户消息
  const userMessage = userInput.value
  messages.value.push({ role: 'user', content: userMessage })
  userInput.value = ''
  loading.value = true
  currentStreamMessage.value = ''
  
  try {
    // 直接请求通义千问 API，不经过代理
    const endpoint = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
    console.log('正在发送请求到:', endpoint)
    console.log('使用的 API Key 前五位:', apiKey.substring(0, 5) + '...')
    
    const requestBody = {
      model: 'qwen-turbo',
      input: { 
        messages: formatMessages(messages.value)
      },
      parameters: {
        stream: true,
        incremental_output: true,
        result_format: 'message'
      }
    }
    
    console.log('请求体:', JSON.stringify(requestBody))
    
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'X-DashScope-SSE': 'enable',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify(requestBody)
    })

    console.log('API 响应状态:', response.status, response.statusText)
    
    if (!response.ok) {
      let errorText = ''
      try {
        const errorData = await response.json()
        errorText = JSON.stringify(errorData)
        console.error('API 错误响应:', errorData)
      } catch (e) {
        errorText = await response.text()
        console.error('无法解析的错误响应:', errorText)
      }
      throw new Error(`HTTP error! status: ${response.status}, 详情: ${errorText}`)
    }

    // 测试读取流的第一个块
    console.log('开始读取响应流...')
    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')
    
    while (true) {
      const { done, value } = await reader.read()
      if (done) {
        console.log('响应流读取完成')
        loading.value = false
        break
      }
      
      const chunk = decoder.decode(value, { stream: true })
      console.log('接收到响应块:', chunk)
      
      chunk.split('\n').forEach(line => {
        if (line.startsWith('data: ') && line !== 'data: [DONE]') {
          try {
            const parsedData = JSON.parse(line.slice(6))
            console.log('解析的数据:', parsedData)
            
            if (parsedData.output?.choices?.[0]?.message?.content) {
              const content = parsedData.output.choices[0].message.content
              currentStreamMessage.value += content
              
              // 更新最后一条AI消息或新增
              const lastMsg = messages.value[messages.value.length - 1]
              if (lastMsg?.role === 'assistant') {
                lastMsg.content = currentStreamMessage.value
              } else {
                messages.value.push({ 
                  role: 'assistant', 
                  content: currentStreamMessage.value 
                })
              }
              
              scrollToBottom()
            }
          } catch (e) {
            console.error('消息解析错误:', e, '原始数据:', line)
          }
        }
      })
    }
  } catch (error) {
    console.error('API请求错误:', error)
    // 添加一条错误消息到聊天
    messages.value.push({
      role: 'assistant',
      content: `请求失败: ${error.message}. 请检查API密钥和网络连接。`
    })
    
    ElMessage.error({
      message: `请求失败: ${error.message}`,
      duration: 5000,
      showClose: true
    })
    loading.value = false
  }
}

// 辅助函数
const formatMessages = (messages) => {
  return messages.map(msg => ({
    role: msg.role === 'system' ? 'system' 
          : msg.role === 'assistant' ? 'assistant' 
          : 'user',
    content: msg.content
  }))
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
  })
}

// 初始化对话
onMounted(() => {
  messages.value = [
    {
      role: 'system',
      content: '你是一个智能手环管理系统的AI助手，回答需简洁专业，首次对话需主动问候用户。'
    },
    {
      role: 'assistant',
      content: '您好！我是智能手环助手，可以帮您查询健康数据、设备设置等问题。'
    }
  ]
  
  // 检查 API Key
  checkApiKey()
})
</script>

<style scoped>
.ai-assistant {
  padding: 20px;
  height: 100%;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  scroll-behavior: smooth;
}

.message {
  margin-bottom: 20px;
  padding: 12px 16px;
  border-radius: 8px;
  max-width: 80%;
  word-wrap: break-word;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message-content {
  line-height: 1.6;
}

.user-message {
  background-color: #e3f2fd;
  margin-left: auto;
  border-bottom-right-radius: 2px;
}

.ai-message {
  background-color: #f5f5f5;
  margin-right: auto;
  border-bottom-left-radius: 2px;
}

.chat-input {
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
  background: #fafafa;
}

.chat-input .el-button {
  align-self: flex-end;
  min-width: 80px;
}

/* 深色模式适配 */
:global(.dark-mode) .chat-container {
  background: #2c2c2c;
}

:global(.dark-mode) .user-message {
  background-color: #1a237e;
  color: #fff;
}

:global(.dark-mode) .ai-message {
  background-color: #424242;
  color: #fff;
}

:global(.dark-mode) .chat-input {
  border-top-color: #444;
  background: #333;
}

.api-key-help {
  font-size: 12px;
  color: #666;
  margin-top: 8px;
}
</style>