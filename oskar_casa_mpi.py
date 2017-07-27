#!/usr/bin/python

import os
import time
from mpi4py import MPI

if __name__ == '__main__':
    time_start = time.time()
    rank = MPI.COMM_WORLD.Get_rank()
    num_process = MPI.COMM_WORLD.Get_size()
    rank_str = str(rank)
    os.system('cat /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge/sim_gleam.json > /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge/config/1_%s' % rank_str)
    os.system('python /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge/create_settings.py /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge/config/1_%s /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge/sim_gleam.json' % rank_str)
    os.system('python /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge/run_interferometer.py /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge/config/1_%s' % rank_str)
    os.system('python /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge/data_reduction.py /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge/config/1_%s' % rank_str) 
    time_stop = time.time()
    use_time = time_stop-time_start
    print "use time: %.3f" % use_time
