#!/bin/bash

VERSION="1.0.3"

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 显示帮助信息
show_help() {
    echo -e "${YELLOW}使用方法:${NC}"
    echo -e "  $0 [选项]"
    echo
    echo -e "${YELLOW}选项:${NC}"
    echo -e "  ${GREEN}-b, --build${NC}     仅构建镜像"
    echo -e "  ${GREEN}-p, --push${NC}      构建并推送镜像到 Docker Hub"
    echo -e "  ${GREEN}-r, --registry${NC}  指定 Docker 仓库 (默认: liyuan123)"
    echo -e "  ${GREEN}-m, --mirror${NC}    使用国内镜像源加速构建"
    echo -e "  ${GREEN}-h, --help${NC}      显示此帮助信息"
    echo
    echo -e "${YELLOW}示例:${NC}"
    echo -e "  $0 --build                # 仅构建镜像"
    echo -e "  $0 --push                 # 构建并推送镜像"
    echo -e "  $0 --push --registry myregistry  # 构建并推送到指定仓库"
    echo -e "  $0 --build --mirror       # 使用国内镜像源加速构建"
}

# 默认值
REGISTRY="liyuan123"
BUILD_ONLY=false
PUSH=false
USE_MIRROR=false

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -b|--build)
            BUILD_ONLY=true
            shift
            ;;
        -p|--push)
            PUSH=true
            shift
            ;;
        -r|--registry)
            REGISTRY="$2"
            shift 2
            ;;
        -m|--mirror)
            USE_MIRROR=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}错误: 未知选项 $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# 如果没有指定操作，显示帮助
if [[ "$BUILD_ONLY" == "false" && "$PUSH" == "false" ]]; then
    show_help
    exit 1
fi

# 确保 Docker 已安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker 未安装${NC}"
    exit 1
fi

echo -e "${YELLOW}=== 构建和推送 Docker 镜像 ===${NC}"
echo -e "${GREEN}使用仓库:${NC} $REGISTRY"

# 构建后端镜像
echo -e "\n${YELLOW}=== 构建后端镜像 ===${NC}"

# 准备构建参数
BACKEND_BUILD_ARGS=""
if [ "$USE_MIRROR" = true ]; then
    echo -e "${GREEN}使用国内镜像源加速构建${NC}"
    BACKEND_BUILD_ARGS="--build-arg USE_MIRROR=true"
fi

docker build \
    --platform linux/amd64 \
    $BACKEND_BUILD_ARGS \
    -t ${REGISTRY}/portal-backend:${VERSION} \
    -f backend/Dockerfile \
    ./backend

if [ $? -ne 0 ]; then
    echo -e "${RED}后端镜像构建失败${NC}"
    exit 1
fi
echo -e "${GREEN}后端镜像构建成功${NC}"

# 构建前端镜像
echo -e "\n${YELLOW}=== 构建前端镜像 ===${NC}"

# 准备构建参数
FRONTEND_BUILD_ARGS=""
NPM_REGISTRY="https://registry.npmjs.org/"
if [ "$USE_MIRROR" = true ]; then
    echo -e "${GREEN}使用国内镜像源加速构建${NC}"
    NPM_REGISTRY="https://registry.npmmirror.com"
    FRONTEND_BUILD_ARGS="--build-arg NPM_REGISTRY=$NPM_REGISTRY"
fi

echo -e "${GREEN}使用 NPM 镜像源: ${NC}$NPM_REGISTRY"

docker build \
    --platform linux/amd64 \
    $FRONTEND_BUILD_ARGS \
    -t ${REGISTRY}/portal-frontend:${VERSION} \
    -f frontend/Dockerfile \
    ./frontend

if [ $? -ne 0 ]; then
    echo -e "${RED}前端镜像构建失败${NC}"
    exit 1
fi
echo -e "${GREEN}前端镜像构建成功${NC}"

# 如果需要推送镜像
if [ "$PUSH" = true ]; then
    echo -e "\n${YELLOW}=== 推送镜像到 Docker Hub ===${NC}"
    
    # 检查是否已登录 Docker Hub
    echo -e "${GREEN}检查 Docker Hub 登录状态...${NC}"
    if ! docker info | grep -q "Username"; then
        echo -e "${YELLOW}请登录 Docker Hub:${NC}"
        docker login
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}Docker Hub 登录失败${NC}"
            exit 1
        fi
    fi
    
    # 推送后端镜像
    echo -e "${GREEN}推送后端镜像...${NC}"
    docker push ${REGISTRY}/portal-backend:${VERSION}
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}后端镜像推送失败${NC}"
        exit 1
    fi
    
    # 推送前端镜像
    echo -e "${GREEN}推送前端镜像...${NC}"
    docker push ${REGISTRY}/portal-frontend:${VERSION}
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}前端镜像推送失败${NC}"
        exit 1
    fi
    
    echo -e "\n${GREEN}所有镜像已成功推送到 Docker Hub${NC}"
    echo -e "${YELLOW}后端镜像:${NC} ${REGISTRY}/portal-backend:${VERSION}"
    echo -e "${YELLOW}前端镜像:${NC} ${REGISTRY}/portal-frontend:${VERSION}"
fi

echo -e "\n${GREEN}操作完成!${NC}"

# 显示使用说明
echo -e "\n${YELLOW}=== 使用说明 ===${NC}"
if [ "$PUSH" = true ]; then
    echo -e "在 Ubuntu 服务器上运行:"
    echo -e "  1. 确保已安装 Docker 和 Docker Compose"
    echo -e "  2. 创建 docker-compose.deploy.yml 文件，使用以下镜像:"
    echo -e "     - ${REGISTRY}/portal-backend:${VERSION}"
    echo -e "     - ${REGISTRY}/portal-frontend:${VERSION}"
    echo -e "  3. 运行: docker-compose -f docker-compose.deploy.yml up -d"
else
    echo -e "镜像已构建完成，可以使用 docker-compose.yml 在本地运行:"
    echo -e "  docker-compose up -d"
fi
