import cv2
import numpy as np

class CentroidTracker:
    def __init__(self, maxDisappeared=50, distanceThreshold=50):
        self.nextObjectID = 0
        self.objects = {}  
        self.disappeared = {}  
        self.maxDisappeared = maxDisappeared
        self.distanceThreshold = distanceThreshold

    def register(self, centroid, state):
        self.objects[self.nextObjectID] = (centroid, state)
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID):
        if objectID in self.objects:
            del self.objects[objectID]
            del self.disappeared[objectID]

    def update(self, rects, polygon):
        inputCentroids = []
        inputStates = []
        for (x1, y1, x2, y2) in rects:
            cX = int((x1 + x2) / 2.0)
            cY = int((y1 + y2) / 2.0)
            inputCentroids.append((cX, cY))
            inside = cv2.pointPolygonTest(polygon, (cX, cY), False) >= 0
            inputStates.append(inside)
        if len(inputCentroids) == 0:
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
            return self.objects
        if len(self.objects) == 0:
            for i in range(len(inputCentroids)):
                self.register(inputCentroids[i], inputStates[i])
            return self.objects
        objectIDs = list(self.objects.keys())
        objectCentroids = [self.objects[objectID][0] for objectID in objectIDs]
        D = np.linalg.norm(np.array(objectCentroids)[:, np.newaxis] - np.array(inputCentroids), axis=2)
        rows = D.min(axis=1).argsort()
        usedCols = set()
        assignment = {}
        for row in rows:
            col = D[row].argmin()
            if col in usedCols:
                continue
            if D[row][col] > self.distanceThreshold:
                continue
            objectID = objectIDs[row]
            assignment[objectID] = col
            usedCols.add(col)
        unmatchedObjectIDs = set(objectIDs) - set(assignment.keys())
        for objectID in unmatchedObjectIDs:
            self.disappeared[objectID] += 1
            if self.disappeared[objectID] > self.maxDisappeared:
                self.deregister(objectID)
        unmatchedInput = set(range(len(inputCentroids))) - set(assignment.values())
        for i in unmatchedInput:
            self.register(inputCentroids[i], inputStates[i])
        for objectID, col in assignment.items():
            self.objects[objectID] = (inputCentroids[col], inputStates[col])
            self.disappeared[objectID] = 0
        return self.objects
