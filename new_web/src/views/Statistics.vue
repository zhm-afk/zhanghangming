<template>
  <div class="statistics-container">
    <el-row :gutter="20">
      <!-- 用户选择 -->
      <el-col :span="24">
        <el-card class="user-select-card">
          <el-select v-model="selectedUser" placeholder="请选择用户" @change="handleUserChange">
            <el-option
              v-for="user in users"
              :key="user.id"
              :label="user.username"
              :value="user.id"
            />
          </el-select>
        </el-card>
      </el-col>

      <!-- 环境数据统计 -->
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>环境数据统计（最近7天）</span>
              <el-button type="primary" @click="sendEnvironmentAdvice" :disabled="!hasEnvironmentAdvice">
                发送环境建议
              </el-button>
            </div>
          </template>
          <div class="chart-container">
            <div ref="environmentChartRef" class="chart"></div>
          </div>
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

      <!-- 原有的统计卡片 -->
      <el-col :span="8">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>平均心率</span>
            </div>
          </template>
          <div class="stat-value">{{ averageHeartRate }} bpm</div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>平均血压</span>
            </div>
          </template>
          <div class="stat-value">{{ averageBloodPressure.systolic }}/{{ averageBloodPressure.diastolic }} mmHg</div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>平均步数</span>
            </div>
          </template>
          <div class="stat-value">{{ averageSteps }} 步</div>
        </el-card>
      </el-col>

      <!-- 原有的图表 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>血压趋势</span>
            </div>
          </template>
          <div class="chart-container">
            <div ref="bloodPressureChartRef" class="chart"></div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>步数统计</span>
            </div>
          </template>
          <div class="chart-container">
            <div ref="stepsChartRef" class="chart"></div>
          </div>
        </el-card>
      </el-col>

      <!-- 心率分析部分 -->
      <el-col :span="24">
        <el-card class="analysis-card">
          <template #header>
            <div class="card-header">
              <span>心率分析</span>
            </div>
          </template>
          <div class="analysis-details">
            <el-descriptions :column="3" border>
              <el-descriptions-item label="平均心率">
                {{ heartRateAnalysis.avg }} 次/分
                <el-tag :type="getHeartRateStatus(heartRateAnalysis.avg).type" size="small">
                  {{ getHeartRateStatus(heartRateAnalysis.avg).text }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="最高心率">
                {{ heartRateAnalysis.max }} 次/分
              </el-descriptions-item>
              <el-descriptions-item label="最低心率">
                {{ heartRateAnalysis.min }} 次/分
              </el-descriptions-item>
            </el-descriptions>
            
            <!-- 添加所有用户心率分析 -->
            <el-descriptions :column="3" border class="mt-3">
              <el-descriptions-item label="所有用户平均心率">
                {{ heartRateAnalysis.allUsersAvg }} 次/分
                <el-tag :type="getHeartRateStatus(heartRateAnalysis.allUsersAvg).type" size="small">
                  {{ getHeartRateStatus(heartRateAnalysis.allUsersAvg).text }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="正常心率用户数">
                {{ heartRateAnalysis.distribution.normal }} 人
              </el-descriptions-item>
              <el-descriptions-item label="异常心率用户数">
                {{ heartRateAnalysis.distribution.high + heartRateAnalysis.distribution.low }} 人
              </el-descriptions-item>
            </el-descriptions>
            
            <div class="analysis-suggestion">
              <el-alert
                :title="heartRateAnalysis.suggestion"
                :type="heartRateAnalysis.suggestionType"
                :closable="false"
                show-icon
              />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';
import { ElMessage } from 'element-plus';
import { 
  getAllUsers, 
  calculateAverageHeartRate, 
  calculateAverageBloodPressure, 
  calculateAverageSteps,
  getHeartRateDistribution
} from '../utils/userData';

// 用户数据
const users = ref(getAllUsers());
const selectedUser = ref(users.value[0]?.id);

// 环境数据相关
const environmentChartRef = ref(null);
const environmentChart = ref(null);
const environmentAdvice = ref('');
const hasEnvironmentAdvice = ref(false);

// 心率分析相关
const heartRateAnalysis = ref({
  avg: 0,
  max: 0,
  min: 0,
  suggestion: '',
  suggestionType: 'success',
  allUsersAvg: 0,
  userCount: 0,
  normalRange: { min: 60, max: 100 },
  distribution: {
    normal: 0,
    high: 0,
    low: 0
  }
});

// 生成最近7天的日期
const getLast7Days = () => {
  const dates = [];
  for (let i = 6; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    dates.push(date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }));
  }
  return dates;
};

// 初始化环境数据图表
const initEnvironmentChart = () => {
  if (!environmentChartRef.value) return;
  
  environmentChart.value = echarts.init(environmentChartRef.value);
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
  
  environmentChart.value.setOption(option);
  
  // 分析环境数据并生成建议
  analyzeEnvironmentData(temperatureData, humidityData, pressureData);
};

