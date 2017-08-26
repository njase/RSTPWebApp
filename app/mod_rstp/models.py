# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from sqlalchemy.exc import IntegrityError, InterfaceError
from flask import flash

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())

# Define a User model
class SimModel(Base):

    __tablename__ = 'UserSimRecord'

    #0 = Ongoing, 1 = Finished success , 2 = Stopped, otherwise = internal error
    sim_status    = db.Column(db.SmallInteger,default=-1)
    solver        = db.Column(db.Integer)
    discontinuity = db.Column(db.Float)
    Vx_left       = db.Column(db.Float)
    Vx_right      = db.Column(db.Float)
    Mx_left       = db.Column(db.Float)
    Mx_right      = db.Column(db.Float)
    D_left        = db.Column(db.Float)
    D_right       = db.Column(db.Float)
    rho_left      = db.Column(db.Float)
    rho_right     = db.Column(db.Float)
    cfl           = db.Column(db.Float, default=1.0)
    mesh_size     = db.Column(db.Integer)

    # New instance instantiation procedure
    def __init__(self,ode_solver,discont,Vx,Mx,D,rho,msize,cfl):
        self.sim_status = 0
        self.solver = ode_solver
        self.discontinuity = discont
        [self.Vx_left,self.Vx_right] = Vx
        [self.Mx_left,self.Mx_right] = Mx
        [self.D_left,self.D_right] = D
        [self.rho_left,self.rho_right] = rho
        self.mesh_size = msize
        self.cfl = cfl    

    def __repr__(self):
        return '<User %d>' % (self.id)

class UserSim:
    def __init__(self):
        self.available_solvers = {"EE":0,"IE":1}
    
    def validate_and_add(self,ode_solver,discont,Vx,Mx,D,rho,msize,cfl=1.0):
        db_id = -1
        solver = self.available_solvers.get(ode_solver)
        if solver == None:
            flash('Error: no such ODE solver supported ' + solver)
            return -1
        #Rest are assumed to be validated by form validation
        usersim = SimModel(solver,discont,Vx,Mx,D,rho,msize,cfl)
        try:
            db.session.add(usersim)
            db.session.flush()
            db_id = usersim.id
            db.session.commit()
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
