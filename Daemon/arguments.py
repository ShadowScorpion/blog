#!/bin/python

import argparse

pid_file = '/var/run/cmdb_agent'

def arguments_reader():
    parser = argparse.ArgumentParser(description='cmdb_agent runner')
    parser.add_argument('operation',
        metavar='OPERATION',
        type=str,
        help='Operation with cmdb agent. Accepts any of these values: start, stop, restart, status',
        choices=['start', 'stop', 'restart', 'status'])
    args = parser.parse_args()
    operation = args.operation 
    return operation   

if __name__ == "__main__":
    action = arguments_reader()
    print(action)
