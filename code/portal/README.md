## 构建Ec2所在的Role
1. principle : ec2.amazon.com
2. permission : 参考ec2_policy.json (需要修改一些变量)

## 打开Ec2 所在的security group
1. 打开80端口


## 设置环境变量
```
cp .env.example .env
# 修改.env
# 修改对应的docker-compose.yml
```

## 启动docker (直接使用docker.io中的image)
```
sudo docker compose up -d
```

## 重新构建docker images(optional)
```
# 构建然后推送
./build_and_push.sh --push

# 直接推送
docker push liyuan123/portal-backend:latest
docker push liyuan123/portal-frontend:latest
```

## 本地运行前端和后端服务器(optional)
```
cd backend & pip install -r requirements.txt
./start_servers.sh
```