<template>
  <div class="monitor-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="monitor-card">
          <template #header>
            <div class="card-header">
              <span>实时数据监控</span>
              <div class="header-controls">
                <el-select v-model="selectedUser" placeholder="选择用户" style="width: 200px; margin-right: 10px;">
                  <el-option
                    v-for="user in users"
                    :key="user.username"
                    :label="user.username"
                    :value="user.username"
                  />
                </el-select>
                <el-button type="primary" @click="exportToExcel">导出数据</el-button>
              </div>
            </div>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="chart" ref="heartRateChart"></div>
            </el-col>
            <el-col :span="12">
              <div class="chart" ref="bloodPressureChart"></div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20" style="margin-top: 20px;">
            <el-col :span="12">
              <div class="chart" ref="stepsChart"></div>
            </el-col>
            <el-col :span="12">
              <div class="chart" ref="accelerationChart"></div>
            </el-col>
          </el-row>

          <!-- 添加环境数据监控 -->
          <el-row style="margin-top: 20px;">
            <el-col :span="24">
              <el-card class="environment-card">
                <template #header>
                  <div class="card-header">
                    <span>环境数据监控（最近7天）</span>
                    <el-button type="primary" @click="sendEnvironmentAdvice" :disabled="!hasEnvironmentAdvice">
                      发送环境建议
                    </el-button>
                  </div>
                </template>
                <div class="chart" ref="environmentChart"></div>
                <div class="advice-container" v-if="environmentAdvice">
                  <el-alert
                    :title="environmentAdvice"
                    type="info"
                    :closable="false"
                    show-icon
                  />
                </div>
              </el-card>
            </el-col>
          </el-row>

          <!-- 添加健康分析部分 -->
          <el-row style="margin-top: 20px;">
            <el-col :span="24">
              <el-card class="analysis-card">
                <template #header>
                  <div class="card-header">
                    <span>健康数据分析</span>
                    <el-tag :type="healthStatus.type">{{ healthStatus.text }}</el-tag>
                  </div>
                </template>
                
                <el-row :gutter="20">
                  <el-col :span="12">
                    <div class="analysis-section">
                      <h4>血压分析</h4>
                      <div class="analysis-content">
                        <p>{{ bloodPressureAnalysis.text }}</p>
                        <el-alert
                          v-if="bloodPressureAnalysis.warning"
                          :title="bloodPressureAnalysis.warning"
                          type="warning"
                          :closable="false"
                          show-icon
                        />
                        <div class="suggestions">
                          <h5>建议：</h5>
                          <ul>
                            <li v-for="(suggestion, index) in bloodPressureAnalysis.suggestions" :key="index">
                              {{ suggestion }}
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </el-col>
                  
                  <el-col :span="12">
                    <div class="analysis-section">
                      <h4>心率分析</h4>
                      <div class="analysis-content">
                        <p>{{ heartRateAnalysis.text }}</p>
                        <el-alert
                          v-if="heartRateAnalysis.warning"
                          :title="heartRateAnalysis.warning"
                          type="warning"
                          :closable="false"
                          show-icon
                        />
                        <div class="suggestions">
                          <h5>建议：</h5>
                          <ul>
                            <li v-for="(suggestion, index) in heartRateAnalysis.suggestions" :key="index">
                              {{ suggestion }}
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </el-col>
                </el-row>
              </el-card>
            </el-col>
          </el-row>

          <!-- 数据日志表格 -->
          <el-row style="margin-top: 20px;">
            <el-col :span="24">
              <el-card>
                <template #header>
                  <div class="card-header">
                    <span>数据日志</span>
                    <el-button type="text" @click="clearLogs">清空日志</el-button>
                  </div>
                </template>
                <el-table :data="logData" height="300" style="width: 100%">
                  <el-table-column prop="time" label="时间" width="180" />
                  <el-table-column prop="heartRate" label="心率(bpm)" width="120" />
                  <el-table-column prop="systolic" label="收缩压(mmHg)" width="120" />
                  <el-table-column prop="diastolic" label="舒张压(mmHg)" width="120" />
                  <el-table-column prop="steps" label="步数" width="120" />
                  <el-table-column prop="acceleration" label="加速度(m/s²)" />
                </el-table>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import * as echarts from 'echarts';
