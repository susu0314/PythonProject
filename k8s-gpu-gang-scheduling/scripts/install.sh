#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_DIR="${SCRIPT_DIR}/../deploy"
kubectl apply -f "${DEPLOY_DIR}/00-namespaces.yaml"
kubectl apply -f "${DEPLOY_DIR}/01-nvidia-device-plugin.yaml"
kubectl rollout status daemonset/nvidia-device-plugin-daemonset -n kube-system --timeout=180s
helm repo add volcano-sh https://volcano-sh.github.io/helm-charts >/dev/null 2>&1 || true
helm repo update
if ! helm status volcano -n volcano-system >/dev/null 2>&1; then
  helm install volcano volcano-sh/volcano -n volcano-system --create-namespace --wait --timeout 10m
fi
if ! helm status kueue -n kueue-system >/dev/null 2>&1; then
  helm install kueue oci://registry.k8s.io/kueue/charts/kueue -n kueue-system --create-namespace --wait --timeout 10m
fi
kubectl apply -f "${DEPLOY_DIR}/02-kueue-resources.yaml"
echo "安装完成。运行 scripts/verify.sh。"
