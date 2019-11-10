import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, Response
from flaskblog import app, db, bcrypt, changes
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post, Algorithms
from flask_login import login_user, current_user, logout_user, login_required
import json
import time
from datetime import datetime

message = 0
posts = [
    {
        'author': 'Flowrate: Normal',
        'title': 'Flow Rate Stabilizer',
        'content': 'Master Node for data monitoring and differential stabilization.',
        'date_posted': 'Master Node'
    },
    {
        'author': 'Flowrate: Normal',
        'title': 'Leakage Prone Node',
        'content': 'Unstable due to placement near turbulent flow Source 1',
        'date_posted': 'Slave Node 1'
    }
]


@app.route("/")
def index():
    return redirect (url_for('login'))
@app.route("/home",methods=['GET','POST'])
@login_required
def home():
    #chart_data()
    global message
    if request.method == 'POST':
        path=request.form['url']
        print("Leak in graphs")
        print('Path',path)
        flash('Leak Detected','danger')
        message+=1

        return redirect(path)#,msg=message)
    return render_template('home.html', msg=message)

@app.route('/chart-data',methods=['GET'])
def chart_data():
    def generate_random_data():
        for change in changes:
            if change is None:
                pass
            else:
                json_data = json.dumps(
                    {'time':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'values':[1,2,3,4,5,6,7,8,9,10,11,12]})
                print(json_data)
                #with app.test_request_context():
                    #if(change['doc']['temperatureField']==20):
                        #print("Leak")
                        #message="Leak"
                        
                        #print("After return")
                        #return app.response_class(url_for('graphs'))
                        #changes.stop()
                        #return redirect(url_for('graphs',title='Graphs',msg=message),Response=Response.)
                yield f"data:{json_data}\n\n"
                #if checkleak(change['doc']):
                    
                #time.sleep(1)
    return Response(generate_random_data(), mimetype='text/event-stream')
@app.route("/about")
def about():
    return render_template('about.html', title='About',)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form,msg=message)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form,msg=message)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form,msg=message)
@app.route('/graphs',methods=['GET','POST'])
def graphs():
    global message
    if request.method == 'POST':
        path=request.form['url']
        print("Leak in graphs")
        print('Path',path)
        flash('Leak Detected','danger')
        message="Leak"

        return redirect(path)#,msg=message)

    return render_template('graphs.html',title='Graphs',msg=message)
