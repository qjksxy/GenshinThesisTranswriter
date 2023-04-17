from Transwriter import Transwriter

if __name__ == '__main__':
    t = Transwriter()
    # 开始第一页
    t.new_page()
    # 绘制首图
    t.draw_pic("imgs/zhi.png")
    # 设置论文标题
    t.title("The Byakuyakoku Collection")
    # 设置论文作者
    t.author("apin")
    # 从文件中读取内容，并取第一行
    ab = t.get_lines_from_file("txt/abstruction")
    ab = ab[0]
    # 设置摘要
    t.abstract(ab)
    # 设置关键字
    t.indexterms("Byakuyakoku Enkanomiya")
    # 设置一级标题
    t.first_heading("content")

    vol1 = t.get_lines_from_file("txt/vol1")
    vol2 = t.get_lines_from_file("txt/vol2")
    # 写入正文内容。参数为二级标题、内容，可多次写入
    t.content("vol i", vol1)
    t.content("vol ii", vol2)
    # vol3 = t.get_lines_from_file("txt/vol3")
    # t.content("vol iii", vol3)
    # vol4 = t.get_lines_from_file("txt/vol4")
    # t.content("vol iv", vol4)
    # vol5 = t.get_lines_from_file("txt/vol5")
    # t.content("vol v", vol5)
    ack = t.get_lines_from_file("txt/acknowledgments")
    # 设置致谢
    t.acknowledgments(ack[0])
    # 添加参考文献 参数为 论文题目 论文作者 论文发表时间
    t.add_references("baiyeguowangshi", "abeiduo shatang xiangling", (1, 12, 23))
    t.add_references("baiyeguochenhunji", "xiangling zhongli alisi", (2, 2, 3))
    # 设置生成的文件名，输出路径为 output/${filename}-${pages}.png
    t.save_path = "test"
    # 保存论文
    t.save_paper()
