from typing import List, Any

def extract_image_urls(data: Any) -> List[str]:
    """Extrai recursivamente todas as strings que parecem URLs de imagem."""
    urls = []
    if isinstance(data, dict):
        for value in data.values():
            urls.extend(extract_image_urls(value))
    elif isinstance(data, list):
        for item in data:
            urls.extend(extract_image_urls(item))
    elif isinstance(data, str):
        if (data.lower().startswith('http') and 
            any(data.lower().endswith(ext) for ext in ('.jpg', '.jpeg', '.heic', '.heif', '.webp', '.png'))):
            urls.append(data)
    return list(set(urls))