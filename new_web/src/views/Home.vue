<template>
  <div class="home-container">
    <!-- 顶部欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-content">
        <h1 class="welcome-title">智能手环管理系统</h1>
        <p class="welcome-subtitle">让健康管理更智能，让生活更美好</p>
      </div>
    </div>

    <!-- 功能特点展示 -->
    <div class="features-section">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8">
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><Monitor /></el-icon>
            </div>
            <h3>实时监测</h3>
            <p>24小时不间断监测心率、血氧、睡眠等健康数据</p>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><DataLine /></el-icon>
            </div>
            <h3>数据分析</h3>
            <p>智能分析健康数据，提供专业的健康建议</p>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><Location /></el-icon>
            </div>
            <h3>位置追踪</h3>
            <p>实时定位，确保安全，支持电子围栏功能</p>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 数据统计展示 -->
    <div class="stats-section">
      <el-row :gutter="20">
        <el-col :xs="12" :sm="6">
          <div class="stat-card">
            <div class="stat-value">{{ stats.users }}</div>
            <div class="stat-label">注册用户</div>
          </div>
        </el-col>
        <el-col :xs="12" :sm="6">
          <div class="stat-card">
            <div class="stat-value">{{ stats.devices }}</div>
            <div class="stat-label">在线设备</div>
          </div>
        </el-col>
        <el-col :xs="12" :sm="6">
          <div class="stat-card">
            <div class="stat-value">{{ stats.dataPoints }}</div>
            <div class="stat-label">数据点数</div>
          </div>
        </el-col>
        <el-col :xs="12" :sm="6">
          <div class="stat-card">
            <div class="stat-value">{{ stats.alerts }}</div>
            <div class="stat-label">今日预警</div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 产品展示 -->
    <div class="product-section">
      <div class="product-content">
        <div class="product-info">
          <h2>新一代智能手环</h2>
          <p>采用最新生物传感器技术，支持多种运动模式，续航持久，防水防尘</p>
          <ul class="product-features">
            <li><el-icon><Check /></el-icon> 心率监测</li>
            <li><el-icon><Check /></el-icon> 血压分析</li>
            <li><el-icon><Check /></el-icon> 血氧检测</li>
            <li><el-icon><Check /></el-icon> 环境感知</li>
            <li><el-icon><Check /></el-icon> 智能提醒</li>
            <li><el-icon><Check /></el-icon> 运动追踪</li>
          </ul>
        </div>
        <div class="product-image">
          <img src="https://img.alicdn.com/imgextra/i4/2200724907121/O1CN01Z5paLt22AdGf4cJzq_!!2200724907121.jpg" alt="智能手环" />
        </div>
      </div>
    </div>
  </div>

  <!-- 底部信息 -->
  <div class="footer-section">
    <div class="footer-content">
      <div class="footer-item">
        <h3>智能手环管理运营团队</h3>
        <p>张航铭，唐涛，蓝金桥，肖欣芮</p>
      </div>
      <div class="footer-item">
        <h3>联系电话</h3>
        <p>18996187039</p>
      </div>
      <div class="footer-item">
        <h3>地址</h3>
        <p>重庆大学</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Monitor, DataLine, Location, Check } from '@element-plus/icons-vue';

const stats = ref({
  users: '12,345',
  devices: '8,765',
  dataPoints: '1,234,567',
  alerts: '23'
});

// 数字增长动画
onMounted(() => {
  const animateValue = (element, start, end, duration) => {
    let startTimestamp = null;
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      const value = Math.floor(progress * (end - start) + start);
      element.textContent = value.toLocaleString();
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };
    window.requestAnimationFrame(step);
  };

  // 为每个统计数字添加动画
  const statValues = document.querySelectorAll('.stat-value');
  statValues.forEach(stat => {
    const endValue = parseInt(stat.textContent.replace(/,/g, ''));
    animateValue(stat, 0, endValue, 2000);
  });
});
</script>

<style scoped>
.home-container {
  padding: 20px;
  min-height: calc(100vh - 60px);
}

