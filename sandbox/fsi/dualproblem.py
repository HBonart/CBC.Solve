"This module specifies the variational forms for the dual FSI problem."

__author__ = "Kristoffer Selim and Anders Logg"
__copyright__ = "Copyright (C) 2010 Simula Research Laboratory and %s" % __author__
__license__  = "GNU GPL Version 3 or any later version"

# Last changed: 2010-08-11

from dolfin import *
from operators import *

def dual_forms(Omega_F, Omega_S, k, problem,
               v_F,  q_F,  v_S,  q_S,  v_M,  q_M,
               Z_F,  Y_F,  Z_S,  Y_S,  Z_M,  Y_M,
               Z_F0, Y_F0, Z_S0, Y_S0, Z_M0, Y_M0,
               U_F0, P_F0, U_S0, P_S0, U_M0,
               U_F1, P_F1, U_S1, P_S1, U_M1):
    "Return bilinear and linear forms for one time step."

    # Get problem parameters
    rho_F = problem.fluid_density()

    # Define normals
    N_S =  FacetNormal(Omega_S)
    N =  N_S('+')
    N_F = FacetNormal(Omega_F)

    # Fluid eq. linearized around fluid variables
    A_FF01 = -(1/k)*inner((Z_F0 - Z_F), rho_F*J(U_M)*v_F)*dx(0)
    A_FF02 =  inner(Z_F, rho_F*J(U_M)*dot(dot(grad(v_F),F_inv(U_M)), (U_F - (U_M0 - U_M)*(1/k))))*dx(0)
    A_FF03 =  inner(Z_F, rho_F*J(U_M)*dot(grad(U_F) , dot(F_inv(U_M), v_F)))*dx(0)
    A_FF04 =  inner(grad(Z_F), J(U_M)*mu_F*dot(grad(v_F) , dot(F_inv(U_M), F_invT(U_M))))*dx(0)
    A_FF05 =  inner(grad(Z_F), J(U_M)*mu_F*dot(F_invT(U_M) , dot(grad(v_F).T, F_invT(U_M))))*dx(0)
    A_FF06 = -inner(grad(Z_F), J(U_M)*q_F*F_invT(U_M))*dx(0)
    A_FF07 =  inner(Y_F, div(J(U_M)*dot(F_inv(U_M),v_F)))*dx(0)

    # Boundary terms (Neumann condition G_N_F, dS(2) = in, dS(3) = out)
    # Note that we assume an infinte long channel -> grad(U_F) = 0
    G_FF_in_1  = -inner(Z_S('+'), dot(J(U_M)('+')*mu_F*dot(F_invT(U_M)('+') , dot(grad(v_F('+')).T, F_invT(U_M)('+'))), N_F('+')))*dS(2)
    G_FF_in_2  =  inner(Z_S('+'), dot(J(U_M)('+')*q_F('+')*F_invT(U_M)('+'), N_F('+')))*dS(2)
    G_FF_out_1 = -inner(Z_S('+'), dot(J(U_M)('+')*mu_F*dot(F_invT(U_M)('+') , dot(grad(v_F('+')).T, F_invT(U_M)('+'))), N_F('+')))*dS(3)
    G_FF_out_2 =  inner(Z_S('+'), dot(J(U_M)('+')*q_F('+')*F_invT(U_M)('+'), N_F('+')))*dS(3)

    # Collect boundary terms
    G_FF = G_FF_in_1 + G_FF_in_2 + G_FF_out_1 + G_FF_out_2

    # Collect A_FF form
    A_FF = A_FF01 + A_FF02 + A_FF03 + A_FF04 + A_FF05 + A_FF06 + A_FF07 + G_FF

    # Fluid eq. linearized around mesh variable
    A_FM01 =  (1/k)*inner(Z_F, rho_F*DJ(U_M, v_M)*(U_F0 - U_F))*dx(0)
    A_FM02 =  inner(Z_F, rho_F*DJ(U_M, v_M)*dot(grad(U_F), dot(F_inv(U_M), (U_M - U_M0)*(1/k))))*dx(0)
    A_FM03 = -inner(Z_F,  rho_F*J(U_M)*dot((dot(grad(U_F), dot(F_inv(U_M), dot(grad(v_M),F_inv(U_M))))),(U_F - (U_M0 - U_M)/k)))*dx(0)
    A_FM04 =  (1/k)*inner((Z_F0 - Z_F), rho_F*J(U_M)*dot(grad(U_F), dot(F_inv(U_M) ,v_M )))*dx(0)
    A_FM05 =  inner(grad(Z_F), DJ(U_M, v_M)*dot(Sigma_F(U_F, P_F, U_M),F_invT(U_M)))*dx(0)
    A_FM06 = -inner(grad(Z_F), J(U_M)*dot(mu_F*(dot(grad(U_F), dot(F_inv(U_M), dot(grad(v_M), F_inv(U_M))))), F_invT(U_M)))*dx(0)
    A_FM07 = -inner(grad(Z_F), J(U_M)*dot(mu_F*(dot(F_invT(U_M), dot(grad(v_M).T, dot(F_invT(U_M), grad(U_F).T )))), F_invT(U_M)))*dx(0)
    A_FM08 = -inner(grad(Z_F), J(U_M)*dot(mu_F*(dot(grad(U_F), dot(F_inv(U_M), dot(F_invT(U_M), grad(v_M).T )))), F_invT(U_M)))*dx(0)
    A_FM09 = -inner(grad(Z_F), J(U_M)*dot(mu_F*(dot(F_invT(U_M), dot(grad(U_F).T, dot(F_invT(U_M), grad(v_M).T )))), F_invT(U_M)))*dx(0)
    A_FM10 =  inner(grad(Z_F), J(U_M)*dot(dot( P_F*I,F_invT(U_M)) ,  dot(grad(v_M).T ,F_invT(U_M) )))*dx(0)
    A_FM11 =  inner(Y_F, div(DJ(U_M,v_M)*dot(F_inv(U_M), U_F)))*dx(0)
    A_FM12 = -inner(Y_F, div(J(U_M)*dot(dot(F_inv(U_M),grad(v_M)), dot(F_inv(U_M) ,U_F))))*dx(0)

    # Boundary terms (Neumann conditions G_N_F, dS(2) = in, dS(3) = out)
    # Note that we assume an inifinte long channel -> grad(U_F) = 0
    G_FM_in_1 = -inner(Z_F('+'), DJ(U_M, v_M)('+')*mu_F*dot(dot(F_invT(U_M)('+'),grad(U_F('+')).T), dot(F_invT(U_M)('+'), N_F('+'))))*dS(2)
    G_FM_in_2 =  inner(Z_F('+'), DJ(U_M, v_M)('+')*dot(P_F('+')*I('+'), N_F('+')))*dS(2)
    G_FM_in_3 =  inner(Z_F('+'), J(U_M)('+')*mu_F*dot(dot(F_invT(U_M)('+'), dot(grad(v_M('+')).T, F_invT(U_M)('+'))), dot(grad(U_F('+')).T, dot(F_invT(U_M)('+'), N_F('+') ))))*dS(2)
    G_FM_in_4 =  inner(Z_F('+'), J(U_M)('+')*mu_F*dot(dot(F_invT(U_M)('+'), dot(grad(U_F('+')).T, F_invT(U_M)('+'))), dot(grad(v_M('+')).T , dot(F_invT(U_M)('+'),N_F('+')))))*dS(2)
    G_FM_out_1 = -inner(Z_F('+'), DJ(U_M, v_M)('+')*mu_F*dot(dot(F_invT(U_M)('+'),grad(U_F('+')).T), dot(F_invT(U_M)('+'), N_F('+'))))*dS(3)
    G_FM_out_2 =  inner(Z_F('+'), DJ(U_M, v_M)('+')*dot(P_F('+')*I('+'), N_F('+')))*dS(3)
    G_FM_out_3 =  inner(Z_F('+'), J(U_M)('+')*mu_F*dot(dot(F_invT(U_M)('+'), dot(grad(v_M('+')).T, F_invT(U_M)('+'))), dot(grad(U_F('+')).T, dot(F_invT(U_M)('+'), N_F('+') ))))*dS(3)
    G_FM_out_4 =  inner(Z_F('+'), J(U_M)('+')*mu_F*dot(dot(F_invT(U_M)('+'), dot(grad(U_F('+')).T, F_invT(U_M)('+'))), dot(grad(v_M('+')).T , dot(F_invT(U_M)('+'),N_F('+')))))*dS(3)

    # Collect boundary terms
    G_FM = G_FM_in_1 + G_FM_in_2 + G_FM_in_3 + G_FM_in_4 + G_FM_out_1 + G_FM_out_2 + G_FM_out_3 + G_FM_out_4

    # Collect A_FM form
    A_FM =  A_FM01 + A_FM02 + A_FM03 + A_FM04 + A_FM05 + A_FM06 + A_FM07 + A_FM08 + A_FM09 + A_FM10 + A_FM11 + A_FM12 + G_FM

    # Structure eq. linearized around the fluid variables
    A_SF01 = -inner(Z_S('+'), mu_F*J(U_M)('+')*dot(dot(grad(v_F('+')), F_inv(U_M)('+')), dot(F_invT(U_M)('+'), N)))*dS(1)
    A_SF02 = -inner(Z_S('+'), mu_F*J(U_M)('+')*dot(dot(F_invT(U_M)('+'), grad(v_F('+')).T), dot(F_invT(U_M)('+'), N)))*dS(1)
    A_SF03 =  inner(Z_S('+'), mu_F*J(U_M)('+')*q_F('+')*dot(I('+'), dot(F_invT(U_M)('+'), N)))*dS(1)

    # Collect A_SF form
    A_SF = A_SF01 + A_SF02 + A_SF03

    # Operators for A_SS
    Fu = F(U_S)
    Eu = Fu*Fu.T - I
    Ev = grad(v_S)*Fu.T + Fu*grad(v_S).T
    Sv = grad(v_S)*(2*mu_S*Eu + lmbda_S*tr(Eu)*I) + Fu*(2*mu_S*Ev + lmbda_S*tr(Ev)*I)

    # Structure eq. linearized around structure variable
    A_SS = - (1/k)*inner(Z_S0 - Z_S, rho_S*q_S)*dx(1) + inner(grad(Z_S), Sv)*dx(1) \
        - (1/k)*inner(Y_S0 - Y_S, v_S)*dx(1) - inner(Y_S, q_S)*dx(1)

    # Structure eq. linearized around mesh variable
    A_SM01 = -inner(Z_S('+'), DJ(U_M,v_M)('+')*mu_F*dot(dot(grad(U_F('+')), F_inv(U_F)('+')), dot(F_invT(U_M)('+'), N)))*dS(1) # FIXME: Replace with Sigma_F
    A_SM02 = -inner(Z_S('+'), DJ(U_M,v_M)('+')*mu_F*dot(dot(F_invT(U_F)('+'), grad(U_F('+')).T), dot(F_invT(U_M)('+'), N)))*dS(1)# FIXME: Replace with Sigma_F
    A_SM03 =  inner(Z_S('+'), DJ(U_M,v_M)('+')*dot(P_F('+')*I('+'), dot(F_invT(U_M)('+'),N)))*dS(1)# FIXME: Replace with Sigma_F
    A_SM04 =  inner(Z_S('+'), J(U_M)('+')*mu_F*dot(dot(grad(U_F('+')), dot(F_inv(U_M)('+'),grad(v_M('+')))), dot(F_inv(U_M)('+'), dot(F_invT(U_M)('+'), N))))*dS(1)
    A_SM05 =  inner(Z_S('+'), J(U_M)('+')*mu_F*dot(dot(grad(U_F('+')).T, dot(F_invT(U_M)('+'), grad(v_M('+')).T)), dot(F_invT(U_M)('+'), dot(F_invT(U_M)('+'),N))))*dS(1)
    A_SM06 =  inner(Z_S('+'), J(U_M)('+')*mu_F*dot(dot(grad(U_F('+')),F_inv(U_M)('+')),dot(F_invT(U_M)('+'), dot(grad(v_M('+')).T, dot(F_invT(U_M)('+'),N)))))*dS(1)
    A_SM07 =  inner(Z_S('+'), J(U_M)('+')*mu_F*dot(dot(F_invT(U_M)('+'),grad(U_M('+')).T),dot(F_invT(U_M)('+'), dot(grad(v_M('+')).T, dot(F_invT(U_M)('+'),N)))))*dS(1)
    A_SM08 = -inner(Z_S('+'), J(U_M)('+')*dot(dot(P_F('+')*I('+'),F_invT(U_M)('+')), dot(grad(v_M('+')).T, dot(F_invT(U_M)('+'), N))))*dS(1)

    # Collect A_SM form
    A_SM = A_SM01 + A_SM02 + A_SM03 + A_SM04 + A_SM05 + A_SM06 + A_SM07 + A_SM08

    # Mesh eq. linearized around mesh variable
    A_MM01 = -(1/k)*inner(v_M, Z_M0 - Z_M)*dx(0) + inner(sym_gradient(Z_M), Sigma_M(v_M))*dx(0)
    A_MM02 = inner(Z_M('+'),v_M('+'))*dS(1)
    A_MM03 = inner(Y_M('+'),q_M('+'))*dS(1)

    # Collect A_MM form
    A_MM = A_MM01 + A_MM02 + A_MM03

    # Mesh eq. linearized around structure variable
    A_MS = - inner(Y_M('+'), q_S('+'))*dS(1)

    # Define goal funtionals
    n_F = FacetNormal(Omega_F)
    area = 0.2*0.5
    goal_functional = (1/T)*(1.0/area)*v_S[0]*dx(1)

    # Define the dual rhs and lhs
    A_system = A_FF + A_FM + A_SS + A_SF + A_SM + A_MM + A_MS
    A = lhs(A_system)
    L = rhs(A_system) + goal_functional

    return A, L