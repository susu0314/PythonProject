from pathlib import Path
import yaml
DEPLOY=Path(__file__).parent.parent/"deploy"
def load(path): return [x for x in yaml.safe_load_all(path.read_text(encoding="utf-8")) if x]
def test_kueue_gpu_quota():
    docs=load(DEPLOY/"02-kueue-resources.yaml"); cq=[x for x in docs if x["kind"]=="ClusterQueue"][0]
    resources=cq["spec"]["resourceGroups"][0]["flavors"][0]["resources"]
    assert any(x["name"]=="nvidia.com/gpu" for x in resources)
def test_gang_job():
    job=load(DEPLOY/"samples/kueue-volcano-gang-job.yaml")[0]
    assert job["metadata"]["labels"]["kueue.x-k8s.io/queue-name"]=="gpu-queue"
    assert job["metadata"]["annotations"]["scheduling.volcano.sh/group-min-member"]=="4"
    assert job["spec"]["parallelism"]==4
    assert job["spec"]["template"]["spec"]["schedulerName"]=="volcano"
def test_gpu_request():
    job=load(DEPLOY/"samples/kueue-volcano-gang-job.yaml")[0]
    assert job["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"]["nvidia.com/gpu"]=="1"
def test_inference_not_gang():
    d=load(DEPLOY/"samples/inference-deployment.yaml")[0]
    assert d["spec"]["template"]["spec"].get("schedulerName")!="volcano"
