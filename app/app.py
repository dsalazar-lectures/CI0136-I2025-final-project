from flask import Flask, render_template
from routes.review_routes import review_bp
from models.review_model import get_all_reviews

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['TESTING'] = False

# Registrar Blueprint
app.register_blueprint(review_bp)


# Datos de ejemplo para los comentarios
comments = get_all_reviews()

@app.route("/")
def home():
    return render_template("index.html", comments=comments)

if __name__ == "__main__":
    app.run(debug=True)