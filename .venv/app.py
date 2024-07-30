from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    firstname = 'john'
    stuff = 'this is <strong>Bold</strong>'

    fav_pizza = ['pep', 'mush', 'cheese']
    return render_template('index.html', firstname = firstname, stuff = stuff, fav_pizza = fav_pizza)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', username = name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)