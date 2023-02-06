from PIL import Image, ImageDraw, ImageFont


def wrap_text_on_image(filename, fontfile, text, font_size=38):
    """
    Adds text to an image, wrapping it if necessary to fit within a defined area.

    Arguments:
    filename -- str, the path of the image file
    fontfile -- str, the path of the truetype font file
    text -- str, the text to be added to the image
    font_size -- int, the starting font size of the text, default is 38

    Returns:
    Image object -- an image object with the text added to it

    """
    image = Image.open(filename)
    draw = ImageDraw.Draw(image)

    # define area to print
    area_x = 650
    area_y = 400
    wraping_percentage = 0.85
    # define text and font
    font = ImageFont.truetype(fontfile, font_size)

    # determine font size based on image and text size
    width, height = draw.textsize(text, font)
    while width < (image.width - area_x) * wraping_percentage and height < (image.height - area_y) * wraping_percentage:
        font_size += 1
        font = ImageFont.truetype(fontfile, font_size)
        width, height = draw.textsize(text, font)

    # wrap text in the area
    text_width, text_height = draw.textsize(text, font)
    lines = []
    line = ""
    for word in text.split(" "):
        word_width, word_height = draw.textsize(word + " ", font)
        if (text_width + word_width) < ((image.width - area_x) * wraping_percentage):
            line += word + " "
            text_width += word_width
        else:
            lines.append(line)
            line = word + " "
            text_width = word_width
    lines.append(line)

    # draw text on image
    y_text = area_y
    for line in lines:
        width, height = draw.textsize(line, font)
        x_text = area_x + (image.width - area_x - width) / 2
        y_text += height
        draw.text((x_text, y_text), line, font=font, fill='#EBE9E3')

    return image
