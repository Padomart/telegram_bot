import textwrap
from itertools import chain

from PIL import Image, ImageDraw, ImageFont


def generate_table_image(data: list):
    # Задаем размеры изображения и ячеек
    cell_widths = [50, 40, 40, 120, 55, 120, 40]
    cell_height = 55
    less_lines = sum(1 for item in chain.from_iterable(data) if item == "+")
    table_width = sum(cell_widths)
    table_height = cell_height * (len(data) - less_lines)

    # Создаем изображение
    image = Image.new("RGB", (table_width, table_height), "white")
    draw = ImageDraw.Draw(image)

    # Загружаем шрифт с поддержкой кириллицы
    font_path = "DejaVuSans.ttf"
    font_size = 12
    font = ImageFont.truetype(font_path, font_size)

    # Задаем начальные координаты
    x, y = 0, 0

    # Рисуем данные в таблице
    for row in data:
        x = 0
        if row[-1] == "+":
            continue

        for cell, width in zip(row, cell_widths):
            wrapped_text = textwrap.fill(cell, width=15)
            draw.rectangle((x, y, x + width, y + cell_height), outline="black")
            draw.text((x + 5, y + 5), wrapped_text.strip("-"), fill="black", font=font)
            x += width
        y += cell_height

    return image
