import dcel
import convex_hull_helper as chh
import random


class IncrementalHull3D:
    def __init__(self, points):
        self.points = points
        self.vertices = []

        # convert points to Vertex objects
        for i in range(len(self.points)):
            self.vertices.append(dcel.Vertex(points[i][0], points[i][1], points[i][2]))

        self.hull = dcel.DCEL(self.tetrahedron())  # initially construct a tetrahedron

        random.shuffle(self.vertices)  # randomly permute the rest of the points

        #  initialize conflict faces for all vertices
        for v in self.vertices:
            for f in self.hull.faces:
                if chh.visible(f, v) < 0:
                    v.conflict_face = f
                    f.conflict_vertices.append(v)
                    break

            if v.conflict_face is None:
                v.interior = True  # if there are no visible faces then it must be inside the tetrahedron

        self.build_hull(self.vertices)

    def get_hull(self):
        return self.hull

    # iterates through vertices and incrementally adds them to the hull
    def build_hull(self, v_list):
        for v in v_list:
            if not v.interior:
                self.add_vertex(v)

    def add_vertex(self, v):
        horizon_stuff = self.horizon(v)
        horizon_edges = horizon_stuff[0]
        horizon_faces = horizon_stuff[1]
        twins = {}
        new_edges = []
        new_faces = []
        all_edges = []

        # get edges that need to be deleted before they are altered
        for f in horizon_faces:
            all_edges.extend(f.get_edges())

        # make the new neighbors and faces of the horizon edges 
        for e in horizon_edges:
            e1 = dcel.HalfEdge(v, e.origin)
            e2 = dcel.HalfEdge(e.end, v)

            e1.next = e
            e1.prev = e2
            e2.next = e1
            e2.prev = e
            e.next = e2
            e.prev = e1

            new_face = self.hull.create_face(e, e1, e2)

            new_faces.append(new_face)
            new_edges.append(e1)
            new_edges.append(e2)

            e1_twin = (e1.end, e1.origin)
            e2_twin = (e2.end, e2.origin)

            # check if the new_edges twins are in the hashmap
            if e1_twin in twins.keys():
                twin = twins[e1_twin]
                e1.twin = twin
                twin.twin = e1
                del twins[e1_twin]
            # if not add it 
            else:
                twins[(e1.origin, e1.end)] = e1

            if e2_twin in twins.keys():
                twin = twins[e2_twin]
                e2.twin = twin
                twin.twin = e2
                del twins[e2_twin]
            else:
                twins[(e2.origin, e2.end)] = e2

            self.hull.edges.append(e1)
            self.hull.edges.append(e2)

        # update conflict faces for exterior vertices
        for f in horizon_faces:
            if f.conflict_vertices is not None:
                for v in f.conflict_vertices:
                    v.conflict_face = None

                    # check which of the new cone faces are visible
                    for nf in new_faces:
                        if chh.visible(nf, v) < 0:
                            v.conflict_face = nf
                            nf.conflict_vertices.append(v)
                            break
                    if v.conflict_face is None:
                        v.interior = True

        for e in all_edges:
            if e not in horizon_edges:
                self.hull.edges.remove(e)  # remove edge if it is not on the horizon

        for f in horizon_faces:
            if f in self.hull.faces:
                self.hull.faces.remove(f)  # remove the face

    def tetrahedron(self):
        i = 0
        tetra = []

        # find 3 noncollinear points to start off
        while chh.collinear(self.vertices[i], self.vertices[i + 1], self.vertices[i + 2]):
            if i == len(self.vertices) - 3:
                raise Exception("All points are collinear!")
            i = i + 1

        tetra.extend([self.vertices[i], self.vertices[i + 1], self.vertices[i + 2]])
        del self.vertices[i:i + 3]

        i = 0

        # find another point that is not coplanar with the first 3
        while chh.orient(tetra[0], tetra[1], tetra[2], self.vertices[i]) == 0:
            if i == len(self.vertices) - 3:
                raise Exception("All points are coplanar!")
            i = i + 1

        tetra.append(self.vertices[i])
        self.vertices.remove(self.vertices[i])

        # ensure the first triangle is given in clockwise order
        if chh.orient(tetra[0], tetra[1], tetra[2], tetra[3]) > 0:
            temp = tetra[1]
            tetra[1] = tetra[2]
            tetra[2] = temp

        return tetra

    # calculates edges on the horizon of a vertex
    def horizon(self, v):
        horizon_edges = []  # list of edges around the horizon
        ignore_faces = [v.conflict_face]  # list of faces that have been explored so far
        
        for e in v.conflict_face.get_edges():
            # if neighboring face is not visible then add the current edge and face to horizon
            if chh.visible(e.twin.face, v) >= 0:
                horizon_edges.append(e)
            # otherwise explore the neighboring face
            elif e.twin.face not in ignore_faces:
                self.explore_face(e.twin.face, v, horizon_edges, ignore_faces)

        return horizon_edges, ignore_faces
    
    # recursive method that expores a face to see if there are visible bordering faces
    def explore_face(self, f, v, he, ignore_faces):
        ignore_faces.append(f)

        for e in f.get_edges():
            if chh.visible(e.twin.face, v) >= 0:
                he.append(e)
            elif e.twin.face not in ignore_faces:
                self.explore_face(e.twin.face, v, he, ignore_faces)


if __name__ == "__main__":
    # test_points = [(-2, -4, 0), (1, -3, 4), (3, -4, 0), (1, 0, 0), (-1, -2, 1),(-3, -1, 1),(1, -3, 6), (2, 3, 2)]
    # test_points = chh.sample_spherical(500)
    test_points = chh.random_points(100, 10000)

    test_hull = IncrementalHull3D(test_points).get_hull()

    chh.display_hull(test_hull, test_points)
