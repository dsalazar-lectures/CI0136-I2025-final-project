from flask import Flask, render_template
from routes.review_routes import review_bp

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Registrar Blueprint
app.register_blueprint(review_bp)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)