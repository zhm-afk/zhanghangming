<template>
  <div class="admin-management">
    <div class="page-header">
      <div class="header-left">
        <h2>管理员管理</h2>
        <span class="header-desc">管理系统管理员账号和权限</span>
      </div>
      <!-- 只有超级管理员可以看到添加按钮 -->
      <el-button 
        v-if="isSuperAdmin" 
        type="primary" 
        @click="showAddDialog"
        class="add-button"
      >
        <el-icon><Plus /></el-icon>
        添加管理员
      </el-button>
    </div>

    <!-- 管理员列表 -->
    <el-card class="admin-card" v-loading="loading">
      <el-table 
        :data="adminList" 
        style="width: 100%" 
        border
        :header-cell-style="{
          background: '#f5f7fa',
          color: '#1a237e',
          fontWeight: 'bold'
        }"
      >
        <el-table-column prop="username" label="用户名" min-width="120">
          <template #default="scope">
            <div class="user-cell">
              <el-avatar 
                :size="32" 
                :src="getAvatarUrl(scope.row.avatar)"
                @error="handleAvatarError"
              >
                {{ scope.row.username.charAt(0) }}
              </el-avatar>
              <span>{{ scope.row.username }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="nickname" label="昵称" min-width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag 
              :type="scope.row.status === '在线' ? 'success' : 'info'"
              :effect="scope.row.status === '在线' ? 'dark' : 'plain'"
              class="status-tag"
            >
              <el-icon class="status-icon" :class="{ 'is-online': scope.row.status === '在线' }">
                <CircleCheck v-if="scope.row.status === '在线'" />
                <CircleClose v-else />
              </el-icon>
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="role" label="角色" width="120">
          <template #default="scope">
            <el-tag 
              :type="scope.row.role === 'super' ? 'danger' : 'success'"
              :effect="!isSuperAdmin ? 'plain' : 'dark'"
              class="role-tag"
            >
              {{ scope.row.role === 'super' ? '超级管理员' : '普通管理员' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="lastLogin" label="最近登录" min-width="180">
          <template #default="scope">
            <div class="time-cell">
              <el-icon><Timer /></el-icon>
              <span>{{ scope.row.lastLogin }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <!-- 只有超级管理员可以删除其他管理员 -->
            <el-button
              v-if="isSuperAdmin && scope.row.username !== currentUser.username"
              type="danger"
              size="small"
              @click="handleDelete(scope.row)"
              class="delete-button"
            >
              <el-icon><Delete /></el-icon>
            </el-button>
            <span v-else-if="!isSuperAdmin" class="no-permission">
              <el-icon><Lock /></el-icon>
              无权限
            </span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加管理员对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="添加管理员"
      width="500px"
      class="add-dialog"
    >
      <el-form 
        :model="adminForm" 
        :rules="formRules"
        ref="adminFormRef"
        label-width="100px" 
        class="admin-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="adminForm.username" placeholder="请输入用户名">
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="adminForm.password" type="password" placeholder="请输入密码">
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="adminForm.nickname" placeholder="请输入昵称">
            <template #prefix>
              <el-icon><UserFilled /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="adminForm.role" placeholder="请选择角色" class="role-select">
            <el-option label="超级管理员" value="super">
              <el-icon><Star /></el-icon>
              <span>超级管理员</span>
            </el-option>
            <el-option label="普通管理员" value="normal">
              <el-icon><User /></el-icon>
              <span>普通管理员</span>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAdd" :loading="submitting">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { 
  Plus, 
  Delete, 
  User, 
  UserFilled, 
  Lock, 
  Star, 
  Timer,
  CircleCheck,
  CircleClose
} from '@element-plus/icons-vue';
import { adminApi } from '../utils/api';

// 获取当前登录用户信息
const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');

// 判断是否是超级管理员
const isSuperAdmin = computed(() => {
  return currentUser.role === 'super';
});

const adminList = ref([]);
const loading = ref(true);
const dialogVisible = ref(false);
const submitting = ref(false);
const adminFormRef = ref(null);

// 获取头像URL
const getAvatarUrl = (avatar) => {
  if (!avatar) return '';
  
  // 调试输出
  console.log('处理头像URL:', avatar);
  
  // 如果已经是完整URL，直接返回
  if (avatar.startsWith('http')) {
    return avatar;
  }
  
  // 如果是静态路径，添加服务器前缀
  if (avatar.startsWith('/static')) {
    return `http://182.92.87.209:5000${avatar}`;
  }
  
  // 如果是Base64数据，直接返回
  if (avatar.startsWith('data:image/')) {
    return avatar;
  }
  
  console.log('无效的头像URL:', avatar);
  return '';
};

// 头像加载错误处理
const handleAvatarError = () => {
  // 头像加载失败时使用默认头像
  console.warn('头像加载失败');
};

const adminForm = ref({
  username: '',
  password: '',
  nickname: '',
  role: 'normal'
});

// 表单验证规则
const formRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' }
  ]
};

// 获取所有管理员
const loadAdmins = async () => {
  loading.value = true;
  try {
    // 检查token是否存在
    const token = localStorage.getItem('token');
    if (!token) {
      ElMessage.warning('未检测到登录信息，请先登录');
      loading.value = false;
      return;
    }

    console.log('开始获取管理员列表，token存在:', !!token);
    
    // 先尝试直接通过API URL请求
    const API_BASE_URL = 'http://182.92.87.209:5000'; 
    try {
      console.log('尝试直接访问API获取管理员列表');
      const response = await fetch(`${API_BASE_URL}/api/admins`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const responseData = await response.json();
      console.log('直接API响应:', responseData);
      
      if (responseData.success) {
        adminList.value = responseData.data;
        ElMessage.success('获取管理员列表成功');
        loading.value = false;
        return;
      }
    } catch (directError) {
      console.error('直接API请求失败:', directError);
    }
    
    // 如果直接请求失败，尝试通过axios调用
    const response = await adminApi.getAllAdmins();
    console.log('管理员列表API响应:', response);
    
    if (response.success) {
      adminList.value = response.data;
      ElMessage.success('获取管理员列表成功');
    } else {
      ElMessage.error(response.message || '获取管理员列表失败');
    }
  } catch (error) {
    console.error('获取管理员列表失败:', error);
    
    // 检查是否为401认证错误
    if (error.response && error.response.status === 401) {
      console.log('收到401响应，但不做任何处理，继续使用本地数据');
      // 使用本地存储数据，不清除token或提示登录过期
    } else {
      ElMessage.error('获取管理员列表失败，请检查网络连接');
    }
  } finally {
    loading.value = false;
  }
};

// 显示添加对话框
const showAddDialog = () => {
  if (!isSuperAdmin.value) {
    ElMessage.warning('只有超级管理员可以添加新管理员');
    return;
  }
  dialogVisible.value = true;
};

// 添加管理员
const handleAdd = async () => {
  if (!adminFormRef.value) return;

  await adminFormRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true;
      try {
        const response = await adminApi.createAdmin(adminForm.value);
        
        if (response.success) {
          ElMessage.success('添加管理员成功');
          dialogVisible.value = false;
          // 重新加载管理员列表
          await loadAdmins();
          // 重置表单
          resetForm();
        } else {
          ElMessage.error(response.message || '添加管理员失败');
        }
      } catch (error) {
        console.error('添加管理员失败:', error);
        if (error.response && error.response.data && error.response.data.message) {
          ElMessage.error(error.response.data.message);
        } else {
          ElMessage.error('添加管理员失败，请检查网络连接');
        }
      } finally {
        submitting.value = false;
      }
    } else {
      ElMessage.warning('请完善表单信息');
    }
  });
};

