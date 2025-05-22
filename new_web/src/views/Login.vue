<template>
  <div class="login-container">
    <div class="sci-fi-bg">
      <div class="cyber-grid"></div>
      <div class="cyber-lines"></div>
      <div class="cyber-glow"></div>
      <div class="cyber-particles"></div>
      <div class="cyber-circles"></div>
      <div class="cyber-scan"></div>
    </div>
    <div class="login-wrapper">
      <div class="login-content">
        <div class="card-header">
          <img src="/智能手环.png" alt="智能手环" class="logo-image" />
          <h2 class="title">智能手环后台管理系统</h2>
          <p class="subtitle">Smart Band Admin Console</p>
        </div>
        
        <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef">
          <el-form-item prop="username">
            <el-input 
              v-model="loginForm.username" 
              placeholder="请输入管理员用户名"
              prefix-icon="User"
              size="large"
              class="cyber-input"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input 
              v-model="loginForm.password" 
              type="password" 
              placeholder="请输入密码"
              prefix-icon="Lock"
              show-password
              size="large"
              class="cyber-input"
            />
          </el-form-item>
          
          <!-- 随机验证码 -->
          <el-form-item prop="verifyCode">
            <div class="code-input">
              <el-input 
                v-model="loginForm.verifyCode" 
                placeholder="请输入验证码"
                prefix-icon="Key"
                size="large"
                class="cyber-input"
              />
              <div class="identifybox" @click="refreshCode">
                <canvas ref="canvas" width="120" height="40"></canvas>
              </div>
            </div>
          </el-form-item>
          
          <el-form-item>
            <el-button 
              type="primary" 
              @click="handleLogin" 
              size="large"
              :loading="loading"
              class="cyber-button"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>

        <!-- 注意事项 -->
        <div class="agreement-section">
          <p>
            登录即表示您同意
            <el-popover
              placement="top"
              :width="400"
              trigger="click"
              popper-class="notice-popover"
            >
              <template #reference>
                <span class="agreement-link">注意事项</span>
              </template>
              <div class="notice-content">
                <h4>系统使用注意事项</h4>
                <ol>
                  <li>本系统仅供管理员使用，请勿将账号信息泄露给他人</li>
                  <li>首次登录后请及时修改密码</li>
                  <li>如遇到问题请联系超级管理员</li>
                  <li>请勿在公共场所登录系统</li>
                </ol>
              </div>
            </el-popover>
            和
            <el-popover
              placement="top"
              :width="400"
              trigger="click"
              popper-class="notice-popover"
            >
              <template #reference>
                <span class="agreement-link">隐私协议</span>
              </template>
              <div class="notice-content">
                <h4>隐私协议</h4>
                <ol>
                  <li>我们承诺对您的个人信息进行严格保密</li>
                  <li>系统仅收集必要的用户信息用于身份验证</li>
                  <li>未经授权，我们不会向第三方披露您的信息</li>
                  <li>您有权随时查看和修改您的个人信息</li>
                </ol>
              </div>
            </el-popover>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { User, Lock, Key } from '@element-plus/icons-vue';
import { adminApi } from '../utils/api';

const router = useRouter();
const loginFormRef = ref(null);
const canvas = ref(null);
const loading = ref(false);

// 背景样式
const bgStyle = {
  background: 'linear-gradient(135deg, #1a237e 0%, #283593 100%)'
};

// 登录表单
const loginForm = ref({
  username: '张航铭',
  password: 'zhanghangming',
  verifyCode: ''
});

// 验证码相关
const identifyCode = ref('');

// 登录验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ],
  verifyCode: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { validator: validateVerifyCode, trigger: 'blur' }
  ]
};

// 验证码验证
function validateVerifyCode(rule, value, callback) {
  if (value === '') {
    callback(new Error('请输入验证码'));
  } else if (value.toLowerCase() !== identifyCode.value.toLowerCase()) {
    callback(new Error('验证码不正确'));
  } else {
    callback();
  }
}

// 生成随机验证码
function refreshCode() {
  const chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
  identifyCode.value = '';
  for (let i = 0; i < 4; i++) {
    identifyCode.value += chars[Math.floor(Math.random() * chars.length)];
  }
  drawCanvas();
}

