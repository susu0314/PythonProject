# k8s-gpu-gang-scheduling

Kubernetes GPU 批任务调度参考项目：Kueue 负责配额与 Workload 准入，Volcano 负责 Gang Scheduling。

两层通过标准 Kubernetes Job 衔接：Kueue 决定 Job 何时获得配额并启动，Volcano 决定其 Pod 是否满足 Gang 条件。

## 前置条件
- Kubernetes 集群
- Helm 3、kubectl
- NVIDIA GPU 节点及可用驱动/容器运行时
- GPU 节点存在 accelerator=nvidia 标签
- 节点可见 nvidia.com/gpu

## 安装
运行 scripts/install.sh，然后运行 scripts/verify.sh。

## GPU 节点
kubectl label node <gpu-node> accelerator=nvidia --overwrite
kubectl get nodes -L accelerator

## Gang Job
kubectl apply -f deploy/samples/kueue-volcano-gang-job.yaml
kubectl get workloads -n ml-training
kubectl get jobs -n ml-training
kubectl get podgroup -n ml-training

该 Job 是标准 batch/v1 Job：Kueue 通过 queue-name label 管理它，Job Pod 使用 Volcano scheduler，并通过 group-min-member 指定成组成员数。

## 单卡与推理
单卡任务使用 deploy/samples/single-gpu-job.yaml；在线推理使用 deploy/samples/inference-deployment.yaml。

## 监控
python scripts/monitor_gpu.py --count 5 --interval 10

这是轻量巡检器，不替代 Prometheus/DCGM Exporter。

## 测试
pip install -r requirements.txt
pytest -v

项目不写死 GPU 利用率提升数字，因为结果取决于 GPU 型号、负载、并发、模型和集群资源。