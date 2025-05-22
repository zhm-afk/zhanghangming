<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <h3>设备管理</h3>
        <div>
          <el-button @click="loadDevices">刷新</el-button>
        </div>
      </div>
    </template>

    <el-table :data="devices" style="width: 100%" v-loading="loading">
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="deviceId" label="设备ID" />
      <el-table-column prop="status" label="状态">
        <template #default="scope">
          <el-tag :type="scope.row.status === 'online' ? 'success' : 'danger'">
            {{ scope.row.status === 'online' ? '在线' : '离线' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="lastActive" label="最后活动时间">
        <template #default="scope">
          {{ new Date(scope.row.lastActive).toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column prop="location" label="位置">
        <template #default="scope">
          {{ scope.row.location ? scope.row.location.area : '未知' }}
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button type="primary" size="small" @click="refreshDeviceStatus(scope.row)">
            刷新状态
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { ElMessage } from 'element-plus';
import { getAllUsers } from '../utils/userData';
import { userApi } from '../utils/api';

const devices = ref([]);
const loading = ref(false);
let pollingTimer = null;
const API_BASE_URL = 'http://182.92.87.209:5000'; // 添加API根URL

// 生成随机状态和活动时间
const generateRandomStatus = () => {
  return {
    status: Math.random() > 0.2 ? 'online' : 'offline',
    lastActive: new Date(Date.now() - Math.random() * 86400000).toISOString()
  };
};

// 从用户数据中加载设备信息
const processUsersToDevices = (users) => {
  return users.map(user => ({
    deviceId: user.deviceId,
    username: user.username,
    status: generateRandomStatus().status,
    lastActive: user.registerTime ? new Date(user.registerTime).toISOString() : new Date().toISOString(),
    location: user.location || { area: '未知' }
  }));
};

// 加载设备数据
const loadDevices = async () => {
  loading.value = true;
  try {
    // 检查token是否存在
    const token = localStorage.getItem('token');
    if (!token) {
      ElMessage.warning('未检测到登录信息，请先登录');
      devices.value = processUsersToDevices(getAllUsers()); // 使用本地数据
      loading.value = false;
      return;
    }

    console.log('开始获取设备数据，token存在:', !!token);
    console.log('token值:', token);
    
    // 直接通过完整URL访问API，绕过代理
    try {
      console.log('尝试直接访问API获取设备数据');
      const response = await fetch(`${API_BASE_URL}/api/smart-band-users/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const responseData = await response.json();
      console.log('直接API响应:', responseData);
      
      if (responseData.success) {
        devices.value = processUsersToDevices(responseData.data);
        ElMessage.success('成功直接加载设备数据');
        loading.value = false;
        return;
      }
    } catch (directError) {
      console.error('直接API请求失败:', directError);
    }
    
    // 尝试从API获取数据
    try {
      const response = await userApi.getAllUsers();
      if (response && response.success) {
        devices.value = processUsersToDevices(response.data);
      } else {
        // 如果API请求失败，使用本地数据作为后备
        const users = getAllUsers();
        devices.value = processUsersToDevices(users);
        ElMessage.warning('从API获取数据失败，显示本地数据');
      }
    } catch (error) {
      console.error('加载设备数据失败', error);
      // 如果出错，使用本地数据作为后备
      const users = getAllUsers();
      devices.value = processUsersToDevices(users);
      ElMessage.error('加载设备数据失败，显示本地数据');
    }
  } finally {
    loading.value = false;
  }
};

// 刷新单个设备状态
const refreshDeviceStatus = (device) => {
  const index = devices.value.findIndex(d => d.deviceId === device.deviceId);
  if (index !== -1) {
    const newStatus = generateRandomStatus();
    devices.value[index].status = newStatus.status;
    devices.value[index].lastActive = newStatus.lastActive;
    ElMessage.success(`已刷新 ${device.deviceId} 的状态`);
  }
};

// 设置轮询以定期更新设备状态
const startPolling = () => {
  // 每30秒自动刷新一次数据
  pollingTimer = setInterval(() => {
    loadDevices();
  }, 30000);
};

// 停止轮询
const stopPolling = () => {
  if (pollingTimer) {
    clearInterval(pollingTimer);
    pollingTimer = null;
  }
};

onMounted(() => {
  loadDevices();
  startPolling();
});

onUnmounted(() => {
  stopPolling();
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

:deep(.el-tag) {
  min-width: 60px;
  text-align: center;
}
</style> 