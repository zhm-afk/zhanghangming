<template>
  <div class="feedback-container">
    <div class="page-header">
      <div class="header-left">
        <h2>用户反馈</h2>
        <span class="header-desc">查看用户对智能手环的使用反馈</span>
      </div>
      <div class="header-right">
        <el-select v-model="filterStatus" placeholder="反馈状态" class="filter-select">
          <el-option label="全部" value="all" />
          <el-option label="待处理" value="pending" />
          <el-option label="处理中" value="processing" />
          <el-option label="已完成" value="completed" />
        </el-select>
        <el-select v-model="filterType" placeholder="反馈类型" class="filter-select">
          <el-option label="全部" value="all" />
          <el-option label="功能建议" value="feature" />
          <el-option label="问题反馈" value="bug" />
          <el-option label="使用体验" value="experience" />
        </el-select>
      </div>
    </div>

    <el-card class="feedback-card">
      <el-table 
        :data="filteredFeedbacks" 
        style="width: 100%" 
        v-loading="loading"
        @row-click="handleRowClick"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="userName" label="用户" min-width="120">
          <template #default="scope">
            <div class="user-cell">
              <el-avatar :size="32" :src="scope.row.userAvatar">
                {{ scope.row.userName.charAt(0) }}
              </el-avatar>
              <span>{{ scope.row.userName }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="100">
          <template #default="scope">
            <el-tag :type="getTypeTag(scope.row.type)">
              {{ getTypeLabel(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusTag(scope.row.status)">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="提交时间" width="180" />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button 
              type="primary" 
              link
              @click.stop="handleReply(scope.row)"
            >
              回复
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 反馈详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="currentFeedback?.title"
      width="60%"
      class="feedback-dialog"
    >
      <div class="feedback-detail">
        <div class="feedback-header">
          <div class="user-info">
            <el-avatar :size="48" :src="currentFeedback?.userAvatar">
              {{ currentFeedback?.userName?.charAt(0) }}
            </el-avatar>
            <div class="user-meta">
              <span class="user-name">{{ currentFeedback?.userName }}</span>
              <span class="feedback-time">{{ currentFeedback?.createTime }}</span>
            </div>
          </div>
          <div class="feedback-meta">
            <el-tag :type="getTypeTag(currentFeedback?.type)">
              {{ getTypeLabel(currentFeedback?.type) }}
            </el-tag>
            <el-tag :type="getStatusTag(currentFeedback?.status)">
              {{ getStatusLabel(currentFeedback?.status) }}
            </el-tag>
          </div>
        </div>
        
        <div class="feedback-content">
          <h3>反馈内容</h3>
          <p>{{ currentFeedback?.content }}</p>
        </div>

        <div class="feedback-replies" v-if="currentFeedback?.replies?.length">
          <h3>回复记录</h3>
          <div 
            v-for="reply in currentFeedback.replies" 
            :key="reply.id"
            class="reply-item"
          >
            <div class="reply-header">
              <span class="reply-author">{{ reply.author }}</span>
              <span class="reply-time">{{ reply.time }}</span>
            </div>
            <p class="reply-content">{{ reply.content }}</p>
          </div>
        </div>

        <div class="feedback-reply-form">
          <h3>回复反馈</h3>
          <el-input
            v-model="replyContent"
            type="textarea"
            :rows="3"
            placeholder="请输入回复内容"
          />
          <div class="form-actions">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitReply" :loading="submitting">
              提交回复
            </el-button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { ElMessage } from 'element-plus';

// 状态和类型过滤器
const filterStatus = ref('all');
const filterType = ref('all');
const loading = ref(false);
const dialogVisible = ref(false);
const currentFeedback = ref(null);
const replyContent = ref('');
const submitting = ref(false);

// 模拟反馈数据
const feedbacks = ref([
  {
    id: 1,
    userName: '张三',
    userAvatar: '',
    type: 'feature',
    title: '建议增加睡眠质量分析功能',
    content: '希望可以增加更详细的睡眠质量分析，包括深度睡眠时长、睡眠周期等数据。',
    status: 'pending',
    createTime: '2024-03-20 10:30:00',
    replies: []
  },
  {
    id: 2,
    userName: '李四',
    userAvatar: '',
    type: 'bug',
    title: '心率监测数据异常',
    content: '手环在运动时心率数据波动较大，可能与实际心率不符。',
    status: 'processing',
    createTime: '2024-03-19 15:20:00',
    replies: [
      {
        id: 1,
        author: '管理员',
        time: '2024-03-19 16:00:00',
        content: '感谢您的反馈，我们正在检查相关算法。'
      }
    ]
  },
  {
    id: 3,
    userName: '王五',
    userAvatar: '',
    type: 'experience',
    title: '使用体验建议',
    content: '手环的佩戴舒适度很好，但希望可以增加更多的表盘样式。',
    status: 'completed',
    createTime: '2024-03-18 09:15:00',
    replies: [
      {
        id: 1,
        author: '管理员',
        time: '2024-03-18 10:00:00',
        content: '感谢您的建议，我们将在下个版本增加更多表盘样式。'
      }
    ]
  }
]);

// 过滤后的反馈列表
const filteredFeedbacks = computed(() => {
  return feedbacks.value.filter(feedback => {
    const statusMatch = filterStatus.value === 'all' || feedback.status === filterStatus.value;
    const typeMatch = filterType.value === 'all' || feedback.type === filterType.value;
    return statusMatch && typeMatch;
  });
});

// 获取状态标签
const getStatusTag = (status) => {
  const tags = {
    pending: 'info',
    processing: 'warning',
    completed: 'success'
  };
  return tags[status] || 'info';
};

const getStatusLabel = (status) => {
  const labels = {
    pending: '待处理',
    processing: '处理中',
    completed: '已完成'
  };
  return labels[status] || status;
};

// 获取类型标签
const getTypeTag = (type) => {
  const tags = {
    feature: 'success',
    bug: 'danger',
    experience: 'warning'
  };
  return tags[type] || 'info';
};

const getTypeLabel = (type) => {
  const labels = {
    feature: '功能建议',
    bug: '问题反馈',
    experience: '使用体验'
  };
  return labels[type] || type;
};

// 处理行点击
const handleRowClick = (row) => {
  currentFeedback.value = row;
  dialogVisible.value = true;
};

// 处理回复
const handleReply = (row) => {
  currentFeedback.value = row;
  dialogVisible.value = true;
};

// 提交回复
const submitReply = async () => {
  if (!replyContent.value.trim()) {
    ElMessage.warning('请输入回复内容');
    return;
  }

  submitting.value = true;
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 添加回复
    const newReply = {
      id: Date.now(),
      author: '管理员',
      time: new Date().toLocaleString(),
      content: replyContent.value
    };
    
    currentFeedback.value.replies.push(newReply);
    currentFeedback.value.status = 'processing';
    
    ElMessage.success('回复成功');
    replyContent.value = '';
  } catch (error) {
    ElMessage.error('回复失败');
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.feedback-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.header-left h2 {
  margin: 0;
  color: #1a237e;
  font-size: 24px;
}

.header-desc {
  color: #666;
  font-size: 14px;
}

.header-right {
  display: flex;
  gap: 10px;
}

.filter-select {
  width: 120px;
}

.feedback-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* 反馈详情对话框样式 */
.feedback-dialog :deep(.el-dialog__body) {
  padding: 20px;
}

.feedback-detail {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-meta {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.user-name {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.feedback-time {
  font-size: 12px;
  color: #999;
}

.feedback-meta {
  display: flex;
  gap: 10px;
}

.feedback-content {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.feedback-content h3 {
  margin: 0 0 10px 0;
  color: #1a237e;
  font-size: 16px;
}

.feedback-content p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

.feedback-replies {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.feedback-replies h3 {
  margin: 0 0 10px 0;
  color: #1a237e;
  font-size: 16px;
}

.reply-item {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
}

.reply-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.reply-author {
  font-weight: 500;
  color: #1a237e;
}

.reply-time {
  font-size: 12px;
  color: #999;
}

.reply-content {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

.feedback-reply-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.feedback-reply-form h3 {
  margin: 0;
  color: #1a237e;
  font-size: 16px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 