import { ElMessage } from 'element-plus';
import { getAllUsers, getUserHealthData } from '../utils/userData';

// 用户数据
const users = ref(getAllUsers());
const selectedUser = ref(users.value[0]?.username);
const logData = ref([]);

// 图表引用
const heartRateChart = ref(null);
const bloodPressureChart = ref(null);
const stepsChart = ref(null);
const accelerationChart = ref(null);
const environmentChart = ref(null);

// 图表实例
let hrChart = null;
let bpChart = null;
let stepsChartInstance = null;
let accChart = null;
let envChart = null;

// 数据存储
const heartRateData = ref([]);
const bloodPressureData = ref([]);
const stepsData = ref([]);
const accelerationData = ref([]);

// 添加健康状态计算
const healthStatus = ref({
  type: 'success',
  text: '健康状况良好'
});

// 血压分析
const bloodPressureAnalysis = ref({
  text: '',
  warning: '',
  suggestions: []
});

// 心率分析
const heartRateAnalysis = ref({
  text: '',
  warning: '',
  suggestions: []
});

// 环境数据相关
const environmentAdvice = ref('');
const hasEnvironmentAdvice = ref(false);

// 生成随机变化的数据
function generateRandomChange(base, range) {
  return base + (Math.random() * 2 - 1) * range;
}

// 分析血压数据
function analyzeBloodPressure(systolic, diastolic) {
  let analysis = {
    text: '',
    warning: '',
    suggestions: []
  };

  // 分析收缩压
  if (systolic > 140) {
    analysis.warning = '收缩压偏高，请注意！';
    analysis.suggestions = [
      '建议立即休息，避免剧烈运动',
      '保持情绪稳定，避免激动',
      '必要时咨询医生',
      '注意饮食，减少盐分摄入'
    ];
  } else if (systolic < 90) {
    analysis.warning = '收缩压偏低，请注意！';
    analysis.suggestions = [
      '适当补充水分',
      '避免突然站起',
      '保持充足休息',
      '必要时咨询医生'
    ];
  }

  // 分析舒张压
  if (diastolic > 90) {
    analysis.warning = '舒张压偏高，请注意！';
    analysis.suggestions = [
      '建议立即休息',
      '避免情绪激动',
      '保持规律作息',
      '必要时咨询医生'
    ];
  } else if (diastolic < 60) {
    analysis.warning = '舒张压偏低，请注意！';
    analysis.suggestions = [
      '适当补充营养',
      '避免剧烈运动',
      '保持充足休息',
      '必要时咨询医生'
    ];
  }

  // 正常情况
  if (!analysis.warning) {
    analysis.text = '血压在正常范围内';
    analysis.suggestions = [
      '继续保持良好的生活习惯',
      '定期监测血压',
      '保持适量运动',
      '注意饮食均衡'
    ];
  }

  return analysis;
}

// 分析心率数据
function analyzeHeartRate(heartRate, previousHeartRate) {
  let analysis = {
    text: '',
    warning: '',
    suggestions: []
  };

  // 计算心率变化
  const heartRateChange = previousHeartRate ? Math.abs(heartRate - previousHeartRate) : 0;

  // 分析心率值
  if (heartRate > 100) {
    analysis.warning = '心率过快，请注意！';
    analysis.suggestions = [
      '建议立即休息',
      '避免剧烈运动',
      '保持情绪稳定',
      '必要时咨询医生'
    ];
  } else if (heartRate < 60) {
    analysis.warning = '心率过慢，请注意！';
    analysis.suggestions = [
      '适当活动身体',
      '避免久坐',
      '保持规律作息',
      '必要时咨询医生'
    ];
  }

  // 分析心率变化
  if (heartRateChange > 20) {
    analysis.warning = '心率变化较大，请注意！';
    analysis.suggestions = [
      '避免剧烈运动',
      '保持情绪稳定',
      '注意休息',
      '必要时咨询医生'
    ];
  }

  // 正常情况
  if (!analysis.warning) {
    analysis.text = '心率在正常范围内';
    analysis.suggestions = [
      '继续保持良好的生活习惯',
      '保持适量运动',
      '注意休息',
      '保持情绪稳定'
    ];
  }

  return analysis;
}

