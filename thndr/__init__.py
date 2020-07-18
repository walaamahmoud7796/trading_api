from flask import Flask ,request
from flask_restful import Resource,Api,reqparse
from flask import current_app, g
import docker

import sqlite3
import docker

import paho.mqtt.client as mqtt
import time
import logging

from  datetime import datetime
import json
import pandas as pd 
import uuid 
import os 
import pathlib
import sys 

current_file = pathlib.Path(__file__).parent.absolute()
print(current_file)
sys.path.append(str(current_file)+'/')
import db

app = Flask(__name__) 
api = Api(app) 
stocks = pd.DataFrame()
class listner:
	
	
	def listen(self):
		def on_connect(client, userdata, flags,rc):
				print("Connected with result code "+str(rc))
				# Subscribing in on_connect() means that if we lose the connection and
				# reconnect then subscriptions will be renewed.
				client.subscribe("thndr-trading")

	# The callback for when a PUBLISH message is received from the server.
		def on_message(client, userdata, msg):
			# print('on_message is called')
			# print(msg.topic+" "+str(msg.payload))
			global stocks
			
			stream_df = pd.DataFrame(eval(msg.payload),index=[0])
			
			# csv_df = pd.read_csv('streamer.csv')
			stocks = stocks.append(stream_df,ignore_index = True)
			# print(stocks)
			# stocks['timestamp'] = pd.to_datetime(stocks['timestamp'])
			# print(stocks.dtypes)
		# 	csv_df = csv_df.append(stream_df)

		# csv_df.to_csv('streamer.csv',index=False)
		client = mqtt.Client()
		client.on_connect = on_connect
		client.on_message = on_message
		print("TRYING TO CONNECT........................................")
		# Gets or creates a logger
		logger = logging.getLogger("walaa")  
		# set log level
		logger.setLevel(logging.DEBUG)

		ch = logging.StreamHandler()
		ch.setLevel(logging.INFO)
		# create formatter and add it to the handlers
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		# fh.setFormatter(formatter)
		ch.setFormatter(formatter)
		# add the handlers to the logger
		logger.addHandler(ch)

		client.enable_logger(logger=logger)
		time.sleep(10)

		client.connect("vernemq", 1883, 60)
		client.loop_start()
		

		

DATABASE = 'thndr_test.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn





class Helper:
	def get_args(self,params,required):
		parser = reqparse.RequestParser()
		for param,is_required in zip(params,required):
			parser.add_argument(param,required=is_required)
		# parser.add_argument('user_id',required=True)
		# parser.add_argument('stock_id',required=True)
		# parser.add_argument('total',required=True)

		# parser.add_argument('upper_bound',required=True)
		# parser.add_argument('lower_bound',required=True)

		args = parser.parse_args()
		return args
	
	def update_tables(self,values):
		cursor = get_db()
		update_sql ="""
				INSERT INTO fact_trade(  trade_id
										,stock_id
										,user_id
										,total_stocks
										,stock_price
										,trade_type
										,trade_timestamp
										,status
										,note) 
				VALUES(?,?,?,?,?,?,?,?,?)

			"""
		trade_id =str(uuid.uuid1())
		cursor.execute(update_sql,values)
		cursor.commit()
	def get_stock_data(self,stock_id,timestamp):
		
		while True:
			global stocks
			print(stocks)
			index = stocks[(stocks['stock_id']==stock_id)& (stocks['timestamp'].str.contains(timestamp))].index
			print('index',index)
			print('size',len(index))
			if len(index)>0:
				stock_price = stocks['price'][index[0]]
				break

		# return len(stock_price)
		print('stock_price',stock_price)
		return stock_price
	def update_user_balance(self,new_balance,user_id):
		cursor = get_db()
		cursor.execute("UPDATE dim_user  set balance = ? where user_id= ?",(new_balance,user_id))
		cursor.commit()






