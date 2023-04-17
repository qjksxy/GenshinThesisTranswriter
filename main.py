from PIL import Image, ImageDraw, ImageFont
import textwrap
import re

FONT_TCLR = "fonts/TCLR.ttf"  # 提瓦特通用语
FONT_KLR = "fonts/KLR.ttf"  # 坎瑞亚文字

class Transwriter:
    def __init__(self):

        self.page_width, self.page_height = 2479, 3508 # 纸张像素尺寸，以 300ppi A4 为例
        self.padtop, self.padbottom, self.padleft, self.padright = 200, 200, 200, 200 # 纸张边距
        self.text_color = "#5A5359" # 文字颜色
        self.text_color_i = "#312520" # 强调颜色
        self.page_bg = (248, 224, 181) # 纸张颜色
        self.curr_page_num = 1 # 当前页码
        self.page = None # 当前页面
        self.save_path = "test"
        self.curr_height = 0
        self.pages=[]

    def new_page(self):
        self.page = Image.new('RGB', (self.page_width, self.page_height), color=self.page_bg)

    def get_txt_size(self, txt, font_size):
        """
        获取文字大小
        :param txt:
        :param font_size:
        :return: 返回文字占用的宽和高
        """
        font = ImageFont.truetype(FONT_TCLR, size=font_size)
        left, top, right, bottom = font.getbbox(txt)
        w = right - left
        h = bottom - top
        return w, h

    def detect_bottom(self, font_size=0):
        """
        检测当前高度加上一行字体之后是否会超过纸张边缘
        :param height: 当前高度
        :param font_size: 字体大小
        :return: 超过返回 True；否则返回 False
        """
        if font_size > 0:
            _, h = self.get_txt_size(txt="a", font_size=font_size)
        else:
            h = 0
        if self.curr_height + h > self.page_height - self.padbottom:
            return True
        else:
            return False

    def cut_page(self):
        """
        切断纸张，另起一页
        :return: 返回新的一页纸张
        """
        self.pages.append(self.page)
        self.curr_page_num += 1
        self.new_page()
        self.curr_height = self.padtop

    def save_paper(self):
        self.pages.append(self.page)
        for i in range(self.curr_page_num):
            page = self.pages[i]
            page.save("output/{}-{:0>2d}.png".format(self.save_path, i + 1), "PNG")

    def draw_txt(self, txt, font_size, w, h, font_name=FONT_TCLR, maxW=80, pad=20, txt_color=None):
        if txt_color == None:
            txt_color = self.text_color
        font = ImageFont.truetype(font_name, size=font_size)
        para = textwrap.wrap(txt, width=maxW)
        self.curr_height = h
        for line in para:
            if self.detect_bottom(font_size):
                self.cut_page()
            draw = ImageDraw.Draw(self.page)
            words = re.split(r'\W+', line)
            sum_width, curr_w = 0, 0
            for word in words:
                w, _ = self.get_txt_size(word, font_size)
                sum_width += w
            interval = int((self.page_width - self.padleft - self.padright - sum_width) // (len(words) - 1))
            for word in words:
                draw.text((curr_w, self.curr_height), word)
            # draw.text((w, self.curr_height), line, font=font, fill=txt_color)
            _, h = self.get_txt_size(line, font_size)
            self.curr_height += h + pad

    def title(self, txt):
        """
        设置文章标题，每行长度限制在 26 个字符，过长则换行
        标题位置： w=0, h=300, 宽度居中。字体大小=40
        :param txt: 标题内容
        :return: 标题结束位置高度
        """
        para = textwrap.wrap(txt, width=26)
        font_size = 80
        self.curr_height = 600
        for line in para:
            w, h = self.get_txt_size(line, font_size)
            x = int((self.page_width - w) // 2)
            self.draw_txt(line, font_size, x, self.curr_height, txt_color=self.text_color_i)

    def author(self, txt):
        para = textwrap.wrap(txt, width=26)
        font_size = 60
        self.curr_height += 100
        for line in para:
            w, h = self.get_txt_size(line, font_size)
            x = int((self.page_width - w) // 2)
            self.draw_txt(line, font_size, x, self.curr_height)

    def abstarction(self, txt):
        # 留出 标题与摘要之间的间距
        self.curr_height += 200
        # 第一行
        self.draw_txt("ABSTRACTION", 60, self.padleft, self.curr_height, txt_color=self.text_color_i)
        self.curr_height += 20
        self.draw_txt(txt, 60, self.padleft, self.curr_height, maxW=40)

    def get_lines_from_file(self, file_path):
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
    t = Transwriter()
    # t.new_page()
    # t.title("Writing specification instruction")
    # t.author("apin")
    lines = t.get_lines_from_file("txt/longtxt")
    para = textwrap.wrap(lines[0], width=20)
    print(para)
    for line in para:
        words = re.split(r'\W+', line)
        print(words)
    # t.abstarction(lines[0])
    # t.save_paper()