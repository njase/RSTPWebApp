# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

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
    gamma         = db.Column(db.Float, default = 0)
    max_iter_count     = db.Column(db.Integer, default = 1)

    # New instance instantiation procedure
    def __init__(self,ode_solver,discont,Vx,Mx,D,rho,msize,cfl,gamma,max_iter):
        self.sim_status = 0
        self.solver = ode_solver
        self.discontinuity = discont
        [self.Vx_left,self.Vx_right] = Vx
        [self.Mx_left,self.Mx_right] = Mx
        [self.D_left,self.D_right] = D
        [self.rho_left,self.rho_right] = rho
        self.mesh_size = msize
        self.cfl = cfl    
        self.gamma = gamma
        self.max_iter_count = max_iter

    def __repr__(self):
        return '<User %d>' % (self.id)
