from flask import Blueprint, render_template, request, flash, redirect, send_file
import io
from werkzeug.utils import secure_filename
from app.services.conversor import heic_para_jpg_bytes

bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'heic', 'heif'}

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifica se o arquivo foi enviado
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
                # Retorna o arquivo JPG diretamente para download
                return send_file(
                    io.BytesIO(jpg_bytes),
                    mimetype='image/jpeg',
                    as_attachment=True,
                    download_name=filename.rsplit('.', 1)[0] + '.jpg'
                )
            except ValueError as e:
                flash(str(e))
                return redirect(request.url)
        else:
            flash('Formato não suportado. Envie arquivos .heic ou .heif')
            return redirect(request.url)
    
    # GET: renderiza a página única com o formulário
    return render_template('index.html')