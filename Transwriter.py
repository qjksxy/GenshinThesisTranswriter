from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
import textwrap
import re
import os

FONT_TCLR = "fonts/TCLR.ttf"  # 提瓦特通用语
FONT_KLR = "fonts/KLR.ttf"  # 坎瑞亚文字

class Transwriter:
    def __init__(self):
        self.page_width, self.page_height = 2479, 3508 # 纸张像素尺寸，以 300ppi A4 为例
        self.padtop, self.padbottom, self.padleft, self.padright = 200, 200, 400, 400 # 纸张边距
        self.text_color = "#5A5359" # 文字颜色
        self.text_color_i = "#312520" # 强调颜色
        self.page_bg = "#F5DEB3" # 纸张颜色
        self.curr_page_num = 1 # 当前页码
        self.page = None # 当前页面
        self.save_path = "Writing_specification_instruction"
        self.curr_height = 0
        self.pages=[]
        self.first_heading_index = 1
        self.second_heading_index = 1
        self.reference_index = 1

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
        if not os.path.exists("output/{}".format(self.save_path)):
            os.makedirs("output/{}".format(self.save_path))
        self.pages.append(self.page)
        for i in range(self.curr_page_num):
            page = self.pages[i]
            page.save("output/{}/{}-{:0>2d}.png".format(self.save_path, self.save_path, i + 1), "PNG")
        pdf_size = (2479, 3508)
        pdf = canvas.Canvas("output/{}/{}.pdf".format(self.save_path, self.save_path))
        pdf.setPageSize(pdf_size)
        for i in range(self.curr_page_num):
            page_file = "output/{}/{}-{:0>2d}.png".format(self.save_path, self.save_path, i + 1)
            pdf.drawImage(page_file, 0, 0, self.page_width, self.page_height)
            pdf.showPage()
        pdf.save()

    def draw_txt(self, txt, font_size, w, h, font_name=FONT_TCLR, maxW=65, pad=15, txt_color=None, equispaced=True):
        """
        绘制文字
        :param txt: 文字
        :param font_size: 文字大小
        :param w: 绘制起始位置的宽度坐标
        :param h: 绘制起始位置的高度坐标
        :param font_name: 字体名
        :param maxW: 每行最多字符数
        :param pad: 折行时行与行之间的间隔
        :param txt_color: 文字颜色
        :param equispaced: 是否每行均分间隔（最后一行不均分）
        """
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

    def draw_pic(self, pic):
        """
        绘制首图
        :param pic: 图片路径
        :return:
        """
        img = Image.open(pic)
        _, _, _, a = img.split()
        x = int((self.page_width - img.width)//2)
        self.page.paste(img, (x, 380), mask=a)

    def title(self, txt):
        """
        设置文章标题，每行长度限制在 35 个字符，过长则换行
        标题位置： w=0, h=500, 宽度居中。字体大小=60
        :param txt: 标题内容
        :return: 标题结束位置高度
        """
        para = textwrap.wrap(txt, width=35)
        font_size = 60
        self.curr_height = 1000
        for line in para:
            w, h = self.get_txt_size(line, font_size)
            x = int((self.page_width - w) // 2)
            self.draw_txt(line, font_size, x, self.curr_height, txt_color=self.text_color_i, equispaced=False)

    def author(self, txt):
        """
        设置文章作者
        每行最多 30 字符
        字号 40
        与标题间距 80
        :param txt:
        :return:
        """
        para = textwrap.wrap(txt, width=30)
        font_size = 40
        self.curr_height += 80
        for line in para:
            w, h = self.get_txt_size(line, font_size)
            x = int((self.page_width - w) // 2)
            self.draw_txt(line, font_size, x, self.curr_height, equispaced=False)

    def abstract(self, txt):
        """
        设置摘要
        :param txt: 摘要文本
        :return:
        """
        # 留出 标题与摘要之间的间距
        self.curr_height += 200
        # 第一行
        self.draw_txt("ABSTRACT", 40, self.padleft, self.curr_height, txt_color=self.text_color_i, equispaced=False)
        self.curr_height += 20
        self.draw_txt(txt, 30, self.padleft, self.curr_height)

    def indexterms(self, txt):
        """
        添加关键字
        :return:
        """
        self.curr_height += 50
        self.draw_txt("INDEX TERMS", 40, self.padleft, self.curr_height, txt_color=self.text_color_i, equispaced=False)
        self.curr_height += 20
        self.draw_txt(txt, 30, self.padleft, self.curr_height)

    def num2letter(self, num):
        letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                  'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                  'w', 'x', 'y', 'z']
        temp = []
        res = ""
        while(num > 0):
            num -= 1
            temp.append(letter[num % 26])
            num = num // 26
        for i in range(len(temp)):
            l = len(temp) - i - 1
            res += temp[l]
        return res

    def num2rom(self, num):
        """
        整数转罗马字母
        :param num:
        """
        c = {0: ("", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"),
             1: ("", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"),
             2: ("", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"),
             3: ("", "M", "MM", "MMM")}
        roman = []
        roman.append(c[3][num // 1000 % 10])
        roman.append(c[2][num // 100 % 10])
        roman.append(c[1][num // 10 % 10])
        roman.append(c[0][num % 10])
        s = ''
        for i in roman:
            s = s + i
        return s

    def first_heading(self, heading):
        """
        设置一级标题
        :param heading:
        :return:
        """
        self.curr_height += 100
        txt = self.num2letter(self.first_heading_index) + " " + heading
        w, _ = self.get_txt_size(txt, 40)
        w = int((self.page_width - w) // 2)
        self.draw_txt(txt, 40, w, self.curr_height,
                      txt_color=self.text_color_i, equispaced=False)
        self.first_heading_index += 1
        self.second_heading_index = 1

    def content(self, title, lines):
        """设置正文"""
        # 留出 标题与摘要之间的间距
        self.curr_height += 50
        # 第一行
        self.draw_txt(self.num2rom(self.second_heading_index) + " " + title, 35, self.padleft, self.curr_height,
                      txt_color=self.text_color_i, equispaced=False)
        self.second_heading_index += 1
        self.curr_height += 20
        for line in lines:
            self.draw_txt(line, 30, self.padleft, self.curr_height)
            self.curr_height += 20


    def acknowledgments(self, txt):
        """
        致谢部分
        致谢最后默认附加：
        礼赞摩诃善法大吉祥智慧主
        :return:
        """
        self.curr_height += 100
        self.draw_txt("ACKNOWLEDGMENTS", 35, self.padleft, self.curr_height,
                      txt_color=self.text_color_i, equispaced=False)
        self.curr_height += 20
        if len(txt) > 0:
            self.draw_txt(txt, 30, self.padleft, self.curr_height)
            self.curr_height += 15
        txt = "pay tribute to the Blessed One of Wisdom Mahakusaladhamma"
        self.draw_txt(txt, 30, self.padleft, self.curr_height)

    def add_references(self, thesis, authors, time):
        """
        添加参考文献
        时间采用原式纪年，以2020年为元年，2021年为1年，精确至日期
        :param thesis: 文献名
        :param authors: 文献作者
        :param time: 时间,格式为 (y,m,d)，如(1,12,14),为 2020-12-14
        :return:
        """
        if time[0] > 2019:
            year = self.num2letter(time[0] - 2019)
        else:
            year = self.num2letter(time[0])
        month = self.num2letter(time[1])
        day = self.num2letter(time[2])
        index = self.num2letter(self.reference_index)
        txt = authors + " " + year + " " + month + " " + day

        if (self.reference_index == 1):
            # size of "REFERENCES", 40 is (366, 41)
            # 另起一页居中写 REFERENCES
            self.cut_page()
            w = int((self.page_width - 366) // 2)
            self.draw_txt("REFERENCES", 40, w, self.curr_height,
                          txt_color=self.text_color_i, equispaced=False)
            self.curr_height += 100
        _, h = self.get_txt_size(index, 30)
        self.draw_txt(index, 30, self.padleft, self.curr_height)
        self.curr_height = self.curr_height - h - 15
        self.draw_txt(thesis, 30, self.padleft + 60, self.curr_height)
        self.draw_txt(txt, 30, self.padleft + 60, self.curr_height)
        self.reference_index += 1

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
