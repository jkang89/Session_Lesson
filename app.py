from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("username"):
        return render_template("wall.html")
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
    else:
        flash('Password incorrect, there may be a ferret stampede in progress!')

    return redirect(url_for("index"))

@app.route("/register")
def register():
    return render_template("register.html")

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
                                        username = session.get(username, None))

if __name__ == "__main__":
    app.run(debug = True)
