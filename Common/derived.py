"""
Derived Quantities.
"""


def compute_utilization(number_of_nodes_down, \
                        number_of_jobs_by_partition, \
                        number_of_allocated_cpus):
    """
    Compute Cluster Utilization.

    @todo: Less Hardcoding.

    @param: number_of_nodes_down - [Dict {'partition': 2, ...}]
    @param: number_of_jobs_by_partition - [Dict {'zbox': {'running': 1}, ...]
    @return: utilization - [Dict {'cpu': 0.3, 'tasna': 0.5, ..., 'gpu': 0.9}]
    """

    utilization = {}

    # CPU Utilization (Without Hyperthreading)
    # 2 Sockets per Server, 8 Cores per Socket, 192 Servers = 3072 Cores
    total_cpu_cores = 16*192
    cpu_nodes_down = number_of_nodes_down['cpu']*16
    allocated_cpu_cores = number_of_allocated_cpus['cpu']
    utilization['cpu'] = \
        float(allocated_cpu_cores) / float(total_cpu_cores - cpu_nodes_down)

    # Tasna Utilization
    # 4 GTX 590 Boards per Server, 2 GPUs per Board, 5 Servers = 40 Slots
    total_tasna_slots = 40 - number_of_nodes_down['tasna'] * 8
    allocated_tasna_slots = number_of_jobs_by_partition['tasna']['running']
    utilization['tasna'] = \
        float(allocated_tasna_slots) / float(total_tasna_slots)

    # Vesta Utilization
    # 8 K80 Boards per Server, 2 GPUs per Board, 2 Servers = 32 Slots
    total_vesta_slots = 32 - number_of_nodes_down['vesta'] * 16
    allocated_vesta_slots = number_of_jobs_by_partition['vesta']['running']
    utilization['vesta'] = \
        float(allocated_vesta_slots) / float(total_vesta_slots)

    # GPU Utilization
    total_gpu_slots = total_tasna_slots + total_vesta_slots
    allocated_gpu_slots = allocated_tasna_slots + allocated_vesta_slots
    utilization['gpu'] = float(allocated_gpu_slots) / float(total_gpu_slots)

    return utilization
