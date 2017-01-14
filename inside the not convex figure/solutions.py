import numpy as np
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import math, random
from sympy import Ray, Segment
from sympy import Point as sPoint
from sympy import intersection
from random import randint

def orientation(points, p):
    """Возвращает ориентацию точки p относительно точек points (0, 1 или -1)."""
    return np.sign(np.linalg.det(np.array(points) - p))

def check(points, point): 
    p = Polygon(points)
    point = Point(point)
    return 'in' if p.contains(point) else 'out'


def generateTest(ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts):
    irregularity = clip( irregularity, 0,1 ) * 2*math.pi / numVerts
    spikeyness = clip( spikeyness, 0,1 ) * aveRadius

    # generate n angle steps
    angleSteps = []
    lower = (2 * math.pi / numVerts) - irregularity
    upper = (2 * math.pi / numVerts) + irregularity
    sum = 0
    for i in range(numVerts) :
        tmp = random.uniform(lower, upper)
        angleSteps.append( tmp )
        sum = sum + tmp

    # normalize the steps so that point 0 and point n+1 are the same
    k = sum / (2 * math.pi)
    for i in range(numVerts) :
        angleSteps[i] = angleSteps[i] / k

    # now generate the points
    points = []
    angle = random.uniform(0, 2*math.pi)
    for i in range(numVerts) :
        r_i = clip( random.gauss(aveRadius, spikeyness), 0, 2*aveRadius )
        x = ctrX + r_i*math.cos(angle)
        y = ctrY + r_i*math.sin(angle)
        points.append( (int(x),int(y)) )
        angle = angle + angleSteps[i]

    return [points,[randint(0,10),randint(0,10)]]

def clip(x, min, max) :
    if( min > max ) :  return x    
    elif( x < min ) :  return min
    elif( x > max ) :  return max
    else :             return x
	
def intersect(ray, segment):
    ray = Ray(sPoint(*ray[0]),sPoint(*ray[1]))
    segment = Segment(segment[0],segment[1])
    return len(intersection(ray,segment)) != 0
	
	
    