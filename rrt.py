"""

Path planning Sample Code with Randomized Rapidly-Exploring Random Trees (RRT)

author: AtsushiSakai(@Atsushi_twi)

"""

import math
import random

import matplotlib.pyplot as plt
# from RRTStar.cost_map import CostMap, Vehicle

show_animation = True


class RRT:
    """
    Class for RRT planning
    """

    class Node:
        """
        RRT Node
        """

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.parent = None

    def __init__(self, start, goal, obstacle_list,
                 rand_area, expand_dis=1.0, goal_sample_rate=5, max_iter=500):
        """
        Setting Parameter

        start:Start Position [x,y]
        goal:Goal Position [x,y]
        obstacleList:obstacle Positions [[x,y,size],...]
        randArea:Ramdom Samping Area [min,max]

        """
        self.start = self.Node(start[0], start[1])
        self.end = self.Node(goal[0], goal[1])
        self.expand_dis = expand_dis
        self.goal_sample_rate = goal_sample_rate
        self.max_iter = max_iter
        self.obstacleList = obstacle_list
        self.node_list = []
        self.min_rand_x = rand_area[0]
        self.max_rand_x = rand_area[1]
        self.min_rand_y = rand_area[2]
        self.max_rand_y = rand_area[3]

    def planning(self, animation=True):
        """
        rrt path planning

        animation: flag for animation on or off
        """

        self.node_list = [self.start]
        for i in range(self.max_iter):
            rnd = self.get_random_point()
            nearest_ind = self.get_nearest_list_index(self.node_list, rnd)
            nearest_node = self.node_list[nearest_ind]

            new_node = self.steer(rnd, nearest_node)
            new_node.parent = nearest_node

            if not self.check_collision(new_node, self.obstacleList):
                continue

            self.node_list.append(new_node)
            print("nNodelist:", len(self.node_list))

            # check goal
            if self.calc_dist_to_goal(new_node.x, new_node.y) <= self.expand_dis:
                print("Goal!!")
                return self.generate_final_course(len(self.node_list) - 1)

            if animation and i % 5:
                self.draw_graph(rnd)

        return None  # cannot find path

    def steer(self, rnd, nearest_node):
        new_node = self.Node(rnd[0], rnd[1])
        d, theta = self.calc_distance_and_angle(nearest_node, new_node)
        if d > self.expand_dis:
            new_node.x = nearest_node.x + self.expand_dis * math.cos(theta)
            new_node.y = nearest_node.y + self.expand_dis * math.sin(theta)

        return new_node

    def generate_final_course(self, goal_ind):
        path = [[self.end.x, self.end.y]]
        node = self.node_list[goal_ind]
        while node.parent is not None:
            path.append([node.x, node.y])
            node = node.parent
        path.append([node.x, node.y])

        return path

    def calc_dist_to_goal(self, x, y):
        dx = x - self.end.x
        dy = y - self.end.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def get_random_point(self):
        if random.randint(0, 100) > self.goal_sample_rate:
            rnd = [random.uniform(self.min_rand_x, self.max_rand_x),
                   random.uniform(self.min_rand_y, self.max_rand_y)]
        else:  # goal point sampling
            rnd = [self.end.x, self.end.y]
        return rnd

    def draw_graph(self, rnd=None):
        plt.clf()
        plt.contourf(self.map.mesh_grid[0], self.map.mesh_grid[1], self.map.cost_map)
        if rnd is not None:
            plt.plot(rnd[0], rnd[1], "^k")
        for node in self.node_list:
            if node.parent:
                plt.plot([node.x, node.parent.x],
                         [node.y, node.parent.y],
                         "-y")

        for (ox, oy, size) in self.obstacleList:
            plt.plot(ox, oy, "ok", ms=30 * size)

        plt.plot(self.start.x, self.start.y, "xr")
        plt.plot(self.end.x, self.end.y, "xr")
        plt.axis([self.min_rand_x, self.max_rand_x, self.min_rand_y, self.max_rand_y])
        plt.axis('equal')
        plt.grid(True)
        plt.pause(0.01)

    def calc_dist_to_end(self, from_node):
        d = []
        dx = []
        dy = []
        for goal in self.end.goals:
            dx.append(goal[0] - from_node.x)
            dy.append(goal[1] - from_node.y)
            d.append(math.sqrt(dx[len(dx) - 1] ** 2 + dy[len(dy) - 1] ** 2))
        d_min = min(d)
        idx = d.index(d_min)
        theta_min = math.atan2(dy[idx], dx[idx])
        return d_min, theta_min

    @staticmethod
    def get_nearest_list_index(node_list, rnd):
        dlist = [(node.x - rnd[0]) ** 2 + (node.y - rnd[1])
                 ** 2 for node in node_list]
        minind = dlist.index(min(dlist))

        return minind

    @staticmethod
    def check_collision(node, obstacleList):
        for (ox, oy, size) in obstacleList:
            dx = ox - node.x
            dy = oy - node.y
            d = dx * dx + dy * dy
            if d <= size ** 2:
                return False  # collision

        return True  # safe

    @staticmethod
    def calc_distance_and_angle(from_node, to_node):
        dx = to_node.x - from_node.x
        dy = to_node.y - from_node.y
        d = math.sqrt(dx ** 2 + dy ** 2)
        theta = math.atan2(dy, dx)
        return d, theta



def main(gx=5.0, gy=10.0):
    print("start " + __file__)

    # ====Search Path with RRT====
    obstacleList = [
        (5, 5, 1),
        (3, 6, 2),
        (3, 8, 2),
        (3, 10, 2),
        (7, 5, 2),
        (9, 5, 2)
    ]  # [x,y,size]
    # Set Initial parameters
    rrt = RRT(start=[0, 0],
              goal=[gx, gy],
              rand_area=[-2, 15],
              obstacle_list=obstacleList)
    path = rrt.planning(animation=show_animation)

    if path is None:
        print("Cannot find path")
    else:
        print("found path!!")

        # Draw final path
        if show_animation:
            rrt.draw_graph()
            plt.plot([x for (x, y) in path], [y for (x, y) in path], '-r')
            plt.grid(True)
            plt.pause(0.01)  # Need for Mac
            plt.show()


if __name__ == '__main__':
    main()
