import io
import zipfile
from pathlib import Path
import requests
from app.services.conversor import heic_para_jpg_bytes

def download_and_convert_to_zip(urls: list) -> io.BytesIO:
    """Baixa cada URL, converte para JPG e retorna um buffer ZIP."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for url in urls:
            try:
                resp = requests.get(url, timeout=30)
                resp.raise_for_status()
                jpg_bytes = heic_para_jpg_bytes(resp.content)
                original_name = url.split('/')[-1]
                base_name = Path(original_name).stem
                zf.writestr(f"{base_name}.jpg", jpg_bytes)
            except Exception as e:
                error_filename = f"erro_{Path(url).stem}.txt"
                zf.writestr(error_filename, str(e))
    zip_buffer.seek(0)
    return zip_buffer