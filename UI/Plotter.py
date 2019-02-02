from matplotlib import pyplot as plt
from shapely.geometry.polygon import Polygon
from descartes import PolygonPatch

from Geometry.Geom2D import Poly, Pnt


def plotPolys(polys,f,title='figure'):
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
    for poly in polys:
        ring_patch = PolygonPatch(poly.poly,alpha=0.4)
        ax.add_patch(ring_patch)

    ax.set_title('General Polygon')
    xrange = [minX, maxX]
    yrange = [minY, maxY]
    ax.set_xlim(*xrange)
    ax.set_xticks(range(*xrange) + [xrange[-1]])
    ax.set_ylim(*yrange)
    ax.set_yticks(range(*yrange) + [yrange[-1]])
    ax.set_aspect(1)



if __name__ == "__main__":
    poly1 = Poly([Pnt(0, 1), Pnt(1, 0), Pnt(6, 5), Pnt(5, 6)])
    polys = [poly1]
    plotPolys(polys,1)
    poly2 = Poly([Pnt(1, 2), Pnt(2, 1), Pnt(7, 6), Pnt(6, 7)])
    polys = [poly2]
    plotPolys(polys, 2)
    poly2 = poly2.intersection(poly1)
    polys = poly1.subtractPoly(poly2)
    plotPolys(polys, 3,'result')
    plt.show()