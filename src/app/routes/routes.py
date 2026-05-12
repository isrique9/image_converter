from flask import Blueprint, request, send_file, flash, redirect
import io
from werkzeug.utils import secure_filename
from app.services.conversor import heic_para_jpg_bytes

bp = Blueprint('conversor', __name__)

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_bytes = file.read()
            try:
                jpg_bytes = heic_para_jpg_bytes(file_bytes)
                return send_file(io.BytesIO(jpg_bytes), mimetype='image/jpeg', as_attachment=True, download_name=filename.rsplit('.', 1)[0] + '.jpg')
            except ValueError as e:
                flash(str(e))
                return redirect(request.url)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload HEIC Image</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'heic', 'heif'}