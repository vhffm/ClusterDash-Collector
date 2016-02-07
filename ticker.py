"""
Read, Parse, Post Stats to InfluxDB.
"""

import Common.slurm as slurm
import Common.sensors as sensors
import Common.influx as influx
import Common.derived as derived
import Common.nvidia as nvidia
import time


# #############################################################################
# Load Data from Slurm
# #############################################################################

# Number of Nodes Down
number_of_nodes_down = slurm.get_number_of_nodes_down()

# CPU Allocations
cpu_allocations = slurm.get_cpu_allocations()

# Jobs per Partition per State
njobs_by_partition_and_state = \
    slurm.get_number_of_jobs_by_partition_and_state()

# #############################################################################
# Compute Derived Quantities
# #############################################################################
utilization_by_partition = \
    derived.compute_utilization(number_of_nodes_down, \
                                njobs_by_partition_and_state, \
                                cpu_allocations)

# #############################################################################
# Load Data from Netatmo
# #############################################################################
temperature, netatmo_epoch = sensors.get_netatmo_temperature()

# #############################################################################
# Build Data Post
# NB: For InfluxDB >=0.9.3, integer data points require a trailing i.
#     For example, ncpus_allocated,parititon=cpu value=5i
# #############################################################################
epoch = int(time.time())
lines = []

# CPU Allocations
for partition, ncpus_allocated in cpu_allocations.iteritems():
    line = "ncpus_allocated,partition=%s value=%ii %i" % \
        (partition, ncpus_allocated, epoch)
    lines.append(line)

# Number of Nodes Down
for partition, nnodes_down in number_of_nodes_down.iteritems():
    line = "nodes,state=down,partition=%s value=%ii %i" % \
        (partition, nnodes_down, epoch)
    lines.append(line)

# Jobs per Partition per State
for partition, njobs_by_state in njobs_by_partition_and_state.iteritems():
    for state, njobs in njobs_by_state.iteritems():
        line = "jobs,state=%s,partition=%s value=%ii %i" % \
            (state, partition, njobs, epoch)
        lines.append(line)

# Cluster Utilization
for partition, utilization in utilization_by_partition.iteritems():
    line = "utilization,partition=%s value=%.6f %i" % \
        (partition, utilization, epoch)
    lines.append(line)

# Netatmo
line = "room_temperature,room=zbox_room value=%.2f %i" % \
    (temperature, netatmo_epoch)
lines.append(line)

# GPU Stats
for gpu_node in [ 'vesta1', 'vesta2' ]:
    df, gpu_epoch, sucess = nvidia.read_gpu_stats(node=gpu_node)
    for irow, [ index, row ] in enumerate(df.iterrows()):
        line_01 = "gpu_temperature,node=%s,uuid=%s value=%.2f %i" % \
            (row.node, row.uuid, row.gpu_temperature, gpu_epoch)
        line_02 = "gpu_power_draw,node=%s,uuid=%s value=%.2f %i" % \
            (row.node, row.uuid, row.power_draw, gpu_epoch)
        line_03 = "gpu_utilization,node=%s,uuid=%s value=%.2f %i" % \
            (row.node, row.uuid, row.gpu_utilization, gpu_epoch)
        line_04 = "gpu_memory_utilization,node=%s,uuid=%s value=%.2f %i" % \
            (row.node, row.uuid, row.memory_utilization, gpu_epoch)
        lines.append(line_01)
        lines.append(line_02)
        lines.append(line_03)
        lines.append(line_04)

# Join
data = "\n".join(lines)

# #############################################################################
# Post Data
# #############################################################################
influx.post_data(data)
