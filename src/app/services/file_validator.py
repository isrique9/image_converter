ALLOWED_EXTENSIONS = {'heic', 'heif', 'json'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS