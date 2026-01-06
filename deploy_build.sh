#!/bin/bash
set -e

echo "🚀 开始构建 Docker 镜像 (Target Platform: linux/amd64)..."

# 1. Build Backend
echo "📦 Building Backend..."
docker build --platform linux/amd64 -t woody-backend:latest -f backend/Dockerfile .

# 2. Build Frontend
echo "📦 Building Frontend..."
docker build --platform linux/amd64 -t woody-frontend:latest -f frontend/Dockerfile .

# 3. Save Images
echo "💾 Saving images to woody-app.tar..."
docker save -o woody-app.tar woody-backend:latest woody-frontend:latest

echo "✅ 构建完成！"
