"""
Home controller module.

This module defines routes and handlers for the home page of the application.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.audit import log_audit, AuditActionType
from ..utils.auth import login_required

# Create a Blueprint for home-related routes
home_bp = Blueprint('home', __name__)

@home_bp.route("/")
def home():
    log_audit("Aaron", AuditActionType.CONTENT_READ, "Home page viewed")
    return render_template('home.html')