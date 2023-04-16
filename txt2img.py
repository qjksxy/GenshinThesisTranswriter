import os
import pdb

import PIL
import numpy as np
from PIL import Image, ImageFont
from PIL import ImageDraw

CANVAS_SIZE = 256
# CANVAS_SIZE = 224
# CHAR_SIZE = 200
CHAR_SIZE = 220
EMBEDDING_DIM = 128
X_OFFSET = 20
Y_OFFSET = 20


def _draw_single_char(font, ch, width, height):
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), ch, fill=0, font=font)
    # 这里的设置是为了和原始的训练集参数设置一致
    # draw.text((X_OFFSET, Y_OFFSET), ch, fill=0, font=font)
    return img


def get_textsize(font, ch):
    img = Image.new("RGB", (1, 1), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    char_size = draw.textsize(ch, font=font)
    return char_size


def draw_single_char(img, canvas_size, char_size):
    width, height = img.size
    factor = width * 1.0 / char_size

    max_height = canvas_size * 2
    if height / factor > max_height:  # too long
        img = img.crop((0, 0, width, int(max_height * factor)))
    if height / factor > char_size + 5:  # CANVAS_SIZE/CHAR_SIZE is a benchmark, height should be less
        factor = height * 1.0 / char_size

    img = img.resize((int(width / factor), int(height / factor)), resample=PIL.Image.LANCZOS)

    bg_img = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
    offset = ((canvas_size - img.size[0]) // 2, (canvas_size - img.size[1]) // 2)
    bg_img.paste(img, offset)
    return bg_img


def draw_single_char_by_font(ch, font, canvas_size, char_size):
    width, height = get_textsize(font, ch)
    char_img = _draw_single_char(font, ch, width, height)

    return draw_single_char(char_img, canvas_size, char_size)


def save_imgs(imgs, count, save_dir):
    # 这里的0是label标签
    p = os.path.join(save_dir, "0_%03d.jpg" % count)
    imgs.save(p)


def draw_paired_image(src_img, dst_img, canvas_size):
    assert src_img.size == (canvas_size, canvas_size)
    assert dst_img.size == (canvas_size, canvas_size)

    example_img = Image.new("RGB", (canvas_size * 2, canvas_size), (255, 255, 255))
    example_img.paste(dst_img, (0, 0))
    example_img.paste(src_img, (canvas_size, 0))
    return example_img


def draw_example(ch, src_font, dst_font, canvas_size, filter_hashes, char_size):
    src_img = draw_single_char_by_font(ch, src_font, canvas_size, char_size)
    dst_img = draw_single_char_by_font(ch, dst_font, canvas_size, char_size)

    # check the filter example in the hashes or not
    dst_hash = hash(dst_img.tobytes())
    if dst_hash in filter_hashes or np.min(src_img) == 255 or np.min(dst_img) == 255:
        return None

    return draw_paired_image(src_img, dst_img, canvas_size)


def draw_example_src_only(ch, src_font, dst_img, canvas_size, char_size):
    src_img = draw_single_char_by_font(ch, src_font, canvas_size, char_size)

    assert dst_img.size == (canvas_size, canvas_size), pdb.set_trace()

    if np.min(src_img) == 255 or np.min(dst_img) == 255:
        return None

    example_img = Image.new("RGB", (canvas_size * 2, canvas_size), (255, 255, 255))
    example_img.paste(dst_img, (0, 0))
    example_img.paste(src_img, (canvas_size, 0))
    return example_img


if __name__ == '__main__':
    dst_font = "fonts/InazumaLanguageNoVert-Regular.ttf"
    src_font = "fonts/TCLR.ttf"
    save_dir = "test/"
    test = "abc"

    src_font = ImageFont.truetype(src_font, size=CHAR_SIZE)
    dst_font = ImageFont.truetype(dst_font, size=CHAR_SIZE)
    count = 0
    for ch in list(test):
        dst_img = draw_single_char_by_font(ch, dst_font, CANVAS_SIZE, CHAR_SIZE)
        example_img1 = draw_example_src_only(ch, src_font, dst_img, CANVAS_SIZE, CHAR_SIZE)
        save_imgs(example_img1, count, save_dir)
        count = count + 1