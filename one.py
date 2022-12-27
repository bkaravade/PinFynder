from flask import Flask, render_template, request, jsonify
# from flask_restful import Resource, Api, reqparse
from flask_mail import Mail, Message
import pandas as pd
import json


app = Flask(__name__) # app Init
mail = Mail(app) # Mail Init

# Mail Config
app.config['MAIL_SERVER']='mail.spellsys.tech'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'Mail Here'
app.config['MAIL_PASSWORD'] = 'Password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Read data convert into Json Format
rdata = pd.read_csv('PincodeData.csv', sep=",")
pindata = rdata.to_json(orient = 'records')
pindata = json.loads(pindata)

# Function will return Pincode json 
def fid_details(code):
   return_elements_list = []
   for i in pindata:
      if i['Pincode'] == int(code):
         return_elements_list.append(i)

   if len(return_elements_list) == 0:
      return_elements_list = [{
         'Message': 'Record Not Found',
         'Error': 'Custom Error',
         'Hint': 'Check Pincode'
      }]
   return return_elements_list

# Function will return Postoffice Json
def fid_PostName(PostName):
   return_elements_list = []
   # print(PostName)
   for i in pindata:
      if (PostName in i['Place / City / Area']):
         return_elements_list.append(i)
   
   if len(return_elements_list) == 0:
      return_elements_list = [{
         'Message': 'Record Not Found',
         'Error': 'Custom Error',
         'Hint': 'Check Post Office Name'
      }]
   return return_elements_list



@app.route('/api', methods = ['GET', 'POST'])
def api():
   return jsonify({ 'Pincode': pindata})

#  API Data From Pincode<int>
@app.route('/api/<int:pcode>', methods = ['GET', 'POST'])
def api_code(pcode):
      return jsonify({ 'Pincode': fid_details(pcode) })

# API Data From PostName<string>
@app.route('/api/<string:postName>', methods = ['GET', 'POST'])
def api_name(postName):
      return jsonify({ 'Pincode': fid_PostName(postName) })

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/name')
def pname():
   return render_template('name.html')

@app.route('/code')
def hello_world():
   return render_template('code.html')

@app.route('/getCode', methods = ['POST'])
def getPincode():
   output = request.form.to_dict()
   code = output['code']
   if len(code) == 6 and code.isnumeric():
      return render_template('code.html', name = fid_details(code))
   else:
      return render_template('code.html', name1 = 'Pincode Length Should be 6 Numbers Not Characters!')

@app.route('/getPin',  methods = ['POST'])
def getPin():
   output = request.form.to_dict()
   name = output['name']
   if name.isnumeric():
      return render_template('name.html', name1 = 'PostName Should be String and case Sensitive!')
   else:
      # print(type(name)) 
      return render_template('name.html', name = fid_PostName(name))
      


@app.route('/send-mail', methods = ['POST'])
def send():
   output = request.form.to_dict()
   if output['name'].isnumeric() or len(output['pno']) != 10:
      return render_template('index.html' , name1 = 'Name Should ne String and Mobile Not Valid!')
   elif (type(output['name']) == str) and (len(output['pno']) == 10):
      msg = Message(
                'Hello! Pinfynder Mail from ' + output['name'] ,
                sender = output['mail'],
                recipients = ['karawadeballal@gmail.com' , 'info@spellsys.tech', 'raddibasket05@gmail.com']
               )
      msg.body = 'Hello Flask message sent from Flask-Mail'+ '\n' + output['msg'] + '\nPhoneNO: '+ output['pno'] + '\n'
      mail.send(msg)
      return render_template('index.html' , name = 'Mail has been sent. Thank You!')


@app.route('/ballal')
def hello_ballal():
   return "Hello ballal"


app.run(debug = False, host = '0.0.0.0')
