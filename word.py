import tkinter as tk
from tkinter import messagebox

def generate_text():
    # 获取输入框内容
    title = entry_title.get()
    name = entry_name.get()
    student_id = entry_id.get()
    college = entry_college.get()
    major = entry_major.get()
    teacher = entry_teacher.get()
    prof_title = entry_prof_title.get()
    date = entry_date.get()
    
    # 动态计算下划线长度，保持整体美观
    # 使用全角空格（　）来保证中文字符的绝对对齐
    template = f"""
题　　目： {title}
姓　　名： {name}
学　　号： {student_id.ljust(15, ' ')}
所在学院： {college}
年级专业： {major}
指导教师： {teacher.ljust(8, '　')} 职　称： {prof_title}
完成时间： {date}
"""
    
    # 清空并插入预览框
    text_preview.delete("1.0", tk.END)
    text_preview.insert(tk.END, template.strip())

def copy_to_clipboard():
    content = text_preview.get("1.0", tk.END).strip()
    if content:
        root.clipboard_clear()
        root.clipboard_append(content)
        messagebox.showinfo("复制成功", "内容已复制！\n\n请粘贴到 Word 中，全选文本，然后将字体设置为【黑体】，字号设置为【三号】。")
    else:
        messagebox.showwarning("警告", "请先点击生成模板！")

# 创建主窗口
root = tk.Tk()
root.title("论文封面排版生成器")
root.geometry("600x650")

# 设置全局字体（模拟三号黑体，三号约为16磅）
default_font = ("SimHei", 16)

# 输入表单区域
frame_inputs = tk.Frame(root, pady=10)
frame_inputs.pack(fill=tk.X, padx=20)

labels_texts = ["题　　目:", "姓　　名:", "学　　号:", "所在学院:", "年级专业:", "指导教师:", "职　　称:", "完成时间:"]
default_values = [
    "目的论视角下社科类文本的翻译策略——以《内容混淆》为例",
    "陈冠臻",
    "________________",  # 留白给学号
    "高级翻译学院",
    "翻译专业",
    "任亚峰",
    "教授",
    "2026年2月25日"
]

entries = []
for i, (label_text, default_val) in enumerate(zip(labels_texts, default_values)):
    tk.Label(frame_inputs, text=label_text, font=default_font).grid(row=i, column=0, pady=5, sticky="e")
    entry = tk.Entry(frame_inputs, font=default_font, width=35)
    entry.insert(0, default_val)
    entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")
    entries.append(entry)

# 解包对应的输入框变量
entry_title, entry_name, entry_id, entry_college, entry_major, entry_teacher, entry_prof_title, entry_date = entries

# 按钮区域
frame_buttons = tk.Frame(root, pady=10)
frame_buttons.pack()

btn_generate = tk.Button(frame_buttons, text="生成对齐模板", font=("SimHei", 14), command=generate_text, bg="#e0e0e0")
btn_generate.grid(row=0, column=0, padx=10)

btn_copy = tk.Button(frame_buttons, text="一键复制", font=("SimHei", 14), command=copy_to_clipboard, bg="#4CAF50", fg="white")
btn_copy.grid(row=0, column=1, padx=10)

# 预览区域
tk.Label(root, text="效果预览 (全角空格对齐):", font=("SimHei", 12)).pack(anchor="w", padx=20)
text_preview = tk.Text(root, font=("SimHei", 16), height=9, width=50, bg="#f5f5f5")
text_preview.pack(padx=20, pady=5)

# 初始化生成一次
generate_text()

root.mainloop()