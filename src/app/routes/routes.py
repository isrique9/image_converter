from flask import Blueprint, render_template, request, flash, redirect, send_file
import io
import json as json_lib
from werkzeug.utils import secure_filename
from app.services.conversor import heic_para_jpg_bytes
from app.services.image_downloader import download_and_convert_to_zip
from app.services.json_parser import extract_image_urls
from app.services.file_validator import allowed_file

bp = Blueprint('main', __name__)

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
            
            # ===== CASO 1: Arquivo JSON (conversão em lote) =====
            if filename.lower().endswith('.json'):
                try:
                    # Carrega o JSON a partir dos bytes
                    data = json_lib.loads(file_bytes.decode('utf-8'))
                    # Extrai todas as URLs de imagem do JSON
                    urls = extract_image_urls(data)
                    
                    if not urls:
                        flash('Nenhuma URL de imagem encontrada no arquivo JSON.')
                        return redirect(request.url)
                    
                    # Baixa todas as imagens, converte e empacota em ZIP
                    zip_buffer = download_and_convert_to_zip(urls)
                    
                    # Retorna o ZIP para download
                    return send_file(
                        zip_buffer,
                        mimetype='application/zip',
                        as_attachment=True,
                        download_name='imagens_convertidas.zip'
                    )
                
                except Exception as e:
                    flash(f'Erro ao processar o JSON: {str(e)}')
                    return redirect(request.url)
            
            # ===== CASO 2: Arquivo HEIC/HEIF (conversão individual) =====
            else:
                try:
                    jpg_bytes = heic_para_jpg_bytes(file_bytes)
                    # Retorna o arquivo JPG diretamente
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
            flash('Formato não suportado. Envie arquivos .heic, .heif ou .json')
            return redirect(request.url)
    
    # GET: renderiza a página com o formulário
    return render_template('index.html')