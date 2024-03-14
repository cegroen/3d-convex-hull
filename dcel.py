import numpy as np


class Vertex:
    num_of_v = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.point = (self.x, self.y, self.z)
        self.edge = None
        self.conflict_face = None
        self.interior = False
        self.num = Vertex.num_of_v
        Vertex.num_of_v += 1

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self) -> str:
        return f"v{self.num}"

    def __repr__(self) -> str:
        return f"v{self.num}"


class HalfEdge:
    def __init__(self, v1, v2):
        self.origin = v1
        self.end = v2
        self.twin = None
        self.face = None
        self.next = None
        self.prev = None

    def __hash__(self):
        return hash((self.origin, self.end))

    def __eq__(self, other):
        return self.origin == other.origin and self.end == other.end

    def __str__(self) -> str:
        if self.prev is None and self.next is None:
            return f"Edge: {self.origin}-{self.end}, From: {self.origin}, Twin:{self.twin.origin}-{self.twin.end}, Face: {self.face}, Next: TBD, Prev: TBD"

        elif self.next is None:
            return f"Edge: {self.origin}-{self.end}, From: {self.origin}, Twin: {self.twin.origin}-{self.twin.end}, Face: {self.face}, Next: TBD, Prev: {self.prev.origin}-{self.prev.end}"

        elif self.twin is None:
            return f"Edge: {self.origin}-{self.end}, From: {self.origin}, Twin: TBD, Face: {self.face}, Next: {self.next.origin}-{self.next.end}, Prev: {self.prev.origin}-{self.prev.end}"
        elif self.prev is None:
            return f"Edge: {self.origin}-{self.end}, From: {self.origin}, Twin: {self.twin.origin}-{self.twin.end}, Face: {self.face}, Next: {self.next.origin}-{self.next.end}, Prev: TBD"

        return f"Edge: {self.origin}-{self.end}, From: {self.origin}, Twin: {self.twin.origin}-{self.twin.end}, Face: {self.face}, Next: {self.next.origin}-{self.next.end}, Prev: {self.prev.origin}-{self.prev.end}"

    def __repr__(self) -> str:
        if self.twin is None:
            return f"Edge: {self.origin}-{self.end}, From: {self.origin}, Twin: TBD, Face: {self.face}, Next: {self.next.origin}-{self.next.end}, Prev: {self.prev.origin}-{self.prev.end}"
        elif self.prev is None:
            return f"Edge: {self.origin}-{self.end}, From: {self.origin}, Twin: {self.twin.origin}-{self.twin.end}, Face: {self.face}, Next: {self.next.origin}-{self.next.end}, Prev: TBD"

        if self.next is None:
            return f"Edge: {self.origin}-{self.end}, From: {self.origin}, Twin: {self.twin.origin}-{self.twin.end}, Face: {self.face}, Next: TBD, Prev: {self.prev.origin}-{self.prev.end}"

        if self.prev is None and self.next is None:
            return f"Edge: {self.origin}-{self.end}, From: {self.origin}, Twin: {self.twin.origin}-{self.twin.end}, Face: {self.face}, Next: TBD, Prev: TBD"

        return f"Edge: {self.origin}-{self.end}, From: {self.origin}, Twin: {self.twin.origin}-{self.twin.end}, Face: {self.face}, Next: {self.next.origin}-{self.next.end}, Prev: {self.prev.origin}-{self.prev.end}"


class Face:
    num_of_faces = 0

    def __init__(self, edge):
        self.edge = edge
        self.num = Face.num_of_faces
        self.conflict_vertices = []
        Face.num_of_faces += 1

        # gets the points incident on a face f

    def get_points(self):
        edges = self.get_edges()
        points = []

        for e in edges:
            points.append(e.origin.point)

        return points

    def get_vertices(self):
        edges = self.get_edges()
        vertices = []

        for e in edges:
            vertices.append(e.origin)

        return vertices

    def get_edges(self):
        starting_edge = self.edge
        edges = [starting_edge]
        temp = starting_edge.next

        while temp != starting_edge:
            edges.append(temp)
            temp = temp.next

        return edges

    def get_face_half_edges(self):
        starting_edge = self.edge
        edges = [starting_edge, starting_edge.twin]
        temp = starting_edge.next

        while temp != starting_edge:
            edges.append(temp)
            edges.append(temp.twin)
            temp = temp.next

        return edges

    def print_face_edges(self):
        stuff = self.get_face_half_edges()
        for e in stuff:
            print(e)

    def __eq__(self, other):
        return self.num == other.num

    def __str__(self) -> str:
        return f"f{self.num}"

    def __repr__(self):
        return f"f{self.num}"


