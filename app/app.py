from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['TESTING'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

# Registrar Blueprint

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)