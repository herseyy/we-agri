import math
import heapq
from typing import List, Dict, Union


def squared_euclidean(p: List[float], q: List[float]) -> float:
    d = 0
    for i in range(len(p)):
        d += (p[i] - q[i]) ** 2
    return d


def euclidean(p: List[float], q: List[float]) -> float:
    return math.sqrt(squared_euclidean(p, q))


class Node:
    def __init__(self, obj: Union[Dict[str, float], List[float]], dimension: int, parent):
        self.obj = obj
        self.left = None
        self.right = None
        self.parent = parent
        self.dimension = dimension


class KDTree:
    def __init__(self, points: Union[Dict[str, int], List[List[float]]], metric):
        if not isinstance(points, list):
            self.dimensions = points['dimensions']
            self.root = self.restore_parent(points)
        else:
            self.dimensions = list(range(len(points[0])))
            self.root = self.build_tree(points, 0, None, self.dimensions)
        self.metric = metric

    def to_json(self) -> Node:
        return self.to_json_impl(self.root)

    @staticmethod
    def to_json_impl(src: Node) -> Node:
        dest = Node(src.obj, src.dimension, None)
        if src.left:
            dest.left = KDTree.to_json_impl(src.left)
        if src.right:
            dest.right = KDTree.to_json_impl(src.right)
        return dest

    def restore_parent(self, root: Node):
        if root.left:
            root.left.parent = root
            self.restore_parent(root.left)
        if root.right:
            root.right.parent = root
            self.restore_parent(root.right)

    def build_tree(self, points: List[List[float]], depth: int, parent: Node, dimensions: List[int]) -> Node:
        if not points:
            return None

        axis = depth % len(dimensions)
        points.sort(key=lambda x: x[axis])
        median = len(points) // 2

        node = Node(points[median], dimensions[axis], parent)
        node.left = self.build_tree(points[:median], depth + 1, node, dimensions)
        node.right = self.build_tree(points[median + 1:], depth + 1, node, dimensions)
        return node

    def nearest(self, point: List[float], max_nodes: int, max_distance: float = None) -> List[float]:
        best_nodes = []

        def nearest_search(node: Node):
            dimension = self.dimensions[node.dimension]
            own_distance = self.metric(point, node.obj)
            linear_point = {}
            best_child, linear_distance, other_child = None, None, None

            def save_node(node, distance):
                heapq.heappush(best_nodes, (-distance, node))
                if len(best_nodes) > max_nodes:
                    heapq.heappop(best_nodes)

            for i in range(len(self.dimensions)):
                if i == node.dimension:
                    linear_point[self.dimensions[i]] = point[self.dimensions[i]]
                else:
                    linear_point[self.dimensions[i]] = node.obj[self.dimensions[i]]

            linear_distance = self.metric(linear_point, node.obj)

            if node.right is None and node.left is None:
                if len(best_nodes) < max_nodes or own_distance < -best_nodes[0][0]:
                    save_node(node, own_distance)
                return

            if node.right is None:
                best_child = node.left
            elif node.left is None:
                best_child = node.right
            else:
                if point[dimension] < node.obj[dimension]:
                    best_child = node.left
                else:
                    best_child = node.right

            nearest_search(best_child)

            if len(best_nodes) < max_nodes or own_distance < -best_nodes[0][0]:
                save_node(node, own_distance)

            if len(best_nodes) < max_nodes or abs(linear_distance) < -best_nodes[0][0]:
                if best_child == node.left:
                    other_child = node.right
                else:
                    other_child = node.left
                if other_child is not None:
                    nearest_search(other_child)

        if max_distance is not None:
            for i in range(max_nodes):
                heapq.heappush(best_nodes, (float('-inf'), None))

        if self.root is not None:
            nearest_search(self.root)

        result = []
        for item in best_nodes:
            if item[1] is not None:
                result.append((item[1].obj, -item[0]))
        return result


def predict_weather(test_data):
    training = {
        "data": [
            [18, 19, 20, 21, 22, 0, 1, 1],
            [17, 18, 19, 20, 21, 1, 1, 0],
            [19, 20, 21, 22, 23, 1, 1, 0],
            [20, 21, 22, 23, 24, 2, 1, 0],
            [19, 20, 21, 22, 23, 1, 1, 0],
            [22, 23, 24, 25, 26, 3, 1, 0],
            [23, 24, 25, 26, 27, 2, 1, 0]
        ],
        "label": [1, 1, 1, 0, 0, 0, 1]
    }

    kdtree = KDTree(training["data"], metric=euclidean)
    neighbors = kdtree.nearest(test_data, 3)

    labels = [neighbor[0][-1] for neighbor in neighbors]

    ones = labels.count(1)
    zeros = labels.count(0)

    return 1 if ones > zeros else 0


test_data = [23, 24, 25, 26, 27, 2, 1]
predicted_weather = predict_weather(test_data)
print(f"The predicted weather is: {predicted_weather}")

