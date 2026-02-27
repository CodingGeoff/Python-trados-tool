# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# import xml.etree.ElementTree as ET
# import os
# import random
# from datetime import datetime, timedelta

# # 尝试导入 pandas 库，用于处理表格格式
# try:
#     import pandas as pd
# except ImportError:
#     messagebox.showerror("缺少依赖", "请先在命令行运行: pip install pandas openpyxl")
#     exit()

# class UltimateTermConverter:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("🌈 全能本地化术语转换中心 Pro Max (支持 Excel/TBX)")
#         self.root.geometry("780x680")
#         self.root.resizable(False, False)
        
#         # 护眼配色方案 (现代扁平化柔和色调)
#         self.colors = {
#             "bg": "#F0F4F8",          # 整体柔和浅灰蓝背景
#             "panel": "#FFFFFF",       # 面板纯白
#             "text": "#334155",        # 护眼深灰文字
#             "primary": "#3B82F6",     # 柔和主色蓝
#             "success": "#10B981",     # 柔和成功绿
#             "warning": "#F59E0B",     # 柔和警告黄
#             "border": "#E2E8F0"       # 边框浅灰
#         }
#         self.root.configure(bg=self.colors["bg"])

#         # 界面变量
#         self.input_file_path = tk.StringVar()
#         self.output_dir_path = tk.StringVar()
#         self.author_id = tk.StringVar(value="msm16")
        
#         # 导出格式勾选变量
#         self.export_simple_xml = tk.BooleanVar(value=True)
#         self.export_multiterm = tk.BooleanVar(value=True)
#         self.export_tmx = tk.BooleanVar(value=False)
#         self.export_md = tk.BooleanVar(value=False)

#         self.setup_styles()
#         self.setup_ui()

#     def setup_styles(self):
#         """配置 TTK 现代样式"""
#         style = ttk.Style()
#         style.theme_use('clam')
        
#         style.configure("TFrame", background=self.colors["bg"])
#         style.configure("Panel.TFrame", background=self.colors["panel"])
        
#         style.configure("TLabel", background=self.colors["panel"], foreground=self.colors["text"], font=("Microsoft YaHei", 10))
#         style.configure("Header.TLabel", background=self.colors["bg"], foreground=self.colors["primary"], font=("Microsoft YaHei", 14, "bold"))
#         style.configure("TCheckbutton", background=self.colors["panel"], foreground=self.colors["text"], font=("Microsoft YaHei", 10))
        
#         style.configure("TButton", font=("Microsoft YaHei", 10), padding=5)
#         style.configure("Primary.TButton", background=self.colors["primary"], foreground="white", font=("Microsoft YaHei", 12, "bold"))
#         style.map("Primary.TButton", background=[('active', '#2563EB')])

#     def setup_ui(self):
#         main_container = tk.Frame(self.root, bg=self.colors["bg"], padx=20, pady=15)
#         main_container.pack(fill="both", expand=True)

#         ttk.Label(main_container, text="智能术语转换工作台", style="Header.TLabel").pack(anchor="w", pady=(0, 15))

#         # --- 第一部分：文件与路径配置 ---
#         panel_file = tk.Frame(main_container, bg=self.colors["panel"], highlightbackground=self.colors["border"], highlightthickness=1, padx=15, pady=15)
#         panel_file.pack(fill="x", pady=(0, 15))

#         ttk.Label(panel_file, text="📁 数据源 (CSV/Excel/TBX/XML):").grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))
#         tk.Entry(panel_file, textvariable=self.input_file_path, width=42, font=("Consolas", 10), bg="#F8FAFC", fg=self.colors["text"], relief="solid", bd=1).grid(row=0, column=1, padx=5, ipady=4)
#         ttk.Button(panel_file, text="浏览...", command=self.browse_input).grid(row=0, column=2, padx=5)

#         ttk.Label(panel_file, text="📂 导出目标文件夹:").grid(row=1, column=0, sticky="w", pady=8, padx=(0, 10))
#         tk.Entry(panel_file, textvariable=self.output_dir_path, width=42, font=("Consolas", 10), bg="#F8FAFC", fg=self.colors["text"], relief="solid", bd=1).grid(row=1, column=1, padx=5, ipady=4)
#         ttk.Button(panel_file, text="浏览...", command=self.browse_output_dir).grid(row=1, column=2, padx=5)

#         ttk.Label(panel_file, text="👤 修改人标识 (ID):").grid(row=2, column=0, sticky="w", pady=8, padx=(0, 10))
#         tk.Entry(panel_file, textvariable=self.author_id, width=15, font=("Consolas", 10), bg="#F8FAFC", fg=self.colors["text"], relief="solid", bd=1).grid(row=2, column=1, sticky="w", padx=5, ipady=4)

#         # --- 第二部分：导出格式勾选 ---
#         panel_format = tk.Frame(main_container, bg=self.colors["panel"], highlightbackground=self.colors["border"], highlightthickness=1, padx=15, pady=15)
#         panel_format.pack(fill="x", pady=(0, 15))
        
#         ttk.Label(panel_format, text="✨ 请选择需要生成的格式 (支持多选):", font=("Microsoft YaHei", 10, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

#         ttk.Checkbutton(panel_format, text="标准 XML (Simple)", variable=self.export_simple_xml).grid(row=1, column=0, sticky="w", padx=10, pady=5)
#         ttk.Checkbutton(panel_format, text="MultiTerm MTF (Trados)", variable=self.export_multiterm).grid(row=1, column=1, sticky="w", padx=10, pady=5)
#         ttk.Checkbutton(panel_format, text="TMX 翻译记忆库", variable=self.export_tmx).grid(row=1, column=2, sticky="w", padx=10, pady=5)
#         ttk.Checkbutton(panel_format, text="Markdown 表格", variable=self.export_md).grid(row=1, column=3, sticky="w", padx=10, pady=5)

#         # --- 第三部分：执行按钮 ---
#         btn_frame = tk.Frame(main_container, bg=self.colors["bg"])
#         btn_frame.pack(fill="x", pady=10)
        
#         start_btn = ttk.Button(btn_frame, text="🚀 一 键 执 行 转 换", style="Primary.TButton", command=self.start_conversion)
#         start_btn.pack(ipady=8, fill="x", padx=120)

#         # --- 第四部分：运行日志 ---
#         ttk.Label(main_container, text="📋 运行日志", style="Header.TLabel", font=("Microsoft YaHei", 11, "bold")).pack(anchor="w", pady=(5, 5))
        
#         log_frame = tk.Frame(main_container, bg=self.colors["panel"], highlightbackground=self.colors["border"], highlightthickness=1)
#         log_frame.pack(fill="both", expand=True)
        
#         scrollbar = tk.Scrollbar(log_frame)
#         scrollbar.pack(side="right", fill="y")
#         self.log_text = tk.Text(log_frame, height=9, bg="#F8FAFC", fg="#475569", font=("Consolas", 9), relief="flat", yscrollcommand=scrollbar.set, padx=10, pady=10)
#         self.log_text.pack(side="left", fill="both", expand=True)
#         scrollbar.config(command=self.log_text.yview)
#         self.log_text.config(state="disabled")

#     # --- 基础交互 ---
#     def log(self, message):
#         time_str = datetime.now().strftime("[%H:%M:%S]")
#         self.log_text.config(state="normal")
#         self.log_text.insert(tk.END, f"{time_str} {message}\n")
#         self.log_text.see(tk.END)
#         self.log_text.config(state="disabled")
#         self.root.update()

#     def browse_input(self):
#         filepath = filedialog.askopenfilename(filetypes=[
#             ("所有支持的文件", "*.csv *.xls *.xlsx *.tbx *.xml"),
#             ("TBX/XML 术语库", "*.tbx *.xml"),
#             ("表格文件", "*.csv *.xlsx *.xls"),
#             ("All Files", "*.*")
#         ])
#         if filepath:
#             self.input_file_path.set(filepath)
#             self.output_dir_path.set(os.path.dirname(filepath))

#     def browse_output_dir(self):
#         dirpath = filedialog.askdirectory()
#         if dirpath:
#             self.output_dir_path.set(dirpath)

#     # --- 核心引擎：智能数据提取 ---
#     def load_data_smart(self, filepath):
#         """智能分发解析器：根据文件后缀和内容决定使用哪种解析引擎"""
#         ext = os.path.splitext(filepath)[1].lower()
        
#         if ext in ['.csv', '.xls', '.xlsx']:
#             self.log("➡️ 检测到表格文件，启用 Pandas 解析引擎...")
#             return self.load_data_via_pandas(filepath)
#         elif ext in ['.tbx', '.xml']:
#             self.log("➡️ 检测到 XML/TBX 文件，启用 XML DOM 解析引擎...")
#             return self.parse_tbx_xml(filepath)
#         else:
#             raise ValueError(f"不支持的文件格式: {ext}")

