# ACF Snakemake Profile

This repo contains a [Snakemake profile][1] for executing workflows on the [Advanced Computing Facility (ACF)][2] HPC, hosted by Oak Ridge National Laboratory. The profile is an amalgmation of the original [pbs-torque][5] profile and @warrenmcg's [moab fork][6] to accomodate the ACF, which uses both [Torque][3] and [Moab][4] (for job scheduling). 

**NOTE:** This is very much a work in progress as I work out the optimal approach for using conda environments and Snakemake on the ACF, so YMMV. That said, please let me know if you have any suggestions for improving it.

## Details

A few notes about changes I've made.

### `config.yaml`

* Passes the following environment variables to `qsub`'s `variable_list` argument: `PATH`, `LOADEDMODULES`, and `_LMFILES_`. This enables modules loaded in your interactive session to be available within PBS jobs.

### `pbs-status.py`

* `qstat`'s output is now converted to a python `dict` instead of attempting XML parsing. 

### Template variables

- **profile_name**: Specifies the [account][acf-job-opts] to which the job will be charged. If omitted `qsub` throws a warning and uses the default profile associated with your ACF account. This is passed to `qsub -A`.

## Setup

In order to use `conda` with this profile you need to activate the module and initialize it by adding the following to `.bashrc`:

    module load python3/conda3-4.4.0
    . /sw/acf/anaconda3/4.4.0/centos7.3_gnu6.3.0/   anaconda3-4.4.0/etc/profile.d/conda.sh

### Deploy profile

To deploy this profile, run

    mkdir -p ~/.config/snakemake
    cd ~/.config/snakemake
    cookiecutter https://github.com/aaronwolen/pbs-acf.git

Then, you can run Snakemake with

    snakemake --profile pbs-acf ...


### Parameters

The following resources are supported on a per-rule basis:

- **node** - set the node resource request (integer; defaults to 1).
- **mem_mb** - set the memory resource request (integer in MB units).
- **walltime_min** - set the walltime resource (integer in minutes).

**Note**: The [`threads`](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#threads)
directive maps to the "ppn" resource request.

<!-- links -->
[1]: https://snakemake.readthedocs.io/en/stable/executable.html#profiles
[2]: https://www.jics.utk.edu/acf
[3]: https://www.adaptivecomputing.com/products/torque/
[4]: https://www.adaptivecomputing.com/moab-hpc-basic-edition/
[5]: https://github.com/Snakemake-Profiles/pbs-torque
[6]: https://github.com/warrenmcg/moab
[acf-job-opts]: https://www.nics.utk.edu/computing-resources/acf/running-jobs#options