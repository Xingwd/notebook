# 欺诈检测示例

https://nightlies.apache.org/flink/flink-docs-release-1.16/zh/docs/try-flink/datastream/

## 启动

Per-job Cluster Mode

```shell
/home/xingweidong/flink/flink-1.15.1/bin/flink run frauddetection-0.1.jar

/home/xingweidong/flink/flink-1.15.1/bin/flink run -t yarn-per-job frauddetection-0.1.jar

/home/xingweidong/flink/flink-1.15.1/bin/flink run -t yarn-per-job --detached frauddetection-0.1.jar
```
