<template>
  <div class="settings-container">
    <el-card class="settings-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="header-title">系统设置</span>
        </div>
      </template>

      <el-form label-width="120px" class="settings-form">
        <!-- 主题设置 -->
        <el-form-item label="主题模式">
          <div class="theme-switch">
            <el-switch
              v-model="isDarkMode"
              active-text="夜间模式"
              inactive-text="默认模式"
              @change="handleThemeChange"
              class="custom-switch"
            />
            <div class="theme-preview" :class="{ 'dark': isDarkMode }">
              <div class="preview-header"></div>
              <div class="preview-content"></div>
            </div>
          </div>
        </el-form-item>

        <!-- 主题颜色 -->
        <el-form-item label="主题颜色">
          <div class="color-picker">
            <el-radio-group v-model="themeColor" @change="handleThemeColorChange">
              <el-radio-button label="#1a237e">默认蓝</el-radio-button>
              <el-radio-button label="#2e7d32">森林绿</el-radio-button>
              <el-radio-button label="#c62828">中国红</el-radio-button>
              <el-radio-button label="#6a1b9a">典雅紫</el-radio-button>
            </el-radio-group>
          </div>
        </el-form-item>

        <!-- 字体大小设置 -->
        <el-form-item label="字体大小">
          <div class="font-size-control">
            <el-slider
              v-model="fontSize"
              :min="12"
              :max="20"
              :step="1"
              show-input
              @change="handleFontSizeChange"
              class="custom-slider"
            />
            <div class="font-preview" :style="{ fontSize: fontSize + 'px' }">
              预览文字大小
            </div>
          </div>
        </el-form-item>

        <!-- 字体样式 -->
        <el-form-item label="字体样式">
          <el-select v-model="fontFamily" @change="handleFontFamilyChange" class="font-family-select">
            <el-option label="默认字体" value="default" />
            <el-option label="微软雅黑" value="Microsoft YaHei" />
            <el-option label="思源黑体" value="Source Han Sans CN" />
            <el-option label="苹方" value="PingFang SC" />
          </el-select>
        </el-form-item>

        <!-- 数据刷新频率 -->
        <el-form-item label="数据刷新频率">
          <el-radio-group v-model="refreshRate" @change="handleRefreshRateChange" class="refresh-rate-group">
            <el-radio-button label="1000">1秒</el-radio-button>
            <el-radio-button label="3000">3秒</el-radio-button>
            <el-radio-button label="5000">5秒</el-radio-button>
            <el-radio-button label="10000">10秒</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <!-- 消息通知 -->
        <el-form-item label="消息通知">
          <div class="notification-setting">
            <el-switch
              v-model="enableNotification"
              @change="handleNotificationChange"
              class="custom-switch"
            />
            <span class="notification-desc">
              {{ enableNotification ? '已开启消息通知' : '已关闭消息通知' }}
            </span>
          </div>
        </el-form-item>

        <!-- 通知声音 -->
        <el-form-item label="通知声音" v-if="enableNotification">
          <div class="sound-setting">
            <el-switch
              v-model="enableSound"
              @change="handleSoundChange"
              class="custom-switch"
            />
            <el-select v-model="soundType" :disabled="!enableSound" class="sound-select">
              <el-option label="默认提示音" value="default" />
              <el-option label="清脆铃声" value="bell" />
              <el-option label="柔和提示" value="soft" />
            </el-select>
          </div>
        </el-form-item>

        <!-- 数据导出设置 -->
        <el-form-item label="数据导出">
          <div class="export-setting">
            <el-checkbox-group v-model="exportFormats" @change="handleExportFormatsChange">
              <el-checkbox label="excel">Excel</el-checkbox>
              <el-checkbox label="csv">CSV</el-checkbox>
              <el-checkbox label="pdf">PDF</el-checkbox>
            </el-checkbox-group>
            <el-select v-model="defaultExportFormat" class="export-format-select">
              <el-option label="Excel" value="excel" />
              <el-option label="CSV" value="csv" />
              <el-option label="PDF" value="pdf" />
            </el-select>
          </div>
        </el-form-item>

        <!-- 自动备份 -->
        <el-form-item label="自动备份">
          <div class="backup-setting">
            <el-switch
              v-model="enableAutoBackup"
              @change="handleAutoBackupChange"
              class="custom-switch"
            />
            <el-select 
              v-model="backupFrequency" 
              :disabled="!enableAutoBackup"
              class="backup-frequency-select"
            >
              <el-option label="每天" value="daily" />
              <el-option label="每周" value="weekly" />
              <el-option label="每月" value="monthly" />
            </el-select>
          </div>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="info-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="header-title">系统信息</span>
        </div>
      </template>
      
      <div class="system-info">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="info-item">
              <el-icon><Monitor /></el-icon>
              <div class="info-content">
                <div class="info-label">系统版本</div>
                <div class="info-value">v1.0.0</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="info-item">
              <el-icon><Cpu /></el-icon>
              <div class="info-content">
                <div class="info-label">CPU使用率</div>
                <div class="info-value">45%</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="info-item">
              <el-icon><Connection /></el-icon>
              <div class="info-content">
                <div class="info-label">内存使用</div>
                <div class="info-value">60%</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="info-item">
              <el-icon><DataLine /></el-icon>
              <div class="info-content">
                <div class="info-label">数据总量</div>
                <div class="info-value">2.5TB</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { Monitor, Cpu, Connection, DataLine } from '@element-plus/icons-vue';

