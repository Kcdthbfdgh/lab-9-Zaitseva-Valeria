from flask import Flask, render_template, request, redirect, url_for
from models import db, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'add' in request.form:
            game_name = request.form['game']
            year = request.form['year']
            if game_name and year.isdigit():
                new_game = Game(game=game_name, year=int(year))
                db.session.add(new_game)
                db.session.commit()
        elif 'clear' in request.form:
            Game.query.delete()
            db.session.commit()
        return redirect(url_for('index'))

    games = Game.query.all()
    return render_template('index.html', games=games)

if __name__ == '__main__':
    app.run(debug=True)
