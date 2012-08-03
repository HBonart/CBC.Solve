"This module specifies the Residual forms for the monolithic FSI problem."

__author__ = "Gabriel Balaban"
__copyright__ = "Copyright (C) 2010 Simula Research Laboratory and %s" % __author__
__license__  = "GNU GPL Version 3 or any later version"

from dolfin import *
from cbc.swing.operators import *
from cbc.twist import PiolaTransform
from cbc.swing.operators import Sigma_F as _Sigma_F
from cbc.swing.operators import Sigma_S as _Sigma_S
from cbc.swing.operators import Sigma_M as _Sigma_M
from cbc.swing.operators import F, J, I

##Throughout this module the following notation is used.

##u_F Fluid Velocity
##p_F Fluid Pressure
##l_F Fluid lagrange multiplier that enforces kinematic continuity of fluid and structure

##u_S Structure displacement
##p_S Structure Velocity

##u_M Mesh Displacement
##l_M Mesh lagrange multiplier that enforces displacement matching with structure on FSI boundary

##Test functions are related to their trial functions by the following letter substitution.
## u-> v , p-> q, l-> m

def fsi_residual(U1list,Umidlist,Udotlist,Vlist,matparams,measures,forces,normals,solver_params):
    """"
    Build the residual forms for the full FSI problem
    including the fluid, structure and mesh equations

    U1list   - List of current fsi variables
             - u1_F,p1_F,l1_F,u1_S,p1_S,u1_M,l1_M

    Umidlist - List of time approximated fsi variables.
             - u_Fmid,p_Fmid,l_Fmid,u_Smid,p_Smid,u_Mmid,l_Mmid

    V        - List of Test functions
             - v_F,q_F,m_F,v_S,q_S,v_M,m_M
               
    matparams - Dictionary of material parameters
              - mu_F,rho_F,mu_S,lmbda_S,rho_S

    measures  - Dictionary of measures
              - dxF,dxS,dxM,dsF,dsS,dFSI
               (dx = interior, ds = exterior boundary, dFSI = FSI interface)

    forces - Dictionary of body and boundary forces
           - F_F,F_S,F_M,G_S,g_F
             (F = body force, G_S = extra FSI traction on structure, g_F = fluid boundary force)

    normals - Dictionary of outer normals
            - N_F, N_S       
    """
    info_blue("Creating residual forms")

    #Unpack the functions
    u1_F,p1_F,l1_F,u1_S,p1_S,u1_M,l1_M = U1list

    #Test Functions
    v_F,q_F,m_F,v_S,q_S,v_M,m_M = Vlist

    #Unpack Material Parameters
    mu_F = matparams["mu_F"]
    rho_F = matparams["rho_F"]
    mu_S = matparams["mu_S"]
    lmbda_S = matparams["lmbda_S"]
    rho_S = matparams["rho_S"]
    mu_M = matparams["mu_M"]
    lmbda_M = matparams["lmbda_M"]

    #Unpack Measures
    dxF = measures["dxF"]
    dxS = measures["dxS"]
    dxM = measures["dxM"]
    dsF = measures["dsF"]
    dsS = measures["dsS"]
    #dsM = measures["dsM"] (not in use at the moment)
    dFSI = measures["dFSI"]
    dsDN = measures["dsDN"] #do nothing fluid boundary

    #Unpack forces
    F_F = forces["F_F"]
    F_S = forces["F_S"]
    F_M = forces["F_M"]
    G_S = forces["G_S"]
    G_F = forces["G_F"]
    G_F_FSI = forces["G_F_FSI"]

    #Unpack Normals
    N_F = normals["N_F"]
    N_S = normals["N_S"]

    #FSI Interface Mesh conditions, lagrange multipliers should only apply to current time step
    r_M2 = mesh_fsibound(u1_S,u1_M,l1_M,v_M,m_M,dFSI,innerbound = True)

    #Unpack the time approximations
    u_Fmid,p_Fmid,l_Fmid,u_Smid,p_Smid,u_Mmid,l_Mmid = Umidlist
    u_Fdot,p_Fdot,l_Fdot,u_Sdot,p_Sdot,u_Mdot,l_Mdot = Udotlist

    ##Stress couplings
    if solver_params["stress_coupling"] == "forward":
        #Stress F->S
        r_S2 = struc_fsibound(u_Fmid,p_Fmid,u_Mmid,mu_F,v_S,N_F,G_S,dFSI, innerbound = True,Exact_SigmaF = G_F_FSI)
        r_F2 = fluid_fsibound(p1_S,u1_F,l1_F,v_F,v_S,m_F,dFSI,innerbound = True)

    elif solver_params["stress_coupling"] == "backward":
        #Stress S->F
        r_S2 = struc_fsibound2(p1_S,u1_F,l1_F,v_F,v_S,m_F,dFSI,innerbound = True)
        r_F2 = fluid_fsibound2(u_Smid,v_F,N_S,mu_S,lmbda_S,G_S,dFSI, innerbound = True,Exact_SigmaF = G_F_FSI)
    else:
        raise Exception("Only forward and backward are possible stress coupling - direction parameters")

    #Decoupled equations, should contain time discretized variables
    r_F1 = fluid_residual(u_Fdot,u_Fmid,u1_F,p1_F,v_F,q_F,mu_F,rho_F,u1_M,N_F,dxF,dsDN,dsF,F_F,u_Mdot,G_F)
