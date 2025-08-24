from datetime import datetime
from flask import redirect, render_template, request, url_for, Blueprint, flash, session
from models import Note, db

notes_bp = Blueprint('notes', __name__)

@notes_bp.route("/")
def home():
    if "user" not in session:
        flash("Para poder ver las notas debes iniciar sesión", "error")
        return redirect(url_for("auth.login"))
    notes = Note.query.all()
    return render_template("home.html", notes=notes)

@notes_bp.route("/crear-nota", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        created_at = request.form.get("created_at", "")

        if not len(title.strip()) > 10:
            flash("El título es muy corto, minimo 10 caracteres", "error")
            return render_template("note_form.html")
        if not len(description.strip()) > 20:
            flash("La descripción es muy corta, minimo 20 caracteres", "error")
            return render_template("note_form.html")
        if not created_at:
            flash("La fecha es obligatoria", "error")
            return render_template("note_form.html")
        
        created_at = datetime.strptime(created_at, "%Y-%m-%d").date()

        note_db =Note(
            title=title, description=description, created_at=created_at    
        )
        
        db.session.add(note_db)
        db.session.commit()
        flash("Nota creada", "success")
        return redirect(
                url_for("notes.home")
            )
    return render_template("note_form.html")

@notes_bp.route('/editar-nota/<int:id>', methods=["GET","POST"])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == "POST":
        title       = request.form.get("title", "Sin título")
        description = request.form.get("description", "Sin descripción")
        created_at  = request.form.get("created_at", "")

        created_at = datetime.strptime(created_at, "%Y-%m-%d").date()

        note.title       = title
        note.description = description
        note.created_at  = created_at

        db.session.commit()
        flash("Nota actualizada correctamente", "success")

        return redirect(url_for("notes.home"))

    return render_template("edit_note.html", note=note)

@notes_bp.route('/eliminar-nota/<int:id>', methods=["POST","GET"])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    flash("Nota eliminada correctamente", "success")
    return redirect(url_for("notes.home"))