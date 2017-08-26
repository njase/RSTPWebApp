# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  jsonify

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_rstp.forms import InputForm, OutputForm

# Import module models (i.e. User)
from app.mod_rstp.models import User

# Define the blueprint: 'rstp', set its url prefix: app.url/rstp
mod_rstp = Blueprint('rstp', __name__, static_folder='static', url_prefix='/rstp')

# Set the route and accepted methods
@mod_rstp.route('/input')
def home():
   form = InputForm()
   if request.method == 'GET':
       return render_template('rstp/rwa_input.html', form = form)
   else:
       print("Unexpected request methof received and ignored")
   
# Set the route and accepted methods
@mod_rstp.route('/input', methods = ['POST'])
def input():
   form = InputForm()
   if form.validate() == False:
       flash('All fields are required.')
       return render_template('rstp/rwa_input.html', form = form)
   else:
        ##Here, store values in DB and then redirect as GET
        return redirect(url_for('rstp.output',messages=1))


@mod_rstp.route('/check/', methods=['GET'])
def check():
    D = "Noimage"
    P = D
    U = D
    V = D
    #Read the DB index from GET request
    db_id = 1
    #Read the status of this simulation from DB
    #0 = Ongoing, 1 = Finished success , 2 = Stopped, otherwise = internal error
    sim_status = 1
    #Make return data
    if sim_status == 1:
        D = "/static/"+str(db_id)+"_D_img.jpeg"
        P = "/static/"+str(db_id)+"_P_img.jpeg"
        U = "/static/"+str(db_id)+"_U_img.jpeg"
        V = "/static/"+str(db_id)+"_V_img.jpeg"
    
    ret_data = {"sim_status":sim_status,"D":D,"P":P,"U":U,"V":U}
    return jsonify(ret_data)

      
@mod_rstp.route('/output', methods = ['GET','POST'])
def output():
   form = OutputForm()
   if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template("rstp/rwa_output.html", form=form)
      else:
         flash('Stopping of simulation is not supported yet!')
   elif request.method == 'GET':
         ##Now here read from DB and render output values
         return render_template('rstp/rwa_output.html', form = form)
