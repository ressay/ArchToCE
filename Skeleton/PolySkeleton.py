from Skeleton.Skelet import Skelet


class PolySkeleton(Skelet):
    def __init__(self,poly):
        super(PolySkeleton, self).__init__()
        self.poly = poly