#     def parse_tbx_xml(self, filepath):
#         """深度解析 TBX (Martif) 和常规 XML 文件"""
#         data_list = []
#         try:
#             tree = ET.parse(filepath)
#             root = tree.getroot()

#             # 兼容处理：寻找所有的 termEntry (TBX 标准)
#             term_entries = list(root.iter('termEntry'))
            
#             if not term_entries:
#                 # 兼容处理：如果你传入的是之前导出的 <root><row> Simple XML
#                 rows = list(root.iter('row'))
#                 if rows:
#                     self.log("检测到 Simple XML 格式，正在提取...")
#                     for row in rows:
#                         zh_node = row.find('Chinese')
#                         en_node = row.find('English')
#                         zh = zh_node.text.strip() if zh_node is not None and zh_node.text else ""
#                         en = en_node.text.strip() if en_node is not None and en_node.text else ""
#                         if zh or en: data_list.append((zh, en))
#                     return data_list
#                 raise ValueError("未在文件中找到 <termEntry> 或 <row> 节点，可能不是有效的术语库文件。")

#             # 遍历解析 TBX 的 termEntry
#             for entry in term_entries:
#                 zh_term = ""
#                 en_term = ""
                
#                 # 遍历条目下的语言集
#                 for lang_set in entry.findall('.//langSet'):
#                     # XML 命名空间处理 (xml:lang)
#                     lang = lang_set.get('{http://www.w3.org/XML/1998/namespace}lang')
#                     if not lang:
#                         lang = lang_set.attrib.get('xml:lang', '')

#                     # 找到该语言下的 term
#                     term_node = lang_set.find('.//term')
#                     if term_node is not None and term_node.text:
#                         text = term_node.text.strip()
#                         lang_lower = lang.lower()
#                         # 模糊匹配中英文标识
#                         if 'zh' in lang_lower or 'chinese' in lang_lower:
#                             zh_term = text
#                         elif 'en' in lang_lower or 'english' in lang_lower:
#                             en_term = text

#                 if zh_term or en_term:
#                     data_list.append((zh_term, en_term))

#             return data_list
#         except ET.ParseError as e:
#             raise Exception(f"XML 结构损坏或解析失败: {str(e)}")
#         except Exception as e:
#             raise Exception(f"TBX 读取错误: {str(e)}")

#     def load_data_via_pandas(self, filepath):
#         """Pandas 读取表格逻辑"""
#         try:
#             ext = os.path.splitext(filepath)[1].lower()
#             if ext == '.csv': df = pd.read_csv(filepath, header=None)
#             else: df = pd.read_excel(filepath, header=None)

#             df.dropna(how='all', inplace=True)
#             if len(df.columns) < 2: raise ValueError("表格数据不足两列，无法提取中英对照。")

#             data_list = []
#             for _, row in df.iterrows():
#                 zh = str(row.iloc[0]).strip()
#                 en = str(row.iloc[1]).strip()
#                 if zh.lower() in ['chinese', '中文', 'zh', 'nan'] and en.lower() in ['english', '英文', 'en', 'nan']: continue
#                 if zh.lower() == 'nan' or en.lower() == 'nan': continue
#                 if zh or en: data_list.append((zh, en))
                    
#             return data_list
#         except Exception as e:
#             raise Exception(f"表格读取失败: {str(e)}")

#     # --- 辅助生成工具 ---
#     def generate_logical_dates(self):
#         base_start = datetime(2024, 1, 1)
#         base_end = datetime(2026, 2, 27)
#         delta_seconds = int((base_end - base_start).total_seconds())
#         c_orig = base_start + timedelta(seconds=random.randint(0, delta_seconds))
#         c_mod = c_orig + timedelta(seconds=random.randint(10, 2592000))
#         def fmt(dt): return dt.strftime("%Y-%m-%dT%H:%M:%S")
#         return {"c_orig": fmt(c_orig), "c_mod": fmt(c_mod), "zh_orig": fmt(c_orig - timedelta(seconds=random.randint(1,5))), "en_mod": fmt(c_mod)}

#     def build_transac_grp(self, parent, t_type, author, date_str):
#         grp = ET.SubElement(parent, "transacGrp")
#         ET.SubElement(grp, "transac", type=t_type).text = author
#         ET.SubElement(grp, "date").text = date_str
#         return grp