// 主题设置
const isDarkMode = ref(false);
const themeColor = ref('#1a237e');
const fontSize = ref(14);
const fontFamily = ref('default');
const refreshRate = ref('1000');
const enableNotification = ref(true);
const enableSound = ref(true);
const soundType = ref('default');
const exportFormats = ref(['excel', 'csv']);
const defaultExportFormat = ref('excel');
const enableAutoBackup = ref(false);
const backupFrequency = ref('daily');

// 初始化设置
onMounted(() => {
  // 从localStorage加载设置
  const settings = JSON.parse(localStorage.getItem('userSettings') || '{}');
  isDarkMode.value = settings.isDarkMode || false;
  themeColor.value = settings.themeColor || '#1a237e';
  fontSize.value = settings.fontSize || 14;
  fontFamily.value = settings.fontFamily || 'default';
  refreshRate.value = settings.refreshRate || '1000';
  enableNotification.value = settings.enableNotification !== false;
  enableSound.value = settings.enableSound !== false;
  soundType.value = settings.soundType || 'default';
  exportFormats.value = settings.exportFormats || ['excel', 'csv'];
  defaultExportFormat.value = settings.defaultExportFormat || 'excel';
  enableAutoBackup.value = settings.enableAutoBackup || false;
  backupFrequency.value = settings.backupFrequency || 'daily';

  // 应用设置
  applySettings();
});

// 处理主题切换
function handleThemeChange(value) {
  document.body.className = value ? 'dark-mode' : '';
  saveSettings();
}

// 处理主题颜色变化
function handleThemeColorChange(value) {
  // 设置主题颜色
  document.documentElement.style.setProperty('--el-color-primary', value);
  
  // 计算不同亮度的颜色变体
  const menuBgColor = value; // 使用主题色本身作为菜单背景色
  const menuHoverColor = getLighterColor(value, 0.2); // 略微亮一点的悬停色
  const menuActiveColor = getLighterColor(value, 0.3); // 更亮一点的选中背景色
  const menuTextColor = '#ffffff'; // 统一使用白色文本
  const activeTextColor = '#ffffff'; // 选中状态也使用白色文本
  
  // 设置CSS变量用于菜单样式
  document.documentElement.style.setProperty('--menu-bg-color', menuBgColor);
  document.documentElement.style.setProperty('--menu-hover-color', menuHoverColor);
  document.documentElement.style.setProperty('--menu-active-bg-color', menuActiveColor);
  document.documentElement.style.setProperty('--menu-text-color', menuTextColor);
  document.documentElement.style.setProperty('--menu-active-text-color', activeTextColor);
  
  // 直接将样式应用到DOM上（不使用setTimeout）
  updateMenuStyles(menuBgColor, menuHoverColor, menuActiveColor, menuTextColor, activeTextColor);
  
  saveSettings();
}

