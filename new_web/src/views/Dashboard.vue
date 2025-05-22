<template>
  <el-container class="dashboard-container">
    <el-aside :width="isCollapse ? '64px' : '200px'" class="aside-menu">
      <div class="header-section">
        <div class="collapse-btn" @click="toggleCollapse">
          <el-icon :class="{ 'is-collapse': isCollapse }">
            <Fold v-if="!isCollapse" />
            <Expand v-else />
          </el-icon>
        </div>
      </div>
      <el-menu 
        :default-active="$route.path" 
        router
        class="el-menu-vertical"
        :collapse="isCollapse">
        <el-menu-item index="/dashboard">
          <el-icon><HomeFilled /></el-icon>
          <template #title>首页</template>
        </el-menu-item>
        <el-menu-item index="/dashboard/admin">
          <el-icon><User /></el-icon>
          <template #title>管理员管理</template>
        </el-menu-item>
        <el-menu-item index="/dashboard/users">
          <el-icon><UserFilled /></el-icon>
          <template #title>用户管理</template>
        </el-menu-item>
        <el-menu-item index="/dashboard/devices">
          <el-icon><Monitor /></el-icon>
          <template #title>设备管理</template>
        </el-menu-item>
        <el-menu-item index="/dashboard/analysis">
          <el-icon><DataLine /></el-icon>
          <template #title>数据统计分析</template>
        </el-menu-item>
        <el-menu-item index="/dashboard/monitor">
          <el-icon><View /></el-icon>
          <template #title>实时数据监控</template>
        </el-menu-item>
        <el-menu-item index="/dashboard/location">
          <el-icon><Location /></el-icon>
          <template #title>设备位置</template>
        </el-menu-item>
        <el-menu-item index="/dashboard/feedback">
          <el-icon><ChatLineRound /></el-icon>
          <template #title>用户反馈</template>
        </el-menu-item>
        <el-menu-item index="/dashboard/ai-assistant">
          <el-icon><ChatDotRound /></el-icon>
          <template #title>AI助手</template>
        </el-menu-item>
        <el-menu-item index="/dashboard/settings">
          <el-icon><Setting /></el-icon>
          <template #title>系统设置</template>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container class="main-container">
      <el-header class="main-header">
        <div class="header-left">
          <div class="header-avatar">
            <el-avatar :size="40" :src="userAvatar" @error="handleAvatarError">
              {{ userNickname.charAt(0) }}
            </el-avatar>
            <span class="header-username">{{ userNickname }}</span>
          </div>
          <el-breadcrumb separator="/" class="header-breadcrumb">
            <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentRoute }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <img src="/智能手环.png" alt="智能手环" class="header-logo" />
          <span class="admin-role" :class="{ 'super-admin': isSuperAdmin }">
            {{ adminRole }}
          </span>
          <el-dropdown @command="handleCommand">
            <span class="user-dropdown">
              {{ userNickname }}
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="avatar">修改头像</el-dropdown-item>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <!-- 标签页导航 -->
      <tabs-view ref="tabsViewRef" />
      
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <keep-alive :include="cachedViews">
            <component :is="Component" :key="$route.path" />
          </keep-alive>
        </router-view>
      </el-main>
    </el-container>

    <!-- 个人信息设置对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="个人信息设置"
      width="500px"
      class="profile-dialog"
    >
      <el-form :model="profileForm" label-width="100px">
        <el-form-item label="昵称">
          <el-input v-model="profileForm.nickname" placeholder="请输入昵称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveProfile">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 头像上传对话框 -->
    <el-dialog
      v-model="avatarDialogVisible"
      title="修改头像"
      width="400px"
      class="avatar-dialog"
    >
      <div class="avatar-upload-container">
        <div class="avatar-preview">
          <el-avatar 
            :size="100" 
            :src="avatarForm.previewUrl || userAvatar"
          >
            {{ userNickname.charAt(0) }}
          </el-avatar>
        </div>
        <el-upload
          class="avatar-uploader"
          action="#"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleAvatarChange"
        >
          <el-button type="primary">选择图片</el-button>
          <div class="avatar-tip">支持JPG、PNG格式，大小不超过2MB</div>
        </el-upload>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="avatarDialogVisible = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="saveAvatar" 
            :loading="avatarSubmitting"
            :disabled="!avatarForm.file"
          >
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </el-container>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import TabsView from '../components/TabsView.vue';
import { adminApi } from '../utils/api';
import { 
  ArrowDown, 
  Plus, 
  Fold, 
  Expand,
  User,
  UserFilled,
  Monitor,
  DataLine,
  View,
  Setting,
  Location,
  ChatDotRound,
  ChatLineRound,
  HomeFilled
} from '@element-plus/icons-vue';

