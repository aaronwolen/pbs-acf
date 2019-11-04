#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess

from snakemake.utils import read_job_properties

parser=argparse.ArgumentParser(add_help=False)
parser.add_argument("--depend", help="Space separated list of ids for jobs this job should depend on.")
parser.add_argument("-a", help="Declare the time when the job becomes eligible for execution.")
parser.add_argument("-A", help="Define the account string.")
parser.add_argument("-c", help="Checkpoint options.")
parser.add_argument("-C", help="Directive prefix in script file.")
parser.add_argument("-d", help="Working directory to be used (default: $HOME for TORQUE; submission directory for SLURM).")
parser.add_argument("-e", help="standard error path.")
parser.add_argument("-E", help="Moab Environment variables. Only works if TORQUE or SLURM is the underlying resource manager.")
parser.add_argument("-h", help="Apply user hold at submission time",action="store_true")
parser.add_argument("-j", help="Merge standard error and standard out. (oe|n). Default is n.")
parser.add_argument("-k", help="Defines which of output and error streams will be retained. (e|o|eo|oe|n). Default is n.")
parser.add_argument("-l", help="Resource list.")
parser.add_argument("-m", help="Mail options.")
parser.add_argument("-M", help="Mail users.")
parser.add_argument("-N", help="Name for the job.")
parser.add_argument("-o", help="standard output path.")
parser.add_argument("-p", help="Set job priority.")
parser.add_argument("-q", help="Set destination queue.")
parser.add_argument("-r", help="Declare whether a job is rerunable.", action="store_true")
parser.add_argument("-S", help="Shell path.")
parser.add_argument("-u", help="Set user name for job.")
parser.add_argument("-v", help="Environment variables to export to the job.")
parser.add_argument("-V", help="Export all environment variables.",action="store_true")
parser.add_argument("-W", help="Additional attributes.")
parser.add_argument("-z", help="Job's identifier will not be printed to stdout upon submission.", action="store_true")
parser.add_argument("--help", help="Display help message.",action="store_true")

parser.add_argument("positional",action="append",nargs="?")
args = parser.parse_args()

if args.help :
    parser.print_help()
    sys.exit(0)

jobscript = sys.argv[-1]

job_properties = read_job_properties(jobscript)

atime=""
acc_string=""
chkpt=""
pref=""
dd=""
se=""
me=""
hold=""
j=""
k=""
resource=""
mail=""
mailuser=""
jname=""
so=""
priority=""
q=""
r=""
sp=""
user=""
ev=""
eall=""
add=""
quiet=""
depend=""
resourceparams=""
extras=""


if args.depend:
	for m in args.depend.split(" "):
		depend = depend + ":" + m
if depend:
	depend = " -W \"depend=afterok" + depend + "\""

if args.positional:
	for m in args.positional:
		extras = extras + " " + m

if args.a: atime = " -a " + args.a
if args.A: acc_string = " -A " + args.A
if args.c: chkpt = " -c " + args.c
if args.C: pref = " -C " + args.C
if args.d: dd = " -d " + args.d
if args.e: se = " -e " + args.e
if args.E: me = " -E " + args.E
if args.h: hold = " -h"
if args.j: j = " -j " + args.j
if args.k: k = " -k " + args.k
if args.l: resource = " -l " + args.l
if args.m: mail = " -m " + args.m
if args.M: mailuser = " -M " + args.M
if args.N: jname = " -N " + args.N
if args.o: so = " -o " + args.o
if args.p: priority = " -p " + args.p
if args.q: q = " -q " + args.q
if args.r: r = " -r"
if args.S: sp = " -S " + args.S
if args.u: user = " -u " + args.u
if args.v: ev = " -v " + args.v
if args.V: eall = " -V"
if args.W: add= " -W \"" + args.W + "\""
if args.z: quiet = " -z"

nodes=""
ppn=""
mem=""
walltime=""

if "threads" in job_properties:
    ppn = "ppn=" + str(job_properties["threads"])

if "resources" in job_properties:
    resource = "" # job-specific resources override general resource list
    resources = job_properties["resources"]
    if "nodes" in resources: nodes="nodes=" + str(resources["nodes"])
    if ppn and not nodes: nodes="nodes=1"
    if "mem_mb" in resources:
        if nodes:
            mem="pmem=" + str(resources["mem"]) + "mb"
        else:
            mem="mem=" + str(resources["mem"]) + "mb"
    if "walltime_min" in resources: walltime="walltime=" + str(60*resources["walltime"])

if nodes or ppn or mem or walltime: resourceparams = " -l \""
if nodes: resourceparams = resourceparams + nodes
if nodes and ppn: resourceparams = resourceparams + ":" + ppn
if nodes and mem: resourceparams = resourceparams + ","
if mem: resourceparams = resourceparams + mem
if walltime and (nodes or mem): resourceparams = resourceparams + ","
if walltime: resourceparams = resourceparams + walltime
if nodes or mem or walltime: resourceparams = resourceparams + "\""

cmd = "msub {a}{A}{c}{C}{d}{e}{E}{h}{j}{k}{l}{m}{M}{N}{o}{p}{q}{r}{S}{u}{v}{V}{W}{z}{rp}{dep}{ex}".format(\
	a=atime,A=acc_string,c=chkpt,C=pref,d=dd,e=se,E=me,h=hold,j=j,k=k,l=resource,m=mail,M=mailuser,\
	N=jname,o=so,p=priority,q=q,r=r,S=sp,u=user,v=ev,V=eall,W=add,z=quiet,rp=resourceparams,dep=depend,ex=extras)

try:
    res = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE)
except subprocess.CalledProcessError as e:
    raise e

res = res.stdout.decode()
print(res.strip())
