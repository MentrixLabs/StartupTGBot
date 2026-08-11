from PIL import Image, ImageDraw, ImageFont
import io
import random

def add_text_to_image(image_bytes, text):

    # Открываем картинку из bytes
    image = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(image)
    
    # Выбираем случайные координаты
    width, height = image.size
    x = random.randint(0, width // 2)
    y = random.randint(0, height // 2)
    
    # Шрифт (можно указать свой .ttf файл)
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    # Рисуем текст
    draw.text((x, y), text, fill="red", font=font)
    
    # Сохраняем в bytes
    output = io.BytesIO()
    image.save(output, format="JPEG")
    return output.getvalue()