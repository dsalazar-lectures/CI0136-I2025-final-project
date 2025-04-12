from flask import Blueprint, render_template,  request, redirect, url_for
from app.services.note_services import get_all_notes, create_note, delete_note

notes = Blueprint('notes', __name__)

@notes.route('/notes')
def home():
    notes = get_all_notes()
    return render_template('notes.html', notes=notes)

@notes.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    create_note(title, content)
    return redirect(url_for('notes.home'))

@notes.route('/delete/<int:note_id>')
def delete_note_route(note_id):
    delete_note(note_id)
    return redirect(url_for('notes.home'))
    