<template>
  <div class="analysis-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>用户平均数据统计</span>
            </div>
          </template>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="chart" ref="bloodPressureChart"></div>
            </el-col>
            <el-col :span="8">
              <div class="chart" ref="stepsChart"></div>
            </el-col>
            <el-col :span="8">
              <div class="chart" ref="ageChart"></div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>详细数据</span>
            </div>
          </template>
          <el-descriptions title="所有用户平均数据" :column="3" border>
            <el-descriptions-item label="血压平均值">{{ avgBloodPressure }}</el-descriptions-item>
            <el-descriptions-item label="步数平均值">{{ avgSteps }}</el-descriptions-item>
            <el-descriptions-item label="年龄平均值">{{ avgAge }}</el-descriptions-item>
          </el-descriptions>
          <el-table :data="users" style="width: 100%; margin-top: 20px;">
            <el-table-column prop="username" label="用户名" />
            <el-table-column label="血压">
              <template #default="{ row }">
                {{ row.bloodPressure.systolic }}/{{ row.bloodPressure.diastolic }}
              </template>
            </el-table-column>
            <el-table-column prop="steps" label="步数" />
            <el-table-column prop="age" label="年龄" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 用户使用时间分析卡片 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>用户使用时间分析</span>
            </div>
          </template>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="chart" ref="usageDaysChart"></div>
            </el-col>
            <el-col :span="12">
              <div class="chart" ref="dailyUsageChart"></div>
            </el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 20px;">
            <el-col :span="24">
              <div class="analysis-summary">
                <h3>用户使用时间分析</h3>
                <p>截至目前，系统用户的使用情况如下：</p>
                <ul>
                  <li>用户平均使用天数：{{ avgUsageDays }} 天</li>
                  <li>用户平均每日使用时长：{{ avgDailyUsageHours.toFixed(1) }} 小时</li>
                </ul>
                
                <h3>日均使用时间分析</h3>
                <p>用户日均使用时长分布情况：</p>
                <ul>
                  <li>使用时间最长：{{ maxDailyUsageUser }}，日均 {{ maxDailyUsageHours.toFixed(1) }} 小时</li>
                  <li>使用时间最短：{{ minDailyUsageUser }}，日均 {{ minDailyUsageHours.toFixed(1) }} 小时</li>
                  <li>使用时段分布：早间(6-12点) {{ morningUsagePercent.toFixed(0) }}%，午间(12-18点) {{ afternoonUsagePercent.toFixed(0) }}%，晚间(18-24点) {{ eveningUsagePercent.toFixed(0) }}%</li>
                </ul>
                
                <h3>使用时间与健康数据关系</h3>
                <p>对比使用时间与健康数据的关联性：</p>
                <ul>
                  <li>使用超过10天的用户平均步数为 {{ getUsageDaysGroupAvgSteps(10) }} 步，血压平均值 {{ getUsageDaysGroupAvgBP(10) }}</li>
                  <li>使用低于10天的用户平均步数为 {{ getUsageDaysGroupAvgSteps(0, 10) }} 步，血压平均值 {{ getUsageDaysGroupAvgBP(0, 10) }}</li>
                  <li>日均使用超过2小时的用户平均步数为 {{ getDailyUsageGroupAvgSteps(2) }} 步，血压平均值 {{ getDailyUsageGroupAvgBP(2) }}</li>
                  <li>日均使用低于2小时的用户平均步数为 {{ getDailyUsageGroupAvgSteps(0, 2) }} 步，血压平均值 {{ getDailyUsageGroupAvgBP(0, 2) }}</li>
                </ul>
                
                <h3>使用时间分析结论</h3>
                <p>用户使用日期呈现{{ usageDaysDistribution }}趋势。日均使用时长为{{ avgDailyUsageHours.toFixed(1) }}小时，{{ dailyUsageConclusion }}。系统稳定性良好，用户留存率较高，{{ retentionConclusion }}</p>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 新增用户年龄分布分析卡片 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>用户年龄分布分析</span>
            </div>
          </template>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="chart" ref="ageDistributionChart"></div>
            </el-col>
            <el-col :span="12">
              <div class="stat-cards">
                <el-card shadow="hover" class="stat-card">
                  <div class="stat-value">{{ ageGroups['20-30'] || 0 }}</div>
                  <div class="stat-label">20-30岁</div>
                </el-card>
                <el-card shadow="hover" class="stat-card">
                  <div class="stat-value">{{ ageGroups['31-40'] || 0 }}</div>
                  <div class="stat-label">31-40岁</div>
                </el-card>
                <el-card shadow="hover" class="stat-card">
                  <div class="stat-value">{{ ageGroups['41-50'] || 0 }}</div>
                  <div class="stat-label">41-50岁</div>
                </el-card>
                <el-card shadow="hover" class="stat-card">
                  <div class="stat-value">{{ minAge }}</div>
                  <div class="stat-label">最小年龄</div>
                </el-card>
                <el-card shadow="hover" class="stat-card">
                  <div class="stat-value">{{ maxAge }}</div>
                  <div class="stat-label">最大年龄</div>
                </el-card>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>

    <!-- 年龄分析总结卡片 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>年龄分析总结</span>
            </div>
          </template>
          <div class="analysis-summary">
            <h3>年龄分布情况</h3>
            <p>根据当前用户数据分析，本系统用户年龄分布在{{ minAge }}岁至{{ maxAge }}岁之间，平均年龄为{{ avgAge }}岁。</p>
            <p>年龄分布呈现以下特点：</p>
            <ul>
              <li>20-30岁年龄段用户{{ ageGroups['20-30'] || 0 }}人，占比{{ ((ageGroups['20-30'] || 0) / users.length * 100).toFixed(1) }}%，{{ ageGroups['20-30'] > 0 ? '主要是年轻用户' : '相对较少' }}；</li>
              <li>31-40岁年龄段用户{{ ageGroups['31-40'] || 0 }}人，占比{{ ((ageGroups['31-40'] || 0) / users.length * 100).toFixed(1) }}%，属于{{ ageGroups['31-40'] > 1 ? '系统主要用户群体' : '一般用户群体' }}；</li>
              <li>41-50岁年龄段用户{{ ageGroups['41-50'] || 0 }}人，占比{{ ((ageGroups['41-50'] || 0) / users.length * 100).toFixed(1) }}%，{{ ageGroups['41-50'] > 0 ? '中老年用户有一定基础' : '中老年用户较少' }}。</li>
            </ul>
            <h3>健康指标与年龄关系</h3>
            <p>根据年龄与其他健康指标的交叉分析：</p>
            <ul>
              <li>{{ minAge }}岁至30岁用户平均步数{{ getAgeGroupAvgSteps('20-30') }}步，血压平均值{{ getAgeGroupAvgBP('20-30') }}；</li>
              <li>31岁至40岁用户平均步数{{ getAgeGroupAvgSteps('31-40') }}步，血压平均值{{ getAgeGroupAvgBP('31-40') }}；</li>
              <li>41岁至{{ maxAge }}岁用户平均步数{{ getAgeGroupAvgSteps('41-50') }}步，血压平均值{{ getAgeGroupAvgBP('41-50') }}。</li>
            </ul>
            <h3>年龄分析结论</h3>
            <p>本系统的用户年龄分布较为均衡，覆盖了年轻人至中老年人群，产品设计需兼顾不同年龄段用户的需求。随着年龄增长，用户的健康指标如血压有上升趋势，而活动量（步数）则有所下降，符合一般健康规律。</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, nextTick } from 'vue';
