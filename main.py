from Transwriter import Transwriter

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