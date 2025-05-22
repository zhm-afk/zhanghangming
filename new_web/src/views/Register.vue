<template>
  <div class="register-container">
    <div class="register-content">
      <div class="register-header">
        <h2>智能手环管理系统</h2>
        <p>管理员注册</p>
      </div>
      
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        class="register-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名"
            :prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="确认密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            class="register-button"
            :loading="loading"
            @click="onRegister"
          >
            注册
          </el-button>
        </el-form-item>
        
        <div class="register-options">
          <router-link to="/login" class="login-link">
            已有账号？立即登录
          </router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { User, Lock } from '@element-plus/icons-vue';

const router = useRouter();
const formRef = ref(null);
const loading = ref(false);

const form = ref({
  username: '',
  password: '',
  confirmPassword: ''
});

const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'));
  } else if (value !== form.value.password) {
    callback(new Error('两次输入密码不一致'));
  } else {
    callback();
  }
};

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePass, trigger: 'blur' }
  ]
};

const onRegister = async () => {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    loading.value = true;
    
    // 检查用户名是否已存在
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    if (users.some(u => u.username === form.value.username)) {
      ElMessage.error('用户名已存在');
      return;
    }
    
    // 保存新用户
    const newUser = {
      username: form.value.username,
      password: form.value.password
    };
    users.push(newUser);
    localStorage.setItem('users', JSON.stringify(users));
    
    ElMessage.success('注册成功');
    router.push('/login');
  } catch (error) {
    console.error('表单验证失败:', error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
  position: relative;
  overflow: hidden;
}

.register-container::before {
  content: '';
  position: absolute;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 60%);
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.register-content {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  position: relative;
  z-index: 1;
}

.register-header {
  text-align: center;
  margin-bottom: 40px;
  color: #fff;
}

.register-header h2 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 10px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.register-header p {
  font-size: 16px;
  opacity: 0.9;
}

.register-form {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.9);
  box-shadow: none !important;
  border: 1px solid rgba(255, 255, 255, 0.2);
  height: 45px;
}

:deep(.el-input__inner) {
  color: #333;
}

:deep(.el-input__prefix-inner) {
  color: #1e88e5;
}

.register-button {
  width: 100%;
  height: 45px;
  font-size: 16px;
  background: linear-gradient(45deg, #1e88e5, #1565c0);
  border: none;
  border-radius: 8px;
  margin-top: 20px;
  transition: all 0.3s ease;
}

.register-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
}

.register-options {
  margin-top: 20px;
  text-align: center;
}

.login-link {
  color: #fff;
  text-decoration: none;
  font-size: 14px;
  opacity: 0.9;
  transition: all 0.3s ease;
}

.login-link:hover {
  opacity: 1;
  text-decoration: underline;
}

@media screen and (max-width: 480px) {
  .register-content {
    padding: 20px;
  }
  
  .register-header h2 {
    font-size: 24px;
  }
  
  .register-form {
    padding: 20px;
  }
}
</style> 