##    r_F1 = fluid_residual(u_Fdot,u_Fmid,u1_F,p1_F,v_F,q_F,mu_F,rho_F,u1_M,N_F,dxF,dsDN,dsF,F_F,u_Mdot,G_F)
    r_S1 = struc_residual(u_Sdot,p_Sdot,u_Smid,p_Smid,v_S,q_S,mu_S,lmbda_S,rho_S,dxS,dsS,F_S)    
    r_M1 = mesh_residual(u_Mdot,u_Mmid,v_M,mu_M,lmbda_M,dxM,F_M)

    #Fluid Residual
    r_F = r_F1 + r_F2
    #Structure Residual
    r_S = r_S1 + r_S2
    #Mesh Residual
    r_M = r_M1 + r_M2
    
    #Define full FSI residual
    r = r_F + r_S + r_M

    #Store the partial residuals in a dictionary
    blockresiduals = {"r_F":r_F,"r_S":r_S,"r_M":r_M}

    #return the full residual and partial residuals (for testing)
    return r,blockresiduals

def fluid_residual(Udot,U,U1_F,P,v,q,mu,rho,U_M,N,dx_F,ds_DN,ds_F,F_F,Udot_M, G_F=None):
    #ALE term present here
    Dt_U = rho*J(U_M)*(Udot + dot(grad(U),dot(inv(F(U_M)),U - Udot_M)))
        
    Sigma_F = PiolaTransform(_Sigma_F(U, P, U_M, mu), U_M)

    #DT
    R_F  = inner(v, Dt_U)*dx_F                                                                      

    #Div Sigma F
    R_F += inner(grad(v), Sigma_F)*dx_F

    #Incompressibility
    R_F += inner(q, div(J(U_M)*dot(inv(F(U_M)), U)))*dx_F                                           

    #Use do nothing BC if specified
    if ds_DN is not None:
        info("Using Do nothing Fluid BC")
        R_F += -inner(v, J(U_M)*dot((mu*inv(F(U_M)).T*grad(U).T - P*I)*inv(F(U_M)).T, N))*ds_DN
        
    #Add boundary traction (sigma dot n) to fluid boundary if specified.
    if ds_F is not None:
        info("Using Fluid boundary Traction (Neumann) BC")
        R_F += - inner(G_F, v)*ds_F
        
    #Right hand side Fluid (body force)
    if F_F is not None:
        info("Using Fluid body force")
        R_F += -inner(v,J(U_M)*F_F)*dx_F
    return R_F

def fluid_fsibound(P_S,U_F,L_F,v_F,v_S,m_F,dFSI,innerbound):
    if innerbound == False:
        #Kinematic continuity of structure and fluid on the interface
        C_F  = inner(m_F,U_F - P_S)*dFSI
        #Lagrange Multiplier term
        C_F += inner(v_F,L_F)*dFSI
    else:
        #Kinematic continuity of structure and fluid on the interface
        C_F  = inner(m_F,U_F - P_S)('+')*dFSI
        #Lagrange Multiplier term
        C_F += inner(v_F,L_F)('+')*dFSI
    return C_F

