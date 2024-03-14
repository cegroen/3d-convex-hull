import convex_hull_helper as chh


# used here instead of Vertex since we are not using a DCEL to store the convex hull
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z) 


# triangle that stores its vertices
class Face:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3


def brute_force_hull_3d(points):
    vertices = []
    hull_faces = []

    # convert point tuples to Point objects
    for i in range(len(points)):
        vertices.append(Point(points[i][0], points[i][1], points[i][2]))
        
    flag = True  # bool that represents whether the face is on the convex hull
    
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            for k in range(j + 1, len(vertices)):
                if not chh.collinear(vertices[i], vertices[j], vertices[k]):
                    flag = True
                    prev_orient = -2  # stores the side of the face that the previous point was on
                    
                    for p4 in vertices:
                        if p4 not in [vertices[i], vertices[j], vertices[k]] and chh.orient(vertices[i], vertices[j], vertices[k], p4) != 0:
                            # if prev_orient hasn't been changed then set it to the current value
                            if prev_orient == -2:
                                prev_orient = chh.orient(vertices[i], vertices[j], vertices[k], p4)
                            # if the current point is on a different side of the face than the
                            # previous point then the face is not a part of the ocnvex hull
                            elif chh.orient(vertices[i], vertices[j], vertices[k], p4) != prev_orient:
                                flag = False
                     
                # if all of the points are to the same side of the face then it is a part of the convex hull 
                if flag:
                    hull_faces.append(Face(vertices[i], vertices[j], vertices[k]))

    return hull_faces


if __name__ == "__main__":
    test_points = chh.sample_spherical(30)
    
    test_hull = brute_force_hull_3d(test_points)
    
    chh.display_hull_2(test_hull, test_points)