class DCEL:
    # v-list = vertices first three are ones in the same plane
    def __init__(self, v_list: list):
        self.vers = v_list
        self.edges = []
        self.faces = []

        temp_edges = []
        # make the vertices and their twins
        for i in range(len(self.vers) - 1):
            v = self.vers[i]
            v1 = self.vers[(i + 1) % 3]
            e = HalfEdge(v, v1)
            twin = HalfEdge(v1, v)

            v.edge = e
            twin.edge = twin

            e.twin = twin
            twin.twin = e

            self.edges.append(e)
            temp_edges.append(e)
            self.edges.append(twin)

        # make inner face 
        face = Face(temp_edges[0])
        self.faces.append(face)
        for i in range(len(temp_edges)):
            edge = temp_edges[i]
            edge.face = face
            twin = edge.twin
            edge.next = temp_edges[(i + 1) % 3]
            edge.prev = temp_edges[i - 1]

            twin.next = temp_edges[i - 1].twin
            twin.prev = temp_edges[(i + 1) % 3].twin

        # add the other vertex
        v3 = self.vers[3]
        twins = {}
        for i in range(len(temp_edges)):
            e = temp_edges[i].twin
            e1 = HalfEdge(v3, e.origin)
            e2 = HalfEdge(e.end, v3)

            self.edges.append(e1)
            self.edges.append(e2)

            # connect cycle and make face
            e.next = e2
            e.prev = e1

            e2.next = e1
            e2.prev = e

            e1.next = e
            e1.prev = e2

            self.create_face(e, e1, e2)

            # check if twin exist or not add entry
            e1_twin = (e1.end, e1.origin)
            e2_twin = (e2.end, e2.origin)
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
        # for e in self.edges:
        # print(e)
        # print()

    # def __init__(self, v_list: list):
    #     self.vertices = v_list
    #     self.edges = []
    #     self.faces = []
    # 
    #     # make edges
    #     for i in range(3):
    #         # v1, v3 -> v2,v1 -> v3,v2
    #         e = HalfEdge(v_list[i], v_list[(i - 2) % 3])
    #         v_list[i].edge = e
    #         self.edges.append(e)
    #         twin = HalfEdge(v_list[(i - 2) % 3], v_list[i])
    #         v_list[i].edge.twin = twin
    #         self.edges.append(twin)
    # 
    #         # update the twins
    #         e.twin = twin
    #         twin.twin = e
    # 
    #     # update next and previous
    #     for i in range(0, len(self.edges), 2):
    #         e = self.edges[i]
    #         twin = self.edges[i + 1]
    #         twin.next = self.edges[i - 2].twin
    #         e.next = self.edges[(i + 2) % 6]
    #         twin.prev = self.edges[(i + 2) % 6].twin
    #         e.prev = self.edges[i - 2]
    # 
    #     # add inner face
    #     self.faces.append(Face(self.edges[0]))
    # 
    #     # update faces for edges in list
    #     for i in range(0, len(self.edges), 2):
    #         e = self.edges[i]
    # 
    #         # update face to be inner face
    #         e.face = self.faces[0]
    # 
    #     # add edges of the vertex not in the same plane
    #     v4 = self.vertices[3]
    #     for i in range(0, len(self.edges), 2):
    #         v_i = self.edges[i].origin
    #         e = HalfEdge(v_i, v4)
    #         self.edges.append(e)
    #         twin = HalfEdge(v4, v_i)
    #         self.edges.append(twin)
    #         e.twin = twin
    #         twin.twin = e
    # 
    #         # if my drawings are correct this works
    #         e_twin_next = self.edges[i].twin.next
    #         e.prev = self.edges[i].twin
    # 
    #         # update the next of e
    #         self.edges[i].twin.next = e
    # 
    #         # update the next of the twin.twin
    #         twin.next = e_twin_next
    #         e_twin_next.prev = twin
    # 
    #     # connect future next and make faces
    #     for i in range(3):
    #         # twin that needs previous
    #         e = self.vertices[i].edge.twin
    #         e.next.next = e.prev
    #         e.prev.prev = e.next
    #         face = Face(e)
    # 
    #         # update the faces of the other stuff
    #         e.face = face
    #         e.next.face = face
    #         e.next.next.face = face
    #         self.faces.append(face)

    def print_convex_hull(self):
        s = ""

        for f in self.faces:
            edges = f.get_edges()
            s += f"{f}:"
            for e in edges:
                # temp = f"[{e.origin.point},{e.end.point}], "
                temp = f"{e.origin}-{e.end}, "
                s += temp
            s = f"{s[:-2]}\n"

        return s

    def print_convex_hull_e(self):
        s = ""

        for f in self.faces:
            edges = f.get_edges()
            s += f"{f}:\n"
            for e in edges:
                # temp = f"[{e.origin.point},{e.end.point}], "
                temp = f"{e}\n "
                s += temp
            s = f"{s[:-2]}\n"

        return s

    def add_edge(self, edge):
        self.edges.append(edge)

    def create_face(self, e1, e2, e3):
        f = Face(e1)
        self.faces.append(f)
        e1.face = f
        e2.face = f
        e3.face = f
        return f

    def __str__(self) -> str:
        ret_str = ""
        for e in self.edges:
            ret_str = ret_str + e.__str__() + "\n"
        return ret_str

    def __repr__(self) -> str:
        ret_str = ""
        for e in self.edges:
            ret_str = ret_str + e.__str__() + "\n"
        return ret_str
