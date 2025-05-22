# 使用Node.js官方镜像作为基础镜像
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 复制package.json和package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制所有文件到容器中
COPY . .

# 构建应用
RUN npm run build

# 设置环境变量
ENV PORT=5000
ENV NODE_ENV=production

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["node", "server.js"] 