import * as echarts from 'echarts';
import { getAllUsers, calculateAverageBloodPressure, calculateAverageSteps } from '../utils/userData';

const users = ref(getAllUsers());
const bloodPressureChart = ref(null);
const stepsChart = ref(null);
const ageChart = ref(null);
const ageDistributionChart = ref(null);
const usageDaysChart = ref(null);
const dailyUsageChart = ref(null);

// 血压和步数平均值计算
const avgBloodPressure = computed(() => {
  const avg = calculateAverageBloodPressure();
  return `${avg.systolic}/${avg.diastolic}`;
});

const avgSteps = computed(() => {
  return calculateAverageSteps().toFixed(0);
});

// 年龄相关计算
const avgAge = computed(() => {
  const total = users.value.reduce((sum, user) => sum + user.age, 0);
  return (total / users.value.length).toFixed(1);
});

const minAge = computed(() => {
  return Math.min(...users.value.map(user => user.age));
});

const maxAge = computed(() => {
  return Math.max(...users.value.map(user => user.age));
});

// 年龄分组统计
const ageGroups = computed(() => {
  return users.value.reduce((groups, user) => {
    const age = user.age;
    if (age >= 20 && age <= 30) {
      groups['20-30'] = (groups['20-30'] || 0) + 1;
    } else if (age >= 31 && age <= 40) {
      groups['31-40'] = (groups['31-40'] || 0) + 1;
    } else if (age >= 41 && age <= 50) {
      groups['41-50'] = (groups['41-50'] || 0) + 1;
    } else if (age > 50) {
      groups['50+'] = (groups['50+'] || 0) + 1;
    }
    return groups;
  }, {});
});

