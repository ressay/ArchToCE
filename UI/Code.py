import os
import sys
from random import random

import matplotlib
from shapely.geometry import Point, Polygon, LineString
from Geometry.Geom2D import Pnt, line_intersection, seg_intersection
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np


class SlabDivision:
    def __init__(self, storeySkeleton):
        self.storeySkeleton = storeySkeleton
        self.walls = storeySkeleton.wallSkeletons
        self.rooms = self.createSlabRooms()

    def importWalls(self, wallSkeletons):
        self.walls = wallSkeletons

    def createSlabSegments(self, walls=None, slab_poly=None):
        # from self.LSkeleton
        if walls is None:
            walls = self.walls
        segments = []
        for wall in walls:
            seg = self.createSegment(wall, slab_poly)
            if slab_poly is not None:
                seg = self.fixSegment(seg, slab_poly)
                if seg is None:
                    continue
            segments.append(seg)
        return segments

    def createSlabRooms(self):
        rooms = []
        cnt = 1
        for levelSkeleton in self.storeySkeleton.levelSkeletons:
            print("room", cnt)

            cnt += 1
            segments = self.createSlabSegments(levelSkeleton.wallSkeletons, levelSkeleton.slabSkeleton.poly.copy())
            room = Room(segments, levelSkeleton.slabSkeleton.poly.copy())
            print("room", room)
            # room.LocateAll(segments)
            rooms.append(room)

        return rooms

    def createSegment(self, wall, slab_poly=None):
        if slab_poly is not None:
            e1 = wall.topLeftPnt
            e2 = e1 + wall.vecLength
            boolean = False
            if e1.isInPolygon(slab_poly) or e2.isInPolygon(slab_poly):
                wall_seg = Segment(EndOfSegment(Point(e1.x(), e1.y())), EndOfSegment(Point(e2.x(), e2.y())), boolean)
            else:
                e1 = wall.topLeftPnt + wall.vecWidth
                e2 = e1 + wall.vecLength
                wall_seg = Segment(EndOfSegment(Point(e1.x(), e1.y())), EndOfSegment(Point(e2.x(), e2.y())), boolean)
        else:
            e1 = wall.topLeftPnt + (wall.vecWidth / 2)
            e2 = e1 + wall.vecLength
            boolean = False
            wall_seg = Segment(EndOfSegment(Point(e1.x(), e1.y())), EndOfSegment(Point(e2.x(), e2.y())), boolean)
        return wall_seg

    def get_closest_intersection(self, pnt1, pnt2, poly):
        l = len(poly.points)
        intersections = []
        # print("start for poly")
        print('***************', str(pnt1))
        for i in range(l):
            p1, p2 = poly.points[i % l], poly.points[(i + 1) % l]
            inters = seg_intersection((pnt1, pnt2), (p1, p2))
            # print("outcome", inters)
            if inters is not None:
                intersections.append(inters)
        if len(intersections) == 0:
            return None
        min_dist = None
        min_pnt = None
        for inters in intersections:
            dist = pnt1.minus(inters).magn()
            if min_dist is None or min_dist > dist:
                min_dist = dist
                min_pnt = inters
        return min_pnt

    def fixSegment(self, segment, slab_poly):
        e1, e2 = segment.End1.PntCoord, segment.End2.PntCoord
        pnt1 = Pnt(e1.x, e1.y)
        pnt2 = Pnt(e2.x, e2.y)
        end1 = pnt1.copy()
        end2 = pnt2.copy()
        if not pnt1.isInPolygon(slab_poly):
            end1 = self.get_closest_intersection(pnt1, pnt2, slab_poly)

        if not pnt2.isInPolygon(slab_poly):
            end2 = self.get_closest_intersection(pnt2, pnt1, slab_poly)

        if end1 is not None and end2 is None:
            print(e1.x, e1.y, e2.x, e2.y)
            print("polygon")
            for pnt in slab_poly.points:
                print(pnt.x(), pnt.y())
            raise Exception

        if end1 is None and end2 is not None:
            print(e1.x, e1.y, e2.x, e2.y)
            print("polygon")
            for pnt in slab_poly.points:
                print(pnt.x(), pnt.y())
            raise Exception

        # start
        # for poly
        #     ('(-1.82486794037,-1.03558377118)', '(-5.12486794037,-1.03558377118)')
        # ('(-9.12486794037,-5.63558377118)', '(-9.12486794037,-0.960583771182)')
        # ('result', '(-9.12486794037,-1.03558377118)')
        # ('outcome', None)
        # ('(-1.82486794037,-1.03558377118)', '(-5.12486794037,-1.03558377118)')
        # ('(-9.12486794037,-0.960583771182)', '(-4.94986794037,-0.960583771182)')
        # ('result', 'None')
        # ('outcome', None)
        # ('(-1.82486794037,-1.03558377118)', '(-5.12486794037,-1.03558377118)')
        # ('(-4.94986794037,-0.960583771182)', '(-4.94986794037,-5.63558377118)')
        # ('result', '(-4.94986794037,-1.03558377118)')
        # ('outcome', None)
        # ('(-1.82486794037,-1.03558377118)', '(-5.12486794037,-1.03558377118)')
        # ('(-4.94986794037,-5.63558377118)', '(-9.12486794037,-5.63558377118)')
        # ('result', 'None')
        # ('outcome', None)
        # (-5.124867940372748, -1.0355837711820652, -1.824867940372748, -1.0355837711820652)
        # polygon
        # (-9.12486794037277, -5.63558377118204)
        # (-9.12486794037277, -0.9605837711820402)
        # (-4.949867940372769, -0.9605837711820402)
        # (-4.949867940372769, -5.63558377118204)
        if end1 is None or end1.minus(end2).magn() == 0:
            return None
        return Segment(EndOfSegment(end1.pnt), EndOfSegment(end2.pnt), segment.Open)

