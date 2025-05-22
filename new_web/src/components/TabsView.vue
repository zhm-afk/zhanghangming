<template>
  <div class="tabs-view-container">
    <el-scrollbar class="tabs-scrollbar">
      <div class="tabs-wrapper">
        <!-- 标签页列表 -->
        <el-tag
          v-for="tab in visitedViews"
          :key="tab.fullPath"
          :class="{ 'active-tab': isActive(tab) }"
          :closable="tab.path !== '/dashboard'"
          @click="goToTab(tab)"
          @close="closeTab(tab)"
          size="large"
          class="tab-item"
          :data-path="tab.path"
          @contextmenu.prevent="openContextMenu($event, tab)"
        >
          <el-icon class="tab-icon" v-if="tab.meta && tab.meta.icon">
            <component :is="tab.meta.icon" />
          </el-icon>
          {{ getTabTitle(tab) }}
        </el-tag>
      </div>
    </el-scrollbar>

    <!-- 右键菜单 -->
    <ul v-show="contextMenuVisible" class="contextmenu" :style="contextMenuStyle">
      <li @click="refreshSelectedTab">刷新页面</li>
      <li @click="closeSelectedTab">关闭页面</li>
      <li @click="closeOtherTabs">关闭其他页面</li>
      <li @click="closeAllTabs">关闭所有页面</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';

// 路由实例和当前路由
const router = useRouter();
const route = useRoute();

// 已访问页面和页面标题映射
const visitedViews = ref([]);
const pageTitle = {
  '/dashboard': '首页',
  '/dashboard/users': '用户管理',
  '/dashboard/devices': '设备管理',
  '/dashboard/analysis': '数据统计分析',
  '/dashboard/monitor': '实时数据监控',
  '/dashboard/settings': '系统设置',
  '/dashboard/location': '设备位置',
  '/dashboard/admin': '管理员管理',
  '/dashboard/feedback': '用户反馈',
  '/dashboard/ai-assistant': 'AI助手',
  '/dashboard/api-test': 'API测试',
};

// 图标映射
const pageIcons = {
  '/dashboard': 'HomeFilled',
  '/dashboard/users': 'UserFilled',
  '/dashboard/devices': 'Monitor',
  '/dashboard/analysis': 'DataLine',
  '/dashboard/monitor': 'View',
  '/dashboard/settings': 'Setting',
  '/dashboard/location': 'Location',
  '/dashboard/admin': 'User',
  '/dashboard/feedback': 'ChatLineRound',
  '/dashboard/ai-assistant': 'ChatDotRound',
  '/dashboard/api-test': 'Connection',
};

// 右键菜单相关
const contextMenuVisible = ref(false);
const contextMenuStyle = ref({});
const selectedTab = ref(null);

// 初始化
onMounted(() => {
  // 添加首页标签
  const homeTab = {
    name: 'Home',
    path: '/dashboard',
    fullPath: '/dashboard',
    meta: { title: '首页', icon: 'HomeFilled' },
  };
  
  // 添加首页标签
  if (!visitedViews.value.some(tab => tab.path === homeTab.path)) {
    visitedViews.value.push(homeTab);
  }

  // 如果当前路由不是首页，添加当前页面标签
  if (route.path !== '/dashboard') {
    addVisitedView(route);
  }

  // 添加右键菜单事件监听
  document.addEventListener('click', closeContextMenu);
});

onUnmounted(() => {
  document.removeEventListener('click', closeContextMenu);
});

// 监听路由变化以添加新标签
watch(() => route.path, (newPath) => {
  if (newPath.startsWith('/dashboard')) {
    addVisitedView(route);
  }
}, { immediate: true });

// 添加访问过的页面
function addVisitedView(view) {
  const { path, fullPath, meta = {} } = view;
  
  // 检查标签是否已存在
  if (!visitedViews.value.some(v => v.path === path)) {
    // 为路由添加标题和图标
    const title = meta.title || pageTitle[path] || '未命名页面';
    const icon = meta.icon || pageIcons[path] || '';
    
    visitedViews.value.push({
      name: view.name,
      path,
      fullPath,
      meta: { ...meta, title, icon }
    });
  }
}

// 获取标签标题
function getTabTitle(tab) {
  return tab.meta?.title || pageTitle[tab.path] || '未命名页面';
}

// 检查标签是否激活
function isActive(tab) {
  return tab.path === route.path;
}

// 跳转到选中的标签页
function goToTab(tab) {
  if (tab.path !== route.path) {
    router.push(tab.path);
  }
}