// 更新菜单样式的函数
function updateMenuStyles(bgColor, hoverColor, activeColor, textColor, activeTextColor) {
  // 先移除可能存在的样式标签
  const existingStyle = document.getElementById('dynamic-menu-styles');
  if (existingStyle) {
    existingStyle.remove();
  }
  
  // 确保CSS变量存在
  if (!document.documentElement.style.getPropertyValue('--menu-transition-duration')) {
    document.documentElement.style.setProperty('--menu-transition-duration', '0.3s');
  }
  
  // 创建新的样式标签
  const styleEl = document.createElement('style');
  styleEl.id = 'dynamic-menu-styles';
  
  // 定义菜单样式规则
  styleEl.innerHTML = `
    /* 主菜单容器 */
    .el-menu, .el-menu--vertical, .el-menu--horizontal {
      background-color: ${bgColor} !important;
      border-right-color: ${getLighterColor(bgColor, 0.3)} !important;
      transition: all var(--menu-transition-duration) !important;
    }
    
    /* 水平菜单项 */
    .el-menu--horizontal > .el-menu-item,
    .el-menu--horizontal > .el-sub-menu .el-sub-menu__title {
      background-color: ${bgColor} !important;
      color: ${textColor} !important;
      border-bottom-color: transparent !important;
      transition: all var(--menu-transition-duration) !important;
    }
    
    /* 所有菜单项和子菜单标题 */
    .el-menu-item,
    .el-sub-menu__title {
      color: ${textColor} !important;
      background-color: ${bgColor} !important;
      transition: all var(--menu-transition-duration) !important;
    }
    
    /* 悬停和焦点状态 */
    .el-menu-item:hover,
    .el-menu-item:focus,
    .el-sub-menu__title:hover,
    .el-sub-menu:hover > .el-sub-menu__title {
      background-color: ${hoverColor} !important;
      color: ${textColor} !important;
      transition: all var(--menu-transition-duration) !important;
    }
    
    /* 活动菜单项 */
    .el-menu-item.is-active,
    .el-sub-menu.is-active > .el-sub-menu__title {
      color: ${activeTextColor} !important;
      background-color: ${activeColor} !important;
      transition: all var(--menu-transition-duration) !important;
    }
    
    /* 弹出菜单 */
    .el-menu--popup,
    .el-menu--vertical .el-menu--popup,
    .el-menu--horizontal .el-menu--popup {
      background-color: ${bgColor} !important;
      transition: all var(--menu-transition-duration) !important;
    }
    
    /* 弹出菜单项 */
    .el-menu--popup .el-menu-item,
    .el-menu--popup .el-sub-menu__title {
      background-color: ${bgColor} !important;
      color: ${textColor} !important;
      transition: all var(--menu-transition-duration) !important;
    }
    
    /* 弹出菜单悬停 */
    .el-menu--popup .el-menu-item:hover,
    .el-menu--popup .el-menu-item:focus,
    .el-menu--popup .el-sub-menu__title:hover {
      background-color: ${hoverColor} !important;
      color: ${textColor} !important;
      transition: all var(--menu-transition-duration) !important;
    }
    
    /* 弹出菜单活动项 */
    .el-menu--popup .el-menu-item.is-active {
      background-color: ${activeColor} !important;
      color: ${activeTextColor} !important;
      transition: all var(--menu-transition-duration) !important;
    }
    
    /* 图标颜色 */
    .el-menu-item .el-icon,
    .el-sub-menu__title .el-icon {
      color: ${textColor} !important;
      transition: all var(--menu-transition-duration) !important;
    }
    
    /* 折叠菜单 */
    .el-menu--collapse .el-menu-item,
    .el-menu--collapse .el-sub-menu__title {
      background-color: ${bgColor} !important;
      color: ${textColor} !important;
      transition: all var(--menu-transition-duration) !important;
    }
  `;
  
  // 插入到文档头部
  document.head.appendChild(styleEl);
  
  // 直接修改当前菜单元素样式
  try {
    const transitionValue = `all var(--menu-transition-duration)`;
    
    // 主菜单
    const menus = document.querySelectorAll('.el-menu');
    menus.forEach(menu => {
      menu.style.backgroundColor = bgColor;
      menu.style.borderRightColor = getLighterColor(bgColor, 0.3);
      menu.style.transition = transitionValue;
    });
    
    // 所有菜单项
    const menuItems = document.querySelectorAll('.el-menu-item, .el-sub-menu__title');
    menuItems.forEach(item => {
      item.style.backgroundColor = bgColor;
      item.style.color = textColor;
      item.style.transition = transitionValue;
    });
    
    // 活动菜单项
    const activeItems = document.querySelectorAll('.el-menu-item.is-active, .el-sub-menu.is-active > .el-sub-menu__title');
    activeItems.forEach(item => {
      item.style.backgroundColor = activeColor;
      item.style.color = activeTextColor;
      item.style.transition = transitionValue;
    });
    
    // 子菜单
    const subMenus = document.querySelectorAll('.el-menu--popup');
    subMenus.forEach(menu => {
      menu.style.backgroundColor = bgColor;
      menu.style.transition = transitionValue;
    });
    
    // 图标
    const icons = document.querySelectorAll('.el-menu-item .el-icon, .el-sub-menu__title .el-icon');
    icons.forEach(icon => {
      icon.style.color = textColor;
      icon.style.transition = transitionValue;
    });
  } catch (e) {
    console.error('更新菜单样式时出错:', e);
  }
}