// 重置表单
const resetForm = () => {
  if (adminFormRef.value) {
    adminFormRef.value.resetFields();
  }
  
  adminForm.value = {
    username: '',
    password: '',
    nickname: '',
    role: 'normal'
  };
};

// 删除管理员
const handleDelete = async (admin) => {
  if (!isSuperAdmin.value) {
    ElMessage.warning('只有超级管理员可以删除管理员');
    return;
  }

  ElMessageBox.confirm(
    `确定要删除管理员 ${admin.username} 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const response = await adminApi.deleteAdmin(admin.id);
      
      if (response.success) {
        ElMessage.success('删除管理员成功');
        // 重新加载管理员列表
        await loadAdmins();
      } else {
        ElMessage.error(response.message || '删除管理员失败');
      }
    } catch (error) {
      console.error('删除管理员失败:', error);
      ElMessage.error('删除管理员失败，请检查网络连接');
    }
  }).catch(() => {
    // 用户取消，不做任何操作
  });
};

// 页面加载时获取管理员列表
onMounted(async () => {
  await loadAdmins();
});
</script>

<style scoped>
.admin-management {
  padding: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background-color: white;
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.header-left {
  display: flex;
  flex-direction: column;
}

.header-left h2 {
  margin: 0;
  color: #1a237e;
  font-size: 20px;
}

.header-desc {
  color: #909399;
  font-size: 14px;
  margin-top: 5px;
}

.add-button {
  background-color: #1a237e;
  border-color: #1a237e;
}

.add-button:hover {
  background-color: #283593;
  border-color: #283593;
}

.admin-card {
  flex: 1;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.admin-card .el-card__body {
  padding: 0;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-tag {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.status-icon {
  width: 14px;
  height: 14px;
}

.status-icon.is-online {
  color: #67c23a;
}

.role-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  padding: 0 8px;
  height: 24px;
  line-height: 24px;
}

.time-cell {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #606266;
}

.delete-button {
  padding: 5px 10px;
}

.no-permission {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #909399;
  font-size: 12px;
}

/* 添加管理员对话框样式 */
.admin-form {
  margin-top: 20px;
}

.role-select {
  width: 100%;
}

:deep(.el-select-dropdown__item) {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.role-select .el-select__tags .el-tag) {
  background-color: #f0f5ff;
  border-color: #d6e4ff;
  color: #1a237e;
}

/* 响应式样式 */
@media screen and (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
    padding: 15px;
  }
  
  .add-button {
    width: 100%;
  }
  
  .header-left h2 {
    font-size: 18px;
  }
  
  .admin-card {
    margin: 0 -10px 20px;
    border-radius: 0;
  }
  
  .admin-form {
    margin-top: 10px;
  }
  
  :deep(.el-table) {
    border-radius: 0;
  }
  
  :deep(.el-table .cell) {
    padding: 8px;
  }
  
  .user-cell {
    gap: 5px;
  }
  
  .user-cell .el-avatar {
    width: 24px;
    height: 24px;
    font-size: 12px;
  }
  
  .status-tag,
  .role-tag {
    padding: 0 4px;
    font-size: 12px;
  }
  
  .time-cell {
    font-size: 12px;
  }
  
  :deep(.add-dialog) {
    width: 95% !important;
  }
}
</style> 