#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import threading
import time

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from ConfigParser import ConfigParser
from libs.logger import create_log,console_log
from libs.rdsconnect import RdsConn,rds

from jober import Worker

class Guard(object):
    def __init__(self,conf,rds):
        self.conf = conf
        self.rds = rds
        self.workers = {}

    def run(self):
        #get lock
        self.lock = threading.RLock()

        self.start_worker();

        while True:
            time.sleep(10)

    def start_worker(self):
        kwargs = {
            'channel':0
        }

        thread_cnt = int(self.conf.get('worker', 1))

        workers = []
        for cnt in range(thread_cnt):
            params = kwargs.copy()
            params.update({'channel': cnt})

            worker = threading.Thread(target=self.worker_thread, kwargs=params)
            workers.append(worker)

        for w in workers:
            w.setDaemon(True)
            w.start()

    def stop_worker(self):
        for i in self.workers:
            self.workers[i].alive = False
            del self.workers[i]
  
    def worker_thread(self,channel):
        trigger = Worker(self,channel)
        self.workers[channel] = trigger
        trigger.run()

if __name__ == '__main__':

    args = sys.argv
    if len(args) < 2:
        print 'Failed: Configuration file is not specified'
        sys.exit(2)

    conf_file = args[1] #os.getcwd() + '/config.ini'
    if not os.path.isfile(conf_file):
        print 'Failed: Cann\'t found file "%s".' % conf_file
        sys.exit(2)

    config = ConfigParser()
    config.read(conf_file)

    log_level = config.getint('setting', 'log_level')
    if not log_level:
        log_level = 30

    log_file = config.get('setting', 'log_file')
    if log_file:
        create_log(log_file,log_level)
    else:
        console_log(log_level)

    redis_conf = {
        'host': config.get('redis', 'host'),
        'port': int(config.get('redis','port')),
        'db': int(config.get('redis', 'db')),
        'password': config.get('redis','password')
    }

    try:
        rds = Rdsconn(redis_conf)
        if rds.ping() == True:
            pass
        else:
            raise Exception('Redis Connection refused.')
    except Exception:
        print('Failed: Redis Connection refused.')
        sys.exit(2)

    if rds == None:
        print('Failed: Can not connect Redis server...')
        sys.exit(2)    

    conf = {
        'redis' : redis_conf,
        'worker' : config.getint('setting', 'worker'),
    }

    guard = Guard(conf,rds)
    guard.run()   