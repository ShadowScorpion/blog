#!/bin/python

import argparse
import os, sys
import time, datetime
import atexit
import signal
from logsystem import LogginSystem as logsys

pid_file = '/var/run/cmdb_agent'
log_file = '/var/log/cmdb_agent.log'


class Daemon(object):

    def __init__(self, pidfile, stdin='/dev/null',
                 stdout='/dev/null', stderr='/dev/null'):

        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile


    def daemonize(self):

        self.fork()
        self.dettach_env()
        self.fork()
        sys.stdout.flush()
        sys.stderr.flush()
        self.attach_stream('stdin', mode='r')
        self.attach_stream('stdout', mode='a+')
        self.attach_stream('stderr', mode='a+')
        self.create_pidfile()


    def attach_stream(self, name, mode):

        stream = open(getattr(self, name), mode)
        os.dup2(stream.fileno(), getattr(sys, name).fileno())


    def dettach_env(self):

        os.chdir("/")
        os.setsid()
        os.umask(0)


    def fork(self):

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("Fork failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)


    def create_pidfile(self):

        atexit.register(self.delpid)
        pid = str(os.getpid())
        open(self.pidfile,'w+').write("%s\n" % pid)


    def delpid(self):

        os.remove(self.pidfile)


    def start(self):

        pid = self.get_pid()

        if pid:
            message = "pidfile %s already exist. CMDB agent already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        self.daemonize()
        self.run()


    def get_pid(self):

        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except (IOError, TypeError):
            pid = None
        return pid


    def stop(self, silent=False):

        pid = self.get_pid()

        if not pid:
            if not silent:
                message = "pidfile %s does not exist. CMDB agent not running?\n"
                sys.stderr.write(message % self.pidfile)
            return
        try:
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                sys.stdout.write(str(err))
                sys.exit(1)


    def restart(self):

        self.stop(silent=True)
        self.start()


    def run(self):

        raise NotImplementedError



def arguments_reader():

    parser = argparse.ArgumentParser(description='cmdb_agent runner')
    parser.add_argument('operation',
        metavar='OPERATION',
        type=str,
        help='Operation with CMDB agent. Accepts any of these values: start, stop, restart, status',
        choices=['start', 'stop', 'restart', 'status'])
    args = parser.parse_args()
    operation = args.operation
    return operation



class CMDBAgent(Daemon):


    def run(self):
        while True:
            self.some_actions()
            time.sleep(1)


    def some_actions(self):

        test_file = "/tmp/test.txt"
        with open(test_file, "a") as myfile:
            myfile.write("appended text\n")

if __name__ == "__main__":

    action = arguments_reader()
    logginsystem = logsys(log_file)
    daemon = CMDBAgent(pid_file,)

    if action == 'start':
        logginsystem.write("[%s] Starting CMDB agent\n" % datetime.datetime.now().strftime('%B %d %H:%M:%S'))
        daemon.start()
        pid = daemon.get_pid()

        if not pid:
            logginsystem.write("[%s] Unable run CMDB agent\n" % datetime.datetime.now().strftime('%B %d %H:%M:%S'))
        else:
            logginsystem.write("[%s] CMDB agent is running [PID=%d]\n" % datetime.datetime.now().strftime('%B %d %H:%M:%S'), pid)

    elif action == 'stop':
        logginsystem.write("[%s] Stoping CMDB agent\n" % datetime.datetime.now().strftime('%B %d %H:%M:%S'))
        daemon.stop()

    elif action == 'restart':
        logginsystem.write("[%s] Restarting CMDB agent\n" % datetime.datetime.now().strftime('%B %d %H:%M:%S'))
        daemon.restart()

    elif action == 'status':
        logginsystem.write("[%s] Viewing CMDB agent status\n" % datetime.datetime.now().strftime('%B %d %H:%M:%S'))
        pid = daemon.get_pid(logginsystem)

        if not pid:
            logginsystem.write("[%s] CMDB agent isn't running\n" % datetime.datetime.now().strftime('%B %d %H:%M:%S'))
        else:
            logginsystem.write("[%s] CMDB agent is running [PID=%d]\n" % datetime.datetime.now().strftime('%B %d %H:%M:%S'), pid)

    sys.exit(0)