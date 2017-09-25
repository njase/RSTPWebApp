from __future__ import division
from app import db
from sqlalchemy.exc import IntegrityError, InterfaceError
from flask import flash
from threading import Thread
from app.mod_rstp.models import SimModel
from RSTP import RSTPTest, RSTPIV, RSTPBV, RSTPExplicitParams, RSTPImplicitParams
from ODESolver import ODEExplicit, ODEImplicit , FVTransverse

#There seems no easier way to maintain the threads created by our App
SimThreadList = []

class WorkerSim(Thread):
    def __init__(self,db_id):
        self.db_id = db_id
        self.tstop= False #Used for stopping simulation
        Thread.__init__(self, name=str(db_id))
                
    def run(self):        
        #Read parameters from DB
        user_data = UserSim().query(self.db_id)
                
        #Start simulation
        if user_data.solver == 0: #Explicit Euler
            self.explicit_euler(user_data)
            user_data.sim_status = 1
            UserSim().update(user_data)         
        elif user_data.solver == 1: #Implicit Euler
            self.implicit_euler(user_data)
            user_data.sim_status = 1
            UserSim().update(user_data)
        elif user_data.solver == 2: #Crank Nicholson
            self.crank_ni(user_data)
            user_data.sim_status = 1
            UserSim().update(user_data)
        else:
            print("Unknown or unsupported solver")
  
    def explicit_euler(self,user_data):
            params = RSTPExplicitParams(user_data.mesh_size,user_data.gamma,user_data.cfl)             
            params.set_fig_path('./app/static/')
            params.fv_boundary_strategy = FVTransverse #Default, may also be skipped 
            iv = RSTPIV(Vx=[user_data.Vx_left,user_data.Vx_right], \
                        Mx=[user_data.Mx_left,user_data.Mx_right], \
                        D=[user_data.D_left,user_data.D_right], \
                        Rho=[user_data.rho_left,user_data.rho_right])
            bv = RSTPBV()
            testlist = [RSTPTest(self.db_id,params,iv,bv,ode_strategy=ODEExplicit)]
            stats_count = 10
            [test.solve(self.isStop,stats_count) for test in testlist]            
    
    def implicit_euler(self,user_data):
            params = RSTPImplicitParams(user_data.mesh_size,1.0,user_data.gamma,user_data.max_iter_count,user_data.cfl)             
            params.set_fig_path('./app/static/')
            params.fv_boundary_strategy = FVTransverse #Default, may also be skipped 
            iv = RSTPIV(Vx=[user_data.Vx_left,user_data.Vx_right], \
                        Mx=[user_data.Mx_left,user_data.Mx_right], \
                        D=[user_data.D_left,user_data.D_right], \
                        Rho=[user_data.rho_left,user_data.rho_right])
            bv = RSTPBV()
            testlist = [RSTPTest(self.db_id,params,iv,bv,ode_strategy=ODEImplicit)]
            stats_count = 10
            [test.solve(self.isStop,stats_count) for test in testlist]       
                 
    #Unused currently, TBD when second order spatial discretization is implemented
    def crank_ni(self,user_data):
            params = RSTPImplicitParams(user_data.mesh_size,0.5,user_data.gamma)             
            params.set_fig_path('/home/saur/ilastik/miniconda2/envs/RSTPWebApp/app/static/')
            params.fv_boundary_strategy = FVTransverse #Default, may also be skipped 
            iv = RSTPIV(Vx=[user_data.Vx_left,user_data.Vx_right], \
                        Mx=[user_data.Mx_left,user_data.Mx_right], \
                        D=[user_data.D_left,user_data.D_right], \
                        Rho=[user_data.rho_left,user_data.rho_right])
            bv = RSTPBV()
            testlist = [RSTPTest(self.db_id,params,iv,bv,ode_strategy=ODEImplicit)]
            stats_count = 10
            [test.solve(self.isStop,stats_count) for test in testlist]     


    def isStop(self):
        return self.tstop
  
class UserSim:
    def __init__(self):
        self.available_solvers = {"EE":0,"IE":1,"CN":2}
        self.available_gammas = {"0":0,"4/3":4/3,"5/3":5/3,"2":2}
    
    def validate_and_start(self,ode_solver,discont,Vx,Mx,D,rho,msize,gas_gamma,cfl=1.0,max_iter_count=1):
        db_id = -1
        solver = self.available_solvers.get(ode_solver)
        if solver == None:
            print('Error: no such ODE solver supported ' + solver)
            return -1
        
        gamma = self.available_gammas.get(gas_gamma)
        if gamma == None:
            print('Error: Unsupported Gamma values ' + solver)
            return -1
        #Rest are assumed to be validated by form validation
        usersim = SimModel(solver,discont,Vx,Mx,D,rho,msize,cfl,gamma,max_iter_count)
        try:
            db.session.add(usersim)
            db.session.flush()
            db_id = usersim.id
            db.session.commit()
            
            #Make a simple python Thread object and start simulation within it
            sim_thread = WorkerSim(db_id)
            SimThreadList.append(sim_thread)
            sim_thread.start()
            
        except (InterfaceError,IntegrityError) as exc:
            reason = exc.message
            db.session.rollback()
            flash('Error during SQL database addition - ' + reason)
            print('Error during SQL database addition - ' + reason)
            return -1
            
        return db_id
                  
    
    def check_status(self,db_id):
        user_data = SimModel.query.filter(SimModel.id == db_id).first() 
        return user_data.sim_status


    def query(self,db_id):
        user_data = SimModel.query.filter(SimModel.id == db_id).first()
        return user_data
    
    def update(self,user_data):
        db.session.commit()
    
    def stop(self,db_id):
        status = False
        tname = str(db_id)
        for t in SimThreadList:
            if t.name == tname:
                print("Thread found and stopped")
                t.tsop = True
                user_data = self.query(db_id)
                user_data.sim_status = 2
                self.update(user_data)
                status = True
                break
        return status
