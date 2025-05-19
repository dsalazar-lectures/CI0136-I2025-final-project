from flask import Flask, render_template
from routes.review_routes import review_bp
from app.models.review_model import get_all_reviews

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['TESTING'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

# Registrar Blueprint
app.register_blueprint(review_bp)

@app.route("/")
def home():
    comments = get_all_reviews()
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)