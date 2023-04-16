from PIL import Image, ImageDraw, ImageFont
import textwrap

TCLR = "fonts/TCLR.ttf" # 提瓦特通用语
KLR = "fonts/KLR.ttf" # 坎瑞亚文字
page_width, page_height = 2479, 3508
padtop, padbottom, padleft, padright = 200, 200, 200, 200
text_color="#5A5359"
text_color_i="#312520"
def init_img():
    """
    初始化背景图片
    :return: 返回背景图
    """
    bg = (248, 224, 181)
    img = Image.new('RGB', (page_width, page_height), color=bg)
    return img


page = 1
def save_img(img, save_path):
    global page
    img.save("output/{}-{:0>2d}.png".format(save_path, page), "PNG")
    page += 1


def detect_bottom(height, font_size=0):
    """
    检测当前高度加上一行字体之后是否会超过纸张边缘
    :param height: 当前高度
    :param font_size: 字体大小
    :return: 超过返回 True；否则返回 False
    """
    if font_size > 0:
        w, h = get_txt_size(txt="a", font_size=font_size)
    else:
        h = 0
    if height + h > page_height - padbottom:
        return True
    else:
        return False


def cut_paper(img, title):
    """
    切断纸张，另起一页
    :return: 返回新的一页纸张
    """
    save_img(img, title)
    return init_img()

def draw_txt(img, txt, font_size, w, h, font_name=TCLR, maxW=80, pad=20, txt_color=text_color):
    font = ImageFont.truetype(font_name, size=font_size)
    para = textwrap.wrap(txt, width=maxW)
    curr_h = h
    for line in para:
        draw = ImageDraw.Draw(img)
        draw.text((w, curr_h), line, font=font, fill=txt_color)
        _, h = get_txt_size(line, font_size)
        curr_h += h + pad
        if detect_bottom(curr_h, font_size):
            img = cut_paper(img, "test")
            curr_h = padtop
    return curr_h


def title(img, txt):
    """
    设置文章标题，每行长度限制在 26 个字符，过长则换行
    标题位置： w=0, h=300, 宽度居中。字体大小=40
    :param img: 图像
    :param txt: 标题内容
    :return: 标题结束位置高度
    """
    para = textwrap.wrap(txt, width=26)
    font_size = 80
    curr_h, pad = 600, 20
    for line in para:
        w, h = get_txt_size(line, font_size)
        x = int((page_width - w) // 2)
        draw_txt(img, line, font_size, x, curr_h, txt_color=text_color_i)
        curr_h += h + pad
    return curr_h


def author(img, txt, height):
    para = textwrap.wrap(txt, width=26)
    font_size = 60
    curr_h, pad = height + 100, 10
    for line in para:
        w, h = get_txt_size(line, font_size)
        x = int((page_width - w) // 2)
        draw_txt(img, line, font_size, x, curr_h, txt_color=text_color)
        curr_h += h + pad
    return curr_h


def abstarct(img, txt, height):
    # 留出 标题与摘要之间的间距
    height += 300
    # 第一行
    curr_h = draw_txt(img, "ABSTRACT", 60, padleft, height, txt_color=text_color_i)
    curr_h += 20
    draw_txt(img, txt, 60, padleft, curr_h, maxW=40)

def get_txt_size(txt, font_size):
    """
    获取文字大小
    :param txt:
    :param font_size:
    :return: 返回文字占用的宽和高
    """
    font = ImageFont.truetype(TCLR, size=font_size)
    left, top, right, bottom = font.getbbox(txt)
    w = right - left
    h = bottom - top
    return w, h

def get_lines_from_file(file_path):
    f = open(file_path)
    lines = []
    line = f.readline()
    while line:
        l = line.replace('\n', '')
        if len(l) > 0:
            lines.append(l)
        line = f.readline()
    return lines

if __name__ == '__main__':
    img = init_img()
    title_txt = "Ad astra abyssosque"
    curr_h = title(img, title_txt)
    curr_h = author(img, "Apin", curr_h)
    lines = get_lines_from_file("txt/longtxt")
    curr_h = abstarct(img, lines[0], curr_h)
    img.show("hello")
    save_img(img, "hello")