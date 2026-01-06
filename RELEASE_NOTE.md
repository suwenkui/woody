# Release v1.0.0

🎉 这是一个里程碑版本，标志着 Woody API System 的首次正式发布！

## ✨ 主要功能

### 🔌 API 管理与调试
- **API 列表**: 浏览所有系统 API，支持查看详细信息。
- **在线调试**: 
  - 支持动态参数输入（Path, Query, Body）。
  - 实时调用后端接口并展示 JSON 响应结果。
  - 自动高亮显示调用结果。
- **系统预置 API**:
  - `GET /users/me`: 获取当前用户信息。
  - `GET /users/count`: 统计用户总数。

### 🛡️ 用户认证
- **注册/登录**: 完整的 JWT 认证流程。
- **权限控制**: 关键接口受 `OAuth2` 保护。

### 🐳 部署支持
- **Docker 化**: 提供完整的前后端 `Dockerfile`。
- **一键编排**: 提供 `docker-compose.yml` 实现服务编排。
- **自动化脚本**:
  - `deploy_build.sh`: 本地一键构建多架构镜像 (linux/amd64)。
  - `deploy_remote.py`: 基于 Python Paramiko 的远程自动化部署脚本。

## 📦 包含文件
- 源代码 (Source code)
- 部署脚本包 (Deploy Scripts)

## 🚀 快速开始

1. **克隆仓库**:
   ```bash
   git clone https://github.com/suwenkui/woody.git
   ```

2. **使用 Docker 启动**:
   ```bash
   docker-compose up -d
   ```

3. **访问系统**:
   打开浏览器访问 `http://localhost:8080` (或服务器 IP:8080)
