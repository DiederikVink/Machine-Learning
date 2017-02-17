#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import json


#ax1 = graph.add_subplot(111)

with open('files/graphs.json') as graph_file:    
    data = json.load(graph_file)

#ax1.set_title(data["title"])
#ax1.set_xlabel(data["xlabel"])
#ax1.set_ylabel(data["ylabel"])
plt.figure()
plt.title(data["title"])
plt.ylabel(data["ylabel"])
plt.xlabel(data["xlabel"])

x = data["x"]
y = data["y"]

#plt.scatter(x, data["y"], c=data["col"], label=data["legend"])
plt.scatter(x, data["line"], s=1, c='r')
plt.scatter(x, data["pline"], c='b')

plt.legend()
plt.show()
