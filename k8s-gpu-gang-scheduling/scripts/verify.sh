#!/usr/bin/env bash
set -euo pipefail
kubectl get nodes -o custom-columns='NAME:.metadata.name,GPUs:.status.allocatable.nvidia\.com/gpu'
kubectl get pods -n volcano-system
kubectl get pods -n kueue-system
kubectl get clusterqueue
kubectl get localqueue -A
kubectl get nodes -L accelerator
kubectl get workloads -A 2>/dev/null || true
kubectl get podgroups -A 2>/dev/null || true
