#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import json

graph = plt.figure()

ax1 = graph.add_subplot(111)

with open('files/graphs.json') as graph_file:    
    data = json.load(graph_file)

ax1.set_title(data["title"])
ax1.set_xlabel(data["xlabel"])
ax1.set_ylabel(data["ylabel"])

x = data["x"]
y = data["y"]

ax1.plot(x,y, c='r', label=data["legend"])

leg = ax1.legend()

plt.show()
