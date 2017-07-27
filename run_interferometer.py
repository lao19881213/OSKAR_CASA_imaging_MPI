# -*- coding: utf-8 -*-
"""Simulate a Measurement Set."""

import os
from os.path import join
from collections import OrderedDict
import subprocess
import argparse
import json
from shutil import copyfile
import numpy
import math



def run_interferometer(ini, verbose=True):
    """Run the OSKAR interferometer simulator."""
    if verbose:
        subprocess.call(["/BIGDATA/ac_shao_tan_1/OSKAR/OSKAR2.6/bin/oskar_sim_interferometer", ini])
    else:
        subprocess.call(["/BIGDATA/ac_shao_tan_1/OSKAR/OSKAR2.6/bin/oskar_sim_interferometer", "-q", ini])



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Simulation script.',
                                     epilog='')
    parser.add_argument('ini_file', type=str, nargs='?', help='INI config file.')
    args = parser.parse_args()
   
    print(args.ini_file)
    
    run_interferometer('%s.ini' % args.ini_file, True)
