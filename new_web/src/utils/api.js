import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 从localStorage获取token并添加到请求头
    const token = localStorage.getItem('token');
    
    // 请求开始前重新检查token是否有效
    if (token) {
      try {
        // 检查token格式
        console.log('请求URL:', config.url);
        console.log('token格式检查:', token.substring(0, 20) + '...');
        
        // 确保token格式正确
        config.headers['Authorization'] = `Bearer ${token.trim()}`; 
        console.log('已设置Authorization头部');
      } catch (e) {
        console.error('解析token时出错:', e);
        // 如果token无效，清除它
        localStorage.removeItem('token');
        console.warn('移除了无效的token');
      }
    } else {
      console.warn('发送请求没有token:', config.url);
      // 检查是否是认证相关路径
      if (!config.url.includes('/auth/login')) {
        console.warn('未登录用户尝试访问需要认证的接口');
      }
    }
    return config;
  },
  error => {
    console.error('请求拦截器错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 只在调试时打印完整响应
    if (response.config.url.includes('/auth/login')) {
      console.log(`登录API响应:`, response.data);
    } else {
      console.log(`API响应成功 [${response.config.url}]`);
    }
    return response.data;
  },
  error => {
    console.error('API请求错误:', error);
    
    // 打印详细的错误信息
    if (error.response) {
      console.error('错误响应状态:', error.response.status);
      console.error('错误响应数据:', error.response.data);
      console.error('错误请求URL:', error.config.url);
      
      // 不再处理401错误，避免登录过期问题
      // 只有当用户主动点击"退出登录"才会清除token
    }
    
    return Promise.reject(error);
  }
);

// 用户相关接口
export const userApi = {
  // 获取所有用户
  getAllUsers() {
    return api.get('/users');
  },
  
  // 获取单个用户
  getUser(userId) {
    return api.get(`/users/${userId}`);
  },
  
  // 创建新用户
  createUser(userData) {
    return api.post('/users', userData);
  }
};

// 智能手环用户相关接口
export const smartBandUserApi = {
  // 获取所有智能手环用户
  getAllUsers() {
    return api.get('/smart-band-users');
  },
  
  // 获取单个智能手环用户
  getUser(userId) {
    return api.get(`/smart-band-users/${userId}`);
  },
  
  // 创建新智能手环用户
  createUser(userData) {
    return api.post('/smart-band-users', userData);
  },
  
  // 更新智能手环用户
  updateUser(userId, userData) {
    return api.put(`/smart-band-users/${userId}`, userData);
  },
  
  // 删除智能手环用户
  deleteUser(userId) {
    return api.delete(`/smart-band-users/${userId}`);
  }
};

// 管理员相关接口
export const adminApi = {
  // 登录
  login(username, password) {
    return api.post('/auth/login', { username, password });
  },
  
  // 登出
  logout() {
    // 从localStorage获取当前用户
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
    const username = currentUser.username;
    
    return api.post('/auth/logout', { username });
  },
  
  // 获取当前管理员信息
  getProfile() {
    // 从localStorage获取当前用户
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
    const username = currentUser.username;
    
    // 携带username作为查询参数
    return api.get('/auth/profile', {
      params: {
        username: username
      }
    });
  },
  
  // 更新当前管理员信息
  updateProfile(data) {
    return api.put('/auth/profile', data);
  },
  
  // 获取所有管理员
  getAllAdmins() {
    return api.get('/admins');
  },
  
  // 获取单个管理员
  getAdmin(adminId) {
    return api.get(`/admins/${adminId}`);
  },
  
  // 创建新管理员
  createAdmin(adminData) {
    return api.post('/admins', adminData);
  },
  
  // 更新管理员
  updateAdmin(adminId, adminData) {
    return api.put(`/admins/${adminId}`, adminData);
  },
  
  // 删除管理员
  deleteAdmin(adminId) {
    return api.delete(`/admins/${adminId}`);
  }
};

export default api; 