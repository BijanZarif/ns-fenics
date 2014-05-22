'Problems used to test mixed solvers.'

from dolfin import Constant, Mesh, Expression, MeshFunction
from math import pi, cos
import os

# Problem is specified by mesh, domains where Dirichlet bcs should be
# prescribed, Dirichlet values (this includes the inflow profile which
# is a time-dependent expression), the Reynolds number and forcing

# Directory where meshes are stored
mesh_dir = 'meshes'

# Mesh directory aware loading of mesh
mesh_path = lambda mesh: os.path.join(mesh_dir, mesh)


class CylinderFlow(object):
    'Flow past a cylinder'
    name = 'cylinder'
    # Forcing
    f = Constant((0., 0.))

    # Mesh and function marking facets
    mesh = Mesh(mesh_path('cylinder.xml'))
    f_f = MeshFunction('size_t', mesh, mesh_path('cylinder_facet_region.xml'))

    # Inflow and Noslip domains to be used for BC construction
    inflow = [f_f, 13]
    noslip = [f_f, 12]

    Re = Constant(1)
    U_max = 1.5
    u_in = Expression(('4*Um*(x[1]*(ymax-x[1]))*sin(pi*t/8.0)/(ymax*ymax)',
                       '0.0'),
                      Um=U_max, ymax=0.41, t=0)


class LCylinderFlow(object):
    'Flow past a cylinder in the bend of L(V) shaped domain'
    name = 'l-cylinder'
    # Forcing
    f = Constant((0., -1.))

    # Mesh and function marking facets
    mesh = Mesh(mesh_path('l-cylinder.xml'))
    f_f = MeshFunction('size_t', mesh, mesh_path('l-cylinder_facet_region.xml'))

    # Inflow and Noslip domains to be used for BC construction
    inflow = [f_f, 17]
    noslip = [f_f, 16]

    Re = Constant(1000)
    U_max = 3.5
    unit = 0.1
    y_max = 4*unit + 4*unit*cos(pi/4)
    u_in = Expression(('-4*Um*(x[1]*(ymax-x[1]))*sin(pi*t/8.0)/(ymax*ymax)',
                       '+4*Um*(x[1]*(ymax-x[1]))*sin(pi*t/8.0)/(ymax*ymax)'),
                      Um=U_max, ymax=y_max, t=0)

all_problems = [CylinderFlow, LCylinderFlow]