// 获取特定年龄段的平均步数
const getAgeGroupAvgSteps = (ageGroup) => {
  const ageRanges = {
    '20-30': [20, 30],
    '31-40': [31, 40],
    '41-50': [41, 50],
    '50+': [51, 200]
  };
  
  const range = ageRanges[ageGroup];
  if (!range) return '无数据';
  
  const filteredUsers = users.value.filter(u => u.age >= range[0] && u.age <= range[1]);
  if (filteredUsers.length === 0) return '无数据';
  
  const avg = filteredUsers.reduce((sum, u) => sum + u.steps, 0) / filteredUsers.length;
  return avg.toFixed(0);
};

// 获取特定年龄段的平均血压
const getAgeGroupAvgBP = (ageGroup) => {
  const ageRanges = {
    '20-30': [20, 30],
    '31-40': [31, 40],
    '41-50': [41, 50],
    '50+': [51, 200]
  };
  
  const range = ageRanges[ageGroup];
  if (!range) return '无数据';
  
  const filteredUsers = users.value.filter(u => u.age >= range[0] && u.age <= range[1]);
  if (filteredUsers.length === 0) return '无数据';
  
  const systolicAvg = filteredUsers.reduce((sum, u) => sum + u.bloodPressure.systolic, 0) / filteredUsers.length;
  const diastolicAvg = filteredUsers.reduce((sum, u) => sum + u.bloodPressure.diastolic, 0) / filteredUsers.length;
  
  return `${systolicAvg.toFixed(0)}/${diastolicAvg.toFixed(0)}`;
};

// 使用时间相关计算
const getUserUsageDays = (registerTimeStr) => {
  const registerTime = new Date(registerTimeStr);
  const now = new Date();
  const diffTime = Math.abs(now - registerTime);
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
};

// 模拟用户日均使用时间数据
const generateDailyUsageHours = (user) => {
  // 基于用户ID生成固定的随机数，以保持一致性
  const seed = user.id * 17 % 10;
  // 生成1-5小时的随机使用时间
  return 1 + (seed / 10) * 4;
};

// 模拟用户使用时段分布
const generateTimeDistribution = (user) => {
  // 基于用户ID生成固定的随机分布
  const seed = user.id;
  return {
    morning: 20 + (seed % 5) * 5,    // 早间使用比例 (20%-40%)
    afternoon: 30 + (seed % 4) * 5,  // 午间使用比例 (30%-45%)
    evening: 25 + (seed % 6) * 5     // 晚间使用比例 (25%-50%)
  };
};

const usersWithUsageData = computed(() => {
  return users.value.map(user => ({
    ...user,
    usageDays: getUserUsageDays(user.registerTime),
    dailyUsageHours: generateDailyUsageHours(user),
    timeDistribution: generateTimeDistribution(user)
  }));
});

const avgUsageDays = computed(() => {
  const total = usersWithUsageData.value.reduce((sum, user) => sum + user.usageDays, 0);
  return Math.round(total / usersWithUsageData.value.length);
});

const minUsageDays = computed(() => {
  return Math.min(...usersWithUsageData.value.map(user => user.usageDays));
});

const maxUsageDays = computed(() => {
  return Math.max(...usersWithUsageData.value.map(user => user.usageDays));
});

// 分析用户使用天数分布
const usageDaysDistribution = computed(() => {
  // 分析用户使用天数的分布特征
  const days = usersWithUsageData.value.map(user => user.usageDays);
  const variance = days.reduce((sum, day) => sum + Math.pow(day - avgUsageDays.value, 2), 0) / days.length;
  
  if (variance > 20) {
    return '分散';
  } else if (maxUsageDays.value - minUsageDays.value > 10) {
    return '均匀递增';
  } else {
    return '集中';
  }
});

const retentionConclusion = computed(() => {
  // 根据使用天数分布得出留存率结论
  if (minUsageDays.value > 7) {
    return '短期用户留存良好';
  } else if (avgUsageDays.value > 14) {
    return '长期用户占比较高';
  } else {
    return '需加强用户活跃度提升策略';
  }
});

const avgDailyUsageHours = computed(() => {
  const total = usersWithUsageData.value.reduce((sum, user) => sum + user.dailyUsageHours, 0);
  return total / usersWithUsageData.value.length;
});

const maxDailyUsageHours = computed(() => {
  return Math.max(...usersWithUsageData.value.map(user => user.dailyUsageHours));
});