// 更新健康状态
function updateHealthStatus() {
  const hasWarning = bloodPressureAnalysis.value.warning || heartRateAnalysis.value.warning;
  healthStatus.value = {
    type: hasWarning ? 'warning' : 'success',
    text: hasWarning ? '需要注意' : '健康状况良好'
  };
}

// 更新图表数据
function updateCharts() {
  const healthData = getUserHealthData(selectedUser.value);
  if (!healthData) return;

  const now = new Date();
  const time = now.toLocaleTimeString('zh-CN', { hour12: false });

  // 生成新的数据
  const newHeartRate = Math.round(generateRandomChange(healthData.heartRate, 5));
  const newSystolic = Math.round(generateRandomChange(healthData.bloodPressure.systolic, 3));
  const newDiastolic = Math.round(generateRandomChange(healthData.bloodPressure.diastolic, 2));
  const newSteps = Math.round(generateRandomChange(healthData.steps, 100));
  const accX = generateRandomChange(0, 1);
  const accY = generateRandomChange(0, 1);
  const accZ = generateRandomChange(0, 1);

  // 更新心率数据
  heartRateData.value.push({
    time,
    value: newHeartRate
  });
  if (heartRateData.value.length > 20) {
    heartRateData.value.shift();
  }

  // 更新血压数据
  bloodPressureData.value.push({
    time,
    systolic: newSystolic,
    diastolic: newDiastolic
  });
  if (bloodPressureData.value.length > 20) {
    bloodPressureData.value.shift();
  }

  // 更新步数数据
  stepsData.value.push({
    time,
    value: newSteps
  });
  if (stepsData.value.length > 20) {
    stepsData.value.shift();
  }

  // 更新加速度数据
  accelerationData.value.push({
    time,
    x: accX,
    y: accY,
    z: accZ
  });
  if (accelerationData.value.length > 20) {
    accelerationData.value.shift();
  }

  // 添加到日志
  logData.value.push({
    time,
    heartRate: newHeartRate.toFixed(1),
    systolic: newSystolic.toFixed(1),
    diastolic: newDiastolic.toFixed(1),
    steps: newSteps.toFixed(0),
    acceleration: `X:${accX.toFixed(2)} Y:${accY.toFixed(2)} Z:${accZ.toFixed(2)}`
  });
  if (logData.value.length > 100) {
    logData.value.shift();
  }

  // 更新分析结果
  const previousHeartRate = heartRateData.value.length > 1 ? 
    heartRateData.value[heartRateData.value.length - 2].value : null;
  
  bloodPressureAnalysis.value = analyzeBloodPressure(newSystolic, newDiastolic);
  heartRateAnalysis.value = analyzeHeartRate(newHeartRate, previousHeartRate);
  updateHealthStatus();

  // 更新图表
  updateHeartRateChart();
  updateBloodPressureChart();
  updateStepsChart();
  updateAccelerationChart();
}

// 修改 updateHeartRateChart 函数
function updateHeartRateChart() {
  if (!hrChart) return;
  hrChart.setOption({
    xAxis: {
      data: heartRateData.value.map(item => item.time)
    },
    series: [{
      data: heartRateData.value.map(item => item.value)
    }]
  });
}

// 修改 updateBloodPressureChart 函数
function updateBloodPressureChart() {
  if (!bpChart) return;
  bpChart.setOption({
    xAxis: {
      data: bloodPressureData.value.map(item => item.time)
    },
    series: [
      {
        data: bloodPressureData.value.map(item => item.systolic)
      },
      {
        data: bloodPressureData.value.map(item => item.diastolic)
      }
    ]
  });
}

