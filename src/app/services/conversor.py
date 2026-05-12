import io
import json
import requests
from pathlib import Path
from PIL import Image
import pillow_heif

# Registra o suporte a HEIC/HEIF no Pillow
pillow_heif.register_heif_opener()

# -------------------------------------------------------------------
# FUNÇÃO ORIGINAL (mantida inalterada)
# -------------------------------------------------------------------
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

# -------------------------------------------------------------------
# NOVAS FUNÇÕES (baseadas no converter_todas.py)
# -------------------------------------------------------------------
def converter_url_para_jpg(url, caminho_saida):
    """
    Baixa uma imagem a partir de uma URL, converte para JPG
    (se for HEIC/HEIF) e salva no caminho especificado.
    Retorna True em caso de sucesso, False em caso de erro.
    """
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        conteudo = resp.content

        imagem = Image.open(io.BytesIO(conteudo))
        if imagem.mode in ("RGBA", "P", "LA"):
            imagem = imagem.convert("RGB")
        jpg_bytes = heic_para_jpg_bytes(conteudo)
        with open(caminho_saida, "wb") as f:
            f.write(jpg_bytes)
        return True
    except Exception as e:
        print(f"    [ERRO] {url} -> {e}")
        return False

def processar_lista_imagens(lista_imagens, id_item):
    """
    Processa uma lista de dicionários com URLs de imagens,
    baixa e salva cada uma na pasta images/{id_item}/.
    """
    for img_info in lista_imagens:
        url = img_info["url"]
        campo = img_info.get("campo", "desconhecido")

        nome_original = url.split("/")[-1]
        base_name = Path(nome_original).stem
        nome_saida = f"{base_name}.jpg"

        dest_dir = Path("images") / str(id_item)
        dest_dir.mkdir(parents=True, exist_ok=True)
        caminho_jpg = dest_dir / nome_saida

        print(f"  Baixando e convertendo: {nome_saida} (campo: {campo})")
        if converter_url_para_jpg(url, caminho_jpg):
            print(f"    [OK] {nome_saida}")
        else:
            print(f"    [FALHA] {nome_saida}")

# -------------------------------------------------------------------
# BLOCO PRINCIPAL (executado apenas se rodar o script diretamente)
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Carrega o JSON
    with open("imagens_invalidas.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    print("=== Processando seção: heic_com_extensao_jpg ===")
    for item in data["heic_com_extensao_jpg"]["imagens"]:
        item_id = item["id"]
        print(f"\nID {item_id} - {len(item['lista'])} imagem(ns)")
        processar_lista_imagens(item["lista"], item_id)

    print("\n=== Processando seção: heic_com_extensao_heic ===")
    for item in data["heic_com_extensao_heic"]["imagens"]:
        item_id = item["id"]
        print(f"\nID {item_id} - {len(item['lista'])} imagem(ns)")
        processar_lista_imagens(item["lista"], item_id)

    print("\n=== Processando seção: arquivos_heic_falsos ===")
    for item in data["arquivos_heic_falsos"]["imagens"]:
        item_id = item["id"]
        print(f"\nID {item_id} - {len(item['lista'])} imagem(ns)")
        processar_lista_imagens(item["lista"], item_id)

    print("\n✅ Conversão concluída!")