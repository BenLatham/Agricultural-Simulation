import scipy.cluster.vq as vq
from numpy import array


def group(herd, groups=3):
    cows = [cow for group in herd.groups for cow in group]
    herd.groups = [[] for i in range(groups)]
    data = [[cow.protein_requirement,cow.energy_requirement] for cow in cows]
    data_array = array(data)
    data_array = vq.whiten(data_array,"\n")
    grouped = False
    count = 0
    while not grouped:
        try:
            centroids, labels = vq.kmeans2(data_array,groups,missing='raise')
            grouped = True
        except vq.ClusterError:
            if count >20:
                raise vq.ClusterError
            else:
                grouped = False
                count += 1

    for i in range(labels.size):
        herd.groups[labels[i]].append(cows[i])
    # print(herd.groups)

def plot_groups(herd):
    for group in herd.groups:
        plot =[(cow.energy_requirement,cow.protein_requirement) for cow in group]

import matplotlib.pyplot as plt
import plotly.offline as py
import numpy as np

import plotly

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api
def plot(herd, title):
    colors = ['r','g','b']
    fig, ax = plt.subplots()
    plt.title(title)
    for num, group in enumerate(herd.groups):
        x = [cow.energy_requirement for cow in group]
        y = [cow.protein_requirement for cow in group]
        ax.scatter(x, y, color=colors[num%3])
    py.plot_mpl(fig, filename=title+".html", image_filename=title)

# # example
from simulation import dairy_herd as dh
def example():
    h = dh.Herd(dh.CowAfrc)
    h2 = dh.Herd(dh.CowAfrc)
    params = {
        "day_of_lactation":dh.Dist(0,80,0),
        "day_of_gestation": dh.Dist(0,30,0),
        "parity": dh.Dist(1,0, randomise=False),
        "weight": dh.Dist(800,10),
        "yield_at_150": dh.Dist(40,5)
    }
    h.generate(300, **params)
    plot(h, "h1, pre-group")

    group(h)
    plot(h, "h1, grouped")

    params = {
        "day_of_lactation":dh.Dist(0,200,0),
        "day_of_gestation": dh.Dist(0,150,0),
        "parity": dh.Dist(2,0, randomise=False),
        "weight": dh.Dist(800,10),
        "yield_at_150": dh.Dist(35,7)
    }
    h.generate(300, **params)
    h2.generate(300, **params)
    plot(h2, "h2 ungrouped")
    group(h)
    plot(h, "both herds, grouped")
# """        :param day_of_lactation: days since calving
#         :param day_of_gestation: days since insemination
#         :param parity: parity
#         :param weight: live weight kg
#         :param yield_at_150: expected yield 150 days after calving"""
