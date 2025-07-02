from flask import request, jsonify, render_template, session
from werkzeug.utils import secure_filename
import os
import tempfile
import uuid

from ..services.google_drive_service import GoogleDriveService
from ..models.repositories.users.firebase_user_repository import FirebaseUserRepository


class SimpleMediaUploadController:
    def __init__(self):
        self.drive_service = GoogleDriveService()
        self.user_repo = FirebaseUserRepository()
        
        # Configuration for different upload types
        self.config = {
            'profile_picture': {
                'allowed_extensions': {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'},
                'max_size': 5 * 1024 * 1024,  # 5MB for profile pictures
                'folder_prefix': 'profile_pics'
            },
            'attachment': {
                'allowed_extensions': {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'pdf', 'doc', 'docx', 'txt'},
                'max_size': 10 * 1024 * 1024,  # 10MB for attachments
                'folder_prefix': 'attachments'
            }
        }
    
    def is_allowed_file(self, filename, upload_type='attachment'):
        """Check if file extension is allowed for specific upload type"""
        if upload_type not in self.config:
            return False
        
        allowed_extensions = self.config[upload_type]['allowed_extensions']
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    def upload_single_file(self):
        """Handle single file upload via API"""
        try:
            # Check if file is in request
            if 'file' not in request.files:
                return jsonify({
                    'success': False,
                    'error': 'No file provided'
                }), 400
            
            file = request.files['file']
            upload_type = request.form.get('upload_type', 'attachment')  # Default to attachment
            
            if file.filename == '':
                return jsonify({
                    'success': False,
                    'error': 'No file selected'
                }), 400
            
            # Validate file type
            if not self.is_allowed_file(file.filename, upload_type):
                allowed_ext = ', '.join(self.config[upload_type]['allowed_extensions'])
                return jsonify({
                    'success': False,
                    'error': f'File type not allowed. Allowed: {allowed_ext}'
                }), 400
            
            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            max_size = self.config[upload_type]['max_size']
            if file_size > max_size:
                return jsonify({
                    'success': False,
                    'error': f'File too large. Maximum size: {max_size // (1024*1024)}MB'
                }), 400
            
            # Generate filename with type prefix
            original_filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())[:8]
            name, ext = os.path.splitext(original_filename)
            folder_prefix = self.config[upload_type]['folder_prefix']
            filename = f"{folder_prefix}_{name}_{unique_id}{ext}"
            
            # Save to temporary file and upload
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
                file.save(temp_file.name)
                temp_file_path = temp_file.name
            
            try:
                # Upload to Google Drive
                upload_result = self.drive_service.upload_file(
                    file_path=temp_file_path,
                    file_name=filename,
                    make_public=True
                )
                
                # Generate thumbnail URL for Google Drive - this works better for embedding
                file_id = upload_result['id']
                # Use thumbnail URL for better compatibility with image embedding
                direct_image_url = f"https://drive.google.com/thumbnail?id={file_id}&sz=w400-h400"
                
                if upload_type == 'profile_picture' and 'user_id' in session:
                    try:
                        print(f"Generated profile picture thumbnail URL: {direct_image_url}")
                        
                        # Don't save to Firebase immediately - wait for form submission
                        # Just store in session temporarily
                        session['temp_profile_picture_url'] = direct_image_url
                        print(f"Temporarily stored profile picture URL in session")
                    except Exception as e:
                        print(f"Failed to process profile picture: {e}")
                
                # Clean up temp file
                os.unlink(temp_file_path)
                
                return jsonify({
                    'success': True,
                    'file': {
                        'id': upload_result['id'],
                        'name': upload_result['name'],
                        'original_name': file.filename,
                        'size': file_size,
                        'url': direct_image_url,  # Use thumbnail URL for display
                        'view_link': upload_result['webViewLink'],
                        'upload_type': upload_type
                    }
                }), 200
                
            except Exception as e:
                # Clean up temp file on error
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                raise
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Upload failed. Please try again.'
            }), 500
    
    def popup_uploader(self):
        """Render the popup uploader interface"""
        upload_type = request.args.get('type', 'attachment')
        return render_template('popup_uploader.html', upload_type=upload_type)
    
    def get_upload_status(self):
        """Get current upload configuration"""
        upload_type = request.args.get('type', 'attachment')
        config = self.config.get(upload_type, self.config['attachment'])
        
        return jsonify({
            'upload_type': upload_type,
            'max_file_size_mb': config['max_size'] // (1024*1024),
            'allowed_extensions': list(config['allowed_extensions'])
        })
