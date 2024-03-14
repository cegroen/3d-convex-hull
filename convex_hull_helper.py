import random
import numpy
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def cross(a, b):
    return a.x * b.y - b.x * a.y


def collinear(v1, v2, v3):
    return ((v3.z - v1.z) * (v2.y - v1.y) - (v2.z - v1.z) * (v3.y - v1.y) == 0
            and (v2.z - v1.z) * (v3.x - v1.x) - (v2.x - v1.x) * (v3.z - v1.z) == 0
            and (v2.x - v1.x) * (v3.y - v1.y) - (v2.y - v1.y) * (v3.x - v1.x) == 0)


def orient(v1, v2, v3, v4):
    det = (-(v1.z - v4.z) * (v2.y - v4.y) * (v3.x - v4.x) + (v1.y - v4.y) * (v2.z - v4.z) * (v3.x - v4.x)
           + (v1.z - v4.z) * (v2.x - v4.x) * (v3.y - v4.y) - (v1.x - v4.x) * (v2.z - v4.z) * (v3.y - v4.y)
           - (v1.y - v4.y) * (v2.x - v4.x) * (v3.z - v4.z) + (v1.x - v4.x) * (v2.y - v4.y) * (v3.z - v4.z))

    if det < 0:
        return -1
    elif det > 0:
        return 1
    else:
        return 0


# same as orient except it takes a face as a parameter instead of 3 points
def visible(f, v):
    face_vertices = f.get_vertices()

    # 1 = not visible, -1 = visible, 0 = coplanar
    return orient(face_vertices[2], face_vertices[1], face_vertices[0], v)


# displaying the convex hull with matplotlib
def display_hull(hull, points):
    max_coord = points[0][0]
    min_coord = points[0][0]
    hull_points = []

    for p in points:
        point_max = max(p)
        point_min = min(p)
        if point_max > max_coord:
            max_coord = point_max

        if point_min < min_coord:
            min_coord = point_min

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([min_coord, max_coord])
    ax.set_ylim([min_coord, max_coord])
    ax.set_zlim([min_coord, max_coord])
    
    for f in hull.faces:
        triangle = [f.get_points()[0], f.get_points()[1], f.get_points()[2]]
        hull_points.extend(f.get_points())
        face = Poly3DCollection([triangle])
        face.set_color(colors.rgb2hex(numpy.random.rand(3)))
        face.set_edgecolor('k')
        face.set_alpha(0.7)
        ax.add_collection3d(face)

    # uncomment lines below to draw vertices
    vertices = numpy.array(points)
    hull_vertices = numpy.array(hull_points)
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], color='red')
    ax.scatter(hull_vertices[:, 0], hull_vertices[:, 1], hull_vertices[:, 2], color='black')
    
    plt.axis('off')
    plt.show()
    
    
def display_hull_2(hull, points):
    max_coord = points[0][0]
    min_coord = points[0][0]

    for p in points:
        point_max = max(p)
        point_min = min(p)
        if point_max > max_coord:
            max_coord = point_max

        if point_min < min_coord:
            min_coord = point_min

    # displaying the convex hull with matplotlib
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([min_coord, max_coord])
    ax.set_ylim([min_coord, max_coord])
    ax.set_zlim([min_coord, max_coord])

    for f in hull:
        triangle = [(f.p1.x, f.p1.y, f.p1.z), (f.p2.x, f.p2.y, f.p2.z), (f.p3.x, f.p3.y, f.p3.z)]
        face = Poly3DCollection([triangle])
        face.set_color(colors.rgb2hex(numpy.random.rand(3)))
        face.set_edgecolor('k')
        face.set_alpha(1)
        ax.add_collection3d(face)

    plt.axis('off')
    plt.show()


# generates a list of points randomly distributed over the surface of a sphere
def sample_spherical(npoints, ndim=3):
    vec = numpy.random.randn(ndim, npoints)
    vec /= numpy.linalg.norm(vec, axis=0)
    xi, yi, zi = vec
    sphere_points = []
    for i in range(len(xi)):
        sphere_points.append((xi[i] * 10, yi[i] * 10, zi[i] * 10))
    return sphere_points


# randomly generates test points
def random_points(num_pts, coord_range):
    points = []

    for index in range(num_pts):
        points.append((random.randint(-coord_range, coord_range), random.randint(-coord_range, coord_range),
                       random.randint(-coord_range, coord_range)))

    return points
