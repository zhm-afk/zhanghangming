<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <h3>用户管理</h3>
        <div>
          <el-button type="primary" @click="addUserDialogVisible = true">
            添加用户
          </el-button>
          <el-button @click="loadUsers">刷新</el-button>
        </div>
      </div>
    </template>
    
    <el-table :data="users" style="width: 100%" v-loading="loading">
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="nickname" label="昵称" />
      <el-table-column prop="age" label="年龄" />
      <el-table-column prop="deviceId" label="设备ID" />
      <el-table-column prop="registerTime" label="注册时间" />
    </el-table>
    
    <!-- 添加用户对话框 -->
    <el-dialog
      v-model="addUserDialogVisible"
      title="添加新用户"
      width="600px"
    >
      <el-form 
        :model="newUser" 
        label-width="100px"
        :rules="rules"
        ref="userFormRef"
      >
        <!-- 基本信息 -->
        <el-divider>基本信息</el-divider>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="newUser.username" />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="newUser.nickname" />
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input-number v-model="newUser.age" :min="1" :max="120" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addUserDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitting">
            提交
          </el-button>
        </span>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import { getAllUsers } from '../utils/userData';
import { userApi, smartBandUserApi } from '../utils/api';
import { formatDate } from '../utils/format';

const users = ref([]);
const loading = ref(false);
const addUserDialogVisible = ref(false);
const submitting = ref(false);
const userFormRef = ref(null);
const API_BASE_URL = 'http://182.92.87.209:5000'; // 添加API根URL

// 新用户表单数据 - 简化版，只包含基本信息
const newUser = reactive({
  username: '',
  nickname: '',
  age: 30,
  deviceId: '',
  registerTime: formatDate(new Date())
});

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' }
  ],
  age: [
    { required: true, message: '请输入年龄', trigger: 'blur' }
  ]
};

// 加载用户数据
const loadUsers = async () => {
  loading.value = true;
  try {
    // 检查token是否存在
    const token = localStorage.getItem('token');
    if (!token) {
      ElMessage.warning('未检测到登录信息，请先登录');
      users.value = getAllUsers(); // 使用本地数据
      loading.value = false;
      return;
    }

    console.log('开始获取用户数据，token存在:', !!token);
    console.log('token值:', token);
    
    // 直接通过完整URL访问API，绕过代理
    try {
      console.log('尝试直接访问API');
      const response = await fetch(`${API_BASE_URL}/api/smart-band-users/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const responseData = await response.json();
      console.log('直接API响应:', responseData);
      
      if (responseData.success) {
        users.value = responseData.data;
        ElMessage.success('成功直接加载数据');
        loading.value = false;
        return;
      }
    } catch (directError) {
      console.error('直接API请求失败:', directError);
    }
    
    // 从API获取智能手环用户数据
    try {
      console.log('尝试请求智能手环用户API');
      const smartBandResponse = await smartBandUserApi.getAllUsers();
      console.log('智能手环用户API响应:', smartBandResponse);
      
      if (smartBandResponse.success) {
        users.value = smartBandResponse.data;
        ElMessage.success('成功加载智能手环用户数据');
        loading.value = false;
        return;
      }
    } catch (smartBandError) {
      console.error('智能手环用户API请求失败:', smartBandError);
    }
    
    // 如果第一个API失败，尝试获取普通用户数据
    try {
      console.log('尝试请求普通用户API');
      const response = await userApi.getAllUsers();
      console.log('普通用户API响应:', response);
      
      if (response.success) {
        users.value = response.data;
        ElMessage.success('成功加载用户数据');
        loading.value = false;
        return;
      }
    } catch (userError) {
      console.error('普通用户API请求失败:', userError);
    }
    
    // 如果两个API都失败，使用本地数据
    console.warn('所有API请求都失败，使用本地数据');
    users.value = getAllUsers();
    ElMessage.warning('从API获取数据失败，显示本地数据');
      
  } catch (error) {
    console.error('加载用户数据失败:', error);
    // 检查是否为401认证错误
    if (error.response && error.response.status === 401) {
      ElMessage.error('登录已过期，请重新登录');
      // 清除本地token和用户信息
      localStorage.removeItem('token');
      localStorage.removeItem('currentUser');
    } else {
      // 如果出错，使用本地数据作为后备
      users.value = getAllUsers();
      ElMessage.error('加载用户数据失败，显示本地数据');
    }
  } finally {
    loading.value = false;
  }
};

// 生成唯一设备ID
const generateDeviceId = () => {
  const timestamp = new Date().getTime().toString().slice(-4);
  const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
  return `SB${timestamp}${random}`;
};

// 提交表单
const submitForm = async () => {
  if (!userFormRef.value) return;
  
  await userFormRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true;
      try {
        // 确保有一个唯一的设备ID
        if (!newUser.deviceId) {
          newUser.deviceId = generateDeviceId();
        }
        
        console.log('提交的用户数据:', newUser);
        
        // 获取token
        const token = localStorage.getItem('token');
        if (!token) {
          ElMessage.error('未检测到登录信息，请先登录');
          submitting.value = false;
          return;
        }
        
        // 直接通过完整URL访问API，绕过代理
        try {
          console.log('尝试直接访问API创建用户');
          const response = await fetch(`${API_BASE_URL}/api/smart-band-users/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(newUser)
          });
          
          if (!response.ok) {
            throw new Error(`请求失败，状态码: ${response.status}`);
          }
          
          const responseData = await response.json();
          console.log('直接API响应:', responseData);
          
          if (responseData.success) {
            ElMessage.success('添加用户成功');
            addUserDialogVisible.value = false;
            await loadUsers(); // 重新加载用户列表
            resetForm();
            submitting.value = false;
            return;
          } else {
            throw new Error(responseData.message || '创建用户失败');
          }
        } catch (directError) {
          console.error('直接API创建用户失败:', directError);
          
          // 再尝试使用原来的API方法
          const response = await userApi.createUser(newUser);
          if (response.success) {
            ElMessage.success('添加用户成功');
            addUserDialogVisible.value = false;
            await loadUsers(); // 重新加载用户列表
            resetForm();
          } else {
            ElMessage.error(`添加用户失败: ${response.message}`);
          }
        }
      } catch (error) {
        console.error('添加用户失败', error);
        ElMessage.error(`添加用户失败: ${error.message || '未知错误'}`);
      } finally {
        submitting.value = false;
      }
    } else {
      ElMessage.warning('请完善表单信息');
    }
  });
};

// 重置表单
const resetForm = () => {
  if (userFormRef.value) {
    userFormRef.value.resetFields();
  }
  
  // 重置为默认值
  Object.assign(newUser, {
    username: '',
    nickname: '',
    age: 30,
    deviceId: '',
    registerTime: formatDate(new Date()),
    // 保留默认健康和位置数据
    heartRate: 75,
    bloodPressure: { 
      systolic: 120, 
      diastolic: 80 
    },
    steps: 5000,
    location: {
      lat: 39.916527,
      lng: 116.397128,
      area: '北京市'
    }
  });
};

onMounted(() => {
  loadUsers();
});
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.el-table {
  margin-top: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 
