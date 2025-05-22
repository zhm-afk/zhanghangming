<script setup>
import { onBeforeMount } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

onBeforeMount(() => {
  const { params, query } = route;
  const { path } = params;
  
  // 提取要重定向的实际路径
  const redirectPath = Array.isArray(path) ? `/${path.join('/')}` : `/${path}`;
  
  // 使用原始查询参数进行跳转
  router.replace({
    path: redirectPath,
    query,
  });
});
</script> 