import io
from PIL import Image
import pillow_heif

# Registra o suporte a HEIC/HEIF no Pillow
pillow_heif.register_heif_opener()

def heic_para_jpg_bytes(image_bytes):
    """
    Converte bytes de imagem HEIC para JPG.
    Retorna bytes do JPG.
    """
    try:
        imagem = Image.open(io.BytesIO(image_bytes))
        if imagem.mode in ("RGBA", "P", "LA"):
            imagem = imagem.convert("RGB")
        output = io.BytesIO()
        imagem.save(output, format="JPEG", quality=85)
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        raise ValueError(f"Erro ao converter imagem: {e}")