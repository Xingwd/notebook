# Daytona

[Daytona](https://github.com/daytonaio/daytona) 项目提供的docker compose部署方式，API服务（<http://localhost:3000>）只能本地访问，如果想要从外部访问，必须使用https协议。

本部署方式，基于 **自签名证书 + Nginx反向代理**，实现将服务部署到远程服务器，从服务器外部访问服务，可用于搭建长期运行的开发/测试环境。

## 部署方法

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

3、初始化registry服务的默认镜像

```shell
# pull 镜像到宿主机
docker pull daytona/sandbox:0.8.0-slim

# 启动 daytona registry 服务
docker compose up registry -d

# push 镜像到 daytona registry 服务
docker tag daytonaio/sandbox:0.8.0-slim localhost:6000/daytona/sandbox:0.8.0-slim
docker push localhost:6000/daytona/sandbox:0.8.0-slim
```

其他镜像操作方法同理，比如需要使用 `daytona/sandbox:0.8.0` 镜像，按照上述步骤将镜像 push 到 daytona registry 服务，在 dashboard 页面创建 snapshot 时，镜像名指定为 `registry:6000/daytona/sandbox:0.8.0` 即可。

注意，从宿主机 push 镜像到 daytona registry 服务时，使用 `localhost:6000`，在 dashboard 中使用 daytona registry 服务镜像时，使用 `registry:6000`。

4、启动服务

```shell
docker compose up -d
```

## 问题记录

### 跳过 Docker Hub Registry 连接检查

官方提供的 docker-compose.yaml 文件中，将API服务的 `DEFAULT_SNAPSHOT` 设置为 `daytona/sandbox:0.5.0-slim`，这在无法访问 Docker Hub 的时候，无法成功创建默认的snaphost。

原因：

1. docker-compose 里的 DEFAULT_SNAPSHOT=daytonaio/sandbox:0.5.0-slim 会在 API 启动时触发 initializeDefaultSnapshot()（apps/api/src/app.service.ts:316）。
2. API 会创建一个 INSPECT_SNAPSHOT_IN_REGISTRY 类型的 job 发给 runner，并同步等待 30 秒（apps/api/src/sandbox/runner-adapter/runnerAdapter.v2.ts:491-503）。
3. Runner 收到 job 后，会调用 InspectImageInRegistry()（apps/runner/pkg/docker/image_info.go:54），通过 Docker 的 DistributionInspect + go-containerregistry 去向 registry 请求镜像的 digest 和 size。
4. 本地已经有镜像并不会跳过 registry 检查。如果 runner 访问不了 Docker Hub，或者 daytonaio/sandbox:0.5.0-slim 这个 tag 在 Docker Hub 上根本不存在，作业就会一直挂起，最终报错。

本部署已将 `DEFAULT_SNAPSHOT` 设置为 `registry:6000/daytona/sandbox:0.8.0-slim`，这样就会从 daytona registry 服务 pull 镜像，不会触发 Docker Hub Registry 连接检查。
