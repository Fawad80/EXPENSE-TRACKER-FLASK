from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1️⃣ Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 2️⃣ Initialize SQLAlchemy
db = SQLAlchemy(app)

# 3️⃣ Define Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)

# 4️⃣ Create tables inside app context
with app.app_context():
    db.create_all()


# Categories for dropdown
categories = ["All", "Food", "Health", "Shopping", "Transport", "Other"]

# -------------------- Routes -------------------- #

@app.route("/")
def home():
    all_expenses = Expense.query.all()
    return render_template("index.html", expenses=all_expenses, categories=categories)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        amount = int(request.form["amount"])
        description = request.form["description"]
        category = request.form["category"]
        date = request.form["date"]

        # Add to DB
        new_exp = Expense(amount=amount, description=description, category=category, date=date)
        db.session.add(new_exp)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("index.html", expenses=Expense.query.all(), categories=categories)

@app.route("/edit/<int:exp_id>", methods=["GET", "POST"])
def edit(exp_id):
    expense_to_edit = Expense.query.get_or_404(exp_id)

    if request.method == "POST":
        expense_to_edit.amount = int(request.form["amount"])
        expense_to_edit.description = request.form["description"]
        expense_to_edit.category = request.form["category"]
        expense_to_edit.date = request.form["date"]

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", expense=expense_to_edit, categories=categories)

@app.route("/delete/<int:exp_id>")
def delete(exp_id):
    expense_to_delete = Expense.query.get_or_404(exp_id)
    db.session.delete(expense_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/filter/<category>")
def filter_category(category):
    if category == "All":
        filtered = Expense.query.all()
    else:
        filtered = Expense.query.filter_by(category=category).all()

    return render_template("index.html", expenses=filtered, categories=categories)


if __name__ == "__main__":
    app.run(debug=True)
