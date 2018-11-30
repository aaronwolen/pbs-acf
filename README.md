# Moab

This profile configures Snakemake to run on the commerical [Moab HPC Scheduler](http://www.adaptivecomputing.com/moab-hpc-basic-edition/). This
product can be configured to use multiple resource managers, including PBS/TORQUE (for supported managers, see
[here](http://docs.adaptivecomputing.com/mwm/7-2-9/Content/topics/resourceManagers/rmconfiguration.html#types)). This product is in use at
major companies and academic institutions, including my home institution.

Moab uses [`msub`](http://docs.adaptivecomputing.com/maui/commands/msub.php) as the main program to submit jobs,
and it uses [`showq`](http://docs.adaptivecomputing.com/maui/commands/showq.php),
[`checkjob`](http://docs.adaptivecomputing.com/maui/commands/checkjob.php) or
[`mdiag -j`](http://docs.adaptivecomputing.com/maui/commands/mdiag-jobs.php) to monitor jobs in progress.

This profile borrowed heavily from the PBS/TORQUE profile found [here](https://github.com/Snakemake-Profiles/pbs-torque).

**NOTE**: I am a neophyte when it comes to this topic, so please provide feedback on ways this can be improved!

## Setup

### Deploy profile

To deploy this profile, run

    mkdir -p ~/.config/snakemake
    cd ~/.config/snakemake
    cookiecutter https://github.com/warrenmcg/moab.git

Then, you can run Snakemake with

    snakemake --profile moab ...


### Parameters

The following resources are supported by on a per-rule basis:

+ **node** - set the node resource request (integer; defaults to 1).
+ **mem_mb** - set the memory resource request (integer in MB units).
+ **walltime_min** - set the walltime resource (integer in minutes).

**Note**: The [`threads`](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#threads)
directive maps to the "ppn" resource request.
