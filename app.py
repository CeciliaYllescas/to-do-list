from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

#obtener ruta actual
cwd = os.getcwd()
#Crear la extesion sql alchemy
db = SQLAlchemy()
#Crea la app con flask
app = Flask(__name__)
#Configurar la base con sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{cwd}/database/tasks.db'
#inicializar la app con la extension
db.init_app(app)

#El objeto db me da acceso a db.Model, clase para definir modelo y a db.session para ejecutar consultas

# Definir modelo de tareas Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)


# db.session.add(obj) para insertar
# db.session.delete(obj) para eliminar
# db.session.commit() despues de insertar o eliminar, para commitear
#db.session.execute(db.select(...)) para consultar
# Result.scalars() method to get a list of results, 
# or the Result.scalar() method to get a single result.
#EJEMPLO DE CONSULTA
# users = db.session.execute(db.select(User).order_by(User.username)).scalars()
# return render_template("user/list.html", users=users)


#Endpoints
@app.route("/")
def home():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route("/create-task", methods=['POST'])
def create():
    task = Task(content= request.form['content'], done=False)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/done/<id>')
def done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/delete/<id>")
def delete(id):
    task = Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))





if __name__ == '__main__':
    app.run(debug=True)