// 获取较亮版本的颜色（用于菜单背景）
function getLighterColor(hexColor, factor = 0.7) {
  // 解析十六进制颜色
  let r = parseInt(hexColor.slice(1, 3), 16);
  let g = parseInt(hexColor.slice(3, 5), 16);
  let b = parseInt(hexColor.slice(5, 7), 16);
  
  // 调亮颜色
  r = Math.min(255, Math.round(r + (255 - r) * factor));
  g = Math.min(255, Math.round(g + (255 - g) * factor));
  b = Math.min(255, Math.round(b + (255 - b) * factor));
  
  // 转回十六进制
  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
}

// 根据背景颜色确定文本颜色（深色背景用白色文本，浅色背景用深色文本）
function getTextColorForBackground(hexColor) {
  // 解析十六进制颜色
  let r = parseInt(hexColor.slice(1, 3), 16);
  let g = parseInt(hexColor.slice(3, 5), 16);
  let b = parseInt(hexColor.slice(5, 7), 16);
  
  // 计算亮度（简化版）
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  
  // 亮度低于128返回白色，否则返回深灰色
  return brightness < 128 ? '#ffffff' : '#303133';
}

// 处理字体大小变化
function handleFontSizeChange(value) {
  // 设置根元素字体大小（影响rem单位）
  document.documentElement.style.fontSize = value + 'px';
  
  // 设置全局字体大小变量
  document.documentElement.style.setProperty('--global-font-size', value + 'px');
  document.documentElement.style.setProperty('--global-font-size-small', (value - 2) + 'px');
  document.documentElement.style.setProperty('--global-font-size-large', (value + 2) + 'px');
  
  // 应用字体大小到body元素
  document.body.style.fontSize = value + 'px';
  
  saveSettings();
  ElMessage.success('字体大小已全局更新');
}

// 处理字体样式变化
function handleFontFamilyChange(value) {
  document.body.style.fontFamily = value === 'default' ? '' : value;
  saveSettings();
}

// 处理刷新频率变化
function handleRefreshRateChange(value) {
  saveSettings();
  ElMessage.success('刷新频率已更新');
}

// 处理通知开关变化
function handleNotificationChange(value) {
  saveSettings();
  ElMessage.success(value ? '已开启消息通知' : '已关闭消息通知');
}

// 处理声音设置变化
function handleSoundChange(value) {
  saveSettings();
  ElMessage.success(value ? '已开启通知声音' : '已关闭通知声音');
}

// 处理导出格式变化
function handleExportFormatsChange(value) {
  saveSettings();
  ElMessage.success('导出格式已更新');
}

