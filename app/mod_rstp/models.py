# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'UserSimRecord'

    sim_status    = db.Column(db.SmallInteger)
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
    def __init__(self):
        pass

    def __repr__(self):
        return '<User %d>' % (self.id)
