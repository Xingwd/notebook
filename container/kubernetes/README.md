# Kubernetes Python客户端

参考资料：

- <https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/access-cluster-api/>
- <https://kubernetes.io/zh-cn/docs/concepts/security/service-accounts/>
- <https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/service-accounts-admin/>
- <https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/rbac/>
- <https://kubernetes.io/zh-cn/docs/reference/using-api/api-concepts/>
- <https://kubernetes.io/zh-cn/docs/reference/kubernetes-api/>
- <https://kubernetes.io/zh-cn/docs/reference/kubectl/generated/kubectl_create/kubectl_create_token/>
- <https://kubernetes.io/zh-cn/docs/concepts/configuration/secret/>
- <https://github.com/kubernetes-client/python/blob/master/examples/>

## 准备工作

创建`Role`和`ServiceAccount`，以及`ServiceAccount`的`Token`，用于访问Kubernetes。

### 创建Role

下面提供一个示例，具体使用时，根据需要分配权限。

#### 方式一：使用Yaml文件

编写`pod-reader-role.yaml`文件：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # "" 代表核心api组
  resources: ["pods"] # 资源列表
  verbs: ["get", "watch", "list"] # 权限
```

`apiGroups`、`resources`和`verbs`的信息可参考：

- [API 组](https://kubernetes.io/zh-cn/docs/reference/using-api/#api-groups)
- [Kubernetes API 概念](https://kubernetes.io/zh-cn/docs/reference/using-api/api-concepts/)
- [Kubernetes API](https://kubernetes.io/zh-cn/docs/reference/kubernetes-api/)

执行命令：

```shell
kubectl apply -f pod-reader-role.yaml
```

#### 方式二：使用kubectl create命令

```shell
kubectl create role pod-reader -n default --verb=get --verb=list --verb=watch --resource=pods
```

### 创建ServiceAccount

#### 方式一：使用Yaml文件

编写`xwd-serviceaccount.yaml`文件：

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: xwd
  namespace: default
```

执行命令：

```shell
kubectl apply -f xwd-serviceaccount.yaml
```

#### 方式二：使用kubectl create命令

```shell
kubectl create serviceaccount xwd -n default
```

### 绑定ServiceAccount和Role

#### 方式一：使用Yaml文件

编写`xwd-pod-reader-binding.yaml`文件：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
# 此角色绑定允许 "sa-reader" 读取 "default" 名字空间中的 Pod
# 你需要在该名字空间中有一个名为 “pod-reader” 的 Role
kind: RoleBinding
metadata:
  name: xwd-pod-reader-binding
  namespace: default
subjects:
# 你可以指定不止一个“subject（主体）”
- kind: User
  name: xwd # "name" 是区分大小写的
  apiGroup: rbac.authorization.k8s.io
roleRef:
  # "roleRef" 指定与某 Role 或 ClusterRole 的绑定关系
  kind: Role        # 此字段必须是 Role 或 ClusterRole
  name: pod-reader  # 此字段必须与你要绑定的 Role 或 ClusterRole 的名称匹配
  apiGroup: rbac.authorization.k8s.io
```

执行命令：

```shell
kubectl apply -f xwd-pod-reader-binding.yaml
```

#### 方式二：使用kubectl create命令

```shell
kubectl create rolebinding xwd-pod-reader-binding --role=pod-reader --user=xwd --namespace=default
```

### 创建ServiceAccount Token

> 当`Token`用于外部服务时，可以设置较长的有效期。

```shell
kubectl create token xwd -n default --duration 867240h
```

## 笔记说明

- [dynamic_client.ipynb](dynamic_client.ipynb): 动态客户端，更灵活，支持Kubenetes标准对象和自定义对象。
- [remote_cluster.ipynb](remote_cluster.ipynb): 通过ServiceAccount Token连接Kubernetes。
- [out_of_cluster_config.ipynb](out_of_cluster_config.ipynb): 通过kubeconfig文件连接Kubernetes。
