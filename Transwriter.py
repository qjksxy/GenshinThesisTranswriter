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
        # self.page_bg = (248, 224, 181) # 纸张颜色
        self.page_bg = "#F5DEB3"
        # self.page_bg = "#FFFFFF"
        self.curr_page_num = 1 # 当前页码
        self.page = None # 当前页面
        self.save_path = "Writing_specification_instruction"
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

    def draw_txt(self, txt, font_size, w, h, font_name=FONT_TCLR, maxW=80, pad=15, txt_color=None, equispaced=True):
        if txt_color == None:
            txt_color = self.text_color
        font = ImageFont.truetype(font_name, size=font_size)
        para = textwrap.wrap(txt, width=maxW)
        self.curr_height = h
        for li in range(len(para)):
            if self.detect_bottom(font_size):
                self.cut_page()
            draw = ImageDraw.Draw(self.page)
            if equispaced and li != len(para)-1:
                words = re.split(r'\W+', para[li])
                sum_width, curr_w = 0, w
                ws = []
                for word in words:
                    _w, _ = self.get_txt_size(word, font_size)
                    ws.append(_w)
                    sum_width += _w
                interval = int((self.page_width - self.padleft - self.padright - sum_width) // (len(words) - 1))
                for i in range(len(words)):
                    draw.text((curr_w, self.curr_height), words[i], font=font, fill=txt_color)
                    curr_w += (interval + ws[i])
            else:
                draw.text((w, self.curr_height), para[li], font=font, fill=txt_color)
            _, h = self.get_txt_size(para[li], font_size)
            self.curr_height += h + pad

    def draw_pic(self):
        img = Image.open("imgs/abcde.png")
        _, _, _, a = img.split()
        x = int((self.page_width - img.width)//2)
        self.page.paste(img, (x, 400), mask=a)

    def title(self, txt):
        """
        设置文章标题，每行长度限制在 35 个字符，过长则换行
        标题位置： w=0, h=500, 宽度居中。字体大小=60
        :param txt: 标题内容
        :return: 标题结束位置高度
        """
        para = textwrap.wrap(txt, width=35)
        font_size = 60
        self.curr_height = 800
        for line in para:
            w, h = self.get_txt_size(line, font_size)
            x = int((self.page_width - w) // 2)
            self.draw_txt(line, font_size, x, self.curr_height, txt_color=self.text_color_i, equispaced=False)

    def author(self, txt):
        para = textwrap.wrap(txt, width=30)
        font_size = 40
        self.curr_height += 80
        for line in para:
            w, h = self.get_txt_size(line, font_size)
            x = int((self.page_width - w) // 2)
            self.draw_txt(line, font_size, x, self.curr_height, equispaced=False)

    def abstarction(self, txt):
        # 留出 标题与摘要之间的间距
        self.curr_height += 200
        # 第一行
        self.draw_txt("ABSTRACTION", 40, self.padleft, self.curr_height, txt_color=self.text_color_i, equispaced=False)
        self.curr_height += 20
        self.draw_txt(txt, 30, self.padleft, self.curr_height, maxW=85)

    def content(self, lines):
        # 留出 标题与摘要之间的间距
        self.curr_height += 100
        # 第一行
        self.draw_txt("CONTENT", 40, self.padleft, self.curr_height, txt_color=self.text_color_i, equispaced=False)
        self.curr_height += 20
        for line in lines:
            self.draw_txt(line, 30, self.padleft, self.curr_height, maxW=85)
            self.curr_height += 20

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
    t.save_path="The_Byakuyakoku_Collection_Vol2"
    t.new_page()
    t.draw_pic()
    t.title("The Byakuyakoku Collection Vol II")
    t.author("apin")
    ab = t.get_lines_from_file("txt/abstruction")
    t.abstarction(ab[0])
    content = t.get_lines_from_file("txt/content")
    t.content(content)
    t.save_paper()