__author__ = "Kristoffer Selim and Anders Logg"
__copyright__ = "Copyright (C) 2011 Simula Research Laboratory and %s" % __author__
__license__  = "GNU GPL Version 3 or any later version"

# Last changed: 2011-02-16

from fsiproblem import *

# Create application parameters set
application_parameters = Parameters("application_parameters")
application_parameters.add("end_time", 2.0)
application_parameters.add("dt", 0.05)
application_parameters.add("mesh_scale", 32)
application_parameters.add("TOL", 0.1)
application_parameters.add("w_h", 0.45)
application_parameters.add("w_k", 0.45)
application_parameters.add("w_c", 0.1)
application_parameters.add("fraction", 0.5)
application_parameters.add("solve_primal", True)
application_parameters.add("solve_dual", False)
application_parameters.add("estimate_error", False)
application_parameters.add("dorfler_marking", True)
application_parameters.add("uniform_timestep", True)
application_parameters.parse()

# Collect parameters
parameter_info = application_parameters.option_string()

# Define the boundary
sie_boundary = "on_boundary"

# Define problem class
class TaylorGreenVortex(FSI):
    def __init__(self):

        # Define mesh based on a scale factor
        mesh_scale = application_parameters["mesh_scale"]
        mesh = UnitSquare(mesh_scale, mesh_scale)

        # Map to coordinates to [-1, 1]^2
        map = 2*(mesh.coordinates() - 0.5)
        mesh.coordinates()[:, :] = map

        # Save original mesh
        file = File("adaptivity/mesh_0.xml")
        file << mesh

        # Report problem parameters
        mesh_size = mesh.hmin()
        f = open("adaptivity/taylorgreenvortex.txt", "w")
        f.write(parameter_info)
        f.write(str("Mesh size:  ") + (str(mesh_size)) + "\n \n")
        f.close()

        # Define analytical solution for u and p
        self.u_anal = ('-(cos(pi*(x[0]))*sin(pi*(x[1]))) * exp(-2.0*nu*pi*pi*t)',
                       ' (cos(pi*(x[1]))*sin(pi*(x[0]))) * exp(-2.0*nu*pi*pi*t)')
        self.p_anal = '-0.25*(cos(2*pi*(x[0])) + cos(2*pi*(x[1]))) * exp(-4.0*nu*pi*pi*t)'

        # Initialize base class
        FSI.__init__(self, mesh)


    #--- Solver options ---

    def solve_primal(self):
        return application_parameters["solve_primal"]

    def solve_dual(self):
        return application_parameters["solve_dual"]

    def estimate_error(self):
        return application_parameters["estimate_error"]

    def dorfler_marking(self):
        return application_parameters["dorfler_marking"]

    def uniform_timestep(self):
        return application_parameters["uniform_timestep"]


    #--- Common parameters ---

    def end_time(self):
        return application_parameters["end_time"]

    def TOL(self):
        return application_parameters["TOL"]

    def initial_timestep(self):
        return application_parameters["dt"]

    def space_error_weight(self):
        return application_parameters["w_h"]

    def time_error_weight(self):
        return application_parameters["w_k"]

    def non_galerkin_error_weight(self):
        return application_parameters["w_c"]

    def fraction(self):
        return application_parameters["fraction"]

    def evaluate_functional(self, u, p, dt):

        # Compute x-component at the point [0.5, 0.5]
        #functional = u((0.0, 0.5))[0]
        return 0.0
        #return functional

    def __str__(self):
        return "TaylorGreen Vortex test case"


 #--- Fluid parameters ---

    def viscosity(self):
        return 1.0 / 8.0

    def density(self):
        return 1.0

# FIXME: Should the NS solver be based on nu?
    def nu(self, viscosity, density):
        nu = viscosity / rho
        return nu

 # --- Initial conditions  ---

    def velocity_initial_condition(self):
        u = Expression(self.u_anal)
        u.t = 0.0
        return u

    def pressure_initial_condition(self):
        exact_p = Expression(self.p_anal)
        exact_p.t = 0.0
        return exact_p

 # --- Boundary conditions  ---

    def velocity_dirichlet_boundaries(self):
        return [sie_boundary]

    def pressure_dirichlet_boundaries(self):
        return [sie_boundary]

    def velocity_dirichlet_values(self):
        # FIXME: Add when the solver can handle time dependent bcs
        self.u = Expression(self.u_anal)
        self.u.t = 0.0
        return [(self.u)]

    def pressure_dirichlet_values(self):
        # FIXME: Add when the solver can handle time dependent bcs
        self.p = Expression(self.p_anal)
        self.p.t = 0.0
        return [(self.p)]

#     def update_bcs(self, u, p, t):
#         self.u.t = t
#         self.p.t = t

#         return self.u, self.p

# Define problem
problem = TaylorGreenVortex()
problem.parameters["solver_parameters"]["solve_primal"] = problem.solve_primal()
problem.parameters["solver_parameters"]["solve_dual"] = problem.solve_dual()
problem.parameters["solver_parameters"]["estimate_error"] = problem.estimate_error()
problem.parameters["solver_parameters"]["uniform_timestep"]  = problem.uniform_timestep()
problem.parameters["solver_parameters"]["tolerance"] = problem.TOL()

# Solve problem
u, p = problem.solve()


