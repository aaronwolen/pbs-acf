# ACF Snakemake Profile

This repo contains a [Snakemake profile][1] for executing workflows on the [Advanced Computing Facility (ACF)][2] HPC, hosted by Oak Ridge National Laboratory. The PBS system used by ACF is [Torque][3]. However, job scheduling is handled by [Moab][4].

This profile is an amalgmation of the original [pbs-torque][5] profile and @warrenmcg's [moab fork][6].

**NOTE:** This profile is a work in progress, YMMV. Please let me know if you have any suggestions for improving it.

## Setup

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