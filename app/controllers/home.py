"""
Home controller module.

This module defines routes and handlers for the home page of the application.
"""
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.audit import log_audit, AuditActionType
from ..utils.auth import login_or_role_required
from ..models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository
from flask import session
from app.services.recommendation import get_tutoring_recommender

# Create a Blueprint for home-related routes
home_bp = Blueprint('home', __name__, url_prefix="/home")

repo = FirebaseTutoringRepository()

@home_bp.route("/")
@login_or_role_required()
def home():
    log_audit("Aaron", AuditActionType.CONTENT_READ, "Home page viewed")
    
    if session.get('role') == 'Student':
        student_id = session.get('user_id')
        print(f"Student ID: {student_id}")
        tutorias = get_tutoring_recommender(student_id=student_id, repository=repo)
        print(f"Student Tutorias: {tutorias}")
        return render_template('home.html', tutorias=tutorias)

    return render_template('home.html')



