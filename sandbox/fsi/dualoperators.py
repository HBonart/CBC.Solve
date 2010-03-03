from dolfin import *
from cbc.common import CBCSolver
from cbc.twist.kinematics import SecondOrderIdentity
from numpy import array, append, zeros


# Define the Jacobian matrices and determinants
def F(u):
    I = SecondOrderIdentity(u)
    F = (I + grad(u)) 
    return F

def F_inv(u):
    I = SecondOrderIdentity(u)
    F_inv  = inv((I + grad(u)))
    return F_inv

def F_T(u):
    I = SecondOrderIdentity(u)
    F_T  = ((I + grad(u))).T
    return F_T

def F_invT(u):
    I = SecondOrderIdentity(u)
    F_invT  = (inv((I + grad(u)))).T
    return F_invT

def J(u):
    I = SecondOrderIdentity(u)
    J = det(I + grad(u))
    return J

# DJ(u,w) is J(u) linearized around w (w = test function)
def DJ(u,w):
    DJ = w[0].dx(0)*(1 - u[1].dx(1)) - w[0].dx(1)*u[1].dx(0) \
        -w[1].dx(0)*u[0].dx(1) + w[1].dx(1)*(1 + u[0].dx(0))
    return DJ

def I(u):
    I = SecondOrderIdentity(u)
    return I

def sym_gradient(u):
    sym_gradient = 0.5*(grad(u)+ grad(u).T)
    return sym_gradient
    
# Define constants FIXME: Move !!!
rho_F = 1
mu_F = 1
mu_S = 1
lamb_S = 1
mu_M = 1 
lamb_M = 1

def sigma_M(u):
    return 2.0*mu_M*sym_gradient(u) + lamb_M*tr(sym_gradient(u))*I(u)


# mfile = File("matrix.m")
# mfile << dual_matrix
# import sys
# sys.exit(1)