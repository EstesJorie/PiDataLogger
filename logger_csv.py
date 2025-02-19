#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv
import psutil as ps
from datetime import datetime
from time import sleep
import os

class Logger:
    def __init__(self):
        self.dict = {}
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')


    def collectData(self):
        self.dict['cpu'] = (datetime.now(), *ps.cpu_times())  
        self.dict['vmemory'] = (datetime.now(), *ps.virtual_memory()) 
        self.dict['disk'] = (datetime.now(), *ps.disk_usage('/'))
        self.dict['net'] = (datetime.now(), *ps.net_io_counters())
        self.dict['uptime'] = (datetime.now(), ps.boot_time())
        self.dict['sensors'] = (datetime.now(), *ps.sensors_temperatures()) 

    def printData(self):
        print('-' * 100)
        cpu_time = self.dict['cpu']
        vmemory = self.dict['vmemory']
        disk = self.dict['disk']
        net = self.dict['net']

        uptime = self.dict['uptime']
        boot_time = datetime.fromtimestamp(uptime[1])
        uptime_duration = datetime.now() - boot_time
        uptime_str = str(uptime_duration).split(".")[0]
        sensors = self.dict['sensors']

        print("-- {0:%Y-%m-%d, %H:%M:%S} --".format(cpu_time[0]))
        print("CPU TIME // User: {1:,.0f}, System: {2:,.0f}, Idle: {3:,.0f}".format(cpu_time[0], cpu_time[1], cpu_time[2], cpu_time[3]))
        print("VIRTUAL MEMORY // Total: {1:,d}, Available: {2:,d}".format(vmemory[0], vmemory[1], vmemory[2]))
        print("DISK USAGE // Total: {1:,d}, Used: {2:,d}, Free: {3:,d}, Percent: {4}%".format(disk[0], disk[1], disk[2], disk[3], disk[4]))
        print("NETWORK IO // Bytes Sent: {1:,d}, Bytes Received: {2:,d}".format(net[0], net[1], net[2]))
        print(f"UPTIME // {uptime_str}")
        
        if sensors:
            print(f"TEMPERATURE // {sensors[0]}: {sensors[1]}°C")
        else:
            print("TEMPERATURE // No sensors found on system")

    def logData(self):
        os.makedirs(self.data_dir, exist_ok=True)
        for file, data in self.dict.items():
            with open(os.path.join(self.data_dir, file + '.csv'), 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)

def main():
    logger = Logger()
    for _ in range(10):
        logger.collectData()
        logger.printData()
        logger.logData()
        sleep(5)

main()