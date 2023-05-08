from distutils.log import error
import email
from operator import methodcaller
from SearchWebsite.Model import User, pquery
from flask import  render_template, url_for, request, flash, redirect
from SearchWebsite import app, db, bcrypt
from SearchWebsite.semanticsearch import search
import faiss
from sentence_transformers import SentenceTransformer, util
from SearchWebsite.forms import RegistrationForm, LoginForm, QueryForm
from flask_login import login_user, current_user, logout_user, login_required
# from SearchWebsite.Summarizer import summarizer


#using Ginger 2 templating engine
#Bootstrap is served from a content delivery network
queries = []

model = SentenceTransformer('search/search-model')

index = faiss.read_index('SearchWebsite/disease_description.index')

@app.route("/")
@app.route("/home")
def home():
    form = QueryForm()
    if form.validate_on_submit():
        history = pquery(q=form.query.data, author=current_user)
        db.session.add(history)
        db.session.commit()
    return render_template('home.html', form = form)

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')


@app.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, 
                    email= form.email.data, 
                    password= hashed_password)
        #Add to db
        db.session.add(user)
        db.session.commit()
        flash(f'You account has now been created! You can now Login!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods = ["GET", "POST"])
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

    return render_template('login.html', title = 'Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/results", methods= ["POST"])
def results():
    form = QueryForm()
    
    query = request.form.get("query")
    
    if current_user.is_authenticated:
        history = pquery(q=form.query.data, author=current_user)
        db.session.add(history)
        db.session.commit()

    results=search(query, top_k=5, index=index, model=model)
    queries.append(query)

    return render_template('results.html', query = query, 
                            queries = queries, 
                            results = results, 
                            form =form)

@app.route("/account", methods = ["GET", "POST"])
@login_required
def account():
    list_of_queries = pquery.query.filter_by(user_id = current_user.id)
    # summary = {}
    para = ' '
     #summarized query
    Query_history = pquery.query.filter(pquery.user_id==current_user.id)
    for r in Query_history:
        para += ' '+ str(r)
    # summary = summarizer(para)[0]
    return render_template('account.html', title='Account', list_of_queries = list_of_queries) #summary = summary)