// 修改 updateStepsChart 函数
function updateStepsChart() {
  if (!stepsChartInstance) return;
  stepsChartInstance.setOption({
    xAxis: {
      data: stepsData.value.map(item => item.time)
    },
    series: [{
      data: stepsData.value.map(item => item.value)
    }]
  });
}

// 修改 updateAccelerationChart 函数
function updateAccelerationChart() {
  if (!accChart) return;
  accChart.setOption({
    xAxis: {
      data: accelerationData.value.map(item => item.time)
    },
    series: [
      {
        data: accelerationData.value.map(item => item.x)
      },
      {
        data: accelerationData.value.map(item => item.y)
      },
      {
        data: accelerationData.value.map(item => item.z)
      }
    ]
  });
}

// 添加环境数据图表初始化和更新函数
function initEnvironmentChart() {
  envChart = echarts.init(environmentChart.value);
  const dates = getLast7Days();
  
  // 生成模拟数据
  const temperatureData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 15) + 20); // 20-35度
  const humidityData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 30) + 40); // 40-70%
  const pressureData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 20) + 1000); // 1000-1020hPa
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['温度', '湿度', '大气压']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates
    },
    yAxis: [
      {
        type: 'value',
        name: '温度(°C)',
        position: 'left'
      },
      {
        type: 'value',
        name: '湿度(%)',
        position: 'right'
      },
      {
        type: 'value',
        name: '大气压(hPa)',
        position: 'right',
        offset: 80
      }
    ],
    series: [
      {
        name: '温度',
        type: 'line',
        data: temperatureData,
        smooth: true,
        itemStyle: {
          color: '#ff6b6b'
        }
      },
      {
        name: '湿度',
        type: 'line',
        yAxisIndex: 1,
        data: humidityData,
        smooth: true,
        itemStyle: {
          color: '#4ecdc4'
        }
      },
      {
        name: '大气压',
        type: 'line',
        yAxisIndex: 2,
        data: pressureData,
        smooth: true,
        itemStyle: {
          color: '#45b7d1'
        }
      }
    ]
  };
  
  envChart.setOption(option);
  
  // 分析环境数据并生成建议
  analyzeEnvironmentData(temperatureData, humidityData, pressureData);
}

function updateEnvironmentChart() {
  if (!envChart) return;
  
  const dates = getLast7Days();
  const temperatureData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 15) + 20);
  const humidityData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 30) + 40);
  const pressureData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 20) + 1000);
  
  envChart.setOption({
    xAxis: {
      data: dates
    },
    series: [
      {
        data: temperatureData
      },
      {
        data: humidityData
      },
      {
        data: pressureData
      }
    ]
  });
  
  // 更新环境建议
  analyzeEnvironmentData(temperatureData, humidityData, pressureData);
}

// 导出数据到Excel
function exportToExcel() {
  if (logData.value.length === 0) {
    ElMessage.warning('没有可导出的数据');
    return;
  }

  // 创建工作表数据
  const worksheet = [
    ['时间', '心率(bpm)', '收缩压(mmHg)', '舒张压(mmHg)', '步数', '加速度X', '加速度Y', '加速度Z']
  ];

  // 添加数据行
  logData.value.forEach(log => {
    const [accX, accY, accZ] = log.acceleration.split(' ').map(acc => acc.split(':')[1]);
    worksheet.push([
      log.time,
      log.heartRate,
      log.systolic,
      log.diastolic,
      log.steps,
      accX,
      accY,
      accZ
    ]);
  });

  // 转换为CSV格式
  const csvContent = worksheet.map(row => row.join(',')).join('\n');
  
  // 创建Blob对象
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
  
  // 创建下载链接
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  link.setAttribute('href', url);
  link.setAttribute('download', `${selectedUser.value}_数据日志_${new Date().toLocaleDateString()}.csv`);
  link.style.visibility = 'hidden';
  
  // 触发下载
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// 清空日志
function clearLogs() {
  logData.value = [];
  ElMessage.success('日志已清空');
}

// 监听用户选择变化
watch(selectedUser, () => {
  // 清空现有数据和日志
  heartRateData.value = [];
  bloodPressureData.value = [];
  stepsData.value = [];
  accelerationData.value = [];
  logData.value = [];
  
  // 重新初始化图表
  initHeartRateChart();
  initBloodPressureChart();
  initStepsChart();
  initAccelerationChart();
  initEnvironmentChart();
});

let timer = null;

onMounted(() => {
  // 初始化图表
  initHeartRateChart();
  initBloodPressureChart();
  initStepsChart();
  initAccelerationChart();
  initEnvironmentChart();

  // 启动定时更新
  timer = setInterval(updateCharts, 1000);

  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    hrChart?.resize();
    bpChart?.resize();
    stepsChartInstance?.resize();
    accChart?.resize();
    envChart?.resize();
  });
});

