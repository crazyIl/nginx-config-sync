## 项目概述

本项目是一个使用 Flask 构建的 API，用于同步和重新加载 Nginx 配置。通过 Docker 容器化部署，实现了简单的 API 认证和 Nginx
配置的自动更新。

## 项目配置

### 环境变量

| 变量名     | 描述       | 默认值                  |
|---------|----------|----------------------|
| API_KEY | API 认证密钥 | your-default-api-key |

### 挂载目录

| 目录                   | 描述         |
|----------------------|------------|
| /opt/nginx-config    | Nginx 配置目录 |
| /var/run/docker.sock | Docker 套接字 |

## 部署

### nginx-config-sync docker 部署

使用以下命令运行 Docker 容器，确保已经挂载了必要的卷和设置了环境变量。

```bash
docker run --name nginx-config-sync \
-v /opt/nginx-config:/opt/nginx-config \
-v /var/run/docker.sock:/var/run/docker.sock \
-p 15000:5000 \
-e API_KEY=your-default-api-key \
-d crazyl/nginx-config-sync:latest
```

## API 使用

### 同步 Nginx 配置

- **请求类型**: POST
- **端口**: 15000
- **路径**: `/sync`
- **Headers**:
    - `X-API-Key`: `your-default-api-key` (示例 API Key)

#### curl 示例

```bash
curl -X POST http://localhost:15000/sync -H "X-API-Key: your-default-api-key"
```
