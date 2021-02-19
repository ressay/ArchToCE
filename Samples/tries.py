import random
import timeit

from shapely.geometry import Point
from matplotlib import pyplot as plt
from Geometry.Geom2D import Pnt
from shapely.ops import cascaded_union
import geopandas as gpd

p1 = Point(1,2).buffer(2)
p2 = Point(0,1).buffer(2)
arr = []
for i in range(50):
    arr.append(Point(random.uniform(0,10),random.uniform(0,10)).buffer(0.5))
start = timeit.default_timer()
a = cascaded_union(arr)
area = a.area
stop = timeit.default_timer()
un = gpd.GeoSeries(a)
print(("time it took: " + str(stop - start)))
print(("area is: " + str(area)))
un.plot(color='green')
plt.show()