onUnmounted(() => {
  // 清理定时器
  if (timer) {
    clearInterval(timer);
  }
  // 销毁图表实例
  hrChart?.dispose();
  bpChart?.dispose();
  stepsChartInstance?.dispose();
  accChart?.dispose();
  envChart?.dispose();
});

// 初始化心率图表
function initHeartRateChart() {
  hrChart = echarts.init(heartRateChart.value);
  hrChart.setOption({
    title: { text: '心率实时监测' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: heartRateData.value.map(item => item.time)
    },
    yAxis: {
      type: 'value',
      name: '心率(bpm)'
    },
    series: [{
      name: '心率',
      type: 'line',
      data: heartRateData.value.map(item => item.value),
      smooth: true,
      showSymbol: false,
      lineStyle: { width: 2 }
    }]
  });
}

// 初始化血压图表
function initBloodPressureChart() {
  bpChart = echarts.init(bloodPressureChart.value);
  bpChart.setOption({
    title: { text: '血压实时监测' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: bloodPressureData.value.map(item => item.time)
    },
    yAxis: {
      type: 'value',
      name: '血压(mmHg)'
    },
    series: [
      {
        name: '收缩压',
        type: 'line',
        data: bloodPressureData.value.map(item => item.systolic),
        smooth: true,
        showSymbol: false
      },
      {
        name: '舒张压',
        type: 'line',
        data: bloodPressureData.value.map(item => item.diastolic),
        smooth: true,
        showSymbol: false
      }
    ]
  });
}

// 初始化步数图表
function initStepsChart() {
  stepsChartInstance = echarts.init(stepsChart.value);
  stepsChartInstance.setOption({
    title: { text: '步数实时监测' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: stepsData.value.map(item => item.time)
    },
    yAxis: {
      type: 'value',
      name: '步数'
    },
    series: [{
      name: '步数',
      type: 'bar',
      data: stepsData.value.map(item => item.value)
    }]
  });
}

// 初始化加速度图表
function initAccelerationChart() {
  accChart = echarts.init(accelerationChart.value);
  accChart.setOption({
    title: { text: '加速度实时监测' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: accelerationData.value.map(item => item.time)
    },
    yAxis: {
      type: 'value',
      name: '加速度(m/s²)'
    },
    series: [
      {
        name: 'X轴',
        type: 'line',
        data: accelerationData.value.map(item => item.x)
      },
      {
        name: 'Y轴',
        type: 'line',
        data: accelerationData.value.map(item => item.y)
      },
      {
        name: 'Z轴',
        type: 'line',
        data: accelerationData.value.map(item => item.z)
      }
    ]
  });
}

// 生成最近7天的日期
function getLast7Days() {
  const dates = [];
  for (let i = 6; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    dates.push(date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }));
  }
  return dates;
}

