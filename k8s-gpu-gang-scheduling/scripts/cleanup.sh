#!/usr/bin/env bash
set -euo pipefail
kubectl delete -f "$(dirname "${BASH_SOURCE[0]}")/../deploy/samples/" --ignore-not-found=true
kubectl delete -f "$(dirname "${BASH_SOURCE[0]}")/../deploy/02-kueue-resources.yaml" --ignore-not-found=true
helm uninstall kueue -n kueue-system 2>/dev/null || true
helm uninstall volcano -n volcano-system 2>/dev/null || true
kubectl delete -f "$(dirname "${BASH_SOURCE[0]}")/../deploy/00-namespaces.yaml" --ignore-not-found=true
