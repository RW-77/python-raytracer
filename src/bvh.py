import random, sys
import settings
from utils import Interval, Ray
from hittable_list import HitRecord, Hittable, HittableList, AABB


class BVH_Node(Hittable):
    """
    Represents a node in a BVH tree.
    """

    def __init__(self, depth: int = 0) -> None:
        """Constructs a BVH node from a `HittableList`."""

        self.bbox: AABB = None
        # left and right could either be `BVH_Node` or `Hittable` objects like a sphere, triangle, etc.
        self.left: 'Hittable' = None
        self.right: 'Hittable' = None
        self.depth: int = depth
    
    def __str__(self) -> str:
        return f"bbox: \n{self.bbox}\n\nleft: \n{type(self.left)}\n\nright: \n{type(self.right)}\n"

    @property
    def bounding_box(self):
        return self.bbox

    def hit(self, _r: Ray, ray_t: Interval) -> HitRecord | None:
        """
        Returns whether the BVH node is hit by the incident ray (should not update the hit_record for AABB intersections).
        """
        settings.count += 1
        # sys.stderr.write(f"BVH_Node depth: {self.depth}\n")
        # does the ray intersect the AABB of this BVH_Node?
        if not self.bbox.hit(_r, ray_t):
            # AABB.hit() returns False
            # sys.stderr.write(f"BVH search terminated at depth: {self.depth}\n")
            settings.max_depth = max(settings.max_depth, self.depth)
            return None

        # recursively searches the binary tree for possible hit, with the smallest AABB being an individual object
        rec_left: HitRecord | None = self.left.hit(_r, ray_t)
        # if rec_left is not None:
        #     sys.stderr.write(f"rec_left hit sphere at point {rec_left.p} at t = {rec_left.t}\n")
        #     sys.stderr.write(f"rec_right will search along interval ({ray_t.lower_b}, {rec_left.t}\n")
        # else:
        #     sys.stderr.write(f"rec_left is None")
        rec_right: HitRecord | None = self.right.hit(_r, Interval(ray_t.lower_b, rec_left.t if rec_left is not None else ray_t.upper_b))

        # return rec_left or rec_right if the other is None
        if rec_left is not None and rec_right is None:
            return rec_left
        elif rec_right is not None:
            return rec_right
        # if nothing is hit, return None
        else:
            return None


class BVH_Tree(Hittable):

    def __init__(self, hit_list: HittableList) -> None:
        """
        Constructs the BVH tree from a `HittableList` by calling the recursive constructor.
        """

        self.root: BVH_Node = BVH_Node(depth=1)  # even if `len(hit_list)` = 1, root will be a `BVH_Node`
        self.construct_bvh_tree(self.root, hit_list.objects[:], 0, len(hit_list.objects))

    @property
    def bounding_box(self):
        return self.root.bbox
    
    def print_bfs(self) -> str:
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            sys.stderr.write("_" * 50 + "\n")
            sys.stderr.write(f"{node}\n")
            sys.stderr.write("_" * 50 + "\n")
            if isinstance(node.left, BVH_Node):
                queue.append(node.left)
            if isinstance(node.right, BVH_Node):
                queue.append(node.right)
        

    def hit(self, _r: Ray, ray_t: Interval) -> HitRecord | None:
        """
        Returns the hit record of the BVH tree by returning `root.hit()`.
        If nothing is hit, returns `None`.
        """
        rec: HitRecord = self.root.hit(_r, ray_t)
        return rec

    def box_compare(self, _a: Hittable, _b: Hittable, axis: int) -> bool:
        match axis:
            case 0:
                return _a.bounding_box.slab_x.lower_b < _b.bounding_box.slab_x.lower_b
            case 1:
                return _a.bounding_box.slab_y.lower_b < _b.bounding_box.slab_y.lower_b
            case 2:
                return _a.bounding_box.slab_z.lower_b < _b.bounding_box.slab_z.lower_b

    def x_axis_key(self, h: Hittable) -> float:
        return h.bounding_box.slab_x.lower_b

    def y_axis_key(self, h: Hittable) -> float:
        return h.bounding_box.slab_y.lower_b

    def z_axis_key(self, h: Hittable) -> float:
        return h.bounding_box.slab_z.lower_b

    def construct_bvh_tree(self, curr_node: BVH_Node, objects: list[Hittable], start: int, end: int) -> None:

        # randomly choose axis (either x, y, or z)
        axis = random.randint(0, 2)
        axis_key = self.x_axis_key if axis == 0 else self.x_axis_key if axis == 1 else self.z_axis_key

        # length of subarray
        object_span: int = end - start

        # sort subarray using randomly chosen axis
        if object_span == 1:  # base case 1
            # left and right are assigned to `Hittable`s
            curr_node.left = objects[start]
            curr_node.right = objects[start]
        elif object_span == 2:  # base case 2
            # left and right are assigned to `Hittable`s
            if self.box_compare(objects[start], objects[start + 1], axis):
                curr_node.left = objects[start]
                curr_node.right = objects[start + 1]
            else:
                curr_node.left = objects[start + 1]
                curr_node.right = objects[start]
        else:
            objects[start:end] = sorted(objects[start:end], key=axis_key)

            mid: int = start + (object_span // 2)

            # this creates the BVH_Nodes, the only actual data field is the bbox (AABB) 
            # which is formed after the last recursive call
            curr_node.left = BVH_Node(depth=curr_node.depth+1)
            curr_node.right = BVH_Node(depth=curr_node.depth+1)
            self.construct_bvh_tree(curr_node.left, objects, start, mid)
            self.construct_bvh_tree(curr_node.right, objects, mid, end)

        curr_node.bbox = AABB.merge(curr_node.left.bounding_box, curr_node.right.bounding_box)