// 关闭标签页
function closeTab(tab) {
  // 不允许关闭首页
  if (tab.path === '/dashboard') {
    return;
  }
  
  // 查找要关闭的标签索引
  const tabIndex = visitedViews.value.findIndex(v => v.path === tab.path);
  if (tabIndex !== -1) {
    // 如果关闭的是当前激活的标签，则需要跳转到其他标签
    if (isActive(tab)) {
      const nextTab = visitedViews.value[tabIndex - 1] || visitedViews.value[tabIndex + 1];
      if (nextTab) {
        router.push(nextTab.path);
      } else {
        // 如果没有其他标签，则跳转到首页
        router.push('/dashboard');
      }
    }
    
    // 移除标签
    visitedViews.value.splice(tabIndex, 1);
  }
}

// 右键菜单处理程序
function openContextMenu(e, tab) {
  e.preventDefault();
  closeContextMenu();
  
  selectedTab.value = tab;
  contextMenuStyle.value = {
    left: `${e.clientX}px`,
    top: `${e.clientY}px`,
  };
  contextMenuVisible.value = true;
}

// 关闭右键菜单
function closeContextMenu() {
  contextMenuVisible.value = false;
}

// 刷新选中标签
function refreshSelectedTab() {
  if (selectedTab.value) {
    const { fullPath } = selectedTab.value;
    // 先跳转到一个不存在的路径，再回到当前路径以触发组件重新渲染
    router.replace(`/redirect${fullPath}`).catch(() => {
      // 错误处理
      ElMessage.warning('页面刷新失败');
    });
  }
  closeContextMenu();
}

// 关闭选中标签
function closeSelectedTab() {
  if (selectedTab.value && selectedTab.value.path !== '/dashboard') {
    closeTab(selectedTab.value);
  }
  closeContextMenu();
}

// 关闭其他标签
function closeOtherTabs() {
  if (selectedTab.value) {
    // 保留首页和当前选中的标签
    visitedViews.value = visitedViews.value.filter(
      tab => tab.path === '/dashboard' || tab.path === selectedTab.value.path
    );
  }
  closeContextMenu();
}

// 关闭所有标签
function closeAllTabs() {
  // 只保留首页
  visitedViews.value = visitedViews.value.filter(tab => tab.path === '/dashboard');
  router.push('/dashboard');
  closeContextMenu();
}

// 提供公共方法
defineExpose({
  addVisitedView,
  closeTab,
});
</script>

<style scoped>
.tabs-view-container {
  position: relative;
  height: 40px;
  width: 100%;
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 0 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 99;
}

.tabs-scrollbar {
  width: 100%;
  white-space: nowrap;
}

.tabs-wrapper {
  display: inline-flex;
  align-items: center;
  height: 100%;
  padding: 4px 0;
}

.tab-item {
  margin: 0 5px;
  cursor: pointer;
  height: 32px;
  line-height: 32px;
  padding: 0 16px;
  border-radius: 4px;
  user-select: none;
  display: flex;
  align-items: center;
  transition: all 0.3s;
  font-weight: 500;
  border: 1px solid #dcdfe6;
  background-color: #f5f7fa;
}

.tab-item:hover {
  background-color: #ecf5ff;
  border-color: #c6e2ff;
}

.tab-icon {
  margin-right: 6px;
  font-size: 16px;
}

.active-tab {
  background-color: var(--el-color-primary);
  color: white;
  border-color: var(--el-color-primary);
}

.active-tab:hover {
  background-color: var(--el-color-primary);
  filter: brightness(1.1);
}

.active-tab .el-icon {
  color: white;
}

/* 右键菜单样式 */
.contextmenu {
  position: fixed;
  z-index: 3000;
  background-color: #fff;
  padding: 5px 0;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  list-style: none;
  margin: 0;
}

.contextmenu li {
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  color: #606266;
}

.contextmenu li:hover {
  background-color: #f5f7fa;
  color: var(--el-color-primary);
}

/* 适配深色模式 */
:global(.dark-mode) .tabs-view-container {
  background-color: #2c2c2c;
  border-bottom: 1px solid #4c4c4c;
}

:global(.dark-mode) .contextmenu {
  background-color: #2c2c2c;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.5);
}

:global(.dark-mode) .contextmenu li {
  color: #d0d0d0;
}

:global(.dark-mode) .contextmenu li:hover {
  background-color: #3c3c3c;
}

/* 移动端响应式 */
@media screen and (max-width: 768px) {
  .tabs-view-container {
    height: 36px;
    padding: 0 5px;
  }
  
  .tab-item {
    padding: 0 8px;
    margin: 0 2px;
    height: 28px;
    line-height: 28px;
    font-size: 12px;
  }
  
  .tab-icon {
    margin-right: 2px;
  }
}
</style> 