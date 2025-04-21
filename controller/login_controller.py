from app import app 

# we have to import model 
from model.login_model import login_model_class

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
