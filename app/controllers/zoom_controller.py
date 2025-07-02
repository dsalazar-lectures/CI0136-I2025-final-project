from flask import Blueprint, request, redirect, session, url_for, flash
from app.services.meetings.zoom_meeting_service import zoom_meeting_service

zoom_bp = Blueprint('zoom', __name__)
zoom_service = zoom_meeting_service()

@zoom_bp.route('/zoom/connect')
def zoom_connect():
    # Redirige al usuario a la autorización de Zoom
    return zoom_service.connect_to_zoom()

@zoom_bp.route('/zoom/callback')
def zoom_callback():
    code = request.args.get('code')
    if not code:
        flash("No se recibió el código de autorización de Zoom.", "danger")
        return redirect(url_for('tutorial.listTutorTutorials'))  # Cambia por la ruta que prefieras

    try:
        token_data = zoom_service.handle_zoom_callback(code)
        # Guarda el access_token en la sesión o base de datos según tu lógica
        session['zoom_access_token'] = token_data['access_token']
        flash("¡Conexión con Zoom exitosa!", "success")
    except Exception as e:
        print("Error en callback:", e)  # <-- Agrega esto para debug
        
        flash(f"Error al conectar con Zoom: {str(e)}", "danger")
    return redirect(url_for('tutorial.listTutorTutorials'))  # Cambia por la ruta que prefieras
