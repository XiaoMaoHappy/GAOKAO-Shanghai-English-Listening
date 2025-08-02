"""
『聪耳慧听』
上海高考外语听说测试 英语听力模拟

版本号：v1.0.0
修改日期：2025年8月2日

开发者：快乐之源毛毛（XiaoMaoHappy）
GitHub地址：https://github.com/XiaoMaoHappy/GAOKAO-Shanghai-English-Listening

非官方软件 仅供个人练习与技术交流使用
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import pygame.mixer
# import os
import json


version = "v1.0.0"

# current_folder = os.path.dirname(os.path.abspath(__file__))
current_folder = "."

path_icon = current_folder + "/picture/icon.png"
path_bg_device_testing = current_folder + "/picture/DeviceTesting.png"
path_bg_listening = current_folder + "/picture/Listening.png"
path_audio_device_testing = current_folder + "/audio/SystemAdvice_DeviceTesting.mp3"

accepted_testpaper_version = (1, 1)  # 可接受的试题文件版本区间 区间两端取闭集


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


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

    def play_music(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def load_music(self, file_path):
        pygame.mixer.music.load(file_path)

    def get_audio_duration(self):
        duration = pygame.mixer.music.get_length()
        return duration


class TestPaper:
    def __init__(self):
        self.name = ""
        self.questions = []
        self.answers = ""

    def load(self, file_path):
        """
        加载试题JSON文件并进行文件合法性校验
        :return: 若成功加载就返回false 若加载失败就返回报错原因字符串
        """
        # 试题JSON文件导入校验
        try:
            file = json.load(open(file_path, "r", encoding="utf-8"))
        except FileNotFoundError:
            return "FileNotFoundError-找不到您选择的试题文件"
        except UnicodeDecodeError:
            return "UnicodeDecodeError-试题文件Unicode解码错误"
        except json.decoder.JSONDecodeError:
            return "json.decoder.JSONDecodeError-试题文件JSON解码错误"

        # 文件合法性校验 若不合法则返回报错原因 若合法则加载文件并返回False
        try:
            # 检测file变量类型为字典
            if type(file) != dict:
                return "您选择的试题文件不是合法的试题文件\n【type(file) != dict】"
            
            # 检测version版本信息是否为整值及其是否兼容
            elif type(file["version"]) != int:
                return "您选择的试题文件不是合法的试题文件\n【type(file[\"version\"]) != int】"
            elif accepted_testpaper_version[0] > file["version"]:
                return "您选择的试题文件版本过低，与本程序不兼容\n您选择的试题文件为第"+str(file["version"])+"代\n本程序仅支持第"+str(accepted_testpaper_version[0])+"代至第"+str(accepted_testpaper_version[1])+"代试题文件"
            elif accepted_testpaper_version[1] < file["version"]:
                return "您选择的试题文件版本过高，请更新程序后重试\n您选择的试题文件为第"+str(file["version"])+"代\n本程序仅支持第"+str(accepted_testpaper_version[0])+"代至第"+str(accepted_testpaper_version[1])+"代试题文件"
            
            # 检测name试卷名称是否为合法字符串
            elif type(file["name"]) != str:
                return "您选择的试题文件不是合法的试题文件\n【type(file[\"version\"]) != str】"

            # 检测questions试卷问题是否合法
            elif type(file["questions"]) != list:
                return "您选择的试题文件不是合法的试题文件\n【type(file[\"questions\"]) != list】"
            elif len(file["questions"]) != 20:
                return "您选择的试题文件不是合法的试题文件\n【len(file[\"questions\"]) != 20】"
            else:
                for i1 in file["questions"]:
                    if type(i1) != list:
                        return "您选择的试题文件不是合法的试题文件\n【type(file[\"questions\"][X]) != list】"
                    elif len(i1) != 4:
                        return "您选择的试题文件不是合法的试题文件\n【len(file[\"questions\"][X]) != 4】"
                    else:
                        for i2 in i1:
                            if type(i2) != str:
                                return "您选择的试题文件不是合法的试题文件\n【type(file[\"questions\"][X][X]) != str】"
                # 检测answers试卷答案是否合法 可为20位字符串或用false表示不设置答案
                if type(file["answers"]) == str:
                    if len(file["answers"]) != 20:
                        return "您选择的试题文件不是合法的试题文件\n【len(file[\"answers\"]) != 20】"
                elif file["answers"] is False:
                    pass
                else:
                    return "您选择的试题文件不是合法的试题文件\n【type(file[\"answers\"])错误】"
        except KeyError:  # 检测是否缺失关键索引
            return "您选择的试题文件不是合法的试题文件\n【KeyError-字典中缺失关键索引】"
        
        # 加载文件并返回False
        self.name = file["name"]
        self.questions = file["questions"]
        self.answers = file["answers"]
        return False


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


class MarkButton(tk.Button):
    def __init__(self, master, width=4, height=1, font=("Times New Roman", 12), bg_on="#FFE699", bg_off="#FFFFFF", foreground="#000000", relief="flat", bd=1, **kw):
        super().__init__(master, width=width, height=height, font=font, bg=bg_off, relief=relief, bd=bd, **kw)
        self.config(command=self.click)
        self.is_on = False
        self.bg_on = bg_on
        self.bg_off = bg_off

    def click(self):
        self.is_on = not self.is_on
        if self.is_on:
            self.config(bg=self.bg_on)
        else:
            self.config(bg=self.bg_off)


def starter_main():
    """
    考试系统启动器界面
    :return: None
    """
    # 窗口初始化
    global starter_root
    starter_root = tk.Tk()
    starter_root.title("『聪耳慧听』 —— 上海高考外语听说测试 英语听力模拟")
    starter_root.geometry("900x600")

    # 窗口图标
    global image_icon
    image_icon = tk.PhotoImage(file=path_icon)
    starter_root.tk.call('wm', 'iconphoto', starter_root._w, image_icon)

    # 窗口背景颜色
    global bg_color
    bg_color = "#BBDDFF"
    starter_root.configure(bg=bg_color)

    # 音乐播放器初始化
    global player
    player = MusicPlayer()

    # 试卷加载器初始化
    global paper
    paper = TestPaper()

    # 定义页面上的元素
    global starter_entry1, starter_entry2
    # 标题
    starter_label1 = tk.Label(starter_root, text="『聪耳慧听』\n\n上海高考外语听说测试 英语听力模拟", font=("simhei", 28), bg=bg_color)
    starter_label2 = tk.Label(starter_root, text="版本号："+version+"\n非官方软件\n仅供个人练习与技术交流使用", font=("fangsong", 18), bg=bg_color)
    # 选择音频&试卷文件夹
    starter_button4 = tk.Button(starter_root, command=starter_select_dir, text="选择试卷文件夹", relief="flat", font=("fangsong", 18), bg="#FFE699", foreground="#7F6000")
    # 选择音频路径
    starter_label3 = tk.Label(starter_root, text="音频路径：", font=("simhei", 18), bg=bg_color)
    starter_entry1 = tk.Entry(starter_root, font=("calibri", 18), width=40, bg="#E2F0D9", foreground="#385723")
    starter_button1 = tk.Button(starter_root, command=starter_select_audio, text="手动选择音频", relief="flat", font=("fangsong", 18), bg="#E2F0D9", foreground="#385723")
    # 选择试题路径
    starter_label4 = tk.Label(starter_root, text="试题路径：", font=("simhei", 18), bg=bg_color)
    starter_entry2 = tk.Entry(starter_root, font=("calibri", 18), width=40, bg="#E2F0D9", foreground="#385723")
    starter_button2 = tk.Button(starter_root, command=starter_select_paper, text="手动选择试题", relief="flat", font=("fangsong", 18), bg="#E2F0D9", foreground="#385723")
    starter_button3 = tk.Button(starter_root, command=starter_test, text="开始测试", relief="flat", font=("simhei", 24), bg="#FBE5D6", foreground="#843C0C")

    # 页面抬头渲染
    starter_label1.grid(row=1, column=1, columnspan=2)
    starter_label2.grid(row=2, column=1, columnspan=2, sticky="e")
    # 选择音频&试卷文件夹渲染
    starter_button4.grid(row=3, column=1, columnspan=2)
    # 选择音频路径渲染
    starter_label3.grid(row=4, column=1, columnspan=2, sticky="w")
    starter_entry1.grid(row=5, column=1, sticky="e")
    starter_button1.grid(row=5, column=2)
    # 选择试题路径渲染
    starter_label4.grid(row=6, column=1, columnspan=2, sticky="w")
    starter_entry2.grid(row=7, column=1, sticky="e")
    starter_button2.grid(row=7, column=2)
    starter_button3.grid(row=8, column=1, columnspan=2)

    # 调整各行列的权重，使各元素显示合理
    starter_root.grid_rowconfigure(0, weight=3)
    starter_root.grid_rowconfigure(1, weight=5)
    starter_root.grid_rowconfigure(2, weight=4)
    starter_root.grid_rowconfigure(3, weight=1)
    starter_root.grid_rowconfigure(4, weight=1)
    starter_root.grid_rowconfigure(5, weight=1)
    starter_root.grid_rowconfigure(6, weight=1)
    starter_root.grid_rowconfigure(7, weight=1)
    starter_root.grid_rowconfigure(8, weight=1)
    starter_root.grid_rowconfigure(9, weight=1)
    starter_root.grid_columnconfigure(0, weight=1)
    starter_root.grid_columnconfigure(1, weight=2)
    starter_root.grid_columnconfigure(2, weight=2)
    starter_root.grid_columnconfigure(3, weight=1)

    # 启动器窗口启动
    starter_root.mainloop()


def starter_select_dir():
    """
    选择试题目录
    加上"/audio.mp3"存为变量path_audio听力音频，填充到starter_entry1输入框中
    加上"/paper.json"存为变量path_paper预设试卷，填充到starter_entry2输入框中
    :return: None
    """
    global path_audio, starter_entry1, path_paper, starter_entry2
    path_dir = filedialog.askdirectory(title="请选择试题文件夹目录")
    path_audio = path_dir + "/audio.mp3"
    path_paper = path_dir + "/paper.json"
    starter_entry1.delete(0, tk.END)
    starter_entry1.insert(0, path_audio)
    starter_entry2.delete(0, tk.END)
    starter_entry2.insert(0, path_paper)


def starter_select_audio():
    """
    选择听力音频，存为变量path_audio，填充到starter_entry1输入框中
    :return: None
    """
    global path_audio, starter_entry1
    path_audio = filedialog.askopenfilename(title="请选择听力音频文件")
    starter_entry1.delete(0, tk.END)
    starter_entry1.insert(0, path_audio)


def starter_select_paper():
    """
    选择预设试卷，存为变量path_paper，填充到starter_entry2输入框中
    :return: None
    """
    global path_paper, starter_entry2
    path_paper = filedialog.askopenfilename(title="请选择预设试卷JSON文件")
    starter_entry2.delete(0, tk.END)
    starter_entry2.insert(0, path_paper)


def starter_test():
    """
    启动器转入考试界面的中间程序
    获取starter_entry1中的路径，检测其是否为可播放的音频
    获取starter_entry2中的路径，检测其是否为合法的试卷
    结束启动器窗口
    :return: None
    """
    global path_audio, path_paper, player, paper
    path_audio = starter_entry1.get()
    path_paper = starter_entry2.get()
    # 加载音频
    try:
        player.load_music(path_audio)
    except pygame.error:
        messagebox.showerror("错误", "您选择的音频文件不是合法的音频文件")
    else:
        # 加载试卷
        is_load_paper_error = paper.load(path_paper)
        if is_load_paper_error is not False:
            messagebox.showerror("错误", is_load_paper_error)
        else:
            # 结束启动器窗口并开始考试
            global starter_root
            starter_root.destroy()
            test_main()


def test_main():
    """
    考试界面初始化
    :return: None
    """
    # 窗口初始化
    global root, paper
    root = tk.Tk()
    root.title(paper.name)

    # 设置窗口全屏
    root.attributes('-fullscreen', True)

    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 创建一个灰色的背景 Frame
    background_frame = tk.Frame(root, bg='gray')
    background_frame.place(x=0, y=0, width=screen_width, height=screen_height)

    # 创建一个 Frame，大小为 900x600
    global window
    window = tk.Frame(root, bg=bg_color, width=900, height=600)

    # 计算 window 的位置，使其居中
    x_position = (screen_width - 900) // 2
    y_position = (screen_height - 600) // 2

    # 将 window 放置在窗口中央
    window.place(x=x_position, y=y_position)
    window.grid_propagate(False)

    test_device_testing()
    root.mainloop()


def test_device_testing():
    """
    试音界面
    :return: None
    """
    global root, window, player, label1, button1
    player.load_music(path_audio_device_testing)
    player.play_music()

    bg_device_testing = tk.PhotoImage(file=path_bg_device_testing)
    label1 = tk.Label(window, image=bg_device_testing, width=900, height=600)
    label1.image = bg_device_testing
    button1 = tk.Button(window, command=test_listening, text="清晰 完成试音", relief="flat", font=("simhei", 16), bg="#FFE699", foreground="#7F6000")
    label1.grid(row=0, column=0, rowspan=3)
    button1.grid(row=1, column=0, padx=10)

    # 调整各行列的权重，使各元素显示合理
    window.grid_rowconfigure(0, weight=16)
    window.grid_rowconfigure(1, weight=2)
    window.grid_rowconfigure(2, weight=1)
    window.grid_columnconfigure(0, weight=1)


def test_listening():
    """
    I. Listening Comprehension 听力部分
    :return: None
    """
    # 去除试音部分有关元素
    global root, window, player, label1, button1 
    player.stop_music()
    label1.grid_remove()
    button1.grid_remove()

    # 背景图label1
    bg_listening = tk.PhotoImage(file=path_bg_listening)
    label1 = tk.Label(window, image=bg_listening, width=900, height=600)
    label1.image = bg_listening

    # 抬头label2
    global label2
    label2 = tk.Label(window, text="I-Section A & B", width=59, font=("Times New Roman", 16), bg="#BED9F7", foreground="#000000")

    # 可上下滑动的选项页面scf
    global scf
    scf = ScrollFrame(window, width=700, height=415, bd=0, relief = "sunken", bg="#FFFFFF")

    # 加载试卷选项并渲染到scf上
    global paper, question_frames_list
    question_frames_list = []
    scf.add(tk.Label(scf, text="Section A", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000", justify="left"), row=0, column=0, columnspan=2, sticky="w")
    for i1 in range(10):
        i = i1
        i2 = i1 + 1
        question_frames_list.append(QuestionFrame(scf, bg="#FFFFFF"))
        question_frames_list[i].load(i+1, paper.questions[i])
        question_frames_list[i].grid(row=i2, column=0, sticky="w")
    scf.add(tk.Label(scf, text="\nSection B\n\nQuestions 11 through 13 are based on the following passage.", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000", justify="left"), row=11, column=0, columnspan=2, sticky="w")
    for i1 in range(3):
        i = i1 + 10
        i2 = i1 + 12
        question_frames_list.append(QuestionFrame(scf, bg="#FFFFFF"))
        question_frames_list[i].load(i+1, paper.questions[i])
        question_frames_list[i].grid(row=i2, column=0, sticky="w")
    scf.add(tk.Label(scf, text="Questions 14 through 16 are based on the following passage.", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000", justify="left"), row=15, column=0, columnspan=2, sticky="w")
    for i1 in range(3):
        i = i1 + 13
        i2 = i1 + 16
        question_frames_list.append(QuestionFrame(scf, bg="#FFFFFF"))
        question_frames_list[i].load(i+1, paper.questions[i])
        question_frames_list[i].grid(row=i2, column=0, sticky="w")
    scf.add(tk.Label(scf, text="Questions 17 through 20 are based on the following passage.", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000", justify="left"), row=19, column=0, columnspan=2, sticky="w")
    for i1 in range(4):
        i = i1 + 16
        i2 = i1 + 20
        question_frames_list.append(QuestionFrame(scf, bg="#FFFFFF"))
        question_frames_list[i].load(i+1, paper.questions[i])
        question_frames_list[i].grid(row=i2, column=0, sticky="w")
    scf.add(tk.Frame(scf, width=10, height=100, bg="#FFFFFF"), row=24, column=1, sticky="w")

    # 界面右侧试题标注区各元素定义
    global frame_mark, label_mark1, label_mark2, button_mark1
    frame_mark = tk.Frame(window, width=140, height=350, bd=0, relief = "sunken", bg="#FFFFFF")
    label_mark1 = tk.Label(frame_mark, text="Section A", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000", justify="left")
    label_mark2 = tk.Label(frame_mark, text="Section B", font=("Times New Roman", 14), bg="#FFFFFF", foreground="#000000", justify="left")
    button_mark1 = tk.Button(frame_mark, command=test_finish, text="结束考试", font=("fangsong", 14), bg="#E2F0D9", foreground="#385723", relief="flat")
    
    # 界面右侧试题标注区渲染到frame_mark上
    mark_buttons_list = []
    label_mark1.grid(row=0, column=0, columnspan=3, sticky="w")
    for i1 in range(3):
        for i2 in range(3):
            i = 3 * i1 + i2
            mark_buttons_list.append(MarkButton(frame_mark, text=str(i+1)))
            mark_buttons_list[i].grid(row=i1+1, column=i2)
    mark_buttons_list.append(MarkButton(frame_mark, text="10"))
    mark_buttons_list[9].grid(row=4, column=0)
    label_mark2.grid(row=5, column=0, columnspan=3, sticky="w")
    for i1 in range(3):
        for i2 in range(3):
            i = 3 * i1 + i2 + 10
            mark_buttons_list.append(MarkButton(frame_mark, text=str(i+1)))
            mark_buttons_list[i].grid(row=i1+6, column=i2)
    mark_buttons_list.append(MarkButton(frame_mark, text="20"))
    mark_buttons_list[19].grid(row=9, column=0)
    button_mark1.grid(row=10, column=0, columnspan=3)
    

    # 渲染页面上各元素
    # label1.grid(row=0, column=0, rowspan=7, columnspan=5)
    label1.grid(row=0, column=0, rowspan=3)
    # label2.grid(row=1, column=0)
    label2.place(x=10, y=85)
    # scf.grid(row=2, column=0, rowspan=3)
    scf.place(x=5, y=120)
    frame_mark.place(x=755, y=180)

    # 调整各行列的权重，使各元素显示合理
    # window.grid_rowconfigure(0, weight=8)
    # window.grid_rowconfigure(1, weight=3)
    # window.grid_rowconfigure(2, weight=6)
    # window.grid_rowconfigure(3, weight=32)
    # window.grid_rowconfigure(4, weight=6)
    # window.grid_rowconfigure(5, weight=3)
    # window.grid_rowconfigure(6, weight=2)
    # window.grid_columnconfigure(0, weight=1)
    # window.grid_columnconfigure(1, weight=72)
    # window.grid_columnconfigure(2, weight=1)
    # window.grid_columnconfigure(3, weight=15)
    # window.grid_columnconfigure(4, weight=1)

    # 播放听力音频
    player.load_music(path_audio)
    player.play_music()

    # UNFINISHED


def test_finish():
    """
    结束考试并启动结算界面
    :return: None
    """
    # 弹窗确认是否结束考试
    global paper
    is_finish = messagebox.askokcancel(paper.name, "是否结束考试？")
    if not is_finish:
        return False            

    # 停止考试界面
    global root, player
    player.stop_music()
    root.destroy()

    # 结束窗口初始化
    global starter_root
    finish_root = tk.Tk()
    finish_root.title(paper.name)
    finish_root.geometry("900x600")

    # 设置窗口图标
    global image_icon
    image_icon = tk.PhotoImage(file=path_icon)
    finish_root.tk.call('wm', 'iconphoto', finish_root._w, image_icon)

    # 结束窗口背景颜色
    global bg_color
    finish_root.configure(bg=bg_color)

    # 结束窗口各元素定义
    label_finish1 = tk.Label(finish_root, text=paper.name, font=("simhei", 20), bg=bg_color, foreground="#000000")
    label_finish1.grid(row=0, column=0, columnspan=7)
    label_finish2 = tk.Label(finish_root, font=("fangsong", 20), bg=bg_color, foreground="#000000")
    label_finish2.grid(row=1, column=0, columnspan=7)
    label_finish3 = tk.Label(finish_root, text="详细作答情况：（ 方括号【】内为正确答案 ）", font=("simhei", 16), bg=bg_color, foreground="#000000")
    label_finish3.grid(row=2, column=1, columnspan=5, sticky="w")

    # 调整各行列的权重，使各元素显示合理
    finish_root.grid_rowconfigure(0, weight=3)
    finish_root.grid_rowconfigure(1, weight=3)
    finish_root.grid_rowconfigure(2, weight=1)
    finish_root.grid_rowconfigure(3, weight=1)
    finish_root.grid_rowconfigure(4, weight=1)
    finish_root.grid_rowconfigure(5, weight=1)
    finish_root.grid_rowconfigure(6, weight=1)
    finish_root.grid_rowconfigure(7, weight=2)
    finish_root.grid_columnconfigure(0, weight=1)
    finish_root.grid_columnconfigure(1, weight=3)
    finish_root.grid_columnconfigure(2, weight=3)
    finish_root.grid_columnconfigure(3, weight=3)
    finish_root.grid_columnconfigure(4, weight=3)
    finish_root.grid_columnconfigure(5, weight=3)
    finish_root.grid_columnconfigure(6, weight=1)

    # 若无预设答案则反馈已选答案 若有预设答案则计算分数并反馈
    global question_frames_list
    if paper.answers is False:
        # 若无预设答案则反馈已选答案
        label_finish2.config(text="试卷中无预设答案")
        for i1 in range(4):
            for i2 in range(5):
                i = 5 * i1 + i2
                t = str(question_frames_list[i].question_number)+". "+question_frames_list[i].answer
                tk.Label(finish_root, text=t, font=("fangsong", 16), bg=bg_color, foreground="#000000").grid(row=i1+3, column=i2+1)
    else:
        # 若有预设答案则计算分数并反馈
        finish_score = 0.0  # 用户得分
        for i1 in range(2):  # 第1-10题短对话 每题1.5分
            for i2 in range(5):
                i = 5 * i1 + i2
                if question_frames_list[i].answer == paper.answers[i]:
                    t = str(question_frames_list[i].question_number)+". "+question_frames_list[i].answer
                    c = "#1D6D1D"
                    finish_score += 1.0
                else:
                    t = str(question_frames_list[i].question_number)+". "+question_frames_list[i].answer+"【"+paper.answers[i]+"】"
                    c = "#EA0000"
                tk.Label(finish_root, text=t, font=("Times New Roman", 16), bg=bg_color, foreground=c).grid(row=i1+3, column=i2+1)
        for i1 in range(2):  # 第11-20题长对话 每题1.5分
            for i2 in range(5):
                i = 5 * i1 + i2 + 10
                if question_frames_list[i].answer == paper.answers[i]:
                    t = str(question_frames_list[i].question_number)+". "+question_frames_list[i].answer
                    c = "#1D6D1D"
                    finish_score += 1.5
                else:
                    t = str(question_frames_list[i].question_number)+". "+question_frames_list[i].answer+"【"+paper.answers[i]+"】"
                    c = "#EA0000"
                tk.Label(finish_root, text=t, font=("Times New Roman", 16), bg=bg_color, foreground=c).grid(row=i1+5, column=i2+1)
        label_finish2.config(text="您的成绩为 "+str(finish_score)+"分 【总分25分】")


# 启动程序
if __name__ == '__main__':
    starter_main()
