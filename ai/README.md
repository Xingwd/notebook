# AI

## Jupyter

文档：<https://docs.jupyter.org/en/latest/>

### Docker部署

```bash
cd deploy/jupyter
docker compose -f docker-compose.yml up -d
```

> 挂载为/home/jovyan/work的本地卷的目录的权限需要和执行上述命令的用户一致，否则在jupyter中创建目录或文件，会出现403权限问题。

参考文档：<https://jupyter-docker-stacks.readthedocs.io/en/latest/>

## 资料

### 神经网络

- <https://colah.github.io/posts/2015-08-Understanding-LSTMs/>
