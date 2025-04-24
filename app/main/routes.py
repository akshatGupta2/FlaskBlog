from flask import Blueprint, render_template, request

from app.models import Post, User


main=Blueprint("main", __name__)


@main.route("/home", methods=['GET'])
def fuck_off():
    page=request.args.get('page', 1, type=int)
    return render_template("base.html", posts=Post.query.order_by(Post.date.desc()).paginate(per_page=3, page=page), User=User)

          
@main.route("/about", methods=['GET'])
def hello():
    return render_template("about.html", title="About")


