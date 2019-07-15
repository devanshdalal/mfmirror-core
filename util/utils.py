#!/usr/bin/env python
import argparse
import os
from django.conf import settings

###########################################################################
### Utils
###########################################################################

MC = 'MC'
VRO = 'VRO'

def ParseCmd(argv):
    """Parses the command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source', nargs='+', choices=[MC, VRO],
        help='The source of scraping')
    parser.add_argument('--config', help='The config as a str')
    parser.add_argument('--to_json', help='out spec', action='store_true')
    parser.add_argument('--clean', help='clean', action='store_true')
    args = parser.parse_args(argv[1:])
    return args

def RemoveSpaces(l):
    if len(l)>0 and isinstance(l[0], list):
        return map(lambda x: filter(lambda y: not y.isspace(), x), l)
    else:
        return filter(lambda y: not y.isspace(), l)

def GetFileByName(name, dir = 'mf-data'):
    mf_data = os.path.join(settings.BASE_DIR, 'util', dir)
    os.system('mkdir -p '+ mf_data);
    if not name.endswith('.csv'):
        name = name + '.csv'
    return os.path.join(mf_data, name)