const router = useRouter();
const route = useRoute();
const tabsViewRef = ref(null);
const dialogVisible = ref(false);
const avatarDialogVisible = ref(false);
const avatarSubmitting = ref(false);
const userAvatar = ref('');
const userNickname = ref('');
const isCollapse = ref(false);
const isSuperAdmin = ref(false);
const cachedViews = ref([]);
const adminRole = computed(() => isSuperAdmin.value ? '超级管理员' : '普通管理员');

// 头像上传表单
const avatarForm = ref({
  file: null,
  previewUrl: ''
});

// 当前路由名称
const currentRoute = computed(() => {
  const path = route.path;
  const routeMap = {
    '/dashboard': '首页',
    '/dashboard/users': '用户管理',
    '/dashboard/devices': '设备管理',
    '/dashboard/analysis': '数据统计分析',
    '/dashboard/monitor': '实时数据监控',
    '/dashboard/location': '设备位置',
    '/dashboard/admin': '管理员管理',
    '/dashboard/feedback': '用户反馈',
    '/dashboard/settings': '系统设置',
    '/dashboard/ai-assistant': 'AI助手',
    '/dashboard/api-test': 'API测试',
  };
  
  return routeMap[path] || '未知页面';
});

const profileForm = ref({
  nickname: ''
});

// 监听路由变化，添加到缓存视图
watch(() => route.path, (newPath) => {
  // 从路径中提取组件名称，用于keep-alive缓存
  const name = getComponentNameFromPath(newPath);
  if (name && !cachedViews.value.includes(name)) {
    cachedViews.value.push(name);
  }
}, { immediate: true });

// 从路径中获取组件名称
function getComponentNameFromPath(path) {
  // 根据路径返回组件名称，用于keep-alive
  const pathToComponent = {
    '/dashboard': 'Home',
    '/dashboard/users': 'UserManagement',
    '/dashboard/devices': 'DeviceManagement',
    '/dashboard/analysis': 'DataAnalysis',
    '/dashboard/monitor': 'RealTimeMonitor',
    '/dashboard/location': 'MapLocation',
    '/dashboard/admin': 'AdminManagement',
    '/dashboard/feedback': 'UserFeedback',
    '/dashboard/settings': 'Settings',
    '/dashboard/ai-assistant': 'AiAssistant',
    '/dashboard/api-test': 'ApiTest',
  };
  
  return pathToComponent[path];
}

// 从localStorage获取用户信息
onMounted(() => {
  const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
  userAvatar.value = currentUser.avatar || 'https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png';
  userNickname.value = currentUser.nickname || currentUser.username || '管理员';
  
  // 判断是否为超级管理员 - 使用数据库中的实际角色
  isSuperAdmin.value = currentUser.role === 'super';
  
  // 初始化表单数据
  profileForm.value = {
    nickname: userNickname.value
  };
});

// 处理头像加载错误
function handleAvatarError() {
  userAvatar.value = 'https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png';
}

// 处理头像上传
function handleAvatarChange(file) {
  const isImage = file.raw.type === 'image/jpeg' || file.raw.type === 'image/png';
  const isLt2M = file.raw.size / 1024 / 1024 < 2;

  if (!isImage) {
    ElMessage.error('头像只能是JPG或PNG格式!');
    return;
  }
  
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过2MB!');
    return;
  }
  
  // 读取文件并预览
  avatarForm.value.file = file.raw;
  const reader = new FileReader();
  reader.onload = (e) => {
    avatarForm.value.previewUrl = e.target.result;
  };
  reader.readAsDataURL(file.raw);
}