// 处理自动备份变化
function handleAutoBackupChange(value) {
  saveSettings();
  ElMessage.success(value ? '已开启自动备份' : '已关闭自动备份');
}

// 保存设置到localStorage
function saveSettings() {
  const settings = {
    isDarkMode: isDarkMode.value,
    themeColor: themeColor.value,
    fontSize: fontSize.value,
    fontFamily: fontFamily.value,
    refreshRate: refreshRate.value,
    enableNotification: enableNotification.value,
    enableSound: enableSound.value,
    soundType: soundType.value,
    exportFormats: exportFormats.value,
    defaultExportFormat: defaultExportFormat.value,
    enableAutoBackup: enableAutoBackup.value,
    backupFrequency: backupFrequency.value
  };
  localStorage.setItem('userSettings', JSON.stringify(settings));
}

// 应用设置
function applySettings() {
  document.body.className = isDarkMode.value ? 'dark-mode' : '';
  
  // 应用字体大小
  const fontSizeValue = fontSize.value + 'px';
  document.documentElement.style.fontSize = fontSizeValue;
  document.documentElement.style.setProperty('--global-font-size', fontSizeValue);
  document.documentElement.style.setProperty('--global-font-size-small', (fontSize.value - 2) + 'px');
  document.documentElement.style.setProperty('--global-font-size-large', (fontSize.value + 2) + 'px');
  document.body.style.fontSize = fontSizeValue;
  
  // 添加特定的Element Plus组件字体覆盖样式
  const existingElFontStyle = document.getElementById('el-font-size-override');
  if (existingElFontStyle) {
    existingElFontStyle.remove();
  }
  
  const elFontStyle = document.createElement('style');
  elFontStyle.id = 'el-font-size-override';
  elFontStyle.innerHTML = `
    .el-button { font-size: ${fontSizeValue} !important; }
    .el-input__inner { font-size: ${fontSizeValue} !important; }
    .el-menu-item { font-size: ${fontSizeValue} !important; }
    .el-dropdown-menu__item { font-size: ${fontSizeValue} !important; }
    .el-form-item__label { font-size: ${fontSizeValue} !important; }
    .el-form-item__content { font-size: ${fontSizeValue} !important; }
    .el-table { font-size: ${fontSizeValue} !important; }
    .el-table th, .el-table td { font-size: ${fontSizeValue} !important; }
    .el-dialog__title { font-size: ${parseInt(fontSizeValue) + 2}px !important; }
    .el-message-box__title { font-size: ${parseInt(fontSizeValue) + 2}px !important; }
    .el-message__content { font-size: ${fontSizeValue} !important; }
    .el-pagination { font-size: ${fontSizeValue} !important; }
    .el-date-table { font-size: ${fontSizeValue} !important; }
    .el-calendar-table { font-size: ${fontSizeValue} !important; }
  `;
  document.head.appendChild(elFontStyle);
  
  // 设置主题颜色
  const color = themeColor.value;
  document.documentElement.style.setProperty('--el-color-primary', color);
  
  // 计算不同亮度的颜色变体
  const menuBgColor = color; // 使用主题色本身作为菜单背景色
  const menuHoverColor = getLighterColor(color, 0.2); // 略微亮一点的悬停色
  const menuActiveColor = getLighterColor(color, 0.3); // 更亮一点的选中背景色
  const menuTextColor = '#ffffff'; // 统一使用白色文本
  const activeTextColor = '#ffffff'; // 选中状态也使用白色文本
  
  // 设置CSS变量
  document.documentElement.style.setProperty('--menu-bg-color', menuBgColor);
  document.documentElement.style.setProperty('--menu-hover-color', menuHoverColor);
  document.documentElement.style.setProperty('--menu-active-bg-color', menuActiveColor);
  document.documentElement.style.setProperty('--menu-text-color', menuTextColor);
  document.documentElement.style.setProperty('--menu-active-text-color', activeTextColor);
  
  // 设置字体
  document.body.style.fontFamily = fontFamily.value === 'default' ? '' : fontFamily.value;
  
  // 直接应用菜单样式，不使用延时
  updateMenuStyles(menuBgColor, menuHoverColor, menuActiveColor, menuTextColor, activeTextColor);
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.settings-card, .info-card {
  border-radius: 8px;
  transition: all 0.3s ease;
}

.settings-card:hover, .info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a237e;
}