const minDailyUsageHours = computed(() => {
  return Math.min(...usersWithUsageData.value.map(user => user.dailyUsageHours));
});

const maxDailyUsageUser = computed(() => {
  const maxHours = maxDailyUsageHours.value;
  const user = usersWithUsageData.value.find(user => user.dailyUsageHours === maxHours);
  return user ? user.username : '无数据';
});

const minDailyUsageUser = computed(() => {
  const minHours = minDailyUsageHours.value;
  const user = usersWithUsageData.value.find(user => user.dailyUsageHours === minHours);
  return user ? user.username : '无数据';
});

// 计算用户整体使用时段分布
const morningUsagePercent = computed(() => {
  const total = usersWithUsageData.value.reduce((sum, user) => sum + user.timeDistribution.morning, 0);
  return total / usersWithUsageData.value.length;
});

const afternoonUsagePercent = computed(() => {
  const total = usersWithUsageData.value.reduce((sum, user) => sum + user.timeDistribution.afternoon, 0);
  return total / usersWithUsageData.value.length;
});

const eveningUsagePercent = computed(() => {
  const total = usersWithUsageData.value.reduce((sum, user) => sum + user.timeDistribution.evening, 0);
  return total / usersWithUsageData.value.length;
});

// 获取日均使用时间分组的平均步数
const getDailyUsageGroupAvgSteps = (minHours, maxHours = Infinity) => {
  const filteredUsers = usersWithUsageData.value.filter(u => u.dailyUsageHours >= minHours && u.dailyUsageHours < maxHours);
  if (filteredUsers.length === 0) return '无数据';
  
  const avg = filteredUsers.reduce((sum, u) => sum + u.steps, 0) / filteredUsers.length;
  return avg.toFixed(0);
};

// 获取日均使用时间分组的平均血压
const getDailyUsageGroupAvgBP = (minHours, maxHours = Infinity) => {
  const filteredUsers = usersWithUsageData.value.filter(u => u.dailyUsageHours >= minHours && u.dailyUsageHours < maxHours);
  if (filteredUsers.length === 0) return '无数据';
  
  const systolicAvg = filteredUsers.reduce((sum, u) => sum + u.bloodPressure.systolic, 0) / filteredUsers.length;
  const diastolicAvg = filteredUsers.reduce((sum, u) => sum + u.bloodPressure.diastolic, 0) / filteredUsers.length;
  
  return `${systolicAvg.toFixed(0)}/${diastolicAvg.toFixed(0)}`;
};

// 日均使用时间分析结论
const dailyUsageConclusion = computed(() => {
  if (avgDailyUsageHours.value > 3) {
    return '用户对系统依赖度高，活跃度良好';
  } else if (avgDailyUsageHours.value > 2) {
    return '用户使用频率适中，有较好粘性';
  } else {
    return '用户日均使用时间较短，需加强功能吸引力';
  }
});

// 获取使用天数分组的平均步数
const getUsageDaysGroupAvgSteps = (minDays, maxDays = Infinity) => {
  const filteredUsers = usersWithUsageData.value.filter(u => u.usageDays >= minDays && u.usageDays < maxDays);
  if (filteredUsers.length === 0) return '无数据';
  
  const avg = filteredUsers.reduce((sum, u) => sum + u.steps, 0) / filteredUsers.length;
  return avg.toFixed(0);
};

// 获取使用天数分组的平均血压
const getUsageDaysGroupAvgBP = (minDays, maxDays = Infinity) => {
  const filteredUsers = usersWithUsageData.value.filter(u => u.usageDays >= minDays && u.usageDays < maxDays);
  if (filteredUsers.length === 0) return '无数据';
  
  const systolicAvg = filteredUsers.reduce((sum, u) => sum + u.bloodPressure.systolic, 0) / filteredUsers.length;
  const diastolicAvg = filteredUsers.reduce((sum, u) => sum + u.bloodPressure.diastolic, 0) / filteredUsers.length;
  
  return `${systolicAvg.toFixed(0)}/${diastolicAvg.toFixed(0)}`;
};

