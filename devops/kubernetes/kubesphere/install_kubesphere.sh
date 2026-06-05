#!/bin/bash

# 如果无法访问 charts.kubesphere.io, 可将 charts.kubesphere.io 替换为 charts.kubesphere.com.cn
nohup helm upgrade \
    --install \
    -n kubesphere-system \
    --create-namespace ks-core https://charts.kubesphere.io/main/ks-core-1.1.4.tgz \
    --debug \
    --wait \
    --set global.imageRegistry=swr.cn-southwest-2.myhuaweicloud.com/ks \
    --set extension.imageRegistry=swr.cn-southwest-2.myhuaweicloud.com/ks \
    > install_kubesphere.log 2>&1 &