class Deposit(Resource):
	
	def post(self):
		helper = Helper()
		args = helper.get_args(['user_id','amount'],[True,True])
		args['type']='deposit'
		args['transaction_timestamp']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		try:
			sql ="""
			INSERT INTO fact_transaction(transaction_id,user_id,amount,type,transaction_timestamp) VALUES(?,?,?,?,?)

			"""
			cur = get_db()
			trans_id = str(uuid.uuid1())
			cur.execute(sql,(trans_id,args['user_id'],args['amount'],args['type'],args['transaction_timestamp'],))
			cur.commit()

			current_amount = cur.execute("SELECT balance from dim_user where user_id=?",(args['user_id'],)).fetchone()
			helper.update_user_balance(current_amount[0]+float(args['amount']),args['user_id'])
			args['user_current_balance'] = current_amount[0]+float(args['amount'])
			args['transaction_id']= trans_id
			return {'message':'Success','data':args},201
		except Exception as e:
			return {'Error': str(e)},500

class Withdraw(Resource):
	def post(self):
		
		
		helper =Helper()
		args = helper.get_args(['user_id','amount'],[True,True])
		args['type']='withdrawal'
		args['transaction_timestamp']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		cur = get_db()
		try:
			current_amount = cur.execute("SELECT balance from dim_user where user_id=?",(args['user_id'],)).fetchone()

			if current_amount[0]<float(args['amount']):
				return {'message':'Insufficient request','data':{'user_current_balance':current_amount[0]}}
			else:
				cur.execute("UPDATE dim_user  set balance = ? where user_id= ?",(current_amount[0]-float(args['amount']),args['user_id']))
				cur.commit()
				sql ="""
				INSERT INTO fact_transaction(transaction_id,user_id,amount,type,transaction_timestamp) VALUES(?,?,?,?,?)

				"""
				trans_id = str(uuid.uuid1())
				cur.execute(sql,(trans_id,args['user_id'],args['amount'],args['type'],args['transaction_timestamp']))
				cur.commit()
				args['user_current_balance'] = current_amount[0]-float(args['amount'])
				args['transaction_id'] = trans_id
				return {'message':'Success','data':args},201
		except Exception as e:
			return {"Error":str(e)},500

class Buy(Resource):
	def post(self):
		cur=  get_db()
		trade_helper = Helper()
		
		args= trade_helper.get_args(['user_id','stock_id','total','upper_bound','lower_bound'],[True,True,True,True,True])
		request_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		stock_price = trade_helper.get_stock_data(args['stock_id'],request_timestamp[:17])

		trade_id =str(uuid.uuid1())
		values = (trade_id,args['stock_id'],args['user_id'],args['total'],float(stock_price),'buy',request_timestamp)
		try:
			if stock_price>=float(args['lower_bound']) and stock_price<=float(args['upper_bound']):
				
				
				args['trade_price'] = float(args['total'])*stock_price
				# print('trade_price',trade_price)
				user_balance = cur.execute("SELECT balance from dim_user where user_id =?",(args['user_id'],)).fetchone()[0]
		
				if args['trade_price'] > user_balance:
					values = values + ('unsuccessful','user balance is Insufficient')
					trade_helper.update_tables(values)
					return {"message":"unsuccessful trade due to insufficient balance","data":{"user_balance":user_balance,"trade_price":args['trade_price']}},406
				else:
					values+=('successful','user balance is sufficient')			
					trade_helper.update_tables(values)				
					trade_helper.update_user_balance(user_balance-args['trade_price'],args['user_id'])
					args['trade_id'] = trade_id
					return {"message":"successful trade","data":args},200
				
				
			else:
				values+= ('unsuccessful','stock price is out of bounds')
				trade_helper.update_tables(values)

				return{"message":"unsuccessful trade, stock price is out of bounds"},406
		except Exception as e:
			return {"Error": str(e)},500
