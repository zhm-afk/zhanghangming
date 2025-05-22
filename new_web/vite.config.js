import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig(({ command, mode }) => {
  // 加载环境变量，确保包含 .env.local 文件
  const env = loadEnv(mode, process.cwd(), '');
  
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    },
    server: {
      port: 3000,
      host: '0.0.0.0',
      open: false,
      proxy: {
        '/api': {
          target: 'http://182.92.87.209:5000',
          changeOrigin: true,
          secure: false,
          headers: {
            Connection: 'keep-alive'
          }
        }
      }
    },
    // 确保环境变量在客户端可用
    define: {
      'import.meta.env.VITE_DASHSCOPE_API_KEY': JSON.stringify(env.VITE_DASHSCOPE_API_KEY),
      'import.meta.env.VITE_API_BASE_URL': JSON.stringify(env.VITE_API_BASE_URL || '/api')
    }
  };
}); 