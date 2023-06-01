import flask
from flask import flash, render_template
import psycopg2
from flask import request

# Make the flask app
app = flask.Flask(__name__)
def debug(s):
    """Prints a message to screen (not web browser)
    if FLASK_DEBUG is set."""
    if app.config['DEBUG']:
        print(s)
def get_db():
    return psycopg2.connect(
        host="localhost",
        database="flask_app",
        port=5432,
        user="postgres",
        password="1111"
    )
@app.route("/add", methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()

        flash('Запис успішно додано!')
        return redirect(url_for('browse'))
    else:
        return render_template('add.html')
@app.route("/browse", methods=['get', 'post'])
def browse():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rowlist = cursor.fetchall()
    print(rowlist);
    return render_template('browse.html', entries=rowlist)
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)