from PIL import Image, ImageDraw, ImageFont

def generate_highlighted_caption_image(text, highlighted_word, temp_output, font_path="/System/Library/Fonts/Arial.ttf", font_size=50):
    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Create an initial image to calculate text size
    dummy_img = Image.new('RGBA', (800, 600), (255, 255, 255, 0))
    dummy_draw = ImageDraw.Draw(dummy_img)

    # Initialize variables to keep track of text width and height
    total_width, max_height = 0, 0

    # Split the text into words
    words = text.split()
    word_sizes = [dummy_draw.textsize(word, font=font) for word in words]

    # Calculate total width and maximum height of the text
    for word_size in word_sizes:
        total_width += word_size[0] + 10  # 10 is spacing between words
        max_height = max(max_height, word_size[1])

    # Create a new image with the calculated text size
    img = Image.new('RGBA', (total_width, max_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Draw each word
    x = 0  # Horizontal position
    for i, word in enumerate(words):
        if word == highlighted_word:
            # Draw highlighted word with a shadow
            draw.text((x + 2, 2), word, font=font, fill=(0, 0, 0, 128))  # Shadow
            draw.text((x, 0), word, font=font, fill=(255, 0, 0, 255))  # Highlighted word in red
        else:
            # Draw regular word with a shadow
            draw.text((x + 2, 2), word, font=font, fill=(0, 0, 0, 128))  # Shadow
            draw.text((x, 0), word, font=font, fill=(255, 255, 255, 255))  # Regular word in white

        # Update the x position for the next word
        x += word_sizes[i][0] + 10  # 10 is spacing between words

    # Save the image
    img.save(temp_output, format="PNG")


def generate_caption_image(text, temp_output, font_path="/System/Library/Fonts/Arial.ttf", font_size=50):
    # Create an image with transparent background
    img = Image.new('RGBA', (800, 600), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text size
    text_width, text_height = draw.textsize(text, font=font)

    # Create a new image with text size
    img = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Optional: Add text shadow for better readability
    shadow_color = (0, 0, 0, 128)  # Semi-transparent black
    shadow_offset = (2, 2)
    draw.text((shadow_offset[0], shadow_offset[1]), text, font=font, fill=shadow_color)

    # Draw the text
    draw.text((0, 0), text, fill=(255, 255, 255, 255), font=font)  # White text

    # Save the image
    img.save(temp_output, format="PNG") 