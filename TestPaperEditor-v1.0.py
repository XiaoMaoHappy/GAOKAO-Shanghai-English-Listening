"""
『聪耳慧听』
上海高考外语听说测试 英语听力模拟
试卷制作工具

版本号：v1.0
修改日期：2025年8月2日

开发者：快乐之源毛毛（XiaoMaoHappy）
GitHub地址：https://github.com/XiaoMaoHappy/GAOKAO-Shanghai-English-Listening

非官方软件 仅供个人练习与技术交流使用
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from shutil import copy2
from os import mkdir
# from os.path import dirname, abspath
from json import dump
from time import strftime

version = "v1.0"  # 试卷制作工具的软件版本号
version_paper = 1  # JSON格式试卷文件的版本号

# current_folder = dirname(abspath(__file__))
current_folder = "."

class ScrollFrame(tk.Frame):  # 带滑动条的Frame
    def __init__(self,master,width=100,height=100, bg="#FFFFFF", **kw):
        self.frame = tk.Frame(master, bg=bg,**kw)
        self.width = width
        self.height = height
        self.bg = bg
        self.is_use_mwsl = False

        self.canvas = tk.Canvas(self.frame, bg=self.bg)     # 创建画布
        self.canvas.grid()

        self.scrolly=tk.Scrollbar(self.frame,orient="vertical",command=self.canvas.yview)      #创建滚动条
        self.scrolly.grid(row = 0,column = 1,sticky = "ns")
        self.canvas.configure(yscrollcommand=self.scrolly.set)

        super().__init__(self.canvas)     # 在画布上创建frame
        self.configure(bg=self.bg, width=self.width)
        self.canvas.create_window((0,0),window=self,anchor='nw')    # 要用create_window才能跟随画布滚动
        self.bind("<Configure>",self.updCanvas)
        self.canvas.grid(row = 0,column = 0,sticky = "nwse")
        self.rowconfigure(0,weight = 1)
        self.columnconfigure(0,weight = 1)
        self.canvas.bind("<MouseWheel>",self.wheelBind)
        self.frame.bind("<MouseWheel>",self.wheelBind)
        self.bind("<MouseWheel>",self.wheelBind)

    def syncColor(self,event = None):
        self.canvas.config(bg = self.bg)

    def wheelBind(self,event=None):
        if event is None:
            self.canvas.yview_scroll(2, "units")
        else:
            self.canvas.yview_scroll(-event.delta // 120, "units")

    def updCanvas(self,event):
        self.canvas.config(bg = self.bg)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width = self.width,height = self.height)
        self.update()

    def add(self,mod,**kw):
        mod.grid(**kw)
        mod.bind("<MouseWheel>",self.wheelBind)

    def grid(self,**kw):
        tk.Grid.grid_configure(self.frame,**kw)

    def place(self,**kw):
        self.frame.place(**kw)


class QuestionFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.question_number = 0  # 题号
        self.choice_list = []  # 本题目的选项 列表
        self.answer = "未作答"  # 本题目所选的答案 字符串
        # 一道题Frame中各元素定义
        self.label_question_number = tk.Label(self, font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000")
        self.button_choice_a = tk.Button(self, command=self.change_answer_a,  relief="flat", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000")
        self.button_choice_b = tk.Button(self, command=self.change_answer_b,  relief="flat", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000")
        self.button_choice_c = tk.Button(self, command=self.change_answer_c,  relief="flat", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000")
        self.button_choice_d = tk.Button(self, command=self.change_answer_d,  relief="flat", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000")
        if type(master) == ScrollFrame:
            self.bind("<MouseWheel>",master.wheelBind)
            self.label_question_number.bind("<MouseWheel>",master.wheelBind)
            self.button_choice_a.bind("<MouseWheel>",master.wheelBind)
            self.button_choice_b.bind("<MouseWheel>",master.wheelBind)
            self.button_choice_c.bind("<MouseWheel>",master.wheelBind)
            self.button_choice_d.bind("<MouseWheel>",master.wheelBind)

    def load(self, question_number, choice_list):
        self.question_number = question_number
        self.choice_list = choice_list
        # 各元素文本插入
        self.label_question_number.config(text=str(question_number)+". ")
        self.button_choice_a.config(text="○ A. "+self.choice_list[0])
        self.button_choice_b.config(text="○ B. "+self.choice_list[1])
        self.button_choice_c.config(text="○ C. "+self.choice_list[2])
        self.button_choice_d.config(text="○ D. "+self.choice_list[3])
        # 各元素渲染至self上
        self.label_question_number.grid(row=0, column=0, sticky="w")
        self.button_choice_a.grid(row=0, column=1, sticky="w")
        self.button_choice_b.grid(row=1, column=1, sticky="w")
        self.button_choice_c.grid(row=2, column=1, sticky="w")
        self.button_choice_d.grid(row=3, column=1, sticky="w")

    def change_answer_a(self):
        self.answer = "A"
        self.button_choice_a.config(text="◉ A. "+self.choice_list[0], foreground="#EA0000")
        self.button_choice_b.config(text="○ B. "+self.choice_list[1], foreground="#000000")
        self.button_choice_c.config(text="○ C. "+self.choice_list[2], foreground="#000000")
        self.button_choice_d.config(text="○ D. "+self.choice_list[3], foreground="#000000")

    def change_answer_b(self):
        self.answer = "B"
        self.button_choice_a.config(text="○ A. "+self.choice_list[0], foreground="#000000")
        self.button_choice_b.config(text="◉ B. "+self.choice_list[1], foreground="#EA0000")
        self.button_choice_c.config(text="○ C. "+self.choice_list[2], foreground="#000000")
        self.button_choice_d.config(text="○ D. "+self.choice_list[3], foreground="#000000")

    def change_answer_c(self):
        self.answer = "C"
        self.button_choice_a.config(text="○ A. "+self.choice_list[0], foreground="#000000")
        self.button_choice_b.config(text="○ B. "+self.choice_list[1], foreground="#000000")
        self.button_choice_c.config(text="◉ C. "+self.choice_list[2], foreground="#EA0000")
        self.button_choice_d.config(text="○ D. "+self.choice_list[3], foreground="#000000")

    def change_answer_d(self):
        self.answer = "D"
        self.button_choice_a.config(text="○ A. "+self.choice_list[0], foreground="#000000")
        self.button_choice_b.config(text="○ B. "+self.choice_list[1], foreground="#000000")
        self.button_choice_c.config(text="○ C. "+self.choice_list[2], foreground="#000000")
        self.button_choice_d.config(text="◉ D. "+self.choice_list[3], foreground="#EA0000")



def select_audio():
    """
    选择听力音频，存为变量path_audio，填充到entry1输入框中
    :return: None
    """
    global path_audio, entry1
    path_audio = filedialog.askopenfilename(title="请选择听力音频文件")
    entry1.delete(0, tk.END)
    entry1.insert(0, path_audio)


def analyse():
    """
    加载输入内容
    :return: 若有报错中断运行则为False 无报错顺利运行则为导出到JSON文件的字典dict_json
    """
    # 加载试卷名称存为name
    global entry2
    name = entry2.get()

    # 加载问题存为questions
    # 获取scr输入框内容存为字符串text_scr
    global scr
    text_scr = scr.get("1.0", tk.END)
    # 将获取到的text字符串按照[".", " ", "\n"]中的任一元素断开 拆分成词语的列表words_list
    words_list = []
    word = ""
    for character in text_scr:
        if character in [".", " ", "\n"]:
            if word == "":
                pass
            else:
                words_list.append(word)
                word = ""
        else:
            word += character
    # 获取1-20题号数字所在words_list中的索引号 存为number_index_list
    number_index_list = []
    for i in range(20):
        try:
            number_index_list.append(words_list.index(str(i+1)))
        except ValueError:
            messagebox.showerror("错误", "试题加载错误\n分词中找不到\""+str(i+1)+"\"")
            return False
    # 比较number_index_list中的元素是否从小到大依次排列
    for i in range(19):
        if number_index_list[i] >= number_index_list[i+1]:
            messagebox.showerror("错误", "试题加载错误\n第"+str(i+1)+"号到第"+str(i+2)+"号题号index排序错误")
            return False
    # 将words_list在各1-20题号数字处切断 分为各列表 存入questions_unchopped_choices_list
    questions_unchopped_choices_list = []
    for i in range(19):
        a = words_list[number_index_list[i]:number_index_list[i+1]]
        del a[0]
        questions_unchopped_choices_list.append(a)
    a = words_list[number_index_list[19]:]
    del a[0]
    questions_unchopped_choices_list.append(a)
    # 准备将questions_unchopped_choices_list中各个元素再从大写字母["A", "B", "C", "D"]中任一元素切断
    questions = []
    question_no = 0
    for i in questions_unchopped_choices_list:  # 将questions_unchopped_choices_list列表的各个元素小列表逐一检验
        question_no += 1  # 题号
        # 获取ABCD选项字母所在i中的索引号 存为choice_index_list
        choice_index_list = []
        for i1 in ["A", "B", "C", "D"]:
            try:
                choice_index_list.append(i.index(i1))
            except ValueError:
                messagebox.showerror("错误", "试题加载错误\n分词中第"+str(question_no)+"题找不到\""+i1+"\"")
                return False
        # 比较choice_index_list中的元素是否从小到大依次排列
        for i1 in range(3):
            if choice_index_list[i1] >= choice_index_list[i1+1]:
                messagebox.showerror("错误", "试题加载错误\n分词中第"+str(question_no)+"题第"+str(i1+1)+"号到第"+str(i1+2)+"号选项index排序错误")
                return False
        # 将i在各ABCD选项字母处切断 将各分段列表a中的词语组合成字符串b 存入choices
        choices = []
        for i1 in range(3):
            a = i[choice_index_list[i1]:choice_index_list[i1+1]]
            del a[0]
            b = a[0]
            del a[0]
            for i2 in a:
                b = b + " " + i2
            b = b + "."
            choices.append(b)
        a = i[choice_index_list[3]:]
        del a[0]
        b = a[0]
        del a[0]
        for i2 in a:
            b = b + " " + i2
        b = b + "."
        choices.append(b)
        # 将存有一道题四个选项的列表choices存入总问题列表questions
        questions.append(choices)

    # 加载答案存为answers
    # 获取输入框entry3中内容存为字符串text_entry3
    global entry3
    text_entry3 = entry3.get()
    if text_entry3 == "":
        answers = False
    else:
        # 只保留text_entry3中["A", "B", "C", "D"]的任一项 存为answers
        answers = ""
        for i in text_entry3:
            if i in ["A", "B", "C", "D"]:
                answers += i
        # 检测answers答案的长度是否为20个
        if len(answers) == 20:
            pass
        else:
            messagebox.showerror("错误", "答案加载错误\n所得的答案个数不为20个")
            return False

    # 将各信息组合成paper.json试卷文件里应有的字典
    global version_paper
    dict_json = {
        "version":version_paper,
        "name":name,
        "questions":questions,
        "answers":answers
    }

    return dict_json


def preview_questions():
    """
    预览试题
    :return: None
    """
    # 分析输入内容
    dict_json = analyse()
    if dict_json is False:
        return False
    
    # 预览窗口初始化
    preview_root = tk.Tk()
    preview_root.title("试题预览")

    # 可上下滑动的选项页面scf
    global scf
    scf = ScrollFrame(preview_root, width=700, height=415, bd=0, relief = "sunken", bg="#FFFFFF")

    # 加载试卷选项并渲染到scf上
    question_frames_list = []
    scf.add(tk.Label(scf, text="Section A", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000", justify="left"), row=0, column=0, columnspan=2, sticky="w")
    for i1 in range(10):
        i = i1
        i2 = i1 + 1
        question_frames_list.append(QuestionFrame(scf, bg="#FFFFFF"))
        question_frames_list[i].load(i+1, dict_json["questions"][i])
        question_frames_list[i].grid(row=i2, column=0, sticky="w")
    scf.add(tk.Label(scf, text="\nSection B\n\nQuestions 11 through 13 are based on the following passage.", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000", justify="left"), row=11, column=0, columnspan=2, sticky="w")
    for i1 in range(3):
        i = i1 + 10
        i2 = i1 + 12
        question_frames_list.append(QuestionFrame(scf, bg="#FFFFFF"))
        question_frames_list[i].load(i+1, dict_json["questions"][i])
        question_frames_list[i].grid(row=i2, column=0, sticky="w")
    scf.add(tk.Label(scf, text="Questions 14 through 16 are based on the following passage.", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000", justify="left"), row=15, column=0, columnspan=2, sticky="w")
    for i1 in range(3):
        i = i1 + 13
        i2 = i1 + 16
        question_frames_list.append(QuestionFrame(scf, bg="#FFFFFF"))
        question_frames_list[i].load(i+1, dict_json["questions"][i])
        question_frames_list[i].grid(row=i2, column=0, sticky="w")
    scf.add(tk.Label(scf, text="Questions 17 through 20 are based on the following passage.", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000", justify="left"), row=19, column=0, columnspan=2, sticky="w")
    for i1 in range(4):
        i = i1 + 16
        i2 = i1 + 20
        question_frames_list.append(QuestionFrame(scf, bg="#FFFFFF"))
        question_frames_list[i].load(i+1, dict_json["questions"][i])
        question_frames_list[i].grid(row=i2, column=0, sticky="w")
    scf.add(tk.Frame(scf, width=10, height=100, bg="#FFFFFF"), row=24, column=1, sticky="w")

    # 渲染scf并启动窗口
    scf.grid(row=0, column=0)
    preview_root.mainloop()


def save():
    """
    导出试卷文件夹
    :return: 若有报错中断运行则为False 无报错顺利运行则为None
    """
    dict_json = analyse()
    if dict_json is False:
        return False
    
    # 加载答案存为answers
    global entry1, path_audio
    path_audio = entry1.get()
    if path_audio == "":
        messagebox.showerror("错误", "未选择音频文件")
        return False

    # 命名并创建导出目录
    if dict_json["name"] == "":
        dir_name = strftime("TestPaperExport_%Y%m%d%H%M%S")
    else:
        dir_name = dict_json["name"]
    try:
        mkdir(dir_name)
    except FileExistsError:
        dir_name += strftime("%Y%m%d%H%M%S")
        try:
            mkdir(dir_name)
        except FileExistsError:
            messagebox.showerror("错误", "FileExistsError-目录下有重名文件夹")
            return False
        except PermissionError:
            messagebox.showerror("错误", "PermissionError-无法访问\n请检查试卷名称有无特殊字符或当前目录有无权限访问")
            return False
    except PermissionError:
        messagebox.showerror("错误", "PermissionError-无法访问\n请检查试卷名称有无特殊字符或当前目录有无权限访问")
        return False
    except FileNotFoundError:
        messagebox.showerror("错误", "FileNotFoundError-无法访问\n请检查试卷名称有无特殊字符或当前目录有无权限访问")
        return False

    try:
        # 在导出目录下创建audio.mp3并将选择的音频复制到此
        path_save_audio = current_folder+'\\'+dir_name+'\\'+'audio.mp3'
        with open(path_save_audio, 'w') as audio_save_file:
            audio_save_file.close()
        copy2(path_audio, path_save_audio)
        # 将dict_json保存到导出目录下paper.json文件
        with open(current_folder+'\\'+dir_name+'\\'+'paper.json', 'w', encoding="utf-8") as json_file:
            dump(dict_json, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        messagebox.showerror("错误", "FileNotFoundError-open函数找不到路径\n请检查音频文件是否存在\n请检查运行根目录是否与程序文件所在目录相同")
        return False

    label5.config(text=strftime("%Y-%m-%d %H:%M:%S 试卷文件夹成功导出 "+dir_name))

def main():
    """
    程序主函数
    :return: None
    """
    # 窗口初始化
    global root
    root = tk.Tk()
    root.title("『聪耳慧听』试卷制作工具 "+version)
    root.geometry("900x600")

    # 听力音频选取部分定义与渲染
    global entry1
    label1 = tk.Label(root, text="选择听力音频MP3文件", font=("simhei", 18), justify="left")
    entry1 = tk.Entry(root, font=("calibri", 18), width=56)
    button1 = tk.Button(root, command=select_audio, text="选择音频文件", font=("fangsong", 18))
    label1.grid(row=1, column=1, columnspan=2, sticky="w")
    entry1.grid(row=2, column=1)
    button1.grid(row=2, column=2)

    # 试卷名称输入部分定义与渲染
    global entry2
    label2 = tk.Label(root, text="输入试卷名称", font=("simhei", 18), justify="left")
    entry2 = tk.Entry(root, font=("fangsong", 18), width=70)
    label2.grid(row=3, column=1, columnspan=2, sticky="w")
    entry2.grid(row=4, column=1, columnspan=2)
    
    # 试题部分输入与渲染
    global scr
    label3 = tk.Label(root, text="输入试题", font=("simhei", 18), justify="left")
    label3.grid(row=5, column=1, columnspan=2, sticky="w")
    scr = scrolledtext.ScrolledText(root, width=90, height=12, font=("Times New Roman", 14))
    scr.grid(row=6, column=1, columnspan=2)

    # 试卷名称输入部分定义与渲染
    global entry3
    label4 = tk.Label(root, text="输入答案（选填）", font=("simhei", 18), justify="left")
    entry3 = tk.Entry(root, font=("Times New Roman", 18), width=70)
    label4.grid(row=7, column=1, columnspan=2, sticky="w")
    entry3.grid(row=8, column=1, columnspan=2)

    # 按钮定义与渲染
    button2 = tk.Button(root, command=preview_questions, text="预览试题", font=("fangsong", 18))
    button2.grid(row=9, column=1, columnspan=2)
    button3 = tk.Button(root, command=save, text="导出试卷文件夹", font=("fangsong", 18), bg="#FFE699")
    button3.grid(row=10, column=1, columnspan=2)

    # 提示反馈定义与渲染
    global label5
    label5 = tk.Label(root, text=":)", font=("fangsong", 18))
    label5.grid(row=11, column=1, columnspan=2)
    
    # 调整各行列的权重，使各元素显示合理
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_rowconfigure(6, weight=5)
    root.grid_rowconfigure(7, weight=1)
    root.grid_rowconfigure(8, weight=1)
    root.grid_rowconfigure(9, weight=1)
    root.grid_rowconfigure(10, weight=1)
    root.grid_rowconfigure(11, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=10)
    root.grid_columnconfigure(2, weight=4)
    root.grid_columnconfigure(3, weight=1)

    root.mainloop()


# 启动程序
if __name__ == '__main__':
    main()