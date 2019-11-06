#!/usr/bin/env python3

import sys
import subprocess

jobid = sys.argv[1]

def make_qstat_dict (res):
    try:
        status = res.stdout.decode()
    except:
        print("res must be a 'subprocess.CompletedProcess'")

    # Every line but the first uses '=' to delimit key/value pairs
    status = status.replace('Id:', 'Id =')
    out = {k.strip():v.strip() for k,v in (row.split(' = ') for row in status.split('\n    '))}
    return out

try:
    res = subprocess.run("qstat -f {}".format(jobid), check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    job_status = make_qstat_dict(res)
    job_state = job_status.get('job_state')

    if job_state == "C":
        exit_status = job_status.get('exit_status')
        if exit_status == '0':
            print("success")
        else:
            print("failed")
    else:
        print("running")

except (subprocess.CalledProcessError, IndexError, KeyboardInterrupt) as e:
    print("failed")
