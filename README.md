# Dashboard Data Collection Tools

## Overview

This is a collection of Python scripts to poll cluster scheduling data from the [Slurm Workload Manager](http://slurm.schedmd.com/), temperature data from a [Netatmo](http://netatmo.com) device, and then upload it to an instance of [InfluxDB](https://influxdb.com/).

## Examples

For example, the [zBox4 Dashboard](https://labs.cheleb.net/grafana/dashboard/db/zbox) uses these scripts.

### Cluster Overview

![Grafana Cluster Overview](/Screenshots/grafana_zbox.png?raw=true)

### GPU Nodes Overview

![Grafana GPU Node Overview](/Screenshots/grafana_zbox_gpu.png?raw=true)

## Usage

- Execute the scripts on a host that can access Slurm data.
- Put your InfluxDB access data in the *userpass_influx* file.
- Put your Netatmo access data in the *userpass_netatmo* file.

If you do not want to use the Netatmo part, simply comment out the code.

## Contact

Questions, comments, rants should be sent to [volker@cheleb.net](mailto:volker@cheleb.net).
