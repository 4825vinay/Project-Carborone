from rrt import RRT, Node
import numpy as np
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt 
from shapely.geometry import Polygon


class Square():
    def __init__(self, x, y, a, b):
        # Take the parameters x, y, z and generate an array of points or the vertices
        self.x = x
        self.y = y
        self.a = a
        self.b = b

    def corners(self):
        corners = [
            (self.x + self.a, self.y + self.b),
            (self.x - self.a, self.y + self.b),
            (self.x - self.a, self.y - self.b),
            (self.x + self.a, self.y - self.b)
        ]

        return corners

class MapGenerator():
    def __init__(self, number, sample_area):
        self.number = number
        self.sample_area = sample_area
    def generate_map(self):
        obst = [Square(np.random.uniform(self.sample_area[0], self.sample_area[1]),np.random.uniform(self.sample_area[0], self.sample_area[1]), np.random.uniform(), np.random.uniform()) for i in range(self.number)]
        return obst

if __name__ == "__main__":
    # Init stuff
    start = Node(0, 0)
    goal = Node(11, 11)
    dim = 2
    planner = RRT(dim=dim)
    map_gen = MapGenerator(15, [0, 10])
    map = map_gen.generate_map()

    # plan a path
    path, optimised_path = planner([-5, 15], 1000, start, goal, [Polygon(obst.corners()) for obst in map])   
    
    # Plotting stuff
    data = [[p[0]for p in path], [p[1]for p in path], [p[2] for p in path]]
    data_optim = [[p[0]for p in optimised_path], [p[1]for p in optimised_path], [p[2] for p in optimised_path]]
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(data[0], data[1], data[2], "gray")
    ax.scatter3D(data[0], data[1], data[2], c=data[2], cmap="Greens")
    ax.plot3D(data_optim[0], data_optim[1], data_optim[2], "red")
    ax.scatter3D(data_optim[0], data_optim[1], data_optim[2], c=data_optim[2], cmap="Blues")

    for obst in map:
        corners = obst.corners()
        verts = [list(zip([p[0] for p in corners], [p[1] for p in corners], [0 for p in corners]))]
        ax.add_collection3d(Poly3DCollection(verts))
    plt.show()
        
