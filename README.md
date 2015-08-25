# Dashboard Data Collection Tools

## Overview

This is a collection of Python scripts to poll cluster scheduling data from the [Slurm Workload Manager](http://slurm.schedmd.com/) and a [Netatmo](http://netatmo.com) device, and then upload it to on instance of [InfluxDB](https://influxdb.com/).

For example, the [zBox4 Dashboard](https://labs.cheleb.net/grafana/dashboard/db/zbox) uses these scripts.

## Requirements

- Execute the scripts on a host that can access Slurm data.
- Put your InfluxDB access data in the *userpass_influx* file.
- Put your Netatmo access data in the *userpass_netatmo* file.

If you do not want to use the Netatmo part, simply comment out the code.

## Contact

Questions, comments, rants should be sent to [volker@cheleb.net](mailto:volker@cheleb.net).
