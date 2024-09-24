# Clipboard-Monitor
这是一个使用Python开发的带有用户界面（UI）的剪切板记录的程序，运行时可以记录用户剪切板输入的内容并显示出来，方便在用户多轮次复制粘贴时找到之前的内容。

## 项目简介

该项目的主要功能是记录用户剪切板输入的内容及复制时间并支持导出。项目已经打包成`main.exe`文件，用户只需下载安装并运行该文件即可体验。


## 如何编译生成

1. 要在 Windows 上使用 PyCharm 将 Python 项目打包成可执行的 .exe 文件，可以使用 PyInstaller 工具。
2. 下载仓库中的py文件。
3. 在 PyCharm 的终端或者命令提示符中运行命令：pip install pyinstaller
4. 在项目目录中，使用 PyInstaller 将 Python 脚本打包成 .exe 文件，命令为：pyinstaller --onefile main.py
5. 打包成功后，PyInstaller 会在项目目录下生成一个 dist 文件夹，里面包含生成的 .exe 文件。你可以在 dist/ 文件夹中找到你的可执行文件，双击即可运行。


## 程序截图图片

![示例图片](./Clipboard.jpg)

## 依赖项

- Python 3.x
- Tkinter (用于构建UI)


## 联系我们

如果您有任何问题或建议，欢迎通过邮件联系我hhy@hhyblog.top。

