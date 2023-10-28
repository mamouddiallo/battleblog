from flask import flash
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "mamoud"
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(100))
	password = db.Column(db.String(100))
	confirm_password = db.Column(db.String(100))
	
	def __init__(self, firstname, lastname, email, password, confirm_password):
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.password = password
		self.confirm_password = confirm_password

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

@app.route('/register', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        user = User(firstname, lastname, email, password, confirmpassword)
        db.session.add(user)
        db.session.commit()
      
        return redirect('/login')
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session["username"] = user.firstname
            return redirect(url_for("connecter"))
    return render_template("login.html")

@app.route('/connecter', methods=['GET', 'POST'])
def connecter():
    return render_template("connecter.html")
@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/poster")
def poster():
	return render_template("poster.html")

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        post = Post(title, content, author)
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('connecter'))  # Redirigez l'utilisateur vers la page d'accueil

    return render_template('poster.html')


if __name__ == '__main__':
	app.run(debug=True)