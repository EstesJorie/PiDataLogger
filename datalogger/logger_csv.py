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

    def printData(self):
        print('-' * 100)
        cpu_time = self.dict['cpu']
        vmemory = self.dict['vmemory']
        print("-- {0:%Y-%m-%d, %H:%M:%S} --".format(cpu_time[0]))
        print("CPU TIME // User: {1:,.0f}, System: {2:,.0f}, Idle: {3:,.0f}".format(cpu_time[0], cpu_time[1], cpu_time[2], cpu_time[3]))
        print("VIRTUAL MEMORY // Total: {1:,d}, Available: {2:,d}".format(vmemory[0], vmemory[1], vmemory[2]))

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