class Room:
    def __init__(self, segments=None, slab_poly=None):
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.segments = segments
        self.slab_poly = slab_poly
        if segments is not None:
            self.LocateAll(segments)

    def LocateAll(self, Seg):
        x1, x2, y1, y2 = [], [], [], []
        minx = min(min(segment.End1.PntCoord.x for segment in Seg), min(segment.End2.PntCoord.x for segment in Seg))
        miny = min(min(segment.End1.PntCoord.y for segment in Seg), min(segment.End2.PntCoord.y for segment in Seg))
        maxx = max(max(segment.End1.PntCoord.x for segment in Seg), max(segment.End2.PntCoord.x for segment in Seg))
        maxy = max(max(segment.End1.PntCoord.y for segment in Seg), max(segment.End2.PntCoord.y for segment in Seg))
        for segment in Seg:
            if segment.End1.PntCoord.x == minx and segment.End2.PntCoord.x == minx:
                x1.append(segment)
            elif segment.End1.PntCoord.x == maxx and segment.End2.PntCoord.x == maxx:
                x2.append(segment)
            elif segment.End1.PntCoord.y == miny and segment.End2.PntCoord.y == miny:
                y1.append(segment)
            elif segment.End1.PntCoord.y == maxx and segment.End2.PntCoord.y == maxy:
                y2.append(segment)
            else:
                print("belongs nowhere")
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2

    def get_segments(self):
        return self.segments

    def plot(self, color=None, alpha=0.4, figax = None):
        if figax is None:
            fig, ax = plt.subplot()
        else:
            fig, ax = figax
        # xs = [p.x() for p in self.slab_poly.points]
        # ys = [p.y() for p in self.slab_poly.points]
        slab = Polygon(np.array([(p.x(), p.y()) for p in self.slab_poly.points]), True)
        collec = PatchCollection(np.array([slab]), alpha=alpha)

        if color is None:
            color = np.array([random(), random(), random()])
        collec.set_color(color)
        ax.add_collection(collec)
        # plt.plot(xs, ys, color=color, alpha=alpha, )


