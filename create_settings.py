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



def dict_to_ini(settings_dict, ini):
    """Convert a dictionary of settings to and OSKAR settings ini file."""
    ini_dir = os.path.dirname(ini)
    if not ini_dir == "" and not os.path.isdir(ini_dir):
        os.makedirs(ini_dir)
    for group in sorted(settings_dict):
        for key in sorted(settings_dict[group]):
            key_ = group + key
            value_ = settings_dict[group][key]
            subprocess.call(["/BIGDATA/ac_shao_tan_1/OSKAR/OSKAR2.6/bin/oskar_settings_set", "-q", ini,
                            key_, str(value_)])



def create_settings(settings, sky_file, ms_path, num_times, freq, smearing=True):
    """Create simulation settings file."""
    sim = settings['sim']
    obs = sim['observation']
    tel = sim['telescope']

    #if not os.path.isdir(os.path.dirname(ms_path)):
    #    os.mkdir(os.path.dirname(ms_path))

    if smearing:
        dt_ave = obs['obs_length'] / num_times
    else:
        dt_ave = 0.0

    s = OrderedDict()
    s['simulator/'] = {
        'double_precision': 'true',
        'keep_log_file': 'false'
    }
    s['sky/'] = {
        'oskar_sky_model/file': sky_file
    }
    s['observation/'] = {
        'start_frequency_hz': freq,
        'num_channels': 1,
        'start_time_utc': obs['start_time_mjd'],
        'length': obs['obs_length'],
        'num_time_steps': num_times,
        'phase_centre_ra_deg': obs['ra_deg'],
        'phase_centre_dec_deg': obs['dec_deg']
    }
    s['telescope/'] = {
        'longitude_deg': tel['lon_deg'],
        'latitude_deg': tel['lat_deg'],
        'input_directory': tel['path'],
        'pol_mode': 'Scalar',
        'station_type': 'Isotropic beam'
    }
    s['interferometer/'] = {
        'time_average_sec': dt_ave,
        'channel_bandwidth_hz': obs['channel_bw_hz'],
        'ms_filename': ms_path
    }
    return s

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Simulation script.',
                                     epilog='')
    parser.add_argument('config', type=str, nargs='?', help='JSON config file.')
    parser.add_argument('sky_model', type=str, nargs='?', help='sky model file.')

    args = parser.parse_args()
    #os.system('source /home/lbq/work/OSKAR/bashrc')
    try:
        settings = json.load(open(args.config))
    except ValueError as e:
        print ('ERROR: FAILED TO PARSE JSON CONFIG FILE!!')
        print (e.message)
        exit(1)
    
    sky_file = args.sky_model
    sim = settings['sim']
    obs = sim['observation']

    freq_start = obs['freq_hz'][0]
    freq_stop = obs['freq_hz'][1]
    freq_c = numpy.linspace(freq_start, freq_stop, 16)
    id_f = args.config.split('_')
    freq_id = int(id_f[len(id_f)-1])
    freq = freq_c[freq_id]
    print(freq,0)

    for n in obs['num_times']:
        ini_file = '%s.ini' % args.config
        ms_out = '%s.ms' % args.config
        #print (ini_file)
        s = create_settings(settings, sky_file, ms_out, num_times=n, freq=freq, smearing=False)
        dict_to_ini(s, ini_file)    

