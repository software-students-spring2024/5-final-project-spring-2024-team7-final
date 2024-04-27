from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pymongo import MongoClient
import os
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import datetime

load_dotenv()

app = Flask(__name__, template_folder='./front-end/templates', static_folder='./front-end/static')

connection = pymongo.MongoClient(os.getenv('MONGO_URI'))
db = connection[os.getenv('MONGO_DBNAME')]

app.secret_key = os.getenv('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def find_index_by_id(task_list, id):
    for index, task in enumerate(task_list):
        if task["_id"] == id:
            return index
    return -1

#Choose to register or login
@app.route('/')
def authenticate():
    return render_template('reglog.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({'username': username, 'password': password})
        if user:
            user_id = str(user['_id'])  # 将 ObjectId 转换为字符串
            login_user(User(user_id))
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error = "Incorrect password entered")
    return render_template('login.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        existing_user = db.users.find_one({'username': username})
        if existing_user:
            return 'Username already exists!'

        new_user = {
            'username': username,
            'password': password,
            'tasks': []
        }
        db.users.insert_one(new_user)
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Home Page
@app.route('/home')
@login_required
def home():
    user_id = ObjectId(current_user.id)
    user = db.users.find_one({'_id': user_id})
    tasks = user['tasks']
    return render_template('index.html', tasks=tasks, user=user)


#Add A Task
@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/add', methods=['POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        course = request.form['course']
        date = request.form['date']
        user_id = ObjectId(current_user.id)
        new_task = {
            "_id": ObjectId(),
            "title": title,
            "course": course,
            "date": date
        }
        db.users.update_one(
            {"_id": user_id},
            {"$push": {"tasks": new_task}}
        )
        return redirect(url_for('home'))
    

#Search Tasks
@app.route('/search')
def search():
    return render_template('search.html')

# Search Tasks by Course Name
@app.route('/search', methods=['POST'])
@login_required
def search_tasks():
    if request.method == 'POST':
        course_name = request.form['course']
        user_id = ObjectId(current_user.id)
        user = db.users.find_one({'_id': user_id})
        tasks = [task for task in user['tasks'] if task['course'] == course_name]
        return render_template('search_results.html', tasks=tasks, user=user, course_name=course_name)



#Edit A Task
@app.route('/edit/<user_id>/<task_id>')
def edit(task_id, user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    index = find_index_by_id(user['tasks'], ObjectId(task_id))
    task = user['tasks'][index]
    title = task['title']
    course = task['course']
    date = task['date']
    return render_template('edit.html', title=title, course=course, date=date, task=task, user=user)

@app.route('/edit/<user_id>/<task_id>', methods=['POST'])
def edit_task(task_id, user_id):
    title = request.form["title"]
    course = request.form["course"]
    date = request.form["date"]
    
    updated_task = {
        "_id": ObjectId(task_id),
        "title": title,
        "course": course,
        "date": date
    }

    db.users.update_one(
    {"_id": ObjectId(user_id), "tasks._id": ObjectId(task_id)},
    {"$set": {"tasks.$": updated_task}}
)
    return redirect(
        url_for("home")
    )


#Delete A Task
@app.route('/delete/<user_id>/<task_id>')
def delete(task_id, user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    index = find_index_by_id(user['tasks'], ObjectId(task_id))
    task = user['tasks'][index]
    title = task['title']
    course = task['course']
    date = task['date']
    return render_template('delete.html', title=title, course=course, date=date, task=task, user=user)

@app.route('/delete/<user_id>/<task_id>', methods=['POST'])
def delete_task(task_id, user_id):
    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"tasks": {"_id": ObjectId(task_id)}}}
    )
    return redirect(
        url_for("home")
    )






if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)



