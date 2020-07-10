import time

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from shapely.geometry import LineString, Polygon


class Node:
    def __init__(self, x, y,z=0):
        self.x = x
        self.y = y
        self.z = z
        self.parent = None
    def __str__(self):
        return "{}, {}, {}".format(self.x, self.y, self.z)


def generate_node(sample_area, alpha, goal, dim=2):
    num = np.random.random()
    if num < alpha:
        #print('goal', goal)
        return goal
    else:
        if dim == 2:
            return Node(
                np.random.uniform(sample_area[0], sample_area[1]),
                np.random.uniform(sample_area[0], sample_area[1]),
                #np.random.uniform(sample_area[0], sample_area[1])
            )
        else:
            return Node(
                np.random.uniform(sample_area[0], sample_area[1]),
                np.random.uniform(sample_area[0], sample_area[1]),
                np.random.uniform(sample_area[0], sample_area[1])
            )

def lineTo(node, nearest_node, delta, dim=2):
    if dim == 3:
        vec = np.array([node.x - nearest_node.x, node.y-nearest_node.y, node.z-nearest_node.z])
        vec = (vec / np.linalg.norm(vec)) * delta
        node = Node(nearest_node.x + vec[0], nearest_node.y + vec[1], nearest_node.z + vec[2])
        return node
    elif dim == 2:
        vec = np.array([node.x - nearest_node.x, node.y-nearest_node.y])
        vec = (vec / np.linalg.norm(vec)) * delta
        node = Node(nearest_node.x + vec[0], nearest_node.y + vec[1])
        return node


def collision(node1, node2, obstacles):
    ## only works for 2d

    for obst in obstacles:
        if isinstance(node1, Node):
            if LineString([(node1.x, node1.y), (node2.x, node2.y)]).intersects(obst):
                #print("collision detected")
                return True
        else:
            if LineString([(node1[0], node1[1]), (node2[0], node2[1])]).intersects(obst):
                return True
    else:
        #print("no collision")
        return False


def nn(node, tree):
    return sorted(tree, key=lambda n: distance(n, node))[0]


def distance(node1, node2, dim=2):
    if dim==3:
        return np.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2 + (node1.z - node2.z)**2)
    else:
        return np.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)


class RRT():
    def __init__(self, animation=False, dim=2):
        self.tree = []
        self.delta = 1
        self.alpha = 0.75
        self.animation = animation
        self.dim = dim
    

    def __call__(self, sample_area, n_iters, start, goal, obstacles):
        self.start = start
        self.goal = goal
        self.obstacles = obstacles
        self.tree = [self.start]
        
        # Run till tne number of iterations are not reached
        time1 = time.time()
        while n_iters >= 0:
            # genertae goal node, biased to return goal as the node with a probability alpha
            node = generate_node(sample_area, self.alpha, self.goal ,dim=self.dim)

            #look for the nearest node in the tree 
            nearest_node = nn(node, self.tree)

            # If distacne to the the nearest node is greater than the threshold

            if distance(node, nearest_node,dim=self.dim) > self.delta:
                
                # Make a new node and then check for collision
                node = lineTo(node, nearest_node, self.delta,dim=self.dim)
                
                # if no collision , then add it to the tree
                if not collision(node, nearest_node, self.obstacles):
                    #print("added")
                    node.parent = nearest_node
                    self.tree.append(node)
            
            # Else, 
            else:
                # Check for collision, If no collision add it to the tree
                if not collision(node, nearest_node, self.obstacles):
                    #print("added")
                    node.parent = nearest_node
                    self.tree.append(node)

            # If you approach the goal node, break the loop
            if abs(node.x - self.goal.x) < 0.01 and abs(node.y - self.goal.y) < 0.01 and abs(node.z - self.goal.z) < 0.01:
                #print("goal reached")
                break
            if self.animation:
                self.animate()
            # Count iteration as done
            n_iters -= 1

        #print([(node.x, node.y, node.z) for node in self.tree])
        
        path = self.get_path()

        optim_path = self.optimised_path(path)
        # print(time.time() - time1)
        return path[::-1], optim_path[::-1]

    def get_path(self):
        
        current = self.tree[-1]        
        path = [(current.x, current.y, current.z)]
        while current.parent != None:
            path.append((current.parent.x, current.parent.y, current.parent.z))
            current = current.parent
        return path

    def optimised_path(self, path):
        optimized_path = [path[0]]
        current_index = 0
        while current_index < len(path) - 1:

            # Keep track of whether index has been updated or not
            index_updated = False

            # Loop from last point in path to the current one, checking if
            # any direct connection exists.
            for lookahead_index in range(len(path) - 1, current_index, -1):
                if not collision(
                    path[current_index], path[lookahead_index], self.obstacles
                ):
                    # If direct connection exists then add this lookahead point to optimized
                    # path directly and skip to it for next iteration of while loop
                    optimized_path.append(path[lookahead_index])
                    current_index = lookahead_index
                    index_updated = True
                    break

            # If index hasnt been updated means that there was no LOS shortening
            # and the edge between current and next point passes through an obstacle.
            if not index_updated:
                # In this case we return the path so far
                return optimized_path

        return optimized_path
    def animate(self):
        pass

