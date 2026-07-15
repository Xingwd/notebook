# Nginx Docker Compose 示例

## 目录结构

```
nginx/
├── compose.yml                 # 多端口
└── nginx.conf                  # 自定义 Nginx 配置
```

## 快速启动

```bash
cd devops/nginx
docker compose up -d
```

访问: <http://localhost>

## 常用命令

```bash
# 启动
docker compose up -d

# 停止
docker compose down

# 查看日志
docker compose logs -f

# 重载配置（不重启容器）
docker compose exec nginx nginx -s reload
```

## 常见示例

### 1. 反向代理到后端服务

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro

  app:
    image: httpd:latest
    ports:
      - "8010:80"
```

在 `nginx.conf` 中：

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://app:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. 负载均衡

```nginx
upstream app_servers {
    server app1:80;
    server app2:80;
}

server {
    listen 80;
    location / {
        proxy_pass http://app_servers;
    }
}
```

### 3. HTTPS 配置

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    location / {
        root /usr/share/nginx/html;
    }
}
```

#### 生成自签名证书

自签名证书，只用于测试环境。

假设你的宿主机 IP 是 10.1.24.26。

```shell
mkdir certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout certs/daytona.key \
    -out certs/daytona.crt \
    -subj "/CN=10.1.24.26" \
    -addext "subjectAltName=IP:10.1.24.26"
```

使用时，把 10.1.24.26 换成你的实际 IP。

### 4. 静态资源缓存

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### 5. Gzip 压缩

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```