def fluid_fsibound2(U_S,v_F,N_S,mu_S,lmbda_S,G_S,dFSI, innerbound,Exact_SigmaF = None):
    """Structure stress on fluid"""
    #Current Structure tensor
    Sigma_S = _Sigma_S(U_S, mu_S, lmbda_S)

    if innerbound == False:
        #Structure Traction on Fluid
        C_S = -(inner(dot(Sigma_S,N_S),v_F))*dFSI
    else:
        if Exact_SigmaF is None:
            #Structure Traction on Fluid
            C_S = -(inner(dot(Sigma_S('-'),N_S('+')),v_F('+')))*dFSI
            if G_S is not None:
                info("Using additional fsi boundary traction term")
                C_S += -inner(G_S('-'),v_F('-'))*dFSI
        else:
            #Prescribed fluid traction on structure
            info("Using perscribed Structure Stress on fsi boundary")
            C_S = (inner(Exact_SigmaF('+'),v_S('-')))*dFSI
    return C_S

def struc_residual(Udot_S,Pdot_S,U_S, P_S,v_S,q_S,mu_S,lmbda_S,rho_S,dx_S,ds_S,F_S):
                    
    Sigma_S = _Sigma_S(U_S, mu_S, lmbda_S)
    #Hyperelasticity equations St. Venant Kirchoff
    R_S = inner(v_S, rho_S*Pdot_S)*dx_S + inner(grad(v_S), Sigma_S)*dx_S + inner(q_S, Udot_S - P_S)*dx_S
    #Right hand side Structure (Body force)
    if F_S is not None:
        info("Using structure body force")
        R_S += -inner(v_S,J(U_S)*F_S)*dx_S
    return R_S

def struc_fsibound(U_F,P_F,U_M,mu_F,v_S,N_F,G_S,dFSI, innerbound, Exact_SigmaF = None):
    #Current Fluid tensor
    Sigma_F = PiolaTransform(_Sigma_F(U_F, P_F, U_M, mu_F), U_M)

    if innerbound == False:
        #Fluid Traction on structure
        C_S = -(inner(dot(Sigma_F,N_F),v_S))*dFSI
        #Optional boundary traction term
        if G_S is not None:
            C_S += -inner(G_S,v_S)*dFSI
    else:
        if Exact_SigmaF is None:
            #Calculated fluid traction on structure
            C_S = -(inner(dot(Sigma_F('+'),N_F('-')),v_S('-')))*dFSI
        else:
            #Prescribed fluid traction on structure
            info("Using perscribed Fluid Stress on fsi boundary")
            C_S = (inner(Exact_SigmaF('+'),v_S('-')))*dFSI
            
        #Optional boundary traction term
        if G_S is not None:
            info("Using additional fsi boundary traction term")
            C_S += inner(G_S('-'),v_S('-'))*dFSI
    return C_S

def struc_fsibound2(P_S,U_F,L_F,v_F,v_S,m_F,dFSI,innerbound):
    if innerbound == False:
        #Kinematic continuity of structure and fluid on the interface
        C_F  = inner(m_F,U_F - P_S)*dFSI
        #Lagrange Multiplier term
        C_F += inner(v_S,L_F)*dFSI
    else:
        #Kinematic continuity of structure and fluid on the interface
        C_F  = inner(m_F,P_S - U_F)('-')*dFSI
        #Lagrange Multiplier term
        C_F += inner(v_S,L_F)('-')*dFSI
    return C_F

def mesh_residual(Udot_M,U_M,v_M,mu_M,lmbda_M,dx_F,F_M):
    #Mesh stress tensor
    Sigma_M = _Sigma_M(U_M, mu_M, lmbda_M)

    #Mesh equation
    R_M = inner(v_M, Udot_M)*dx_F + inner(sym(grad(v_M)), Sigma_M)*dx_F
    #Right hand side mesh (Body Force)
    if F_M is not None:
        info("Using mesh body force")
        R_M += -inner(v_M,F_M)*dx_F
    return R_M

def mesh_fsibound(U_S,U_M,L_M,v_M,m_M,d_FSI,innerbound):
    if innerbound == True:
        #Mesh should follow the structure displacement
        C_MS =  inner(m_M, U_M - U_S)('+')*d_FSI
        #Lagrange Multiplier
        C_MS += inner(v_M, L_M)('+')*d_FSI
    else:
        #Mesh should follow the structure displacement
        C_MS =  inner(m_M, U_M - U_S)*d_FSI
        #Lagrange Multiplier
        C_MS += inner(v_M, L_M)*d_FSI 
    return C_MS