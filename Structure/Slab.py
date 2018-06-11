from Structure import Structure

class Slab(Structure):

    def __init__(self,shape):
        super(Slab, self).__init__(shape)


    def getSupportingWalls(self,walls):
        supportingWalls = []
        for wall in walls:
            if wall.isSupporting(self):
                supportingWalls.append(wall)

        return supportingWalls