// 保存头像
async function saveAvatar() {
  if (!avatarForm.value.file) {
    ElMessage.warning('请先选择头像图片');
    return;
  }
  
  avatarSubmitting.value = true;
  
  try {
    // 获取当前用户信息
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
    // 使用id或username作为标识
    if (!currentUser.id && !currentUser.username) {
      ElMessage.error('获取用户信息失败');
      avatarSubmitting.value = false;
      return;
    }
    // 使用用户ID或用户名作为标识
    const userIdentifier = currentUser.id || currentUser.username;
    
    // 读取文件为Base64
    const reader = new FileReader();
    reader.readAsDataURL(avatarForm.value.file);
    
    reader.onload = async (e) => {
      const base64Data = e.target.result;
      
      // 调用API更新头像
      try {
        const response = await adminApi.updateAdmin(userIdentifier, {
          avatar: base64Data
        });
        
        if (response.success) {
          ElMessage.success('头像更新成功');
          
          // 更新当前头像
          userAvatar.value = response.data.avatar;
          
          // 更新localStorage中的用户信息
          currentUser.avatar = response.data.avatar;
          localStorage.setItem('currentUser', JSON.stringify(currentUser));
          
          // 关闭对话框
          avatarDialogVisible.value = false;
          
          // 重置表单
          avatarForm.value = {
            file: null,
            previewUrl: ''
          };
        } else {
          ElMessage.error(response.message || '头像更新失败');
        }
      } catch (err) {
        console.error('调用API更新头像失败:', err);
        ElMessage.error('调用API更新头像失败');
      } finally {
        avatarSubmitting.value = false;
      }
    };
    
    reader.onerror = () => {
      console.error('读取头像文件失败');
      ElMessage.error('读取头像文件失败');
      avatarSubmitting.value = false;
    };
  } catch (error) {
    console.error('上传头像失败:', error);
    ElMessage.error('上传头像失败，请检查网络连接');
    avatarSubmitting.value = false;
  }
}

// 处理下拉菜单命令
function handleCommand(command) {
  if (command === 'logout') {
    ElMessageBox.confirm(
      '确定要退出登录吗？',
      '退出提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        customClass: 'logout-confirm-dialog'
      }
    ).then(() => {
    // 清除登录信息
    localStorage.removeItem('token');
    localStorage.removeItem('currentUser');
    
    // 跳转回登录页
    router.push('/login');
    
    ElMessage.success('已安全退出登录');
    }).catch(() => {
      // 用户点击取消，不做任何操作
    });
  } else if (command === 'profile') {
    dialogVisible.value = true;
  } else if (command === 'avatar') {
    avatarDialogVisible.value = true;
  }
}

// 保存个人信息
function saveProfile() {
  const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
  currentUser.nickname = profileForm.value.nickname;
  
  localStorage.setItem('currentUser', JSON.stringify(currentUser));
  
  userNickname.value = profileForm.value.nickname;
  
  dialogVisible.value = false;
  ElMessage.success('个人信息更新成功');
}

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value;
};
</script>

<style scoped>
.dashboard-container {
  height: 100vh;
  width: 100vw;
  overflow-x: hidden;
}

.main-container {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
  transition: all 0.3s ease;
}

.main-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  background: 
    radial-gradient(circle at 20% 20%, rgba(26, 35, 126, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(26, 35, 126, 0.03) 0%, transparent 50%);
}

