from PIL import Image, ImageDraw, ImageFont

def generate_highlighted_caption_image(text, highlighted_word, highlighted_word_index, temp_output,
                                       text_padding=10, font_path="/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", font_size=36):
    try:
        # Load the font
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font not found, using default font")
        font = ImageFont.load_default()

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

    # Add additional padding for descenders and ascenders
    max_height += 2 * text_padding  # Add padding to top and bottom

    # Create a new image with the calculated text size
    img = Image.new('RGBA', (total_width, max_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    x = 0  # Horizontal position
    y = text_padding
    for word_index, word in enumerate(words):
        shadow_offset = (4, 4)
        shadow_color = (0, 0, 0, 128)  # Darker shadow for better contrast

        if word.lower() == highlighted_word.lower() and word_index == highlighted_word_index:
            text_color = (255, 213, 128, 255)  # Highlighted word color
        else:
            text_color = (255, 255, 255, 255)  # Regular text color (white)

        # Draw shadow
        draw.text((x + shadow_offset[0], y + shadow_offset[1]), word, font=font, fill=shadow_color)

        # Draw text with outline (stroke)
        stroke_width = 2
        stroke_fill = (0, 0, 0)  # Black stroke
        draw.text((x, y), word, font=font, fill=text_color, stroke_width=stroke_width, stroke_fill=stroke_fill)

        x += draw.textsize(word, font=font)[0] + 10

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


def get_low_confidence_words(caption_data, conf_thres):
    low_conf = ""
    for segments in caption_data["segments"]:
        for word_data in segments["words"]:
            if word_data["confidence"] < conf_thres:
                word = word_data["text"]
                conf = word_data["confidence"]
                low_conf += f" {word}->{conf}"

    return low_conf