// 分析环境数据并生成建议
function analyzeEnvironmentData(temperature, humidity, pressure) {
  const avgTemp = temperature.reduce((a, b) => a + b, 0) / temperature.length;
  const avgHumidity = humidity.reduce((a, b) => a + b, 0) / humidity.length;
  const avgPressure = pressure.reduce((a, b) => a + b, 0) / pressure.length;
  
  let advice = [];
  
  // 温度分析
  if (avgTemp > 30) {
    advice.push('温度偏高，建议适当开启空调，保持室内通风');
  } else if (avgTemp < 22) {
    advice.push('温度偏低，建议适当增加衣物，注意保暖');
  }
  
  // 湿度分析
  if (avgHumidity > 65) {
    advice.push('湿度较大，建议使用除湿器，注意防潮');
  } else if (avgHumidity < 45) {
    advice.push('湿度较低，建议使用加湿器，多补充水分');
  }
  
  // 大气压分析
  if (avgPressure > 1015) {
    advice.push('气压较高，天气晴朗，适合户外活动');
  } else if (avgPressure < 1005) {
    advice.push('气压较低，可能天气变化，建议关注天气预报');
  }
  
  if (advice.length > 0) {
    environmentAdvice.value = advice.join('；');
    hasEnvironmentAdvice.value = true;
  } else {
    environmentAdvice.value = '当前环境数据正常，无需特别建议';
    hasEnvironmentAdvice.value = false;
  }
}

// 发送环境建议
function sendEnvironmentAdvice() {
  if (!hasEnvironmentAdvice.value) return;
  
  ElMessage({
    message: '环境建议已发送给用户',
    type: 'success'
  });
}
</script>

<style scoped>
.monitor-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.monitor-card {
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.monitor-card:hover {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
  background: linear-gradient(to right, #f8f9fa, #ffffff);
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chart {
  height: 300px;
  width: 100%;
  margin-bottom: 20px;
  background: #fff;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.chart:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.analysis-card {
  margin-top: 20px;
  border-radius: 8px;
  overflow: hidden;
}

.analysis-section {
  padding: 20px;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 8px;
  height: 100%;
  transition: all 0.3s ease;
}

.analysis-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.analysis-section h4 {
  margin-top: 0;
  color: #303133;
  border-bottom: 2px solid #409eff;
  padding-bottom: 10px;
  font-size: 16px;
  font-weight: 600;
}

.analysis-content {
  margin-top: 15px;
}

.suggestions {
  margin-top: 20px;
  background: rgba(64, 158, 255, 0.05);
  padding: 15px;
  border-radius: 6px;
  border-left: 4px solid #409eff;
}

.suggestions h5 {
  color: #409eff;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 600;
}

.suggestions ul {
  padding-left: 20px;
  margin: 0;
}

.suggestions li {
  color: #606266;
  margin-bottom: 8px;
  line-height: 1.6;
  position: relative;
  transition: all 0.3s ease;
}

.suggestions li:hover {
  color: #409eff;
  transform: translateX(5px);
}

/* 自定义Element Plus组件样式 */
:deep(.el-card__header) {
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
  background: linear-gradient(to right, #f8f9fa, #ffffff);
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  background-color: #f5f7fa !important;
  color: #606266;
  font-weight: 600;
}

:deep(.el-table--enable-row-hover .el-table__body tr:hover > td) {
  background-color: #ecf5ff;
}

:deep(.el-button--primary) {
  background: linear-gradient(45deg, #409eff, #36cfc9);
  border: none;
  transition: all 0.3s ease;
}

:deep(.el-button--primary:hover) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

:deep(.el-select .el-input__wrapper) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

:deep(.el-alert) {
  border-radius: 6px;
  margin: 10px 0;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

:deep(.el-tag) {
  border-radius: 4px;
  padding: 0 12px;
  height: 28px;
  line-height: 26px;
  font-weight: 500;
}

/* 添加动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.analysis-section {
  animation: fadeIn 0.5s ease-out;
}

.chart {
  animation: fadeIn 0.5s ease-out;
}

/* 响应式布局优化 */
@media screen and (max-width: 768px) {
  .monitor-container {
    padding: 10px;
  }
  
  .chart {
    height: 250px;
  }
  
  .analysis-section {
    margin-bottom: 15px;
  }
}

.environment-card {
  margin-top: 20px;
  border-radius: 8px;
  overflow: hidden;
}

.advice-container {
  margin-top: 20px;
  padding: 0 20px 20px;
}

:deep(.el-alert) {
  margin-top: 10px;
}
</style> 