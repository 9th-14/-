import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox


def get_folder_comment(folder_path):
    """
    从 desktop.ini 读取 InfoTip 注释
    """
    ini_path = os.path.join(folder_path, "desktop.ini")
    if not os.path.exists(ini_path):
        return ""

    try:
        with open(ini_path, "r", encoding="gbk", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line.lower().startswith("infotip="):
                    return line.split("=", 1)[1]
    except:
        return ""

    return ""


def set_folder_comment(folder_path, comment):
    """
    写入 InfoTip 注释并确保 Explorer 能识别
    """
    if not os.path.isdir(folder_path):
        raise ValueError("文件夹不存在")

    ini_path = os.path.join(folder_path, "desktop.ini")

    content = (
        "[.ShellClassInfo]\n"
        f"InfoTip={comment}\n"
    )

    # 必须用 GBK，否则中文会乱码
    with open(ini_path, "w", encoding="gbk", errors="ignore") as f:
        f.write(content)

    # desktop.ini 设为系统+隐藏
    subprocess.run(f'attrib +s +h "{ini_path}"', shell=True)
    # 文件夹设为系统，否则 desktop.ini 不生效
    subprocess.run(f'attrib +s "{folder_path}"', shell=True)


def choose_folder():
    path = filedialog.askdirectory()
    if path:
        folder_var.set(path)
        comment_var.set(get_folder_comment(path))


def apply_comment():
    folder = folder_var.get().strip()
    comment = comment_var.get().strip()

    if not folder:
        messagebox.showwarning("提示", "请先选择文件夹")
        return

    try:
        set_folder_comment(folder, comment)
        messagebox.showinfo("成功", "注释已更新，请刷新资源管理器查看")
    except Exception as e:
        messagebox.showerror("错误", str(e))


# ---------------- GUI 主窗口 ----------------

root = tk.Tk()
root.title("文件夹注释编辑器")
root.geometry("500x200")

folder_var = tk.StringVar()
comment_var = tk.StringVar()

tk.Label(root, text="文件夹路径：").grid(row=0, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=folder_var, width=40).grid(row=0, column=1)
tk.Button(root, text="选择...", command=choose_folder).grid(row=0, column=2, padx=5)

tk.Label(root, text="注释内容：").grid(row=1, column=0, padx=10, sticky="w")
tk.Entry(root, textvariable=comment_var, width=40).grid(row=1, column=1)

tk.Button(root, text="保存注释", command=apply_comment, width=20).grid(row=2, column=1, pady=20)

# 如果是从右键菜单传入路径，则自动加载该文件夹和注释
if len(sys.argv) > 1:
    folder = sys.argv[1]
    folder_var.set(folder)
    comment_var.set(get_folder_comment(folder))

root.mainloop()