.settings-form {
  padding: 20px;
}

.theme-switch {
  display: flex;
  align-items: center;
  gap: 20px;
}

.theme-preview {
  width: 100px;
  height: 60px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #dcdfe6;
  transition: all 0.3s ease;
}

.theme-preview.dark {
  background-color: #2c2c2c;
}

.theme-preview .preview-header {
  height: 20px;
  background-color: #f5f7fa;
}

.theme-preview.dark .preview-header {
  background-color: #1a1a1a;
}

.theme-preview .preview-content {
  height: 40px;
  background-color: #ffffff;
}

.theme-preview.dark .preview-content {
  background-color: #2c2c2c;
}

.font-size-control {
  display: flex;
  align-items: center;
  gap: 20px;
}

.custom-slider {
  width: 300px;
}

.font-preview {
  padding: 8px 16px;
  background-color: #f5f7fa;
  border-radius: 4px;
  color: #606266;
}

.refresh-rate-group {
  display: flex;
  gap: 10px;
}

.notification-setting {
  display: flex;
  align-items: center;
  gap: 15px;
}

.notification-desc {
  color: #606266;
  font-size: 14px;
}

.system-info {
  padding: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.info-item:hover {
  background-color: #eef1f6;
  transform: translateY(-2px);
}

.info-item .el-icon {
  font-size: 24px;
  color: #1a237e;
  padding: 12px;
  background-color: rgba(26, 35, 126, 0.1);
  border-radius: 8px;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 14px;
  color: #909399;
}

.info-value {
  font-size: 20px;
  font-weight: 600;
  color: #1a237e;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #1a237e;
}

:deep(.el-switch__label) {
  color: #606266;
}

:deep(.el-radio-button__inner) {
  border-radius: 4px;
}

/* 深色模式样式 */
:global(.dark-mode) {
  background-color: #1a1a1a;
  color: #ffffff;
}

:global(.dark-mode .el-card) {
  background-color: #2c2c2c;
  border-color: #3a3a3a;
}

:global(.dark-mode .el-form-item__label) {
  color: #ffffff;
}

:global(.dark-mode .el-input__inner) {
  background-color: #3a3a3a;
  border-color: #4a4a4a;
  color: #ffffff;
}

:global(.dark-mode .font-preview) {
  background-color: #3a3a3a;
  color: #ffffff;
}

:global(.dark-mode .info-item) {
  background-color: #2c2c2c;
}

:global(.dark-mode .info-item:hover) {
  background-color: #3a3a3a;
}

:global(.dark-mode .info-label) {
  color: #909399;
}

:global(.dark-mode .info-value) {
  color: #ffffff;
}

.color-picker {
  display: flex;
  gap: 10px;
}

.font-family-select {
  width: 200px;
}

.sound-setting {
  display: flex;
  align-items: center;
  gap: 15px;
}

.sound-select {
  width: 150px;
}

.export-setting {
  display: flex;
  align-items: center;
  gap: 20px;
}

.export-format-select {
  width: 120px;
}

.backup-setting {
  display: flex;
  align-items: center;
  gap: 15px;
}

.backup-frequency-select {
  width: 120px;
}

:deep(.el-checkbox-group) {
  display: flex;
  gap: 20px;
}

:deep(.el-select .el-input__wrapper) {
  background-color: var(--el-bg-color);
}

:deep(.el-radio-button__inner) {
  border-radius: 4px;
}

/* 深色模式样式补充 */
:global(.dark-mode .el-select .el-input__wrapper) {
  background-color: #3a3a3a;
}

:global(.dark-mode .el-checkbox__label) {
  color: #ffffff;
}

:global(.dark-mode .el-radio-button__inner) {
  background-color: #3a3a3a;
  border-color: #4a4a4a;
  color: #ffffff;
}
</style> 