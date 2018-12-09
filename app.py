from flask import Flask, render_template, flash, request,url_for,redirect,session
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField,PasswordField
from wtforms.validators import InputRequired, Length, AnyOf,Email
import pymysql
from flask_wtf import FlaskForm

from pymysql import *


app=Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
conn = pymysql.connect(host="localhost",user="root",password="123456",db="naveen")
cursor = conn.cursor()
conn.autocommit(True)


class RegisterForm(FlaskForm):
	first_name=TextField('first_name:',validators=[InputRequired(),Length(min=5,max=15,message="characters should be between 5 and 15")])
	last_name=StringField('last_name:',validators=[InputRequired(),Length(min=5,max=15,message="characters should be between 5 and 15")])
	college=StringField('college:',validators=[InputRequired(),Length(min=5,max=35,message="characters should be between 5 and 35")])
	email=StringField('email:',validators=[InputRequired(),Email(message="enter a valid email address")])
	username=StringField('username:',validators=[InputRequired(),Length(min=6,max=25,message="characters should be between 6 and 25")])
	password=PasswordField('password:',validators=[InputRequired(),Length(min=5,max=15,message="characters should be between 5 and 15")])
	submit=SubmitField('submit')
@app.route('/',methods=["post","get"])
def main():
	form=RegisterForm(request.form)
	return render_template('index1.html')
	# redirect(url_for('/reg.html'))
	
@app.route('/reg1.html',methods=["POST","GET"])
def reg():
	form=RegisterForm(request.form)
	return render_template('reg1.html',form=form)
	# if request.method == 'POST':

	# redirect(url_for('/check'))

@app.route('/check',methods=["post","get"])
def check():
	# return render_template('index1.html')
	form=RegisterForm()
	if form.validate_on_submit():

		fname=request.form['first_name']
		lname=request.form['last_name']
		college=request.form['college']
		email=request.form['email']
		username=request.form['username']
		password=request.form['password']
		
		cursor.execute("SELECT email FROM user2")
		d=cursor.fetchall()

		k=email
		i=0
		for row in d:
			if row[0]==k:
				i=i+1
		if i==0:
			cursor.execute("INSERT INTO user2 values('%s','%s','%s','%s','%s','%s')" %(fname,lname,college,email,username,password))
			
			print(cursor.execute("SELECT email FROM user2"))
		
			
			
			form=LoginForm()
			return render_template("log.html",form=form)
			# cursor.close()
		else:
		# print("user name alredy exists")
			return render_template("rereg.html")
	else:
		return render_template('reg1.html',form=form)
	
	



class LoginForm(FlaskForm):
	email1=StringField('EMAIL',validators=[InputRequired()])
	password=PasswordField('PASSWORD',validators=[InputRequired()])
	submit=SubmitField('submit')

@app.route('/log.html',methods=["post","get"])
def log():
	form=LoginForm(request.form)
	return render_template('log.html',form=form)


@app.route('/check1',methods=["POST","GET"])
def log1():
	form=LoginForm(request.form)
	email1=request.form['email1']
	password=request.form['password']
	conn = pymysql.connect(host="localhost",user="root",password="123456",db="naveen")
	cursor = conn.cursor()

	cursor.execute("SELECT email FROM user2")
	d=cursor.fetchall()
	i=0
	for row in d:
		if row[0]==email1:
			k=row[0]
			i=i+1
	if i==0:
		# return "no user found"
		flash('email is not registerd')
		return render_template('log1.html',form=form)
	else:
		cursor.execute("SELECT password FROM user2 where email='" + email1 + "'")
		p=cursor.fetchall()
		for row in p:
			if row[0]==password:
				session['user']=email1
				
				return redirect(url_for('getsession'))

			else:
				# print(row[0])
				# return "wrong password"
				flash('incorrect password ')
				return render_template('log1.html',form=form)
@app.route('/getsession')
def getsession():
	form=LoginForm()
	if 'user' in session:
		conn = pymysql.connect(host="localhost",user="root",password="123456",db="naveen")
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM user2 where email='" + session['user'] + "'")
		p=cursor.fetchone()
		return render_template('details.html',p=p)
	else:
		return render_template('log.html',form=form)

@app.route('/logout.html')
def logout():
	session.pop('user',None)
	form=LoginForm()
	return render_template('log.html',form=form)

@app.route('/index1.html')
def ind():
	return render_template('index1.html')



if __name__=='__main__':
	app.run(debug=True,host="192.168.43.216") 