// 绘制验证码
function drawCanvas() {
  const ctx = canvas.value.getContext('2d');
  ctx.fillStyle = '#f0f2f5';
  ctx.fillRect(0, 0, canvas.value.width, canvas.value.height);
  
  // 绘制干扰线
  for (let i = 0; i < 5; i++) {
    ctx.strokeStyle = `rgb(${Math.floor(Math.random() * 100)}, ${Math.floor(Math.random() * 100)}, ${Math.floor(Math.random() * 100)})`;
    ctx.beginPath();
    ctx.moveTo(Math.random() * canvas.value.width, Math.random() * canvas.value.height);
    ctx.lineTo(Math.random() * canvas.value.width, Math.random() * canvas.value.height);
    ctx.stroke();
  }
  
  // 绘制验证码
  for (let i = 0; i < identifyCode.value.length; i++) {
    ctx.fillStyle = `rgb(${Math.floor(Math.random() * 100)}, ${Math.floor(Math.random() * 100)}, ${Math.floor(Math.random() * 100)})`;
    ctx.font = `${Math.floor(Math.random() * 10) + 20}px Arial`;
    ctx.fillText(identifyCode.value[i], 25 * i + 10, 30);
  }
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return;
  
  loading.value = true;
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      const { username, password } = loginForm.value;
      
      try {
        // 调用后端登录接口
        console.log('尝试登录:', username);
        const response = await adminApi.login(username, password);
        console.log('登录响应:', response);
        
        if (response.success) {
          // 保存登录信息与token
          const adminData = response.data.admin;
          const token = response.data.access_token;
          
          console.log('获取到token:', token);
          
          if (!token || token.trim() === '') {
            ElMessage.error('服务器返回的token无效');
            loading.value = false;
            return;
          }
          
          // 保存token和用户信息前先清除
          localStorage.removeItem('token');
          localStorage.removeItem('currentUser');
          
          // 保存新的token和用户信息
          localStorage.setItem('token', token.trim());
          localStorage.setItem('currentUser', JSON.stringify({
            id: adminData.id,
            username: adminData.username,
            nickname: adminData.nickname,
            role: adminData.role
          }));
          
          console.log('保存token和用户信息成功，当前token:', localStorage.getItem('token'));
          
          // 测试token有效性
          try {
            // 尝试获取管理员资料以验证token
            const profileResponse = await adminApi.getProfile();
            console.log('获取资料测试:', profileResponse);
            if (!profileResponse.success) {
              throw new Error('验证token失败');
            }
          } catch (verifyError) {
            console.error('token验证失败:', verifyError);
            ElMessage.warning('登录成功但验证失败，请重试');
            loading.value = false;
            return;
          }
          
          ElMessage.success('登录成功');
          
          // 确保页面完全加载前，暂停一下
          setTimeout(() => {
            router.push('/dashboard');
          }, 1000);
        } else {
          ElMessage.error(response.message || '用户名或密码错误');
        }
      } catch (error) {
        console.error('登录失败:', error);
        if (error.response && error.response.data && error.response.data.message) {
          ElMessage.error(error.response.data.message);
        } else {
          ElMessage.error('登录失败，请检查网络连接');
        }
      }
    }
    loading.value = false;
  });
};

// 初始化验证码
onMounted(() => {
  refreshCode();
});
</script>

<style scoped>
.login-container {
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  overflow: hidden;
  background: linear-gradient(135deg, #0a192f 0%, #112240 100%);
}

.sci-fi-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  overflow: hidden;
}

.cyber-grid {
  position: absolute;
  width: 200%;
  height: 200%;
  background-image: 
    linear-gradient(rgba(64, 156, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(64, 156, 255, 0.1) 1px, transparent 1px);
  background-size: 30px 30px;
  transform: perspective(500px) rotateX(60deg);
  animation: grid-move 15s linear infinite;
}

.cyber-lines {
  position: absolute;
  width: 100%;
  height: 100%;
  background: 
    repeating-linear-gradient(
      90deg,
      transparent 0%,
      transparent 49%,
      rgba(64, 156, 255, 0.1) 50%,
      transparent 51%,
      transparent 100%
    );
  animation: lines-move 3s linear infinite;
}

.cyber-glow {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(64, 156, 255, 0.15) 0%, transparent 70%);
  animation: glow-pulse 4s ease-in-out infinite;
}

.cyber-particles {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 20% 30%, rgba(64, 156, 255, 0.1) 0%, transparent 8%),
    radial-gradient(circle at 80% 70%, rgba(64, 156, 255, 0.1) 0%, transparent 8%),
    radial-gradient(circle at 40% 80%, rgba(64, 156, 255, 0.1) 0%, transparent 8%),
    radial-gradient(circle at 60% 20%, rgba(64, 156, 255, 0.1) 0%, transparent 8%);
  animation: particles-move 20s linear infinite;
}

.cyber-circles {
  position: absolute;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 50% 50%, transparent 0%, transparent 40%, rgba(64, 156, 255, 0.1) 41%, transparent 42%),
    radial-gradient(circle at 50% 50%, transparent 0%, transparent 60%, rgba(64, 156, 255, 0.1) 61%, transparent 62%),
    radial-gradient(circle at 50% 50%, transparent 0%, transparent 80%, rgba(64, 156, 255, 0.1) 81%, transparent 82%);
  animation: circles-rotate 30s linear infinite;
}

