"""
Google Drive API Service for file uploads
"""
import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from google.oauth2 import service_account
from io import BytesIO


class GoogleDriveService:
    def __init__(self, credentials_path=None):
        """Initialize Google Drive service"""
        if credentials_path is None:
            credentials_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 
                'googleDriveServiceKey.json'
            )
        
        self.credentials_path = credentials_path
        self.service = None
        self.folder_id = None
        self._authenticate()
    
    def _authenticate(self):
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/drive']
            )
            self.service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
        except Exception as e:
            raise
    
    def set_upload_folder(self, folder_id):
        self.folder_id = folder_id
    
    def create_folder(self, folder_name, parent_folder_id=None):
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            return folder.get('id')
        except Exception as e:
            raise
    
    def upload_file(self, file_path, file_name=None, folder_id=None, make_public=False):
        try:
            if file_name is None:
                file_name = os.path.basename(file_path)
            
            # Determine MIME type based on file extension
            mime_type = self._get_mime_type(file_path)
            
            file_metadata = {'name': file_name}
            
            if folder_id or self.folder_id:
                file_metadata['parents'] = [folder_id or self.folder_id]
            
            media = MediaFileUpload(file_path, mimetype=mime_type)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink,webContentLink'
            ).execute()
            
            file_id = file.get('id')
            
            # Make file public if requested
            if make_public:
                self._make_file_public(file_id)
            
            return {
                'id': file_id,
                'name': file.get('name'),
                'webViewLink': file.get('webViewLink'),
                'webContentLink': file.get('webContentLink'),
                'public_url': f"https://drive.google.com/uc?id={file_id}" if make_public else None
            }
        except Exception as e:
            raise
    
    def upload_file_from_memory(self, file_content, file_name, mime_type, folder_id=None, make_public=False):
        try:
            file_metadata = {'name': file_name}
            
            if folder_id or self.folder_id:
                file_metadata['parents'] = [folder_id or self.folder_id]
            
            # Create MediaIoBaseUpload from file content
            if isinstance(file_content, bytes):
                file_content = BytesIO(file_content)
            
            media = MediaIoBaseUpload(
                file_content,
                mimetype=mime_type,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink,webContentLink'
            ).execute()
            
            file_id = file.get('id')
            
            # Make file public if requested
            if make_public:
                self._make_file_public(file_id)
            
            return {
                'id': file_id,
                'name': file.get('name'),
                'webViewLink': file.get('webViewLink'),
                'webContentLink': file.get('webContentLink'),
                'public_url': f"https://drive.google.com/uc?id={file_id}" if make_public else None
            }
        except Exception as e:
            raise
    
    def _make_file_public(self, file_id):
        """Make a file publicly accessible"""
        try:
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            self.service.permissions().create(
                fileId=file_id,
                body=permission
            ).execute()
        except Exception as e:
            raise
    
    def delete_file(self, file_id):
        """Delete a file from Google Drive"""
        try:
            self.service.files().delete(fileId=file_id).execute()
            return True
        except Exception as e:
            raise
    
    def list_files(self, folder_id=None, query=None):
        try:
            if folder_id:
                query = f"'{folder_id}' in parents"
            
            results = self.service.files().list(
                q=query,
                fields="nextPageToken, files(id, name, mimeType, size, createdTime, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            return files
        except Exception as e:
            raise
    
    def get_file_info(self, file_id):
        """Get information about a specific file"""
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields="id, name, mimeType, size, createdTime, modifiedTime, webViewLink, webContentLink"
            ).execute()
            return file
        except Exception as e:
            raise
    
    def _get_mime_type(self, file_path):
        """Determine MIME type based on file extension"""
        extension = os.path.splitext(file_path)[1].lower()
        
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.ppt': 'application/vnd.ms-powerpoint',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            '.txt': 'text/plain',
            '.csv': 'text/csv',
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.mov': 'video/quicktime',
            '.wmv': 'video/x-ms-wmv',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.zip': 'application/zip',
            '.rar': 'application/x-rar-compressed',
        }
        
        return mime_types.get(extension, 'application/octet-stream')
