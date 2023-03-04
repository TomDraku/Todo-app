from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)



@app.route('/')
def home():
    todos = Todo.query.all()
    if len(todos) == 0:
        return render_template('index.html')
    else: 
        return render_template('index.html', todos=todos)
        
    


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        todo_title = request.form['title']
        todo = Todo(title=todo_title, complete=0)
        db.create_all()
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('home'))
    
@app.route('/update/<int:id>', methods=["POST"])
def update(id):
    todo = Todo.query.get(id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:id>', methods=["POST"])
def delate(id):
    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('home'))
    
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)