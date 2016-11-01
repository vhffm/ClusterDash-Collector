"""
NVIDIA Interaction.
"""

import pandas as pd
import numpy as np
import glob as glob


def read_gpu_stats(node='vesta1', gpu_type='tesla'):
    """
    Reads stats from CSV file, which was dumped on the GPU nodes.
    
    The following queries generate the CSV files.

    Run on GPU node w/ Tesla Cards:
    $ nvidia-smi --query-gpu=index,uuid,name,temperature.gpu,utilization.gpu,utilization.memory,power.draw --format=csv,noheader > vesta1_`date '+%s'`.csv

    Run on GPU nodes w/ GTX Cards:
    $ nvidia-smi --query-gpu=index,uuid,name,temperature.gpu --format=csv,noheader > tasna1_`date '+%s'`.csv

    CSV files is named "$node_$unix_epoch_in_seconds.csv".
    For example, "vesta1_1454748497.csv".

    @param: node - GPU node, used to nconstruct filename [String]
    @param: gpu_type - GPU Type (Tesla|GTX) [String]
    @return: df - GPU Stats [Pandas Dataframe]
    @return: epoch - Time (Seconds since 01-01-1970) [Integer]
    @return: success - Did we get data? [Boolean]
    """

    # Dev
    # basedir = 'Test/'

    # Prod
    basedir = '/home/ics/volker/TmpDash/'

    # Globbing
    globs = glob.glob("%s/%s_*.csv" % (basedir, node))
    globs = sorted(globs)
    
    # Is there anybody out there?
    if len(globs) > 0:

        # Extract Filename
        fname = globs[-1]

        # Extract Epoch
        epoch = int(fname[:-4].split('_')[-1])

        # Branch on GPU Type. See header documentation.
        # Tesla cards report all stats. GTX cards are gimped.
        if gpu_type == 'tesla':
            names_cols = [ 'gpu_id', 'uuid', \
                           'gpu_name', \
                           'gpu_temperature', \
                           'gpu_utilization', \
                           'memory_utilization', \
                           'power_draw' ]
            df = pd.read_csv(fname, sep=', ', header=None, names=names_cols, \
                             engine='python')

            # Deal With Errors
            df.ix[df.power_draw == '[Unknown Error]', 'power_draw' ] = np.nan

            # Drop Units
            df.power_draw = \
                df.ix[~pd.isnull(df.power_draw), \
                      'power_draw'].apply(lambda a: a.split(' ')[0])
            df.gpu_utilization = \
                df.gpu_utilization.apply(lambda a: a.split(' ')[0])
            df.memory_utilization = \
                df.memory_utilization.apply(lambda a: a.split(' ')[0])

            # Fix Types
            df.power_draw = \
                np.asarray(df.power_draw, dtype=np.float64)
            df.gpu_utilization = \
                np.asarray(df.gpu_utilization, dtype=np.float64)
            df.memory_utilization = \
                np.asarray(df.memory_utilization, dtype=np.float64)

            # Add Node Column
            df['node'] = pd.Series(["%s" % node]*len(df))

        elif gpu_type == 'gtx':
            names_cols = [ 'gpu_id', 'uuid', \
                           'gpu_name', \
                           'gpu_temperature' ]
            df = pd.read_csv(fname, sep=', ', header=None, names=names_cols, \
                             engine='python')

            # Add Node Column
            df['node'] = pd.Series(["%s" % node]*len(df))

        # Return
        return df, epoch, True

    else:
        # Return
        return None, None, False
