
from flask import Flask, render_template,session,flash,redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, connect_db,Feedback
from forms import Register,Login,Feedback_Form
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
toolbar = DebugToolbarExtension(app)


@app.route('/')
def home():
    if 'user_name' in session :
        return redirect('/logout')
    return render_template('index.html')
@app.route('/register',methods=["GET","POST"])
def register_form():
    form = Register()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        new_user = User.register(username, password,email,firstname,lastname)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['user_name'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/feedback')

    return render_template('register.html',form=form)

@app.route('/users/delete/<string:username>',methods=["POST"])
def edit_user(username):
    if 'user_name' not in session :
        flash("Please login first!", "danger")
        return redirect('/')
    
    user = User.query.filter(User.username == username).first()
    user_feedbacks = user.feedbacks
    for fb in user_feedbacks:
        db.session.delete(fb)
        db.session.commit()
    db.session.delete(user)
    db.session.commit()
    return redirect('/logout')
    

@app.route('/login',methods=["GET","POST"])
def login():
    form = Login()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.login(username,password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_name'] = user.username
            return redirect(f'/users/{username}')
        else :
            form.username.errors = ["Invalid Username/Password"]

    return render_template('login.html',form=form)

@app.route('/users/<string:username>',methods=["Get"])
def user_username(username):
    if 'user_name' not in session :
        flash("Please login first!", "danger")
        return redirect('/')
    user = User.query.filter(User.username == username).first()
    myfeedbacks = user.feedbacks
    return render_template('user_info.html',user=user,myfeedbacks = myfeedbacks)

@app.route('/feedback',methods= ["POST","GET"])
def feedback():
    if 'user_name' not in session :
        flash("Please login first!", "danger")
        return redirect('/')

    form = Feedback_Form()
    feedbacks = Feedback.query.order_by('id').all()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data        
        new_feedback = Feedback(title=title,content=content,username=session["user_name"])
        db.session.add(new_feedback)
        db.session.commit()
        flash(f"{new_feedback.username} created New Feedback","primary")
        return redirect('/feedback')
    return render_template('feedback.html',form=form,feedbacks=feedbacks)

@app.route('/feedback/delete/<int:id>',methods=["POST"])
def feedback_delete(id):
    if 'user_name' not in session:
        flash('You must be login First',"danger")
        return redirect('/')
    feedback = Feedback.query.get_or_404(id)
    if feedback.username == session["user_name"] :
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback deleted',"info")
        return redirect('/feedback')
    flash('You have no permission to delete the Feedback',danger)
    return redirect('/feedback')

@app.route('/feedback/edit/<int:id>',methods = ["POST","GET"])
def feedback_edit(id):
    if 'user_name' not in session:
        flash('You must be login First',"danger")
        return redirect('/')
    feedback = Feedback.query.get_or_404(id)
    form = Feedback_Form()
    
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data        
        db.session.add(feedback)
        db.session.commit()
        flash(f"{feedback.username} edits Feedback","primary")
        return redirect('/feedback')
    else :
        if feedback.username == session["user_name"] :
            form.title.data = feedback.title
            form.content.data = feedback.content
        return render_template('feedback_edit.html',form=form,feedback = feedback)
    
@app.route('/logout')
def logout():
    session.pop('user_name')
    flash("Goodbye!", "info")
    return redirect('/')

