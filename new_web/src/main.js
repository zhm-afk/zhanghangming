import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

// 添加全局样式和变量
import './styles.css';

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
}

// 应用初始化前设置CSS变量
const initGlobalStyles = () => {
  // 从localStorage获取用户设置
  const settings = JSON.parse(localStorage.getItem('userSettings') || '{}');
  const themeColor = settings.themeColor || '#1a237e';
  const fontSize = settings.fontSize || 14;
  
  // 设置CSS变量
  document.documentElement.style.setProperty('--el-color-primary', themeColor);
  document.documentElement.style.setProperty('--menu-transition-duration', '0.3s');
  
  // 计算不同亮度的颜色变体
  const menuBgColor = themeColor; // 使用主题色本身作为菜单背景色
  const menuHoverColor = getLighterColor(themeColor, 0.2); // 略微亮一点的悬停色
  const menuActiveColor = getLighterColor(themeColor, 0.3); // 更亮一点的选中背景色
  const menuTextColor = '#ffffff'; // 统一使用白色文本
  const activeTextColor = '#ffffff'; // 选中状态也使用白色文本
  
  // 设置菜单相关的CSS变量
  document.documentElement.style.setProperty('--menu-bg-color', menuBgColor);
  document.documentElement.style.setProperty('--menu-hover-color', menuHoverColor);
  document.documentElement.style.setProperty('--menu-active-bg-color', menuActiveColor);
  document.documentElement.style.setProperty('--menu-text-color', menuTextColor);
  document.documentElement.style.setProperty('--menu-active-text-color', activeTextColor);
  
  // 立即应用菜单样式
  updateMenuStyles(menuBgColor, menuHoverColor, menuActiveColor, menuTextColor, activeTextColor);
  
  // 设置字体大小
  const fontSizeValue = fontSize + 'px';
  document.documentElement.style.fontSize = fontSizeValue;
  document.documentElement.style.setProperty('--global-font-size', fontSizeValue);
  document.documentElement.style.setProperty('--global-font-size-small', (fontSize - 2) + 'px');
  document.documentElement.style.setProperty('--global-font-size-large', (fontSize + 2) + 'px');
  document.body.style.fontSize = fontSizeValue;
  
  // 添加Element Plus组件字体覆盖样式
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
  
  // 设置主题模式
  if (settings.isDarkMode) {
    document.body.classList.add('dark-mode');
  }
};

// 初始化全局样式
initGlobalStyles();
 
const app = createApp(App);
app.use(router);
app.use(ElementPlus);
app.mount('#app'); 