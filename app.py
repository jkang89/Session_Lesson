from flask import Flask, render_template, request, redirect, session, url_for, flash
import model
import datetime

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("username", None):
        username = session['username']
        return redirect(url_for("view_user", username = username))
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    username = model.authenticate(username, password)
    if username != None:
        flash('User authenticated!')
        session['username'] = username
        print username
    else:
        flash('Password incorrect, there may be a ferret stampede in progress!')

    return redirect(url_for("index"))

@app.route("/register")
def register():
    if session.get('username'):
        redirect(url_for("view_user", username = session.get("username")))
    else:
        return render_template("register.html")

@app.route("/register", methods=['POST'])
def create_account():
    if session.get('username'):
        redirect(url_for("view_user", username = session.get("username")))
    else:
        model.connect_to_db()
        username = request.form.get("username")
        user_id = model.new_user_id()
        if request.form.get("password") == request.form.get("password_verify"):
            password = request.form.get("password")
        if model.get_user_by_name(username):
            flash("That username is already taken!")
            return redirect(url_for("register"))
        else:
            model.add_new_user(user_id, username, password)
        return redirect(url_for("view_user", username=username))


@app.route("/logout")
def logout():
    session.clear()
    flash('Logged out!')
    return redirect(url_for("index"))

@app.route("/user/<username>")
def view_user(username):
    model.connect_to_db()
    user_id = model.get_user_by_name(username)[0]
    wall_posts = model.get_wallposts_by_user(user_id)
    return render_template("wall.html", posts = wall_posts,
                                        username = session.get("username", None))

@app.route("/user/<username>", methods=['POST'])
def post_to_wall(username):
    author_id = session.get("username", None)
    new_post = request.form.get("wall_post_text")
    model.connect_to_db()
    user_id = model.get_user_by_name(username)[0]
    model.add_new_post(user_id, user_id, author_id, datetime.datetime.now(), new_post)

    return redirect(url_for("view_user", username=username))

if __name__ == "__main__":
    app.run(debug = True)
