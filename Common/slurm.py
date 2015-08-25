"""
Slurm Polling Functions.
"""

import subprocess as sp


def get_number_of_nodes_down():
    """
    Get Down/Drained Nodes for Partitions.
    
    Slurm Command:
    sinfo --format=%o --list-reasons --noheader --partition=zbox

    @return: number_of_nodes_down [Integer]
    """

    number_of_nodes_down = {}
    partitions = [ 'zbox', 'serial', 'debug', 'tasna', 'vesta' ]
    for partition in partitions:
        cmd = [ 'sinfo', '--format=%o', \
                '--list-reasons', '--noheader', \
                "--partition=%s" % partition ]
        p = sp.Popen(cmd, stdout=sp.PIPE)
        p.wait()
        data, _ = p.communicate()
        if len(data) == 0:
            count = 0
        else:
            count = len(data.strip().split('\n'))
        number_of_nodes_down["%s" % partition] = count

    # Aggregate CPU Counts
    cpu_partitions = [ 'zbox', 'serial', 'debug' ]
    running_sum = 0
    for partition in cpu_partitions:
        running_sum += number_of_nodes_down["%s" % partition]
    number_of_nodes_down['cpu'] = running_sum

    # Aggregate GPU Counts
    gpu_partitions = [ 'tasna', 'vesta' ]
    running_sum = 0
    for partition in gpu_partitions:
        running_sum += number_of_nodes_down["%s" % partition]
    number_of_nodes_down['gpu'] = running_sum

    # Aggregate All Counts
    running_sum = 0
    for partition in partitions:
        running_sum += number_of_nodes_down["%s" % partition]
    number_of_nodes_down['all'] = running_sum

    # Fake Data
    # number_of_nodes_down = \
    #     {'cpu': 15,
    #      'debug': 3,
    #      'gpu': 1,
    #      'serial': 2,
    #      'tasna': 1,
    #      'vesta': 0,
    #      'zbox': 10}

    return number_of_nodes_down


def get_cpu_allocations():
    """
    Get CPU Allocations per Partition. Also return sum over all CPU partitions.

    Slurm Command:
    squeue --format=%C --partition zbox --noheader

    @return: number_of_allocated_cpus [Dict {'partition': ncpus}]
    """

    # Old, Really Slow Command:
    # sacct --format=partition,alloccpus --allocations \
    #       --state=RUNNING --allusers --noheader --parsable2

    partitions = [ 'zbox', 'serial', 'debug' ]
    number_of_allocated_cpus = {}
    for partition in partitions:
        cmd = [ 'squeue', \
                '--format=%C', '--noheader', "--partition=%s" % partition ]
        p = sp.Popen(cmd, stdout=sp.PIPE)
        p.wait()
        data, _ = p.communicate()
        running_sum = 0
        if len(data) > 0:
            for line in data.strip().split('\n'):
                running_sum += int(line)
        number_of_allocated_cpus["%s" % partition] = running_sum
    number_of_allocated_cpus['cpu'] = sum(number_of_allocated_cpus.values())

    # Fake Data
    # number_of_allocated_cpus = { 'zbox': 768, 'serial': 12, 'debug': 198 }

    # Return
    return number_of_allocated_cpus


def get_number_of_jobs_by_partition_and_state():
    """
    Get Number of Jobs by State and Partition.

    Slurm Command:
    squeue --noheader --format=%T:%P --partition=zbox --state=pending

    @return number_of_jobs_by_partition - [Dict {'zbox': {'running': 1}}
    """

    partitions = [ 'zbox', 'serial', 'debug', 'tasna', 'vesta' ]
    states = [ 'pending', 'running' ]

    # Get Raw Data
    number_of_jobs_by_partition = {}
    for partition in partitions:
        number_of_jobs_by_state = {}
        for state in states:
            cmd = [ 'squeue', '--noheader', '--format=%T:%P', \
                    "--partition=%s" % partition, \
                    "--state=%s" % state ]
            p = sp.Popen(cmd, stdout=sp.PIPE)
            p.wait()
            data, _ = p.communicate()
            if len(data) == 0:
                count = 0
            else:
                count = len(data.strip().split('\n'))
            number_of_jobs_by_state["%s" % state] = count
        number_of_jobs_by_partition["%s" % partition] = \
                number_of_jobs_by_state

    # Aggregate CPU Counts
    cpu_partitions = [ 'zbox', 'serial', 'debug' ]
    number_of_jobs_by_state = {}
    for state in states:
        total = 0
        for partition in cpu_partitions:
            total += number_of_jobs_by_partition[partition][state]
        number_of_jobs_by_state[state] = total
    number_of_jobs_by_partition['cpu'] = number_of_jobs_by_state

    # Aggregate GPU Counts
    gpu_partitions = [ 'vesta', 'tasna' ]
    number_of_jobs_by_state = {}
    for state in states:
        total = 0
        for partition in gpu_partitions:
            total += number_of_jobs_by_partition[partition][state]
        number_of_jobs_by_state[state] = total
    number_of_jobs_by_partition['gpu'] = number_of_jobs_by_state

    # Aggregate All Counts
    number_of_jobs_by_state = {}
    for state in states:
        total = 0
        for partition in partitions:
            total += number_of_jobs_by_partition[partition][state]
        number_of_jobs_by_state[state] = total
    number_of_jobs_by_partition['all'] = number_of_jobs_by_state

    # Fake Data
    # number_of_jobs_by_partition = \
    #     {'cpu': {'pending': 0, 'running': 465},
    #      'debug': {'pending': 0, 'running': 0},
    #      'gpu': {'pending': 0, 'running': 62},
    #      'serial': {'pending': 0, 'running': 457},
    #      'tasna': {'pending': 0, 'running': 31},
    #      'vesta': {'pending': 0, 'running': 31},
    #      'zbox': {'pending': 0, 'running': 8}}

    return number_of_jobs_by_partition
