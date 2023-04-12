from flask import Flask,render_template,request,session,redirect,url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/cricket'

mongo = MongoClient('localhost',27017)

@app.route('/')
def index():
    if 'name' in session:
        return 'You are logged in as ' + session['name']
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form.get("name",False)})

    if login_user:
        try:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == \
                    login_user[
                        'password'].encode('utf-8'):
                session['name'] = request.form.get("name",False)
                return redirect(url_for('index'))

        except AttributeError:
            pass
        else:
            return "Invalid username and password"

    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['name']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name': request.form.get("name", False), 'password': hashpass})
            session['name'] = request.form.get("name")
            return redirect(url_for('index'))
        else:
            return 'That username already exists!'

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('name',None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.secret_key = 'mysecret'
    app.run(debug=True)