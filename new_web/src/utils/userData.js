// 用户数据管理
export const defaultUsers = [
  {
    id: 1,
    username: '张三',
    nickname: '张三',
    age: 28,
    deviceId: 'SB1001',
    registerTime: '2024-05-01',
    heartRate: 75,
    bloodPressure: { systolic: 120, diastolic: 80 },
    steps: 8000,
    location: {
      lat: 39.908,
      lng: 116.397,
      area: '海淀区'
    }
  },
  {
    id: 2,
    username: '李四',
    nickname: '李四',
    age: 35,
    deviceId: 'SB1002',
    registerTime: '2024-05-03',
    heartRate: 82,
    bloodPressure: { systolic: 130, diastolic: 85 },
    steps: 9000,
    location: {
      lat: 39.915,
      lng: 116.404,
      area: '朝阳区'
    }
  },
  {
    id: 3,
    username: '王五',
    nickname: '王五',
    age: 22,
    deviceId: 'SB1003',
    registerTime: '2024-05-05',
    heartRate: 68,
    bloodPressure: { systolic: 110, diastolic: 75 },
    steps: 7000,
    location: {
      lat: 39.905,
      lng: 116.390,
      area: '西城区'
    }
  },
  {
    id: 4,
    username: '赵六',
    nickname: '赵六',
    age: 45,
    deviceId: 'SB1004',
    registerTime: '2024-05-07',
    heartRate: 88,
    bloodPressure: { systolic: 135, diastolic: 90 },
    steps: 6000,
    location: {
      lat: 39.920,
      lng: 116.410,
      area: '东城区'
    }
  },
  {
    id: 5,
    username: '钱七',
    nickname: '钱七',
    age: 31,
    deviceId: 'SB1005',
    registerTime: '2024-05-09',
    heartRate: 72,
    bloodPressure: { systolic: 125, diastolic: 82 },
    steps: 8500,
    location: {
      lat: 39.925,
      lng: 116.415,
      area: '丰台区'
    }
  }
];

// 获取所有用户
export function getAllUsers() {
  return defaultUsers;
}

// 根据ID获取用户
export function getUserById(id) {
  return defaultUsers.find(user => user.id === id);
}

// 根据用户名获取用户
export function getUserByUsername(username) {
  return defaultUsers.find(user => user.username === username);
}

// 获取用户健康数据
export function getUserHealthData(username) {
  const user = getUserByUsername(username);
  if (!user) return null;
  
  return {
    heartRate: user.heartRate,
    bloodPressure: user.bloodPressure,
    steps: user.steps
  };
}

// 获取用户位置数据
export function getUserLocation(username) {
  const user = getUserByUsername(username);
  if (!user) return null;
  
  return user.location;
}

// 计算所有用户的平均心率
export function calculateAverageHeartRate() {
  const total = defaultUsers.reduce((sum, user) => sum + user.heartRate, 0);
  return Math.round(total / defaultUsers.length);
}

// 计算所有用户的平均血压
export function calculateAverageBloodPressure() {
  const totalSystolic = defaultUsers.reduce((sum, user) => sum + user.bloodPressure.systolic, 0);
  const totalDiastolic = defaultUsers.reduce((sum, user) => sum + user.bloodPressure.diastolic, 0);
  
  return {
    systolic: Math.round(totalSystolic / defaultUsers.length),
    diastolic: Math.round(totalDiastolic / defaultUsers.length)
  };
}

// 计算所有用户的平均步数
export function calculateAverageSteps() {
  const total = defaultUsers.reduce((sum, user) => sum + user.steps, 0);
  return Math.round(total / defaultUsers.length);
}

// 获取心率分布
export function getHeartRateDistribution() {
  const normalRange = { min: 60, max: 100 };
  return defaultUsers.reduce((dist, user) => {
    if (user.heartRate < normalRange.min) {
      dist.low++;
    } else if (user.heartRate > normalRange.max) {
      dist.high++;
    } else {
      dist.normal++;
    }
    return dist;
  }, { normal: 0, high: 0, low: 0 });
} 