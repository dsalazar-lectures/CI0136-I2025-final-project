from flask import Blueprint, render_template, request, redirect, flash

register_bp = Blueprint('register', __name__, url_prefix='/register')  

@register_bp.route('/', methods=['GET', 'POST'])  
def register():
  """
  Handles user registration.
  Routes:
  - GET: Renders the registration form.
  - POST: Processes the registration form submission.
  """
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
      flash('All fields are required.')
      return redirect('/register/')

    flash('Form submitted (simulated).')
    return redirect('/register/')
    
  return render_template('register.html')
