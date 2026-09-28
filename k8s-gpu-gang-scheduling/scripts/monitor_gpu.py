#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,subprocess,sys,time
from datetime import datetime,timezone
from statistics import mean
def run(cmd):
    try: return subprocess.check_output(cmd,text=True,stderr=subprocess.STDOUT)
    except (FileNotFoundError,subprocess.CalledProcessError) as exc:
        print(f"warning: {' '.join(cmd)}: {exc}",file=sys.stderr); return ""
def gpu_util():
    out=run(["nvidia-smi","--query-gpu=utilization.gpu","--format=csv,noheader,nounits"])
    if not out: return None
    try: values=[float(x) for x in out.splitlines() if x.strip()]
    except ValueError: return None
    return mean(values) if values else None
def pods():
    out=run(["kubectl","get","pods","-A","-o","json"])
    if not out: return {}
    data=json.loads(out); result={}
    for item in data.get("items",[]):
        phase=item.get("status",{}).get("phase","Unknown"); result[phase]=result.get(phase,0)+1
    return result
def workloads():
    out=run(["kubectl","get","workloads","-A","-o","json"])
    if not out: return {}
    result={}
    for item in json.loads(out).get("items",[]):
        for c in item.get("status",{}).get("conditions",[]):
            if c.get("type")=="Admitted":
                s=c.get("status","Unknown"); result[s]=result.get(s,0)+1
    return result
def snapshot():
    return {"ts":datetime.now(timezone.utc).isoformat(),"gpu_utilization_pct":gpu_util(),"pod_phases":pods(),"workload_admitted":workloads()}
def main():
    p=argparse.ArgumentParser(); p.add_argument("--interval",type=int,default=30); p.add_argument("--count",type=int,default=1); p.add_argument("--json",action="store_true"); a=p.parse_args()
    i=0
    while a.count==0 or i<a.count:
        data=snapshot()
        if a.json: print(json.dumps(data,ensure_ascii=False))
        else:
            gpu=data["gpu_utilization_pct"]; print(f"[{data['ts']}] GPU util = {gpu:.1f}%" if gpu is not None else f"[{data['ts']}] GPU util = N/A")
            print("  Pod phases:",data["pod_phases"]); print("  Workload admitted:",data["workload_admitted"])
        i+=1
        if a.count==0 or i<a.count: time.sleep(a.interval)
if __name__=="__main__": main()
