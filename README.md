# 『聪耳慧听』<br> —— 上海高考外语听说测试 英语听力模拟

这是一名来自上海的高中生~~闲来无事~~做的小软件，开发不易，感谢支持！

开发者：快乐之源毛毛（XiaoMaoHappy）

本软件基于Python开发。<br>~~人生苦短，我用Python！~~

点个 Star 再走呗~ 😘


## 软件功能

* 模拟上海高考外语听说测试的界面，把2024届及之前纸质+广播的测试形式转换到模拟软件上供同学们练习


## 使用指南

### 导入已有试卷开始练习

1. 打开『聪耳慧听』主程序。

2. 
    * 【方法 1】点击`选择试卷文件夹`按钮选取试卷文件夹，软件将自动选取目录下的`audio.mp3`和`paper.json`。
    * 【方法 2】点击`手动选择音频`和`手动选择试题`按钮手动选取音频和试题。

<img width="676" height="474" alt="PageStarter" src="https://github.com/user-attachments/assets/cd4b4430-423e-491e-89fb-b8d16553445f" />

3. 点击`开始测试`按钮，进入试音。<br>如放音清晰请点击`清晰 完成试音`。
<img width="960" height="540" alt="PageDeviceTesting" src="https://github.com/user-attachments/assets/62b10a0a-251e-48ed-b008-6d3475912b34" />

4. 开始愉快地刷题叭~😜<br>左侧题目界面可以上下滑动；<br>右侧题目标记可以标记有疑惑的题目。
<img width="960" height="540" alt="PageListening" src="https://github.com/user-attachments/assets/3a9d8dfb-78de-4327-9a17-d0a0f90a7dac" />

5. 点击`结束考试`按钮。<br>软件将自动为您阅卷！
<img width="676" height="474" alt="PageFinish" src="https://github.com/user-attachments/assets/8edae957-85e6-4f7e-8bc6-78375b03a90b" />

### 制作试卷

1. 打开『聪耳慧听』试卷制作工具。

2. 点击`选择音频文件`按钮选取音频。
<img width="676" height="474" alt="TestPaperEditorMain" src="https://github.com/user-attachments/assets/40a30d6b-ed8a-440f-8fa6-c6a3def3f5b1" />

3. 输入试卷名称。

4. 输入试题。
    * 每个词语间必须有`<空格>`或`<换行符>`或`.（英文句点）`隔开；
    * 每道题开头必须有题号阿拉伯数字（如：`10`）作为独立的词语；
    * 每个选项开头必须有选项大写字母（如： `A`）作为独立的词语；
    * 所有选项内部均不得出现`1`-`20`的数字和大写字母`B` `C` `D`作为独立的词语；
    * 不得将分隔符`<空格>`或`<换行符>`或`.（英文句点）`作为选项中的重要信息。

    正确示例：✅
    > 1.A. Use the heater.<br>
    > B. Turn off the heater.<br>
    > C. Help her light a fire.<br>
    > D. Move to another room<br>
    > 2 A. A musician.
    > B. $1500.
    > C. A guitar
    > D.A popular play.

    错误示例：❌
    > __~~1A~~__. Use the heater.<br>
    > __~~b~~__. Turn off the heater.<br>
    > __~~CHelp~~__ her light a fire.<br>
    > D. Move to room __~~B~~__<br>
    > 2.A. __~~9~~__ pounds and 15pence.<br>
    > B. __~~1.55~~__ dollars.<br>
    > __~~CA~~__ guitar<br>
    > D.__~~Apopularplay~~__.<br>

5. 输入答案（可以空白表示无预设答案）。

6. 点击`预览试题`按钮查看试题预览。<br>
如输入内容有错误会弹窗报错。

7. 点击`导出试卷文件夹`按钮导出。


## 更新日志

### 试卷制作工具 v1.0
发布日期：2025年8月3日

『聪耳慧听』第一个试卷制作工具正式发布！
不用手敲JSON试题文件惹~
* 加入了音频选取
* 加入了试卷名称输入（支持utf-8）
* 加入了试题内容输入
* 加入了答案输入（可选项）
* 加入了试题内容智能分析 v1.0
* 加入了试题预览
* 加入了试卷文件夹导出

### v1.0.0
发布日期：2025年8月3日

『聪耳慧听』第一个版本正式发布！
欢迎使用！
* 加入了启动器
* 加入了试音界面
* 加入了测试界面<br>（含单页可上下翻页的试题区和问题标记区）
* 加入了结算器


## 开发环境

### 当前版本

#### Python 3.9.10

|依赖库|版本|
|---|---|
|altgraph                  |0.17.4|
|importlib_metadata        |8.7.0|
|packaging                 |25.0|
|pefile                    |2023.2.7|
|pip                       |21.2.4|
|pygame                    |2.6.1|
|pyinstaller               |6.14.2|
|pyinstaller-hooks-contrib |2025.8|
|pywin32-ctypes            |0.2.3|
|setuptools                |58.1.0|
|zipp                      |3.23.0|

### 过去的版本使用过的开发环境


~~想啥呢，没有过去的版本。~~
