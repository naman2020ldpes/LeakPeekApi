import mysql.connector
import json
from flask import Response , jsonify
"""
400	Bad Request	Input/validation errors (e.g., missing fields)
409	Conflict	Duplicate records (e.g., user already exists)
500	Internal Server Error	Unexpected/unhandled errors
503	Service Unavailable	Database/server temporarily unavailable"""



class login_model_class():
    def __init__(self):  
        try:
            # establish connectin
            self.conn= mysql.connector.connect(host="localhost",user="root",password="root",database="flask_tutorial")
            self.conn.autocommit=True
            self.cor = self.conn.cursor(dictionary=True) # in dictonary format 
            # cursor helps to exicute dml operation 
            print("connection sucess")
        except mysql.connector.Error as e :
            print("error:",e)
            return {"message": str(e), "status": 400}
        except Exception  as e :
            print("error:",e)
            return {"message": "this is other error :  "+ str(e), "status": 500}
    @staticmethod   # to make it global accssable
    def is_empty(data, fields):
        """Check if fields exist and are not empty."""
        missing = [field for field in fields if not data.get(field)]
        return missing  # returns list of missing/empty fields
    
    def user_login_model(self,data):
        # check if any field is empty
        required_fields = ['email', 'password']
        missing_fields = self.is_empty(data, required_fields)
        if missing_fields:
            return jsonify({"message": f"Missing or empty fields: {', '.join(missing_fields)}","status":400})
        
        #self.cor.execute(f"select email,password from user where email = '{data['email']}' and password = '{data['password']}' ;")  # write Query
        self.cor.execute("select email,password from user where email =%s and password =%s", (data['email'], data['password']))
        result=self.cor.fetchall()   # to exicute it 
        #print(data) dictotanry format
        #print(result)
        try:
            if len(result)>0 :
                return jsonify({"message":"loign successful","status":200,"page":"home"})
            else: 
                return jsonify({"message":"invalid email or password","status":401})
            # json.dumps() function will convert a subset of Python objects into a json string;. 
        except mysql.connector.Error as e :
            print("error:",e)
            return jsonify({"message": str(e), "status": 400})
        except Exception  as e :
            print("error:",e)
            return jsonify({"message": "this is other error :  "+ str(e), "status": 500})
        
    def user_register_model(self,data):
        print(data)   # allows to take data from user
        # check if any field is empty
        required_fields = ['email','phone','role','password','name']
        missing_fields = self.is_empty(data, required_fields)
        if missing_fields:
            return jsonify({"message": f"Missing or empty fields: {', '.join(missing_fields)}","status":400})
        # to print specific value 
        #print('\n'+ data['name']) 
        #fstr = f"values('{data['name']}','{data['email']}','{dat021a=['phone']}','{data['role']}','{data['password']}');"
        #self.cor.execute(f"insert into flask_tutorial.user (name,email,phone,role,password) {fstr}")
        #result=self.cor.fetchall()   # to exicute it 
        #print(result)
        try:
            inputs_qry="insert into user (name,email,phone,role,password) values(%s,%s, %s,%s, %s)"
            val=(data['name'],data['email'],data['phone'],data['role'],data['password'])
            self.cor.execute(inputs_qry,val) # to exicute it 
            if self.cor.rowcount > 0:
                return {"message": "created success", "status": 201,"page":"home"}
            else:
                return {"message": "error while creating user", "status": 500}
        except mysql.connector.Error as e :
            print("error:",e)
            return {"message": str(e), "status": 400}
        except Exception  as e :
            print("error:",e)
            return {"message": "this is other error :  "+ str(e), "status": 500}
        
            
    