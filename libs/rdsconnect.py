# -*- coding:utf-8 -*-
import redis

rds = None

def RdsConn(conf):
    global rds
    if rds == None:
        rds = redis.Redis(**conf)

    return rds

rdsconn = RdsConn