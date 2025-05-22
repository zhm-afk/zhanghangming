<template>
  <div class="map-container">
    <el-card class="map-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <span class="title">设备位置监控</span>
            <el-tag type="success" class="user-count">当前在线用户：{{ onlineUsers.length }}</el-tag>
          </div>
          <div class="header-right">
            <el-select v-model="selectedUser" placeholder="选择用户" @change="handleUserChange">
              <el-option
                v-for="user in users"
                :key="user.username"
                :label="user.nickname || user.username"
                :value="user.username"
              />
            </el-select>
            <el-button type="primary" @click="showAllUsers">显示所有用户</el-button>
          </div>
        </div>
      </template>
      
      <div id="map-container" class="map"></div>
      
      <div class="location-info" v-if="selectedUser">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="用户名">
            {{ selectedUser }}
          </el-descriptions-item>
          <el-descriptions-item label="最后更新时间">
            {{ lastUpdateTime }}
          </el-descriptions-item>
          <el-descriptions-item label="当前位置">
            {{ currentAddress }}
          </el-descriptions-item>
          <el-descriptions-item label="设备状态">
            <el-tag :type="getDeviceStatus(selectedUser).type">
              {{ getDeviceStatus(selectedUser).text }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <!-- 用户分布统计 -->
      <div class="distribution-info">
        <h3>用户分布统计</h3>
        <el-row :gutter="20">
          <el-col :span="8" v-for="(count, area) in areaDistribution" :key="area">
            <el-card shadow="hover" class="area-card">
              <template #header>
                <div class="area-header">
                  <span>{{ area }}</span>
                  <el-tag>{{ count }}人</el-tag>
                </div>
              </template>
              <div class="area-users">
                <el-tag 
                  v-for="user in getUsersInArea(area)" 
                  :key="user.username"
                  class="user-tag"
                >
                  {{ user.nickname || user.username }}
                </el-tag>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { getAllUsers, getUserLocation } from '../utils/userData';

const selectedUser = ref('');
const users = ref([]);
const lastUpdateTime = ref('');
const currentAddress = ref('');
let map = null;
let markers = new Map(); // 存储所有用户的标记
let geocoder = null;

// 使用userData.js中的用户数据
const userLocations = computed(() => {
  const locations = {};
  getAllUsers().forEach(user => {
    locations[user.username] = {
      lat: user.location.lat,
      lng: user.location.lng,
      area: user.location.area,
      status: 'online',
      lastUpdate: new Date()
    };
  });
  return locations;
});

// 计算在线用户
const onlineUsers = computed(() => {
  return Object.entries(userLocations.value)
    .filter(([_, data]) => data.status === 'online')
    .map(([username]) => username);
});

// 计算区域分布
const areaDistribution = computed(() => {
  const distribution = {};
  Object.values(userLocations.value).forEach(data => {
    distribution[data.area] = (distribution[data.area] || 0) + 1;
  });
  return distribution;
});

// 获取区域内的用户
function getUsersInArea(area) {
  return Object.entries(userLocations.value)
    .filter(([_, data]) => data.area === area)
    .map(([username]) => ({
      username,
      nickname: username
    }));
}

// 获取设备状态
function getDeviceStatus(username) {
  const status = userLocations.value[username]?.status;
  return {
    online: { type: 'success', text: '在线' },
    offline: { type: 'danger', text: '离线' },
    warning: { type: 'warning', text: '异常' }
  }[status] || { type: 'info', text: '未知' };
}

// 初始化地图
function initMap() {
  map = new BMap.Map("map-container");
  const point = new BMap.Point(116.404, 39.915);
  map.centerAndZoom(point, 12);
  map.enableScrollWheelZoom();
  map.addControl(new BMap.NavigationControl());
  map.addControl(new BMap.ScaleControl());
  
  // 初始化地理编码器
  geocoder = new BMap.Geocoder();
}

// 更新用户位置
function updateUserLocation(username) {
  if (!userLocations.value[username]) return;
  
  const location = userLocations.value[username];
  const point = new BMap.Point(location.lng, location.lat);
  
  // 清除旧的标记
  if (markers.has(username)) {
    map.removeOverlay(markers.get(username));
  }
  
  // 添加新的标记
  const marker = new BMap.Marker(point);
  const label = new BMap.Label(username, {
    offset: new BMap.Size(20, -10)
  });
  marker.setLabel(label);
  map.addOverlay(marker);
  markers.set(username, marker);
  
  if (selectedUser.value === username) {
    map.panTo(point);
  }
  
  // 更新地址信息
  geocoder.getLocation(point, (result) => {
    if (result) {
      currentAddress.value = result.address;
    }
  });
  
  // 更新最后更新时间
  lastUpdateTime.value = new Date().toLocaleString();
}

// 显示所有用户
function showAllUsers() {
  // 清除所有标记
  markers.forEach(marker => map.removeOverlay(marker));
  markers.clear();
  
  // 添加所有用户的标记
  Object.entries(userLocations.value).forEach(([username, location]) => {
    const point = new BMap.Point(location.lng, location.lat);
    const marker = new BMap.Marker(point);
    const label = new BMap.Label(username, {
      offset: new BMap.Size(20, -10)
    });
    marker.setLabel(label);
    map.addOverlay(marker);
    markers.set(username, marker);
  });
  
  // 调整地图视野以显示所有标记
  const points = Object.values(userLocations.value).map(loc => new BMap.Point(loc.lng, loc.lat));
  map.setViewport(points);
}

// 处理用户选择变化
function handleUserChange(username) {
  if (username) {
    updateUserLocation(username);
  }
}

// 模拟位置更新
let locationUpdateTimer = null;
function startLocationUpdates() {
  locationUpdateTimer = setInterval(() => {
    // 随机更新一个用户的位置
    const usernames = Object.keys(userLocations.value);
    const randomUser = usernames[Math.floor(Math.random() * usernames.length)];
    const location = userLocations.value[randomUser];
    
    // 随机更新位置
    location.lat += (Math.random() - 0.5) * 0.001;
    location.lng += (Math.random() - 0.5) * 0.001;
    location.lastUpdate = new Date();
    
    // 随机更新状态
    const statuses = ['online', 'offline', 'warning'];
    location.status = statuses[Math.floor(Math.random() * statuses.length)];
    
    updateUserLocation(randomUser);
  }, 5000); // 每5秒更新一次
}

onMounted(() => {
  // 加载百度地图API
  const script = document.createElement('script');
  script.src = `https://api.map.baidu.com/api?v=3.0&ak=oOPx6yjy2qPJogByYBBqOCHLiDg456YI&callback=initBMap`;
  document.head.appendChild(script);
  
  // 定义回调函数
  window.initBMap = () => {
    initMap();
    // 获取用户列表
    users.value = Object.keys(userLocations.value).map(username => ({
      username,
      nickname: username
    }));
    showAllUsers();
    startLocationUpdates();
  };
});

onUnmounted(() => {
  if (locationUpdateTimer) {
    clearInterval(locationUpdateTimer);
  }
});
</script>

<style scoped>
.map-container {
  padding: 20px;
}

.map-card {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.title {
  font-size: 18px;
  font-weight: bold;
}

.user-count {
  font-size: 14px;
}

.header-right {
  display: flex;
  gap: 10px;
}

.map {
  width: 100%;
  height: 500px;
  margin: 20px 0;
  border-radius: 8px;
  overflow: hidden;
}

.location-info {
  margin-top: 20px;
}

.distribution-info {
  margin-top: 30px;
}

.distribution-info h3 {
  margin-bottom: 20px;
  color: #333;
}

.area-card {
  margin-bottom: 20px;
}

.area-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.area-users {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.user-tag {
  margin: 2px;
}

:deep(.el-descriptions) {
  margin-top: 20px;
}

:deep(.el-descriptions__label) {
  width: 120px;
  background-color: #f5f7fa;
}

@media screen and (max-width: 768px) {
  .map {
    height: 300px;
  }
  
  .card-header {
    flex-direction: column;
    gap: 10px;
  }
  
  .header-right {
    width: 100%;
    flex-direction: column;
  }
  
  .el-select {
    width: 100%;
  }
}
</style> 