.main-header {
  height: 60px;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
  transition: all 0.3s ease;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-avatar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-username {
  font-weight: 500;
  color: #1a237e;
}

.header-breadcrumb {
  margin-left: 15px;
}

.main-content {
  padding: 20px;
  overflow-y: auto;
  overflow-x: hidden;
  flex: 1;
}

.aside-menu {
  background-color: var(--menu-bg-color, #1a237e);
  color: var(--menu-text-color, #ffffff);
  transition: width var(--menu-transition-duration, 0.3s) ease-in-out;
  position: relative;
  z-index: 20;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-x: hidden;
  overflow-y: auto;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.main-content::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

/* 确保内容不会被滚动条遮挡 */
.main-content > * {
  padding-right: 6px;
}

.main-content::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.05);
}

.header-section {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.collapse-btn {
  height: 40px;
  width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1);
  transition: all 0.3s;
  border-radius: 8px;
  margin-left: 10px;
}

.collapse-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.el-menu-vertical:not(.el-menu--collapse) {
  width: 200px;
  border-right: none;
  transition: all 0.3s;
}

.el-menu-vertical.el-menu--collapse {
  width: 64px;
  border-right: none;
  transition: all 0.3s;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
  transition: all 0.3s ease;
  border-radius: 8px;
}

.header-logo:hover {
  transform: scale(1.05);
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #1a237e;
  font-size: 14px;
}

.user-dropdown .el-icon {
  margin-left: 5px;
}

.avatar-upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.avatar-preview {
  margin-bottom: 10px;
}

.avatar-uploader {
  text-align: center;
}

.avatar-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 10px;
}

/* 管理员角色标签 */
.admin-role {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
  background-color: #e6f7ff;
  color: #1890ff;
  border: 1px solid #91d5ff;
}

.admin-role.super-admin {
  background-color: #f6ffed;
  color: #52c41a;
  border: 1px solid #b7eb8f;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 深色模式样式 */
:global(.dark-mode) .main-container {
  background: linear-gradient(135deg, #1a1a1a 0%, #2c2c2c 100%);
}

:global(.dark-mode) .main-container::before {
  background: 
    radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
}

:global(.dark-mode) .main-header {
  background-color: #2c2c2c;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
}

:global(.dark-mode) .user-dropdown,
:global(.dark-mode) .header-username {
  color: #ffffff;
}

:global(.dark-mode) .el-breadcrumb__inner {
  color: #ffffff;
}

:global(.dark-mode) .el-breadcrumb__separator {
  color: #909399;
}

/* 对话框样式 */
:deep(.logout-confirm-dialog) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.logout-confirm-dialog .el-message-box__header) {
  background-color: #f5f7fa;
  padding: 15px 20px;
}

:deep(.logout-confirm-dialog .el-message-box__title) {
  color: #1a237e;
  font-size: 16px;
}

:deep(.logout-confirm-dialog .el-message-box__content) {
  padding: 20px;
  color: #666;
}

:deep(.logout-confirm-dialog .el-message-box__btns) {
  padding: 10px 20px 20px;
}

:deep(.logout-confirm-dialog .el-button--primary) {
  background-color: #1a237e;
  border-color: #1a237e;
}

:deep(.logout-confirm-dialog .el-button--primary:hover) {
  background-color: #283593;
  border-color: #283593;
}

/* 响应式样式 */
@media screen and (max-width: 768px) {
  .dashboard-container {
    flex-direction: column;
    height: auto;
  }
  
  .aside-menu {
    width: 100% !important;
    height: auto;
    min-height: 64px;
    flex-direction: row;
    align-items: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .aside-menu .el-menu {
    width: 100% !important;
  }
  
  .header-section {
    border-bottom: none;
    padding: 5px;
  }
  
  .collapse-btn {
    margin: 0 10px;
    height: 36px;
    width: 36px;
  }
  
  .el-menu-vertical {
    width: 100% !important;
  }
  
  .el-menu-vertical:not(.el-menu--collapse) {
    position: absolute;
    top: 64px;
    left: 0;
    width: 100% !important;
    z-index: 100;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
  
  .main-container {
    width: 100%;
    margin-top: 64px;
  }
  
  .main-header {
    padding: 0 10px;
    height: 50px;
  }
  
  .header-left {
    gap: 10px;
  }
  
  .header-avatar {
    gap: 5px;
  }
  
  .header-breadcrumb {
    margin-left: 5px;
  }
  
  .header-right {
    gap: 10px;
  }
  
  .header-logo {
    width: 32px;
    height: 32px;
  }
  
  .admin-role {
    padding: 2px 8px;
    font-size: 12px;
  }
  
  .user-dropdown {
    font-size: 12px;
  }
  
  /* 隐藏用户名在小屏幕上 */
  .header-username {
    display: none;
  }
  
  /* 隐藏面包屑部分文本在小屏幕上 */
  .el-breadcrumb {
    max-width: 120px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  /* 对话框在移动端的样式 */
  :deep(.profile-dialog),
  :deep(.avatar-dialog) {
    width: 90% !important;
    max-width: 400px;
  }
  
  :deep(.profile-dialog .el-form-item__label),
  :deep(.avatar-dialog .el-form-item__label) {
    width: 80px !important;
  }
  
  .main-content {
    padding: 10px;
  }
}

@media screen and (min-width: 769px) and (max-width: 992px) {
  .header-right {
    gap: 15px;
  }
  
  .admin-role {
    padding: 3px 10px;
    font-size: 13px;
  }
  
  .header-avatar {
    gap: 8px;
  }
}
</style> 