class Sell(Resource):
	def post(self):
		cur =  get_db()
		trade_helper = Helper()
		args= trade_helper.get_args(['user_id','stock_id','total','upper_bound','lower_bound'],[True,True,True,True,True])
		request_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		stock_price = trade_helper.get_stock_data(args['stock_id'],request_timestamp[:17])
		print('stock_price',stock_price)
		print(args)
		trade_id =str(uuid.uuid1())
		values = (trade_id,args['stock_id'],args['user_id'],args['total'],float(stock_price),'sell',request_timestamp)
		try:
			if stock_price>=float(args['lower_bound']) and stock_price<=float(args['upper_bound']):
				values+= ('successful','stock price matches bounds')
				trade_helper.update_tables(values)
				user_balance = cur.execute("SELECT balance from dim_user where user_id =?",(args['user_id'],)).fetchone()[0]
				args['trade_price'] = float(args['total'])*stock_price
				new_balance = user_balance+args['trade_price']
				trade_helper.update_user_balance(new_balance,args['user_id'])
				args['trade_id'] = trade_id
				return {"message":"successful trade","data":args},200
			else:
				values+= ('unsuccessful','stock price is out of bounds')
				trade_helper.update_tables(values)
				return{"message":"unsuccessful trade, stock price is out of bounds"},406
		except Exception as e:
			return {"Error":str(e)}
class Stock(Resource):
	def get(self):
		helper= Helper()
		cur = get_db()
		args = helper.get_args(['stock_id'],[True])
		try:
			stock_sql = """SELECT * FROM fact_trade WHERE stock_id=?"""
			stock_data = cur.execute(stock_sql,(args['stock_id'],))
			stock_columns = list(map(lambda x: x[0], stock_data.description))
			stock_data = stock_data.fetchall()
			stock_info = {'stock_id':args['stock_id']}
			stock_info['trades']=[]
			for row in stock_data:
				trade ={}
				for j in range(len(row)):
					if stock_columns[j]!='stock_id':
						trade[stock_columns[j]] = row[j]
				stock_info['trades'].append(trade)
			return stock_info,200
		except Exception as e:
			return {"Error":str(e)},200

class User(Resource):
	def get(self):
		helper = Helper()
		args = helper.get_args(['user_id'],[True])
		dim_info = """
 		SELECT  du.*
 		FROM dim_user du
 		Where du.user_id = ?
		"""
		try:
			cur = get_db()
			user_info = cur.execute(dim_info,(args['user_id'],)).fetchall()
			user_data={'user_id':user_info[0][0],'current_balance':user_info[0][1]}
			user_data['transactions']=[]
			user_data['trades']=[]

		
			trans_info = """ SELECT * FROM fact_transaction WHERE user_id = ?"""
			trans_data = cur.execute(trans_info,(args['user_id'],))
			# print(data.description)
			trans_columns = list(map(lambda x: x[0], trans_data.description))
			trans_data = trans_data.fetchall()
			for row in trans_data:
				transaction = {}
				for j in range(len(row)):
					if trans_columns[j] !='user_id':
						transaction[trans_columns[j]]= row[j]

				user_data['transactions'].append(transaction)


			trades_info = "SELECT * FROM fact_trade WHERE user_id =?"
			trades_data = cur.execute(trades_info,(args['user_id'],))
			trades_columns = list(map(lambda x: x[0], trades_data.description))
			trades_data = trades_data.fetchall()
			print(trades_columns)
			for row in trades_data:
				trade ={}
				for j in range(len(row)):
					if trades_columns!='user_id':
						trade[trades_columns[j]]= row[j]
				user_data['trades'].append(trade)

			return user_data,200
			# print(i)
		except Exception as e:
			return {"Error": str(e)}

		# return user_data		



api.add_resource(Deposit,'/deposit')
api.add_resource(Withdraw,'/withdraw')
api.add_resource(Buy,'/buy')
api.add_resource(Sell,'/sell')
api.add_resource(Stock,'/stock')

api.add_resource(User,'/user')

# api.add_resource(Stock,'/stock')

# api.add_resource(Stock,'/stock')
if __name__ =='__main__':
	# db.Create_DB()
	# Create_DB()
	# create_dummy_users()
	app.run(host='0.0.0.0',port = 80,debug=True)
