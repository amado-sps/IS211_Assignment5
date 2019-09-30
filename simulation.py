#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""classes modified from algorithm text"""
from urllib.request import urlopen
import csv
import requests

file = "http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv"
servers = 0

def main(file, servers):
    req_list = []
    stream = urlopen(file)
    csvfile = csv.reader(stream.read().decode('utf-8'))
    for row in csvfile:
        req_list.append(row)

    if servers >= 1:
        print("Servers")
    else:
        simulateOneServer(req_list)
class Queue:
    def __init__(self):
        self.items = []
    def is_empty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0, item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)

class Server:
    def __init__(self):
      self.current_task = None
      self.time_remaining = 0
    def tick(self):
      if self.current_task != None:
         self.time_remaining = self.time_remaining - 1
         if self.time_remaining <= 0:
            self.current_task = None
    def busy(self):
      if self.current_task != None:
         return True
      else:
         return False
    def start_next(self, new_task):
      self.current_task = new_task
      self.time_remaining = new_task.get_time()

class Request:
    def __init__(self, time, ptime):
      self.timestamp = time
      self.ptime = ptime
    def get_stamp(self):
      return self.timestamp
    def get_time(self):
      return self.ptime
    def wait_time(self, current_time):
      return current_time - self.timestamp

def simulateOneServer(req_list):
    queue = Queue()
    server = Server()
    waiting_times = []
    for row in req_list:
        timestamp = int(row[0])
        ptime = int(row[2])
        request = Request(timestamp, ptime)
        queue.enqueue(request)
        if (not server.busy()) and (not queue.is_empty()):
            timestamp = queue.dequeue()
            waiting_times.append(timestamp.wait_time(int(timestamp)))
            server.start_next(timestamp)
        server.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining."
          % (average_wait, queue.size()))

def simulateManyServers(req_list, servers):
    queue = Queue()
    waiting_times = []
    server = Server()
    serverlist = []
    for number in range(servers):
        serverlist.append(Server())
    for server in serverlist:
        for row in req_list:
            timestamp = int(row[0])
            ptime = int(row[2])
            request = Request(timestamp, ptime)
            queue.enqueue(request)
            if (not server.busy()) and (not queue.is_empty()):
                next_request = queue.dequeue()
                waiting_times.append(next_request.wait_time(int(timestamp)))
                server.start_next(next_request)
            server.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining."
          % (average_wait, queue.size()))


if __name__ == "__main__":
    main(file, servers)