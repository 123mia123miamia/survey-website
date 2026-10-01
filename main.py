from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import os
app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    DATABASE_URL = "sqlite:///surveysit.db"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
users = {'admin': '12345'}
auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username


db = SQLAlchemy(app)


class SurveyResult(db.Model):
    __tablename__ = "survey_results"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(100))
    favourite_game = db.Column(db.String(100))
    money = db.Column(db.String(100))
    roblox_games = db.Column(db.Text)
    favourite_food = db.Column(db.Text)
    username = db.Column(db.String(100))
    age = db.Column(db.String(100))


with app.app_context():
    db.create_all()


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

        result = SurveyResult(number=namber,
                              favourite_game=favourite_game,
                              money=money,
                              roblox_games=roblox_games_str,
                              favourite_food=favourite_food_str,
                              username=username,
                              age=age)
        db.session.add(result)
        db.session.commit()

        return render_template('goodbye.html')
    return render_template('main.html',namber=namber)


@app.route('/resuts')
@auth.login_required
def results():
    data=SurveyResult.query.all()

    return render_template('resuts.html',data=data)


if __name__ == '__main__':
    app.run(debug = True, port=5001)