#     # --- 四大导出引擎 ---
#     def export_to_simple_xml(self, data, out_path):
#         root = ET.Element("root")
#         for zh, en in data:
#             row_node = ET.SubElement(root, "row")
#             ET.SubElement(row_node, "Chinese").text = zh
#             ET.SubElement(row_node, "English").text = en
#         if hasattr(ET, 'indent'): ET.indent(root, space="  ", level=0)
#         ET.ElementTree(root).write(out_path, encoding="utf-8", xml_declaration=True)

#     def export_to_multiterm_mtf(self, data, author, out_path):
#         root_mtf = ET.Element("mtf")
#         for index, (zh, en) in enumerate(data, start=1):
#             dates = self.generate_logical_dates()
#             concept_grp = ET.SubElement(root_mtf, "conceptGrp")
#             ET.SubElement(concept_grp, "concept").text = str(index)
#             self.build_transac_grp(concept_grp, "origination", author, dates["c_orig"])
#             self.build_transac_grp(concept_grp, "modification", author, dates["c_mod"])

#             for lang_code, lang_type, term_text, d_orig in [("ZH", "Chinese", zh, dates["zh_orig"]), ("EN", "English", en, dates["en_mod"])]:
#                 if term_text:
#                     lgrp = ET.SubElement(concept_grp, "languageGrp")
#                     ET.SubElement(lgrp, "language", lang=lang_code, type=lang_type)
#                     tgrp = ET.SubElement(lgrp, "termGrp")
#                     ET.SubElement(tgrp, "term").text = term_text
#                     self.build_transac_grp(tgrp, "origination", author, d_orig)
#                     self.build_transac_grp(tgrp, "modification", author, dates["c_mod"])

#         if hasattr(ET, 'indent'): ET.indent(root_mtf, space="  ", level=0)
#         mtf_content_str = ET.tostring(root_mtf, encoding="unicode")
#         final_mtf_xml_str = f"<?xml version='1.0' encoding='UTF-16' ?>\n{mtf_content_str}"
#         with open(out_path, "w", encoding="utf-16") as f: f.write(final_mtf_xml_str)

#     def export_to_tmx(self, data, author, out_path):
#         root_tmx = ET.Element("tmx", version="1.4")
#         now_str = datetime.now().strftime("%Y%m%dT%H%M%SZ")
#         ET.SubElement(root_tmx, "header", creationtool="UltimateTermConverter", creationtoolversion="3.0", datatype="PlainText", segtype="sentence", adminlang="en-US", srclang="ZH-CN", creationdate=now_str, creationid=author)
#         body = ET.SubElement(root_tmx, "body")
#         for zh, en in data:
#             if not zh or not en: continue
#             tu = ET.SubElement(body, "tu", creationdate=now_str, creationid=author)
#             tuv_zh = ET.SubElement(tu, "tuv"); tuv_zh.set("xml:lang", "ZH-CN"); ET.SubElement(tuv_zh, "seg").text = zh
#             tuv_en = ET.SubElement(tu, "tuv"); tuv_en.set("xml:lang", "EN-US"); ET.SubElement(tuv_en, "seg").text = en
#         if hasattr(ET, 'indent'): ET.indent(root_tmx, space="  ", level=0)
#         ET.ElementTree(root_tmx).write(out_path, encoding="utf-8", xml_declaration=True)

#     def export_to_markdown(self, data, out_path):
#         md_lines = ["# 本地化术语对照表\n", "| 序号 | 中文 (ZH-CN) | 英文 (EN-US) |", "|:---:|:---|:---|"]
#         for index, (zh, en) in enumerate(data, start=1):
#             md_lines.append(f"| {index} | {zh.replace('|', '&#124;')} | {en.replace('|', '&#124;')} |")
#         with open(out_path, "w", encoding="utf-8") as f: f.write("\n".join(md_lines))

#     # --- 主控制流 ---
#     def start_conversion(self):
#         file_path = self.input_file_path.get()
#         out_dir = self.output_dir_path.get()
#         author = self.author_id.get().strip() or "System"

#         if not file_path or not out_dir:
#             messagebox.showwarning("提示", "请选择完整的输入数据源和导出文件夹。")
#             return

#         if not any([self.export_simple_xml.get(), self.export_multiterm.get(), self.export_tmx.get(), self.export_md.get()]):
#             messagebox.showwarning("提示", "请至少勾选一种【导出格式】！")
#             return

#         self.log(f"--- 转换任务开始 ---")
#         self.log(f"载入文件: {os.path.basename(file_path)}")

#         try:
#             # 1. 智能加载与解析
#             terms_data = self.load_data_smart(file_path)
#             self.log(f"✅ 解析成功！共提取出 {len(terms_data)} 条双语术语对。")

