from flask import Flask, render_template, request, url_for, flash, redirect
from os import urandom
app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            messages.append({'title': title, 'content': content})
            name = "NTA - Assignment 4"
            return redirect(url_for('index', messages=name ))

    return render_template('create.html')

  
messages = [{'title': 'Job One',
             'content': 'Job One - Content'},
            {'title': 'Job Two',
             'content': 'Job Two - Content'}
            ]

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)