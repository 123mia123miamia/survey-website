from flask import Flask,render_template,request,redirect,url_for
import sqlite3
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
users = {'admin': '12345'}
auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username



def init_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    namber TEXT,
    favourite_game TEXT,
    money TEXT,
    roblox_games TEXT,
    favourite_food TEXT,
    username TEXT,
    age TEXT
    )''')

    connection.commit()
    connection.close()


@app.route('/')
def info():
    return render_template('info.html')

@app.route('/submit',methods=['POST'])
def submit():
    namber= request.form['namber'].strip()
    if not namber:
        return render_template('info.html',error='please enter a namber')
    elif len(namber)!=10:
        return render_template('info.html', error='not your namber')
    for symbol in namber:
        if not symbol.isdigit():
            return render_template('info.html', error='delete the letters/symbols!!!')
    return redirect(url_for('main',namber=namber))





@app.route('/main', methods=['GET', 'POST'])
def main():
    namber = request.args.get('namber')
    if request.method == 'POST':
        favourite_game = request.form.get('favourite game')
        money = request.form.get('money')
        roblox_games = request.form.getlist('roblox games')
        roblox_games_str = ','.join(roblox_games)
        favourite_food = request.form.getlist('favourite food')  # checkbox type
        favourite_food_str = ','.join(favourite_food)
        username = request.form.get('username')
        age = request.form.get('age')

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO results(namber,favourite_game,money,roblox_games,favourite_food,username,age)
        VALUES(?,?,?,?,?,?,?)''',(namber,favourite_game,money,roblox_games_str,favourite_food_str,username,age))
        connection.commit()
        connection.close()

        return render_template('goodbye.html')
    return render_template('main.html',namber=namber)


@app.route('/resuts')
@auth.login_required
def results():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM results''')
    data = cursor.fetchall()
    connection.close()
    return render_template('resuts.html',data=data)

init_db()
if __name__ == '__main__':
    app.run(debug = True, port=5001)