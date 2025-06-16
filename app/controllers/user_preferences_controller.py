"""
User preferences setting controller module.

This module defines routes and handlers for preference setting functionality.
"""

from flask import Blueprint, request, session, redirect, url_for
from ..models.repositories.users.firebase_user_repository import FirebaseUserRepository
from app.services.audit import log_audit, AuditActionType

# Create a Blueprint
userPreferencesSetting = Blueprint('userPreferenceSettings', __name__)
# Repository for retrieving and storing user data
user_repo = FirebaseUserRepository()

@userPreferencesSetting.route("/update_notification_status", methods=["POST"])
def update_notification_status_to_disable():
  """
  Update the user notification status to false

  Email notification states:
  - True (enable): Toggle is disable
  - False (disable): Toggle is enable
  """
  # Get email to the actual user
  user_email = session.get("email")
  # Get toggle value
  raw_status = request.form["status"]
  # Transform into boolean
  status = raw_status.lower() == "true"

  # Update the value in the data base
  if not user_repo.update_user_notification_status(user_email, status):
    log_audit(
      user=session.get("name"),
      action_type=AuditActionType.USER_UPDATE,
      details=f"Failed to update notification status to {status}"
    )
  else:
    session["notification_enabled"] = status
    log_audit(
      user=session.get("name"),
      action_type=AuditActionType.USER_UPDATE,
      details=f"Successful update notification status to {status}"
    )
  
  return redirect(url_for("profile.view_profile"))