## The error is estimated using the stored primal and dual velocities
## and pressures.

from dolfin import *
from css_common import *

# Create the mesh
mesh      = UnitSquare(24, 24)
meshes    = []

# Some useful fields related to the geometry
h = CellSize(mesh)
n = FacetNormal(mesh)
def tgt(n):
    return [n[1], -n[0]]

# Load primal and dual solutions
uh  = Function(vector)
uh1 = Function(vector)
ph  = Function(scalar)
wh  = Function(vector)
wh1 = Function(vector)
rh  = Function(scalar)

# Test and trial functions
v = TestFunction(vector)
Pv = TrialFunction(vector)

# Other functions
f  = Constant((0.0, 0.0))
R1 = Function(vector)

mesh_pvd = File("paraview/css/meshes.pvd")

for t in t_range:
   
    useries.retrieve(uh.vector(), t)
    pseries.retrieve(ph.vector(), t)
    wseries.retrieve(wh.vector(), T - t) # Retrieve at a fake time
    rseries.retrieve(rh.vector(), T - t) # Retrieve at a fake time
    
    # Calculate residuals and project them to piecewise constant spaces
    #    R1 = (uh1 - uh)/k + mult(grad(uh), uh) - div(sigma(uh, ph)) - f
    #    R1 = project(uh, vectorDG)
    L = (1/k)*inner(v, uh1 - uh)*dx + inner(v, grad(uh)*uh)*dx \
        + inner(sym(grad(v)), sigma(uh, ph))*dx - inner(v, f)*dx \
        - nu*inner(v, grad(uh).T*n)*ds + inner(v, ph*n)*ds
    a = inner(Pv, v)*dx

    A = assemble(a)
    b = assemble(L)
    solve(A, R1.vector(), b)

#    plot(R1, title='Residual 1 over time')

#     # Calculate derivatives of dual fields
#     # FIXME: Add time derivative contributions here
#     DW = project(div(wh), scalarDG)

# #    plot(DW, title='Divergence of the dual velocity')

#     # Determine error indicators
#     h = array([c.diameter() for c in cells(mesh)])

#     E = zeros(mesh.num_cells())
#     E1 = zeros(mesh.num_cells())
#     E2 = zeros(mesh.num_cells())
	
#     vectorval = array((0.0, 0.0))
#     scalarval = array((0.0))
	
#     i = 0

#     for c in cells(mesh):  
#         x = array((c.midpoint().x(), c.midpoint().y()))
#         R1.eval(vectorval, x)
#         DW.eval(scalarval, x)
#         E1[i] = sqrt(vectorval[0]**2 + vectorval[1]**2)*abs(scalarval)
#         E[i] = h[i]*E1[i]
#         i = i + 1
	
#     Enorm = 0
#     for i2 in range(mesh.num_cells()):
#         Enorm  = Enorm + abs(E[i2])*h[i2]*h[i2]
#     #   Enorm = Enorm + h[i2]*h[i2] # Check area
	           
#     print "*************************"
#     print Enorm
#     print "*************************"

#     cell_markers = MeshFunction("bool", mesh, mesh.topology().dim())
#     marker = sorted(E, reverse=True)[int(len(E)*REFINE_RATIO)]
	    
#     for c in cells(mesh):
#         cell_markers.set(c, bool(E[c.index()] > marker))   

#     mesh_temp = UnitSquare(24, 24)
#     mesh_temp.refine(cell_markers)
#     scalarDG_temp = FunctionSpace(mesh_temp, "DG", 0)
#     meshes.append(mesh_temp)
# #    plot(mesh_temp)
#     h_temp = CellSize(mesh_temp)
# #     plot(h_temp)
#     h_temp = project(h_temp, scalarDG_temp)
#     mesh_pvd << h_temp
    
    
# #     mesh.smooth()
# #     mesh.smooth()
# #     mesh.smooth()

# raw_input()

# # for j in range(N):
# #     plot(meshes[j], title="Refined meshes")
