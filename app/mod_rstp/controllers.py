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
       print("saurabh : 3")
       return render_template('rstp/rwa_input.html', form = form)
   else:
       print("Unexpected request methof received and ignored")
   
# Set the route and accepted methods
@mod_rstp.route('/input', methods = ['POST'])
def input():
   form = InputForm()
   if form.validate() == False:
       print("saurabh : 1")
       flash('All fields are required.')
       return render_template('rstp/rwa_input.html', form = form)
   else:
        print("saurabh : 2")
        ##Here, store values in DB and then redirect as GET
        return redirect(url_for('rstp.output',messages=1))


@mod_rstp.route('/check/', methods=['GET'])
def check():
    #ret_data = {"value": request.args.get('echoValue')}
    ret_data = {"value": 1}
    return jsonify(ret_data)

      
@mod_rstp.route('/output', methods = ['GET','POST'])
def output():
   form = OutputForm()
   if request.method == 'POST':
      if form.validate() == False:
         print("saurabh : 5")
         flash('All fields are required.')
         return render_template("rstp/rwa_output.html", form=form)
      else:
         print("saurabh : 6")
         flash('Stopping of simulation is not supported yet!')
   elif request.method == 'GET':
         print("saurabh : 7")
         ##Now here read from DB and render output values
         return render_template('rstp/rwa_output.html', form = form)