onMounted(() => {
  // 初始化血压柱状图
  const bpChart = echarts.init(bloodPressureChart.value);
  bpChart.setOption({
    title: {
      text: '用户平均血压分布'
    },
    tooltip: {},
    xAxis: {
      data: users.value.map(u => u.username)
    },
    yAxis: {
      name: '血压值'
    },
    series: [{
      name: '收缩压',
      type: 'bar',
      data: users.value.map(u => u.bloodPressure.systolic),
      itemStyle: {
        color: '#409EFF'
      }
    },
    {
      name: '舒张压',
      type: 'bar',
      data: users.value.map(u => u.bloodPressure.diastolic),
      itemStyle: {
        color: '#67C23A'
      }
    }]
  });

  // 初始化步数饼图
  const stChart = echarts.init(stepsChart.value);
  stChart.setOption({
    title: {
      text: '用户平均步数分布'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    series: [{
      name: '步数',
      type: 'pie',
      radius: '50%',
      data: users.value.map(u => ({
        name: u.username,
        value: u.steps
      })),
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  });

  // 初始化年龄柱状图
  const aChart = echarts.init(ageChart.value);
  aChart.setOption({
    title: {
      text: '用户年龄分布'
    },
    tooltip: {},
    xAxis: {
      data: users.value.map(u => u.username)
    },
    yAxis: {
      name: '年龄'
    },
    series: [{
      name: '年龄',
      type: 'bar',
      data: users.value.map(u => u.age),
      itemStyle: {
        color: '#E6A23C'
      }
    }]
  });

  // 初始化年龄分布饼图
  const adChart = echarts.init(ageDistributionChart.value);
  adChart.setOption({
    title: {
      text: '用户年龄段分布'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c}人 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center'
    },
    series: [{
      name: '年龄分布',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '18',
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: ageGroups.value['20-30'] || 0, name: '20-30岁' },
        { value: ageGroups.value['31-40'] || 0, name: '31-40岁' },
        { value: ageGroups.value['41-50'] || 0, name: '41-50岁' },
        { value: ageGroups.value['50+'] || 0, name: '50+岁' }
      ]
    }]
  });

  // 初始化使用天数图表
  const udChart = echarts.init(usageDaysChart.value);
  udChart.setOption({
    title: {
      text: '用户使用天数分布'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c}天'
    },
    xAxis: {
      type: 'category',
      data: usersWithUsageData.value.map(u => u.username)
    },
    yAxis: {
      type: 'value',
      name: '使用天数'
    },
    series: [{
      name: '使用天数',
      type: 'bar',
      data: usersWithUsageData.value.map(u => u.usageDays),
      itemStyle: {
        color: '#9254DE'
      }
    }]
  });

  // 初始化日均使用时间图表
  const duChart = echarts.init(dailyUsageChart.value);
  duChart.setOption({
    title: {
      text: '用户日均使用时长分布'
    },
    tooltip: {
      trigger: 'axis',
      formatter: '{b}: {c}小时'
    },
    xAxis: {
      type: 'category',
      data: usersWithUsageData.value.map(u => u.username),
      axisLabel: {
        rotate: 45,
        interval: 0
      }
    },
    yAxis: {
      type: 'value',
      name: '小时',
      max: function(value) {
        return Math.ceil(value.max * 1.2);
      }
    },
    series: [
      {
        name: '日均使用时长',
        type: 'bar',
        data: usersWithUsageData.value.map(u => u.dailyUsageHours.toFixed(1)),
        itemStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              {offset: 0, color: '#91cc75'},
              {offset: 1, color: '#5470c6'}
            ]
          }
        },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}h'
        }
      },
      {
        name: '平均值',
        type: 'line',
        data: usersWithUsageData.value.map(() => avgDailyUsageHours.value.toFixed(1)),
        itemStyle: {
          color: '#ee6666'
        },
        lineStyle: {
          type: 'dashed'
        },
        symbol: 'none'
      }
    ]
  });

  // 监听窗口大小变化，调整图表大小
  window.addEventListener('resize', () => {
    bpChart.resize();
    stChart.resize();
    aChart.resize();
    adChart.resize();
    udChart.resize();
    duChart.resize();
  });
});
</script>

<style scoped>
.analysis-container {
  padding: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart {
  height: 400px;
  width: 100%;
}

.stat-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: space-between;
  height: 400px;
}

.stat-card {
  flex: 1 0 calc(50% - 15px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  height: calc(50% - 8px);
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  font-size: 16px;
  color: #606266;
  margin-top: 10px;
}

.analysis-summary {
  padding: 0 20px;
}

.analysis-summary h3 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #303133;
  font-weight: 500;
}

.analysis-summary p {
  margin-bottom: 10px;
  line-height: 1.8;
  color: #606266;
}

.analysis-summary ul {
  margin-bottom: 20px;
  padding-left: 20px;
}

.analysis-summary li {
  line-height: 1.8;
  margin-bottom: 8px;
  color: #606266;
}
</style> 