.cyber-scan {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(64, 156, 255, 0.1) 50%,
    transparent 100%
  );
  animation: scan-move 4s linear infinite;
}

@keyframes grid-move {
  0% {
    transform: perspective(500px) rotateX(60deg) translateY(0);
  }
  100% {
    transform: perspective(500px) rotateX(60deg) translateY(-30px);
  }
}

@keyframes lines-move {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 100px 0;
  }
}

@keyframes glow-pulse {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
}

@keyframes particles-move {
  0% {
    transform: translate(0, 0);
  }
  25% {
    transform: translate(-10px, -10px);
  }
  50% {
    transform: translate(0, -20px);
  }
  75% {
    transform: translate(10px, -10px);
  }
  100% {
    transform: translate(0, 0);
  }
}

@keyframes circles-rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes scan-move {
  0% {
    transform: translateY(-100%);
  }
  100% {
    transform: translateY(100%);
  }
}

.login-wrapper {
  width: 100%;
  max-width: 420px;
  padding: 20px;
  position: relative;
  z-index: 1;
  margin: 0 auto;
}

.login-content {
  padding: 30px;
  position: relative;
  z-index: 1;
}

.card-header {
  text-align: center;
  padding: 0 0 30px 0;
  background: transparent;
}

.title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #fff;
  text-shadow: 0 0 10px rgba(64, 156, 255, 0.5);
}

.subtitle {
  margin: 8px 0 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.logo-image {
  width: 120px;
  height: 120px;
  margin-bottom: 16px;
  object-fit: contain;
  filter: drop-shadow(0 0 10px rgba(64, 156, 255, 0.5));
  transition: transform 0.3s ease;
}

.logo-image:hover {
  transform: scale(1.05);
}

:deep(.cyber-input .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  box-shadow: none;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  transition: all 0.3s ease;
}

:deep(.cyber-input .el-input__wrapper:hover) {
  border-color: rgba(64, 156, 255, 0.3);
  box-shadow: 0 0 15px rgba(64, 156, 255, 0.2);
}

:deep(.cyber-input .el-input__inner) {
  color: #fff;
}

:deep(.cyber-input .el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.4);
}

:deep(.cyber-input .el-input__prefix-inner) {
  color: rgba(255, 255, 255, 0.5);
}

:deep(.cyber-button) {
  background: linear-gradient(45deg, rgba(64, 156, 255, 0.8), rgba(100, 181, 246, 0.8));
  border: none;
  box-shadow: 0 0 20px rgba(64, 156, 255, 0.2);
  transition: all 0.3s ease;
  width: 200px !important;
  margin: 0 auto;
  display: block;
}

:deep(.cyber-button:hover) {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(64, 156, 255, 0.3);
  background: linear-gradient(45deg, rgba(64, 156, 255, 0.9), rgba(100, 181, 246, 0.9));
}

:deep(.cyber-button:active) {
  transform: translateY(0);
}

.code-input {
  display: flex;
  gap: 10px;
}

.identifybox {
  width: 180px;
  height: 40px;
  cursor: pointer;
  border-radius: 4px;
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.identifybox:hover {
  transform: scale(1.02);
  border-color: rgba(64, 156, 255, 0.3);
  box-shadow: 0 0 15px rgba(64, 156, 255, 0.2);
}

/* 注意事项样式 */
.agreement-section {
  margin-top: 20px;
  text-align: center;
}

.agreement-link {
  color: #409EFF;
  cursor: pointer;
  text-decoration: underline;
  margin: 0 4px;
}

.agreement-link:hover {
  color: #66b1ff;
}

:deep(.notice-popover) {
  max-width: 400px;
}

.notice-content {
  padding: 10px;
}

.notice-content h4 {
  margin: 0 0 10px 0;
  color: #1a237e;
  font-size: 16px;
}

.notice-content ol {
  margin: 0;
  padding-left: 20px;
}

.notice-content li {
  margin-bottom: 8px;
  color: #666;
  line-height: 1.5;
}

.notice-content li:last-child {
  margin-bottom: 0;
}

:deep(.el-popover) {
  max-height: 80vh;
  overflow-y: auto;
}

:deep(.el-popover::-webkit-scrollbar) {
  width: 6px;
}

:deep(.el-popover::-webkit-scrollbar-thumb) {
  background-color: rgba(64, 156, 255, 0.3);
  border-radius: 3px;
}

:deep(.el-popover::-webkit-scrollbar-track) {
  background-color: rgba(0, 0, 0, 0.1);
}
</style>