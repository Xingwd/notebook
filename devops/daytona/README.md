# Daytona部署

[Daytona](https://github.com/daytonaio/daytona) 项目提供的docker compose部署方式，API服务（<http://localhost:3000>）只能本地访问，如果想要从外部访问，必须使用https协议。>

本部署方式，基于 **自签名证书 + Nginx反向代理**，实现将服务部署到远程服务器，从服务器外部访问服务，可用于搭建长期运行的开发/测试环境。

## 使用方法

假设你的宿主机 IP 是 10.1.24.26。

1、生成自签名证书

把 10.1.24.26 换成你的实际 IP。

```shell
mkdir certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout certs/daytona.key \
    -out certs/daytona.crt \
    -subj "/CN=10.1.24.26" \
    -addext "subjectAltName=IP:10.1.24.26"
```

2、修改配置

将 `docker-compose.override.yaml` 和 `dex/config.yaml` 的中 10.1.24.26 换成你的实际 IP。
