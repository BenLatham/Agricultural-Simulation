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
    print(herd.groups)


