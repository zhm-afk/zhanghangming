import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Dashboard from '../views/Dashboard.vue';
import UserManagement from '../views/UserManagement.vue';
import DeviceManagement from '../views/DeviceManagement.vue';
import DataAnalysis from '../views/DataAnalysis.vue';
import RealTimeMonitor from '../views/RealTimeMonitor.vue';
import Settings from '../views/Settings.vue';
import MapLocation from '../views/MapLocation.vue';
import AdminManagement from '../views/AdminManagement.vue';
import Home from '../views/Home.vue';
import AiAssistant from '../views/AiAssistant.vue';
import UserFeedback from '../views/UserFeedback.vue';
import ApiTest from '../views/ApiTest.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/api-test', component: ApiTest },
  {
    path: '/redirect',
    component: Dashboard,
    meta: { requiresAuth: true },
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => {
          return import('../views/Redirect.vue');
        }
      }
    ]
  },
  {
    path: '/dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
    children: [
      { 
        path: '', 
        component: Home,
        meta: { requiresAuth: true, title: '首页', icon: 'HomeFilled' }
      },
      { 
        path: 'users', 
        component: UserManagement,
        meta: { requiresAuth: true, title: '用户管理', icon: 'UserFilled' }
      },
      { 
        path: 'devices', 
        component: DeviceManagement,
        meta: { requiresAuth: true, title: '设备管理', icon: 'Monitor' }
      },
      { 
        path: 'analysis', 
        component: DataAnalysis,
        meta: { requiresAuth: true, title: '数据统计分析', icon: 'DataLine' }
      },
      { 
        path: 'monitor', 
        component: RealTimeMonitor,
        meta: { requiresAuth: true, title: '实时数据监控', icon: 'View' }
      },
      { 
        path: 'settings', 
        component: Settings,
        meta: { requiresAuth: true, title: '系统设置', icon: 'Setting' }
      },
      { 
        path: 'location', 
        component: MapLocation,
        meta: { requiresAuth: true, title: '设备位置', icon: 'Location' }
      },
      { 
        path: 'admin', 
        component: AdminManagement,
        meta: { requiresAuth: true, title: '管理员管理', icon: 'User' }
      },
      { 
        path: 'feedback', 
        component: UserFeedback,
        meta: { requiresAuth: true, title: '用户反馈', icon: 'ChatLineRound' }
      },
      { 
        path: 'ai-assistant', 
        component: AiAssistant,
        meta: { requiresAuth: true, title: 'AI助手', icon: 'ChatDotRound' }
      },
      {
        path: 'api-test',
        component: ApiTest,
        meta: { requiresAuth: true, title: 'API测试', icon: 'Connection' }
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 路由守卫
router.beforeEach((to, from, next) => {
  // 不进行认证检查，所有人都可以访问
  // 处理重定向路由
  if (to.path.startsWith('/redirect')) {
    const path = to.params.path;
    // 将路径转换回实际路径并跳转
    router.replace('/' + path);
    return;
  }
  
  // 总是允许访问
  next();
});

export default router; 