#             base_name = os.path.splitext(os.path.basename(file_path))[0]
#             success_count = 0

#             # 2. 分发导出
#             if self.export_simple_xml.get():
#                 self.export_to_simple_xml(terms_data, os.path.join(out_dir, f"{base_name}_Simple.xml"))
#                 self.log("💾 已导出: 标准 XML")
#                 success_count += 1

#             if self.export_multiterm.get():
#                 self.export_to_multiterm_mtf(terms_data, author, os.path.join(out_dir, f"{base_name}_MultiTerm.xml"))
#                 self.log("💾 已导出: MultiTerm MTF")
#                 success_count += 1
                
#             if self.export_tmx.get():
#                 self.export_to_tmx(terms_data, author, os.path.join(out_dir, f"{base_name}_Memory.tmx"))
#                 self.log("💾 已导出: TMX 翻译记忆")
#                 success_count += 1

#             if self.export_md.get():
#                 self.export_to_markdown(terms_data, os.path.join(out_dir, f"{base_name}_Table.md"))
#                 self.log("💾 已导出: Markdown 表格")
#                 success_count += 1

#             self.log(f"🎉 全部处理完毕！完美导出 {success_count} 种格式。")
#             messagebox.showinfo("转换成功", f"恭喜，转换成功！\n\n数据源：{os.path.basename(file_path)}\n提取条数：{len(terms_data)}\n成功导出文件数：{success_count}\n\n文件已存放在导出文件夹中。")

#         except Exception as e:
#             self.log(f"❌ 运行报错: {str(e)}")
#             messagebox.showerror("数据解析错误", f"发生异常：\n{str(e)}\n\n请检查文件是否损坏或格式是否正确。")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = UltimateTermConverter(root)
#     root.mainloop()


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import xml.etree.ElementTree as ET
import os
import random
import re
from datetime import datetime, timedelta

try:
    import pandas as pd
except ImportError:
    messagebox.showerror("缺少依赖", "请先在命令行运行: pip install pandas openpyxl")
    exit()

class UltimateTermConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("🌈 全能术语转换中心 Ultra (带智能容错引擎)")
        self.root.geometry("780x680")
        self.root.resizable(False, False)
        
        self.colors = {
            "bg": "#F0F4F8", "panel": "#FFFFFF", "text": "#334155", 
            "primary": "#3B82F6", "success": "#10B981", "warning": "#F59E0B", "border": "#E2E8F0"
        }
        self.root.configure(bg=self.colors["bg"])

        self.input_file_path = tk.StringVar()
        self.output_dir_path = tk.StringVar()
        self.author_id = tk.StringVar(value="msm16")
        
        self.export_simple_xml = tk.BooleanVar(value=True)
        self.export_multiterm = tk.BooleanVar(value=True)
        self.export_tmx = tk.BooleanVar(value=False)
        self.export_md = tk.BooleanVar(value=False)

        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Panel.TFrame", background=self.colors["panel"])
        style.configure("TLabel", background=self.colors["panel"], foreground=self.colors["text"], font=("Microsoft YaHei", 10))
        style.configure("Header.TLabel", background=self.colors["bg"], foreground=self.colors["primary"], font=("Microsoft YaHei", 14, "bold"))
        style.configure("TCheckbutton", background=self.colors["panel"], foreground=self.colors["text"], font=("Microsoft YaHei", 10))
        style.configure("Primary.TButton", background=self.colors["primary"], foreground="white", font=("Microsoft YaHei", 12, "bold"))
        style.map("Primary.TButton", background=[('active', '#2563EB')])

    def setup_ui(self):
        main_container = tk.Frame(self.root, bg=self.colors["bg"], padx=20, pady=15)
        main_container.pack(fill="both", expand=True)

        ttk.Label(main_container, text="智能术语转换工作台 (防弹版)", style="Header.TLabel").pack(anchor="w", pady=(0, 15))

        panel_file = tk.Frame(main_container, bg=self.colors["panel"], highlightbackground=self.colors["border"], highlightthickness=1, padx=15, pady=15)
        panel_file.pack(fill="x", pady=(0, 15))

        ttk.Label(panel_file, text="📁 数据源 (CSV/XLS/TBX/XML):").grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))
        tk.Entry(panel_file, textvariable=self.input_file_path, width=42, font=("Consolas", 10), bg="#F8FAFC").grid(row=0, column=1, padx=5, ipady=4)
        ttk.Button(panel_file, text="浏览...", command=self.browse_input).grid(row=0, column=2, padx=5)

        ttk.Label(panel_file, text="📂 导出目标文件夹:").grid(row=1, column=0, sticky="w", pady=8, padx=(0, 10))
        tk.Entry(panel_file, textvariable=self.output_dir_path, width=42, font=("Consolas", 10), bg="#F8FAFC").grid(row=1, column=1, padx=5, ipady=4)
        ttk.Button(panel_file, text="浏览...", command=self.browse_output_dir).grid(row=1, column=2, padx=5)

        ttk.Label(panel_file, text="👤 修改人标识 (ID):").grid(row=2, column=0, sticky="w", pady=8, padx=(0, 10))
        tk.Entry(panel_file, textvariable=self.author_id, width=15, font=("Consolas", 10), bg="#F8FAFC").grid(row=2, column=1, sticky="w", padx=5, ipady=4)

        panel_format = tk.Frame(main_container, bg=self.colors["panel"], highlightbackground=self.colors["border"], highlightthickness=1, padx=15, pady=15)
        panel_format.pack(fill="x", pady=(0, 15))
        
        ttk.Label(panel_format, text="✨ 勾选导出格式 (无惧源文件损坏):", font=("Microsoft YaHei", 10, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))
        ttk.Checkbutton(panel_format, text="标准 XML", variable=self.export_simple_xml).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(panel_format, text="MultiTerm MTF", variable=self.export_multiterm).grid(row=1, column=1, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(panel_format, text="TMX 记忆库", variable=self.export_tmx).grid(row=1, column=2, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(panel_format, text="Markdown", variable=self.export_md).grid(row=1, column=3, sticky="w", padx=10, pady=5)

        btn_frame = tk.Frame(main_container, bg=self.colors["bg"])
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="🚀 一 键 执 行 转 换", style="Primary.TButton", command=self.start_conversion).pack(ipady=8, fill="x", padx=120)

        ttk.Label(main_container, text="📋 运行日志", style="Header.TLabel", font=("Microsoft YaHei", 11, "bold")).pack(anchor="w", pady=(5, 5))
        log_frame = tk.Frame(main_container, bg=self.colors["panel"], highlightbackground=self.colors["border"], highlightthickness=1)
        log_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")
        self.log_text = tk.Text(log_frame, height=9, bg="#F8FAFC", fg="#475569", font=("Consolas", 9), relief="flat", yscrollcommand=scrollbar.set, padx=10, pady=10)
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.log_text.yview)
        self.log_text.config(state="disabled")

    def log(self, message):
        time_str = datetime.now().strftime("[%H:%M:%S]")
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"{time_str} {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        self.root.update()

    def browse_input(self):
        filepath = filedialog.askopenfilename(filetypes=[("所有支持文件", "*.csv *.xls *.xlsx *.tbx *.xml"), ("All Files", "*.*")])
        if filepath:
            self.input_file_path.set(filepath)
            self.output_dir_path.set(os.path.dirname(filepath))

    def browse_output_dir(self):
        dirpath = filedialog.askdirectory()
        if dirpath: self.output_dir_path.set(dirpath)

    # --- 核心引擎分发 ---
    def load_data_smart(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        if ext in ['.csv', '.xls', '.xlsx']:
            self.log("➡️ 检测到表格文件，启用 Pandas 解析引擎...")
            return self.load_data_via_pandas(filepath)
        elif ext in ['.tbx', '.xml']:
            self.log("➡️ 检测到 XML/TBX 文件，启用 XML DOM 解析引擎...")
            return self.parse_tbx_xml(filepath)
        else:
            raise ValueError(f"不支持的文件格式: {ext}")

    def load_data_via_pandas(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.csv': df = pd.read_csv(filepath, header=None)
        else: df = pd.read_excel(filepath, header=None)
        df.dropna(how='all', inplace=True)
        data_list = []
        for _, row in df.iterrows():
            zh, en = str(row.iloc[0]).strip(), str(row.iloc[1]).strip()
            if zh.lower() in ['chinese', '中文', 'zh', 'nan'] and en.lower() in ['english', '英文', 'en', 'nan']: continue
            if zh or en: data_list.append((zh, en))
        return data_list

    # --- 双核 XML 解析 ---
    def parse_tbx_xml(self, filepath):
        try:
            # 尝试标准 DOM 解析
            tree = ET.parse(filepath)
            root = tree.getroot()
            data_list = []
            
            term_entries = list(root.iter('termEntry'))
            if term_entries:
                for entry in term_entries:
                    zh_term, en_term = "", ""
                    for lang_set in entry.findall('.//langSet'):
                        lang = lang_set.get('{http://www.w3.org/XML/1998/namespace}lang') or lang_set.attrib.get('xml:lang', '')
                        term_node = lang_set.find('.//term')
                        if term_node is not None and term_node.text:
                            if 'zh' in lang.lower() or 'chinese' in lang.lower(): zh_term = term_node.text.strip()
                            elif 'en' in lang.lower() or 'english' in lang.lower(): en_term = term_node.text.strip()
                    if zh_term or en_term: data_list.append((zh_term, en_term))
                return data_list
            
            # Simple XML 格式
            for row in list(root.iter('row')):
                zh, en = row.find('Chinese'), row.find('English')
                z_txt = zh.text.strip() if zh is not None and zh.text else ""
                e_txt = en.text.strip() if en is not None and en.text else ""
                if z_txt or e_txt: data_list.append((z_txt, e_txt))
            return data_list

        except ET.ParseError as e:
            # 捕获异常，立刻启用容错引擎
            self.log(f"⚠️ 捕获到源文件损坏 ({str(e)})")
            self.log("🛡️ 已自动切换至【强力正则容错提取引擎】...")
            return self.parse_xml_fallback(filepath)

    def parse_xml_fallback(self, filepath):
        """【强力容错引擎】：完全无视损坏的根节点和错误标签，强制提取有效数据"""
        with open(filepath, 'r', encoding='utf-8-sig', errors='ignore') as f:
            content = f.read()

        data_list = []
        
        # 匹配 TBX 的 <termEntry> 块
        entries = re.findall(r'<termEntry[^>]*>(.*?)</termEntry>', content, flags=re.DOTALL)
        if entries:
            for entry in entries:
                zh_term, en_term = "", ""
                # 匹配 langSet
                lang_sets = re.findall(r'<langSet[^>]*xml:lang="([^"]+)"[^>]*>(.*?)</langSet>', entry, flags=re.DOTALL)
                for lang_code, lang_content in lang_sets:
                    term_match = re.search(r'<term[^>]*>(.*?)</term>', lang_content, flags=re.DOTALL)
                    if term_match:
                        text = term_match.group(1).strip()
                        lang_lower = lang_code.lower()
                        if 'zh' in lang_lower or 'chinese' in lang_lower: zh_term = text
                        elif 'en' in lang_lower or 'english' in lang_lower: en_term = text
                if zh_term or en_term: data_list.append((zh_term, en_term))
            return data_list

        # 如果匹配不到 TBX，尝试匹配 Simple XML 的 <row> 块
        rows = re.findall(r'<row[^>]*>(.*?)</row>', content, flags=re.DOTALL)
        if rows:
            for row in rows:
                zh_m = re.search(r'<Chinese[^>]*>(.*?)</Chinese>', row, flags=re.DOTALL)
                en_m = re.search(r'<English[^>]*>(.*?)</English>', row, flags=re.DOTALL)
                zh = zh_m.group(1).strip() if zh_m else ""
                en = en_m.group(1).strip() if en_m else ""
                if zh or en: data_list.append((zh, en))
            return data_list

        raise ValueError("容错引擎未能找到有效术语块，文件内容可能并非有效术语库。")

    # --- 辅助生成工具 ---
    def generate_logical_dates(self):
        base = datetime(2024, 1, 1)
        c_orig = base + timedelta(seconds=random.randint(0, 31536000))
        c_mod = c_orig + timedelta(seconds=random.randint(10, 2592000))
        fmt = lambda dt: dt.strftime("%Y-%m-%dT%H:%M:%S")
        return {"c_orig": fmt(c_orig), "c_mod": fmt(c_mod), "zh_orig": fmt(c_orig - timedelta(seconds=3)), "en_mod": fmt(c_mod)}

    def build_tgrp(self, parent, t_type, author, date_str):
        grp = ET.SubElement(parent, "transacGrp")
        ET.SubElement(grp, "transac", type=t_type).text = author
        ET.SubElement(grp, "date").text = date_str

    # --- 导出引擎 ---
    def export_simple(self, data, out_path):
        root = ET.Element("root")
        for zh, en in data:
            row = ET.SubElement(root, "row")
            ET.SubElement(row, "Chinese").text, ET.SubElement(row, "English").text = zh, en
        if hasattr(ET, 'indent'): ET.indent(root, space="  ", level=0)
        ET.ElementTree(root).write(out_path, encoding="utf-8", xml_declaration=True)

    def export_mtf(self, data, author, out_path):
        root = ET.Element("mtf")
        for idx, (zh, en) in enumerate(data, 1):
            dates = self.generate_logical_dates()
            cgrp = ET.SubElement(root, "conceptGrp")
            ET.SubElement(cgrp, "concept").text = str(idx)
            self.build_tgrp(cgrp, "origination", author, dates["c_orig"])
            self.build_tgrp(cgrp, "modification", author, dates["c_mod"])

            for code, typ, txt, d_o in [("ZH", "Chinese", zh, dates["zh_orig"]), ("EN", "English", en, dates["en_mod"])]:
                if txt:
                    lgrp = ET.SubElement(cgrp, "languageGrp")
                    ET.SubElement(lgrp, "language", lang=code, type=typ)
                    tgrp = ET.SubElement(lgrp, "termGrp")
                    ET.SubElement(tgrp, "term").text = txt
                    self.build_tgrp(tgrp, "origination", author, d_o)
                    self.build_tgrp(tgrp, "modification", author, dates["c_mod"])
        if hasattr(ET, 'indent'): ET.indent(root, space="  ", level=0)
        with open(out_path, "w", encoding="utf-16") as f:
            f.write(f"<?xml version='1.0' encoding='UTF-16' ?>\n{ET.tostring(root, encoding='unicode')}")

    def export_tmx(self, data, author, out_path):
        root = ET.Element("tmx", version="1.4")
        now = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        ET.SubElement(root, "header", creationtool="UltraConverter", creationtoolversion="4.0", datatype="PlainText", segtype="sentence", adminlang="en-US", srclang="ZH-CN", creationdate=now, creationid=author)
        body = ET.SubElement(root, "body")
        for zh, en in data:
            if not zh or not en: continue
            tu = ET.SubElement(body, "tu", creationdate=now, creationid=author)
            ET.SubElement(ET.SubElement(tu, "tuv", {"xml:lang": "ZH-CN"}), "seg").text = zh
            ET.SubElement(ET.SubElement(tu, "tuv", {"xml:lang": "EN-US"}), "seg").text = en
        if hasattr(ET, 'indent'): ET.indent(root, space="  ", level=0)
        ET.ElementTree(root).write(out_path, encoding="utf-8", xml_declaration=True)

    def export_md(self, data, out_path):
        lines = ["# 术语对照表\n", "| 序号 | 中文 (ZH-CN) | 英文 (EN-US) |", "|:---:|:---|:---|"]
        for i, (zh, en) in enumerate(data, 1): lines.append(f"| {i} | {zh.replace('|', '&#124;')} | {en.replace('|', '&#124;')} |")
        with open(out_path, "w", encoding="utf-8") as f: f.write("\n".join(lines))

    def start_conversion(self):
        file_path, out_dir, author = self.input_file_path.get(), self.output_dir_path.get(), self.author_id.get() or "Sys"
        if not file_path or not out_dir: return messagebox.showwarning("提示", "请选择输入源和输出目录。")
        if not any([self.export_simple_xml.get(), self.export_multiterm.get(), self.export_tmx.get(), self.export_md.get()]): return messagebox.showwarning("提示", "请勾选导出格式。")

        self.log("--- 转换开始 ---")
        try:
            data = self.load_data_smart(file_path)
            self.log(f"✅ 成功提取 {len(data)} 条数据！")
            
            bn = os.path.splitext(os.path.basename(file_path))[0]
            cnt = 0
            if self.export_simple_xml.get(): self.export_simple(data, os.path.join(out_dir, f"{bn}_Simple.xml")); cnt+=1; self.log("💾 已导出: 基础 XML")
            if self.export_multiterm.get(): self.export_mtf(data, author, os.path.join(out_dir, f"{bn}_MTF.xml")); cnt+=1; self.log("💾 已导出: MultiTerm MTF")
            if self.export_tmx.get(): self.export_tmx(data, author, os.path.join(out_dir, f"{bn}_Memory.tmx")); cnt+=1; self.log("💾 已导出: TMX 记忆库")
            if self.export_md.get(): self.export_md(data, os.path.join(out_dir, f"{bn}_Table.md")); cnt+=1; self.log("💾 已导出: Markdown")
            
            self.log("🎉 全部完成！")
            messagebox.showinfo("成功", f"恭喜！成功越过损坏限制，提取了 {len(data)} 条数据并生成 {cnt} 种格式。")
        except Exception as e:
            self.log(f"❌ 失败: {str(e)}")
            messagebox.showerror("错误", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    UltimateTermConverter(root)
    root.mainloop()