// 分析环境数据并生成建议
const analyzeEnvironmentData = (temperature, humidity, pressure) => {
  const avgTemp = temperature.reduce((a, b) => a + b, 0) / temperature.length;
  const avgHumidity = humidity.reduce((a, b) => a + b, 0) / humidity.length;
  const avgPressure = pressure.reduce((a, b) => a + b, 0) / pressure.length;
  
  let advice = [];
  
  // 温度分析
  if (avgTemp > 30) {
    advice.push('温度偏高，建议适当开启空调，保持室内通风，注意防暑降温');
  } else if (avgTemp < 22) {
    advice.push('温度偏低，建议适当增加衣物，注意保暖，预防感冒');
  }
  
  // 湿度分析
  if (avgHumidity > 65) {
    advice.push('湿度较大，建议使用除湿器，注意防潮，保持室内干燥');
  } else if (avgHumidity < 45) {
    advice.push('湿度较低，建议使用加湿器，多补充水分，注意皮肤保湿');
  }
  
  // 大气压分析
  if (avgPressure > 1015) {
    advice.push('气压较高，天气晴朗，适合户外活动，建议适当增加户外运动时间');
  } else if (avgPressure < 1005) {
    advice.push('气压较低，可能天气变化，建议关注天气预报，注意增减衣物');
  }
  
  if (advice.length > 0) {
    environmentAdvice.value = advice.join('；');
    hasEnvironmentAdvice.value = true;
  } else {
    environmentAdvice.value = '当前环境数据正常，建议保持良好作息，适当运动，注意饮食均衡';
    hasEnvironmentAdvice.value = true;
  }
};

// 发送环境建议
const sendEnvironmentAdvice = () => {
  if (!hasEnvironmentAdvice.value) return;
  
  ElMessage({
    message: '环境建议已发送给用户',
    type: 'success'
  });
};

// 监听窗口大小变化
const handleResize = () => {
  environmentChart.value?.resize();
  // ... 保持原有的resize代码 ...
};

// 组件挂载时初始化
onMounted(() => {
  initEnvironmentChart();
  // ... 保持原有的初始化代码 ...
  
  window.addEventListener('resize', handleResize);
});

// 组件卸载时清理
onUnmounted(() => {
  environmentChart.value?.dispose();
  // ... 保持原有的清理代码 ...
  
  window.removeEventListener('resize', handleResize);
});

// 监听用户变化
watch(selectedUser, () => {
  initEnvironmentChart();
  // ... 保持原有的watch代码 ...
});

// 计算心率分析数据
function calculateHeartRateAnalysis() {
  // 计算所有用户平均心率
  heartRateAnalysis.value.allUsersAvg = calculateAverageHeartRate();
  heartRateAnalysis.value.userCount = users.value.length;
  
  // 获取心率分布
  heartRateAnalysis.value.distribution = getHeartRateDistribution();
  
  // 生成反馈建议
  generateHeartRateFeedback();
}

// 生成心率反馈
function generateHeartRateFeedback() {
  const avg = heartRateAnalysis.value.allUsersAvg;
  const normalCount = heartRateAnalysis.value.distribution.normal;
  const totalCount = heartRateAnalysis.value.userCount;
  const normalPercentage = (normalCount / totalCount) * 100;

  let feedback = '';
  let type = '';

  if (normalPercentage >= 80) {
    feedback = `整体心率状况良好，${normalPercentage.toFixed(1)}%的用户心率在正常范围内。建议继续保持良好的生活习惯，定期进行体检。`;
    type = 'success';
  } else if (normalPercentage >= 60) {
    feedback = `整体心率状况一般，${normalPercentage.toFixed(1)}%的用户心率在正常范围内。建议加强健康管理，适当增加运动量，注意作息规律。`;
    type = 'warning';
  } else {
    feedback = `整体心率状况需要关注，仅${normalPercentage.toFixed(1)}%的用户心率在正常范围内。建议及时进行健康干预，必要时就医检查，加强健康监测。`;
    type = 'danger';
  }

  heartRateAnalysis.value.suggestion = feedback;
  heartRateAnalysis.value.suggestionType = type;
}

// 在 onMounted 中调用计算函数
onMounted(() => {
  initHealthTrendChart();
  initHealthDistributionChart();
  calculateHeartRateAnalysis();
  
  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    healthTrendChart?.resize();
    healthDistributionChart?.resize();
  });
});
</script>

<style scoped>
.statistics-container {
  padding: 20px;
}

.user-select-card {
  margin-bottom: 20px;
}

.stat-card {
  margin-bottom: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  text-align: center;
  padding: 20px 0;
}

.chart-container {
  height: 300px;
}

.chart {
  width: 100%;
  height: 100%;
}

.advice-container {
  margin-top: 20px;
}

:deep(.el-alert) {
  margin-top: 10px;
}

.analysis-card {
  margin-top: 20px;
}

.analysis-details {
  padding: 20px;
}

.mt-3 {
  margin-top: 15px;
}
</style> 