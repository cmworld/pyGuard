# -*- coding:utf-8 -*-
import time
import traceback
from libs import log

class Worker(object):
    def __init__(self,guard,channel):
        self.channel = channel
        self.alive = True
        self.rds = guard.rds
        self.lock = guard.lock

    def _rds_connect(self):
        pass

    def run(self):
        log.debug('watcher thread init')

        while self.alive:

            self.lock.acquire()

            #your queue
            c = self.rds.lpop('queue:list')
            if c:
                log.debug('get key:%s' % c)

                try:
                    #do something
                    pass
                except:
                    excinfo = traceback.format_exc()
                    log.error('thread %d get error: %s' % (self.channel,excinfo))    
                finally:
                    self.lock.release()
            
            time.sleep(0.1)

        log.debug('thread %d leaving...' % self.channel)