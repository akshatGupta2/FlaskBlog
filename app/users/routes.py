
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import db, bcrypt
from app.models import Post, User
from app.users.form import EditUser, LoginForm, RegistrationForm, RequestResetForm, ResetPassword
from app.users.utils import save_picture, send_reset_email

users=Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POst'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.fuck_off"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pawd = bcrypt.generate_password_hash(form.paswd.data)
        user = User(user_name=form.user_name.data, email=form.email.data, paswd=hashed_pawd)
        db.session.add(user)
        db.session.commit()
        flash(f"User Created for the Data {form.user_name.data}!", "success")
        return redirect(url_for("users.login_func"))
    return render_template('register.html', title="Register", form=form)


@users.route('/login', methods=['GET', 'POST'])
def login_func():
    if current_user.is_authenticated:
        return redirect(url_for("main.fuck_off"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.paswd, form.paswd.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Logged In", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.fuck_off"))
        else:
            flash(f"Login Failed", "danger")
    return render_template('login.html', title="Login", form=form)


@users.get("/logout")
def lg_out():
    logout_user()
    flash(f'Logged out successfully', 'success')
    return redirect(url_for('main.fuck_off'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def acc_log():
    form = EditUser()
    if form.validate_on_submit():
        if form.profile_img.data:
            fn_name = save_picture(form.profile_img.data)
            current_user.image_file = fn_name
        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash("your account has been updated", "success")
        return redirect(url_for('users.acc_log')) 
    if request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email
    image_f = url_for("static", filename=f"profile_pic/{current_user.image_file}")
    if not image_f:
        print("failed to load the image file!")
    return render_template("account.html", title="Account", imgf=image_f, form=form)


@users.route("/", methods=['GET'])
def rdc():
    return redirect(url_for("main.fuck_off"))


@users.route("/user/<string:usr_name>", methods=['GET'])
def user_posts(usr_name):
    page=request.args.get('page', 1, type=int)
    user = User.query.filter_by(user_name=usr_name).first_or_404()
    posts=Post.query.filter_by(author=user)\
        .order_by(Post.date.desc())\
        .paginate(per_page=3, page=page)
    return render_template('user_posts.html', posts=posts, user=user)
    

@users.route("/reset_password", methods=['GET', "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.fuck_off"))
    
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent to your registered mail address", "info")
        return redirect(url_for("users.login_func"))
    
    return render_template("reset_request.html", title='Reset Password', form=form)


@users.route("/reset_password/<string:token>", methods=['GET', 'POST'])
def reset_password(token:str):
    if current_user.is_authenticated:
        return redirect(url_for("main.fuck_off"))
    user=User.verify_reset_token(token=token)
    
    if not user:
        flash("invalid or expired Token", "danger")
        return redirect(url_for('users.reset_request'))
    
    form=ResetPassword()
    if form.validate_on_submit():
        hashed_pawd = bcrypt.generate_password_hash(form.paswd.data)
        user.paswd = hashed_pawd
        db.session.commit()
        flash(f"Password has been updated!", "success")
        return redirect(url_for("users.login_func"))
    return render_template("reset_token.html", title="Change password", form=form)