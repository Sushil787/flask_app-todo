from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable =False)
    date_created = db.Column(db.DateTime , default=datetime.utcnow )
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"



@app.route('/', methods=["GET", "POST"])
def home():
    if(request.method == "POST"):
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc = desc)
        db.session.add(todo)
        db.session.commit()

    allTodos = Todo.query.all()
    return render_template('index.html', allTodos=allTodos)
@app.route('/Delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/Update/<int:sno>', methods=["GET","POST"])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return todo.title, todo.desc

    # render_template('update.html', todo=todo)

if __name__ == '__main__':
    app.run(debug=True)