.welcome-section {
  background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
  border-radius: 16px;
  padding: 40px;
  margin-bottom: 30px;
  color: white;
  text-align: center;
  box-shadow: 0 4px 20px rgba(26, 35, 126, 0.2);
  animation: gradientShift 10s ease infinite;
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.welcome-title {
  font-size: 2.5em;
  margin-bottom: 10px;
  animation: fadeInDown 1s ease;
}

.welcome-subtitle {
  font-size: 1.2em;
  opacity: 0.9;
  animation: fadeInUp 1s ease;
}

.features-section {
  margin-bottom: 30px;
}

.feature-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 40px;
  color: #1a237e;
  margin-bottom: 20px;
}

.feature-card h3 {
  color: #1a237e;
  margin-bottom: 15px;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

.stats-section {
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.stat-value {
  font-size: 2em;
  font-weight: bold;
  color: #1a237e;
  margin-bottom: 10px;
}

.stat-label {
  color: #666;
  font-size: 1.1em;
}

.product-section {
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.product-content {
  display: flex;
  align-items: center;
  gap: 40px;
  flex-wrap: wrap;
}

.product-info {
  flex: 1;
  min-width: 300px;
}

.product-info h2 {
  color: #1a237e;
  font-size: 2em;
  margin-bottom: 20px;
}

.product-info p {
  color: #666;
  line-height: 1.8;
  margin-bottom: 30px;
}

.product-features {
  list-style: none;
  padding: 0;
}

.product-features li {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  color: #333;
}

.product-features .el-icon {
  color: #1a237e;
}

.product-image {
  flex: 1;
  text-align: center;
  min-width: 300px;
}

.product-image img {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.product-image img:hover {
  transform: scale(1.05);
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 深色模式样式 */
:global(.dark-mode) .feature-card,
:global(.dark-mode) .stat-card,
:global(.dark-mode) .product-section {
  background-color: #2c2c2c;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

:global(.dark-mode) .feature-card h3,
:global(.dark-mode) .stat-value {
  color: #ffffff;
}

:global(.dark-mode) .feature-card p,
:global(.dark-mode) .stat-label,
:global(.dark-mode) .product-info p,
:global(.dark-mode) .product-features li {
  color: #909399;
}

:global(.dark-mode) .product-info h2 {
  color: #ffffff;
}

/* 底部样式 */
.footer-section {
  margin-top: 40px;
  padding: 30px 0;
  background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
  border-radius: 16px;
  color: white;
  box-shadow: 0 4px 20px rgba(26, 35, 126, 0.2);
}

.footer-content {
  display: flex;
  justify-content: space-around;
  align-items: flex-start;
  padding: 0 40px;
  flex-wrap: wrap;
}

.footer-item {
  text-align: center;
  flex: 1;
  padding: 0 20px;
  position: relative;
  min-width: 250px;
  margin-bottom: 20px;
}

.footer-item:not(:last-child)::after {
  content: '';
  position: absolute;
  right: 0;
  top: 20%;
  height: 60%;
  width: 1px;
  background: rgba(255, 255, 255, 0.2);
}

.footer-item h3 {
  font-size: 1.2em;
  margin-bottom: 15px;
  color: #ffd04b;
  font-weight: 500;
}

.footer-item p {
  font-size: 1em;
  line-height: 1.6;
  opacity: 0.9;
}

/* 深色模式样式补充 */
:global(.dark-mode) .footer-section {
  background: linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 100%);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

:global(.dark-mode) .footer-item h3 {
  color: #ffd04b;
}

:global(.dark-mode) .footer-item p {
  color: #ffffff;
}

/* 响应式调整 */
@media screen and (max-width: 768px) {
  .welcome-section {
    padding: 20px;
  }
  
  .welcome-title {
    font-size: 1.8em;
  }
  
  .welcome-subtitle {
    font-size: 1em;
  }
  
  .product-content {
    flex-direction: column;
    gap: 20px;
  }
  
  .product-section {
    padding: 20px;
  }
  
  .product-info, .product-image {
    flex: 100%;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 20px;
    padding: 0 20px;
  }

  .footer-item:not(:last-child)::after {
    display: none;
  }

  .footer-item {
    padding: 20px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    min-width: 100%;
  }

  .footer-item:last-child {
    border-bottom: none;
  }
}

/* 增加平板端响应式调整 */
@media screen and (min-width: 769px) and (max-width: 992px) {
  .product-content {
    gap: 20px;
  }
}
</style> 