from scipy.spatial import distance

def distanceToTarget(item1, item2):
    return distance(item1["position"], item2["position"])