class Segment:
    def __init__(self, End1, End2, Open):
        self.End1 = End1
        self.End2 = End2
        self.Open = Open

    def join(self, segment, threshold):
        pass

    def getCol(self):
        if self.Open:
            return 'r'
        else:
            return 'k'

    def restrict(self):
        pass

    def plot(self, color=None, figax=None):
        if figax is None:
            fig, ax = plt.subplot()
        else:
            fig, ax = figax
        line = LineString([self.End1.PntCoord, self.End2.PntCoord])
        x, y = line.xy
        if color is None:
            color = self.getCol()
        if figax:
            ax.plot(x, y, color=color)
        else:
            plt.plot(x, y, color=color)


class EndOfSegment:
    def __init__(self, PntCoord):
        self.PntCoord = PntCoord
        self.ConnectedSeg = None

    def FindConnected(self, Seg):
        Conn = []
        for segment in Seg:
            if self.Verif(segment):
                Conn.append(segment)
        self.ConnectedSeg = Conn

    def Verif(self, segment):
        ends = [segment.End1, segment.End2]
        if self in ends:
            return True
        else:
            return False

    def plot(self, color=None, figax=None):
        if figax is None:
            fig, ax = plt.subplot()
        else:
            fig, ax = figax
        if color is None:
            color = 'green'
        if figax:
            ax.scatter(self.PntCoord.x, self.PntCoord.y, color=color)
        else:
            plt.scatter(self.PntCoord.x, self.PntCoord.y, color=color)

    def moveEnd(self, x, y):
        self.PntCoord = Point(self.PntCoord.x + x, self.PntCoord.y + y)
        return self


def main():
    print("Launched")
    # Creating Test Data
    # Segment1 = Segment(EndOfSegment(Point(0.0, 0.0)), EndOfSegment(Point(1.0, 0.0)), False)
    # Segment2 = Segment(EndOfSegment(Point(1.0, 0.0)), EndOfSegment(Point(1.0, 1.0)), False)
    # Segment3 = Segment(EndOfSegment(Point(0.0, 0.0)), EndOfSegment(Point(0.0, 0.33)), False)
    # Segment4 = Segment(EndOfSegment(Point(0.0, 0.33)), EndOfSegment(Point(0.0, 0.66)), True)
    # Segment5 = Segment(EndOfSegment(Point(0.0, 0.66)), EndOfSegment(Point(0.0, 1.0)), False)
    # Segment6 = Segment(EndOfSegment(Point(0.0, 1.0)), EndOfSegment(Point(0.33, 1.0)), False)
    # Segment7 = Segment(EndOfSegment(Point(0.33, 1.0)), EndOfSegment(Point(0.66, 1.0)), True)
    # Segment8 = Segment(EndOfSegment(Point(0.66, 1.0)), EndOfSegment(Point(1.0, 1.0)), False)
    # Seg = []
    # Seg.append(Segment1)
    # Seg.append(Segment2)
    # Seg.append(Segment3)
    # Seg.append(Segment4)
    # Seg.append(Segment5)
    # Seg.append(Segment6)
    # Seg.append(Segment7)
    # Seg.append(Segment8)
    # data

    # R=Room()
    # R.LocateAll(Seg)

    # Drawing one side of room
    # f1 = plt.figure(1)
    # Pts = []
    # for ind in R.x1:
    #     Pts.append(ind.End1.PntCoord)
    #     Pts.append(ind.End2.PntCoord)
    #     ind.End1.plotEnd()
    #     ind.End2.plotEnd()
    #     ind.PlotSeg()
    #
    # Drawing one side of room
    # f1 = plt.figure(2)
    # Pts = []
    # for ind in R.y2:
    #     Pts.append(ind.End1.PntCoord)
    #     Pts.append(ind.End2.PntCoord)
    #     ind.End1.plotEnd()
    #     ind.End2.plotEnd()
    #     ind.PlotSeg()
    #
    #
    # Drawing all segments
    # f2 = plt.figure(3)
    # Pts = []
    # for segment in Seg:
    #     Pts.append(segment.End1.PntCoord)
    #     Pts.append(segment.End2.PntCoord)
    #     segment.End1.plotEnd()
    #     segment.End2.plotEnd()
    #     segment.PlotSeg()
    #
    # plt.show()


main()
