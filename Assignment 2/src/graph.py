#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import json


#ax1 = graph.add_subplot(111)

with open('files/graphs.json') as graph_file:    
    data = json.load(graph_file)

plt.figure()
plt.title(data["title"])
plt.ylabel(data["ylabel"])
plt.xlabel(data["xlabel"])

x = data["x"]
y = data["y"]
col = []

for i in data["col"]:
    if (i == 98):
        col.append('b')
    else:
        col.append('r')

plt.scatter(x, data["y"], s=1, color=col, label=data["legend"])
plt.scatter(x, data["line"], s=1, color='green')
plt.scatter(x, data["pline"], s=1, color='cyan')

plt.legend()
plt.show()
