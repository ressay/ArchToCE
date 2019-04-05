import random

from matplotlib import pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from descartes import PolygonPatch

from Geometry.Geom2D import Poly, Pnt


def plotPolys(polys,f,title='figure',colors=None):
    if not len(polys):
        return
    fig = plt.figure(f, figsize=(5, 5), dpi=90)
    fig.canvas.set_window_title(title+str(f))
    X = [pnt.x() for poly in polys for pnt in poly.points]
    Y = [pnt.y() for poly in polys for pnt in poly.points]

    minX = int(min(X))
    maxX = int(max(X))
    minY = int(min(Y))
    maxY = int(max(Y))
    # p1 = Polygon([(0, 0), (0, 2), (2, 2), (2, 0)])
    # p2 = Polygon([(1, 0), (1, 2), (3, 2), (3, 0)])
    ax = fig.add_subplot(111)
    if not colors:
        colors = [[random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),1] for poly in polys]
    for poly,c in zip(polys,colors):
        ring_patch = PolygonPatch(poly.poly,alpha=c[-1])
        ring_patch.set_color(c[:-1])
        ax.add_patch(ring_patch)

    ax.set_title('General Polygon')
    xrange = [minX-4, maxX+4]
    yrange = [minY-4, maxY+4]
    ax.set_xlim(*xrange)
    ax.set_xticks(range(*xrange) + [xrange[-1]])
    ax.set_ylim(*yrange)
    ax.set_yticks(range(*yrange) + [yrange[-1]])
    ax.set_aspect(1)

def plotShapely(shapes,colors,alphas,f,title='figure'):
    if not len(shapes):
        return
    fig = plt.figure(f, figsize=(5, 5), dpi=90)
    fig.canvas.set_window_title(title+str(f))
    ax = fig.add_subplot(111)
    for shape,c,a in zip(shapes,colors,alphas):
        xs, ys = shape.exterior.xy
        ax.fill(xs, ys, alpha=a, fc=c, ec=[0,0,0])



if __name__ == "__main__":
    # poly1 = Poly([Pnt(0, 1), Pnt(1, 0), Pnt(6, 5), Pnt(5, 6)])
    # polys = [poly1]
    # plotPolys(polys,1)
    # poly2 = Poly([Pnt(1, 2), Pnt(2, 1), Pnt(7, 6), Pnt(6, 7)])
    # polys = [poly2]
    # plotPolys(polys, 2)
    distance = 2
    center = Pnt(1,1)
    vecLength = Pnt(10,1)
    wid = Pnt(vecLength.y(), -vecLength.x())
    wid = wid.copy().resize(distance) * 2 + wid.copy().resize(1)
    # leng = self.vecLength.copy().resize(distance)*2 + self.vecLength
    leng = vecLength
    pnts = []
    pnts.append(center - leng / 2 - wid / 2)
    pnts.append(pnts[0] + leng)
    pnts.append(pnts[1] + wid)
    pnts.append(pnts[0] + wid)
    polyPnts = [[pnt.x(), pnt.y()] for pnt in pnts]
    polygon = Polygon(polyPnts)
    p = center - leng / 2
    p = Point(p.x(), p.y())
    p2 = center + leng / 2
    p2 = Point(p2.x(), p2.y())
    circle = p.buffer(distance+0.5)
    circle2 = p2.buffer(distance+0.5)
    result = polygon.union(circle).union(circle2)
    xs, ys = result.exterior.xy

    # plot it
    # fig, axs = plt.subplots()
    # axs.fill(xs, ys, alpha=0.5, fc='r', ec='none')
    # xs, ys = circle.exterior.xy
    # axs.fill(xs,ys,alpha=0.2,fc='r',ec='none')
    plotShapely([polygon,circle,circle2],[[0.5,0.5,0.5],'r','b'],[1,0.2,0.2],1)
    plt.show()  # if not interactive


    # poly2 = poly2.intersection(poly1)
    # polys = poly1.subtractPoly(poly2)
    # plotPolys(polys, 3,'result')
    # plt.show()