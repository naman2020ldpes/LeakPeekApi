from app import app 

# we have to import model 
from model.login_model import login_model_class

#from email 
from model.email_varify_model import emailVarify as demo
from flask import request

obj = login_model_class()
obj2 = login_model_class()

#Create/insert opration Post methord
@app.route("/user/login",methods=["POST","GET"])
def user_login_controller():
    #print(request.form)   # allows to take data from user
    #return obj.user_login_model(request.form)
    request_data = request.get_json()
    email = request_data.get("email")
    password = request_data.get("password")
    return obj.user_login_model(request_data)

@app.route("/user/register",methods=["POST","GET"])
def user_register_model():
    #print(request.form)   # allows to take data from user in other format
    request_data = request.get_json()
    return obj2.user_register_model(request_data)

@app.route("/user/email",methods=["POST","GET"])
def user_email_model():
    #print(request.form)   # allows to take data from user in other format
    request_data = request.get_json()
    print(request_data)
    email =request_data["email"]
    action =request_data["action"]
    
# Check if the "code" key exists in the request data
    if "code" in request_data:
        code = request_data["code"]
        # Call the demo function with email, action, and code
        return demo(email, action, code)
    else:
        # Call the demo function with only email and action
        return demo(email, action)