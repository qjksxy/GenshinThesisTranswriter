<div align="center">
  <img src="https://github.com/qjksxy/GenshinThesisTranswriter/blob/master/github/logoGtt.png" width="300" height="200">

# GenshinThesisTranswriter

_✨ GTT，原神论文转写器。可以通过英文文本生成提瓦特语的论文，小巧易用 ✨_

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
</p>

</div>



## 项目展示

<table><tr>
<td><img src="https://github.com/qjksxy/GenshinThesisTranswriter/blob/master/github/test-01.png" border=0></td>
<td><img src="https://github.com/qjksxy/GenshinThesisTranswriter/blob/master/github/test-02.png" border=0></td>
<td><img src="https://github.com/qjksxy/GenshinThesisTranswriter/blob/master/github/test-05.png" border=0></td>
<td><img src="https://github.com/qjksxy/GenshinThesisTranswriter/blob/master/github/test-06.png" border=0></td>
</tr></table>

## 使用说明

克隆本项目，然后运行 main.py 即可。

main.py 文件中有使用的充分注释信息，只需要略作修改便可快速入手。具体如下：

```python
from Transwriter import Transwriter

if __name__ == '__main__':
    # 初始化转写器
    t = Transwriter()
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
    ack = t.get_lines_from_file("txt/acknowledgments")
    # 设置致谢
    t.acknowledgments(ack[0])
    # 添加参考文献 参数为 论文题目 论文作者 论文发表时间
    t.add_references("baiyeguowangshi", "abeiduo shatang xiangling", (1, 12, 23))
    t.add_references("baiyeguochenhunji", "xiangling zhongli alisi", (2, 2, 3))
    # 设置生成的文件名，输出路径为 output/${filename}/
    t.save_path = "test"
    # 保存论文
    t.save_paper()

```

## 项目状态

计划中的功能：

- [ ] 插入图表
- [ ] 插入表格
- [ ] 自定义主题

## 联系方式

如有任何问题，可以在此仓库的 issue 页面中提出，或直接联系：qjksxy@163.com
