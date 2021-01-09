import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

# Configure app
app = Flask(__name__)

# Connect to database
db = sqlite3.connect("store.db",check_same_thread=False)

c = db.cursor()
# Configure sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    books = db.execute("SELECT * FROM books")
    ayse =[dict(id=book[0], title=book[1]) for book in books.fetchall() ]
    return render_template("books.html", books=ayse)


@app.route("/cart", methods=["GET", "POST"])
def cart():

    # Ensure cart exists
    if "cart" not in session:
        session["cart"] = []

    # POST
    if request.method == "POST":
        id = request.form.get("id")
        if id:
            session["cart"].append(id)
        return redirect("/cart")

    # GET
   
    
    query = f"SELECT * FROM books WHERE id IN ({','.join(['?'] * len(session['cart']))})"
    books =  db.execute(query,session['cart'])
    ayse =[dict(id=book[0], title=book[1]) for book in books.fetchall()]
    return render_template("cart.html", books=ayse)
