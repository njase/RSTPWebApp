# Import Form and RecaptchaField (optional)
from flask_wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import IntegerField, DecimalField, SubmitField, SelectField

# Import Form validators
from wtforms import validators, ValidationError

class InputForm(Form):
    ode_solver = SelectField('Solver method', choices = [('EE', 'Forward Euler'), ('IE', 'Backward Euler'),('CN', 'Crank Nicholson')])
    discontinuity = DecimalField("Discontinuity location (%)",[validators.Required("Please enter the location of discontinuity")])
    Vx_left = DecimalField("",[validators.InputRequired("Please enter the initial value for Vx_left")])
    Vx_right = DecimalField("",[validators.InputRequired("Please enter the initial value for Vx_right")])
    Mx_left = DecimalField("",[validators.InputRequired("Please enter the initial value for Mx_left")])
    Mx_right = DecimalField("",[validators.InputRequired("Please enter the initial value for Mx_right")])
    D_left = DecimalField("",[validators.InputRequired("Please enter the initial value for D_left")])
    D_right = DecimalField("",[validators.InputRequired("Please enter the initial value for D_right")])
    Rho_left = DecimalField("",[validators.InputRequired("Please enter the initial value for Rho_left")])
    Rho_right = DecimalField("",[validators.InputRequired("Please enter the initial value for Rho_right")])
    cfl = DecimalField("CFL (only for explicit method)")
    mesh_size = IntegerField("Number of FV cells",[validators.Required("Please enter the number of FV cells")])
    gamma = SelectField('Gamma', choices = [('0', 'Isothermal'), ('4/3', '4/3'),('5/3', '5/3'),('2', '2')])
    
    start_sim = SubmitField("Start Simulation")

class OutputForm(Form):
    stop_sim = SubmitField("Stop Simulation")
