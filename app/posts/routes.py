from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app import db
from app.models import Post, User
from app.posts.forms import PostForm


posts=Blueprint("posts", __name__)
@posts.route("/posts/new", methods=["POST", "GET"])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash("Your Post was created successfuly", "success")
        return redirect(url_for('main.fuck_off'))
    return render_template('create_posts.html', title="New Post", form=form, nature="New")

@posts.route("/post/<int:post_id>/")
def view_post(post_id):
    post:Post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=f'{post.title}', post=post, User=User)

@posts.route("/post/<int:post_id>/update", methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post:Post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("You edited the post securely", "success")    
        return redirect(url_for("posts.view_post", post_id=post.id))
    elif request.method == "GET":
        form.content.data = post.content
        form.title.data = post.title
    return render_template("create_posts.html", title="Edit Post", form=form, nature="Edit")


@posts.route("/post/<int:post_id>/delete", methods=["POST", "GET"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if (post.author != current_user):
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully", "warning")
    return redirect(url_for("main.fuck_off"))


