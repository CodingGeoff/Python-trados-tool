# import tkinter as tk
# from tkinter import filedialog, messagebox
# from tkinter import ttk
# import xml.etree.ElementTree as ET
# import random
# from datetime import datetime, timedelta
# import os

# class XMLConverterApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("XML 术语转换器 (Simple to MTF)")
#         self.root.geometry("600x450")
#         self.root.resizable(False, False)

#         # 界面变量
#         self.input_file_path = tk.StringVar()
#         self.output_file_path = tk.StringVar()
#         self.author_id = tk.StringVar(value="msm16") # 默认作者 ID

#         self.setup_ui()

#     def setup_ui(self):
#         # --- 文件选择区域 ---
#         frame_file = tk.LabelFrame(self.root, text="文件配置", padx=10, pady=10)
#         frame_file.pack(padx=10, pady=10, fill="x")

#         # 输入文件
#         tk.Label(frame_file, text="输入文件 (XML):").grid(row=0, column=0, sticky="w", pady=5)
#         tk.Entry(frame_file, textvariable=self.input_file_path, width=45).grid(row=0, column=1, padx=5)
#         tk.Button(frame_file, text="浏览...", command=self.browse_input).grid(row=0, column=2)

#         # 输出文件
#         tk.Label(frame_file, text="输出文件 (XML):").grid(row=1, column=0, sticky="w", pady=5)
#         tk.Entry(frame_file, textvariable=self.output_file_path, width=45).grid(row=1, column=1, padx=5)
#         tk.Button(frame_file, text="浏览...", command=self.browse_output).grid(row=1, column=2)

#         # 作者 ID (可自定义)
#         tk.Label(frame_file, text="操作人标识 (Transac):").grid(row=2, column=0, sticky="w", pady=5)
#         tk.Entry(frame_file, textvariable=self.author_id, width=15).grid(row=2, column=1, sticky="w", padx=5)

#         # --- 操作按钮 ---
#         frame_action = tk.Frame(self.root)
#         frame_action.pack(pady=5)
#         tk.Button(frame_action, text="⚡ 开始转换", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
#                   width=20, command=self.start_conversion).pack()

#         # --- 日志区域 ---
#         frame_log = tk.LabelFrame(self.root, text="运行日志", padx=10, pady=10)
#         frame_log.pack(padx=10, pady=5, fill="both", expand=True)

#         self.log_text = tk.Text(frame_log, height=10, state="disabled", bg="#f4f4f4")
#         self.log_text.pack(fill="both", expand=True)

#     def log(self, message):
#         """向界面日志窗口输出信息"""
#         self.log_text.config(state="normal")
#         self.log_text.insert(tk.END, message + "\n")
#         self.log_text.see(tk.END)
#         self.log_text.config(state="disabled")
#         self.root.update()

#     def browse_input(self):
#         filepath = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")])
#         if filepath:
#             self.input_file_path.set(filepath)
#             # 自动生成默认输出路径
#             out_path = os.path.splitext(filepath)[0] + "_mtf_converted.xml"
#             self.output_file_path.set(out_path)

#     def browse_output(self):
#         filepath = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML Files", "*.xml")])
#         if filepath:
#             self.output_file_path.set(filepath)

#     def generate_logical_dates(self):
#         """
#         生成一套逻辑合理的随机日期时间：
#         保证 Origination (创建) 早于或等于 Modification (修改)
#         时间范围随机落在近 1-2 年内。
#         """
#         # 随机设定一个基准日期 (2024年初 ~ 2026年初)
#         base_start = datetime(2024, 1, 1)
#         base_end = datetime(2026, 2, 27)
#         delta_seconds = int((base_end - base_start).total_seconds())
        
#         # Concept 的创建时间
#         concept_orig_time = base_start + timedelta(seconds=random.randint(0, delta_seconds))
#         # Concept 的修改时间 (创建之后的 10秒 到 30天 不等)
#         concept_mod_time = concept_orig_time + timedelta(seconds=random.randint(10, 2592000))

#         # 中文术语时间和英文术语时间 (紧贴 Concept 的时间)
#         # 模拟操作：先建中文，后建英文，或者同时
#         zh_orig_time = concept_orig_time - timedelta(seconds=random.randint(1, 5))
#         zh_mod_time = zh_orig_time # 假设没改过
        
#         en_orig_time = concept_mod_time
#         en_mod_time = concept_mod_time

#         def fmt(dt): return dt.strftime("%Y-%m-%dT%H:%M:%S")

#         return {
#             "c_orig": fmt(concept_orig_time),
#             "c_mod": fmt(concept_mod_time),
#             "zh_orig": fmt(zh_orig_time),
#             "zh_mod": fmt(zh_mod_time),
#             "en_orig": fmt(en_orig_time),
#             "en_mod": fmt(en_mod_time)
#         }

#     def build_transac_grp(self, parent, t_type, author, date_str):
#         """辅助方法：构建 <transacGrp> 节点"""
#         grp = ET.SubElement(parent, "transacGrp")
#         transac = ET.SubElement(grp, "transac", type=t_type)
#         transac.text = author
#         date_node = ET.SubElement(grp, "date")
#         date_node.text = date_str
#         return grp

#     def start_conversion(self):
#         in_file = self.input_file_path.get()
#         out_file = self.output_file_path.get()
#         author = self.author_id.get().strip() or "msm16"

#         if not in_file or not out_file:
#             messagebox.showwarning("提示", "请先选择输入和输出文件路径！")
#             return

#         self.log("="*40)
#         self.log(f"开始读取文件: {in_file}")

#         try:
#             # 1. 解析原始 XML
#             tree = ET.parse(in_file)
#             root_in = tree.getroot()
#             rows = root_in.findall("row")
#             self.log(f"成功解析源文件，共找到 {len(rows)} 条 <row> 记录。")

#             # 2. 构建目标 XML (MTF 结构)
#             root_out = ET.Element("mtf")

#             for index, row in enumerate(rows, start=1):
#                 chinese_node = row.find("Chinese")
#                 english_node = row.find("English")

#                 zh_text = chinese_node.text.strip() if chinese_node is not None and chinese_node.text else ""
#                 en_text = english_node.text.strip() if english_node is not None and english_node.text else ""

#                 if not zh_text and not en_text:
#                     self.log(f"警告：跳过第 {index} 行，中英文均为空。")
#                     continue

#                 # 生成随机时间
#                 dates = self.generate_logical_dates()

#                 # --- 组装 <conceptGrp> ---
#                 concept_grp = ET.SubElement(root_out, "conceptGrp")
                
#                 concept = ET.SubElement(concept_grp, "concept")
#                 concept.text = str(index)

#                 # Concept 级别的 transacGrp
#                 self.build_transac_grp(concept_grp, "origination", author, dates["c_orig"])
#                 self.build_transac_grp(concept_grp, "modification", author, dates["c_mod"])

#                 # --- 组装 中文 <languageGrp> ---
#                 if zh_text:
#                     lang_grp_zh = ET.SubElement(concept_grp, "languageGrp")
#                     ET.SubElement(lang_grp_zh, "language", lang="ZH", type="Chinese")
#                     term_grp_zh = ET.SubElement(lang_grp_zh, "termGrp")
                    
#                     term_zh = ET.SubElement(term_grp_zh, "term")
#                     term_zh.text = zh_text
                    
#                     self.build_transac_grp(term_grp_zh, "origination", author, dates["zh_orig"])
#                     self.build_transac_grp(term_grp_zh, "modification", author, dates["zh_mod"])

#                 # --- 组装 英文 <languageGrp> ---
#                 if en_text:
#                     lang_grp_en = ET.SubElement(concept_grp, "languageGrp")
#                     ET.SubElement(lang_grp_en, "language", lang="EN", type="English")
#                     term_grp_en = ET.SubElement(lang_grp_en, "termGrp")
                    
#                     term_en = ET.SubElement(term_grp_en, "term")
#                     term_en.text = en_text
                    
#                     self.build_transac_grp(term_grp_en, "origination", author, dates["en_orig"])
#                     self.build_transac_grp(term_grp_en, "modification", author, dates["en_mod"])

#             self.log("正在生成目标 XML 结构并格式化...")

#             # 3. 缩进格式化 (仅适用于 Python 3.9+，如果是旧版本会跳过自动缩进)
#             if hasattr(ET, 'indent'):
#                 ET.indent(root_out, space="  ", level=0)

#             # 4. 写入文件 (强制指定 UTF-16)
#             out_tree = ET.ElementTree(root_out)
            
#             # 手动添加特殊的 XML 声明
#             xml_declaration = "<?xml version='1.0' encoding='UTF-16' ?>\n"
            
#             # ElementTree 写出时直接获取 byte string 再转码写入，确保声明头绝对正确
#             xml_bytes = ET.tostring(root_out, encoding="utf-16", xml_declaration=False)
            
#             with open(out_file, "wb") as f:
#                 # 写入 UTF-16 的 BOM 和我们自定义的 Declaration 头
#                 # 在 utf-16 编码下，我们要先把字符串转成 byte 写入
#                 f.write(xml_declaration.encode('utf-16')) 
#                 f.write(xml_bytes)

#             self.log(f"✅ 转换完成！成功输出 {len(rows)} 条概念记录。")
#             self.log(f"💾 输出文件保存至：{out_file}")
#             messagebox.showinfo("成功", f"XML 转换完毕！\n共转换 {len(rows)} 条记录。")

#         except Exception as e:
#             self.log(f"❌ 发生错误：{str(e)}")
#             messagebox.showerror("错误", f"转换过程中发生错误：\n{str(e)}")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = XMLConverterApp(root)
#     root.mainloop()


import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
import random
import csv
import os
from datetime import datetime, timedelta

class CSVtoXMLConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("全能术语转换器 (CSV ➜ Simple XML & MultiTerm XML)")
        self.root.geometry("650x500")
        self.root.resizable(False, False)

        # 界面变量
        self.input_csv_path = tk.StringVar()
        self.output_dir_path = tk.StringVar()
        self.author_id = tk.StringVar(value="msm16")

        self.setup_ui()

    def setup_ui(self):
        # --- 文件配置区域 ---
        frame_file = tk.LabelFrame(self.root, text="文件与路径配置", padx=10, pady=10)
        frame_file.pack(padx=10, pady=10, fill="x")

        # 输入 CSV
        tk.Label(frame_file, text="输入文件 (CSV):").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(frame_file, textvariable=self.input_csv_path, width=45).grid(row=0, column=1, padx=5)
        tk.Button(frame_file, text="浏览...", command=self.browse_input).grid(row=0, column=2)

        # 输出目录
        tk.Label(frame_file, text="输出文件夹:").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(frame_file, textvariable=self.output_dir_path, width=45).grid(row=1, column=1, padx=5)
        tk.Button(frame_file, text="浏览...", command=self.browse_output_dir).grid(row=1, column=2)

        # 作者 ID
        tk.Label(frame_file, text="操作人标识 (Transac):").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(frame_file, textvariable=self.author_id, width=15).grid(row=2, column=1, sticky="w", padx=5)

        # --- 操作按钮 ---
        frame_action = tk.Frame(self.root)
        frame_action.pack(pady=5)
        tk.Button(frame_action, text="⚡ 一键生成两种 XML", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
                  width=25, command=self.start_conversion).pack()

        # --- 日志区域 ---
        frame_log = tk.LabelFrame(self.root, text="运行日志", padx=10, pady=10)
        frame_log.pack(padx=10, pady=5, fill="both", expand=True)

        self.log_text = tk.Text(frame_log, height=12, state="disabled", bg="#f4f4f4")
        self.log_text.pack(fill="both", expand=True)

    def log(self, message):
        """输出日志到界面"""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        self.root.update()

    def browse_input(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if filepath:
            self.input_csv_path.set(filepath)
            # 自动设置输出目录为 CSV 所在目录
            self.output_dir_path.set(os.path.dirname(filepath))

    def browse_output_dir(self):
        dirpath = filedialog.askdirectory()
        if dirpath:
            self.output_dir_path.set(dirpath)

    def generate_logical_dates(self):
        """生成合理的随机日期时间"""
        base_start = datetime(2024, 1, 1)
        base_end = datetime(2026, 2, 27)
        delta_seconds = int((base_end - base_start).total_seconds())
        
        c_orig = base_start + timedelta(seconds=random.randint(0, delta_seconds))
        c_mod = c_orig + timedelta(seconds=random.randint(10, 2592000))

        zh_orig = c_orig - timedelta(seconds=random.randint(1, 5))
        en_orig = c_mod

        def fmt(dt): return dt.strftime("%Y-%m-%dT%H:%M:%S")

        return {
            "c_orig": fmt(c_orig), "c_mod": fmt(c_mod),
            "zh_orig": fmt(zh_orig), "zh_mod": fmt(zh_orig),
            "en_orig": fmt(en_orig), "en_mod": fmt(en_orig)
        }

    def build_transac_grp(self, parent, t_type, author, date_str):
        """辅助方法：构建 transacGrp 节点"""
        grp = ET.SubElement(parent, "transacGrp")
        ET.SubElement(grp, "transac", type=t_type).text = author
        ET.SubElement(grp, "date").text = date_str
        return grp

    def read_csv_data(self, filepath):
        """稳健读取 CSV 数据，处理可能的 BOM 和编码问题"""
        data = []
        # 尝试 utf-8-sig 以自动去除 CSV 文件可能带有的 UTF-8 BOM
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                for row in reader:
                    # 过滤空行，并确保至少有两列
                    if row and len(row) >= 2:
                        zh_text = row[0].strip()
                        en_text = row[1].strip()
                        # 跳过可能的表头 (如果第一行刚好写着 Chinese 和 English)
                        if zh_text.lower() == "chinese" and "english" in en_text.lower():
                            continue
                        if zh_text or en_text:
                            data.append((zh_text, en_text))
            return data
        except Exception as e:
            raise Exception(f"读取 CSV 失败，请检查是否为逗号分隔的格式。错误: {str(e)}")

    def start_conversion(self):
        csv_file = self.input_csv_path.get()
        out_dir = self.output_dir_path.get()
        author = self.author_id.get().strip() or "msm16"

        if not csv_file or not out_dir:
            messagebox.showwarning("提示", "请完整选择输入文件和输出文件夹！")
            return

        self.log("="*40)
        self.log(f"📥 开始读取 CSV: {csv_file}")

        try:
            # 1. 读取 CSV
            terms_data = self.read_csv_data(csv_file)
            if not terms_data:
                self.log("❌ 错误：CSV 文件中没有读取到有效数据。")
                return
            self.log(f"✅ 成功读取 {len(terms_data)} 条术语数据。")

            # 2. 准备输出文件名
            base_name = os.path.splitext(os.path.basename(csv_file))[0]
            out_simple = os.path.join(out_dir, f"{base_name}_simple.xml")
            out_mtf = os.path.join(out_dir, f"{base_name}_multiterm.xml")

            # ---------------------------------------------------------
            # 3. 构建 Simple XML (<root><row>...)
            # ---------------------------------------------------------
            self.log("正在生成基础版 XML (Simple Format)...")
            root_simple = ET.Element("root")
            for zh, en in terms_data:
                row_node = ET.SubElement(root_simple, "row")
                ET.SubElement(row_node, "Chinese").text = zh
                ET.SubElement(row_node, "English").text = en
            
            if hasattr(ET, 'indent'): ET.indent(root_simple, space="  ", level=0)
            
            # Simple XML 通常用 UTF-8 保存即可
            tree_simple = ET.ElementTree(root_simple)
            tree_simple.write(out_simple, encoding="utf-8", xml_declaration=True)
            self.log(f"💾 基础版 XML 已保存: {out_simple}")

            # ---------------------------------------------------------
            # 4. 构建 MultiTerm MTF XML (<mtf><conceptGrp>...)
            # ---------------------------------------------------------
            self.log("正在生成 MultiTerm 专属 XML (MTF Format)...")
            root_mtf = ET.Element("mtf")
            
            for index, (zh, en) in enumerate(terms_data, start=1):
                dates = self.generate_logical_dates()
                concept_grp = ET.SubElement(root_mtf, "conceptGrp")
                ET.SubElement(concept_grp, "concept").text = str(index)

                self.build_transac_grp(concept_grp, "origination", author, dates["c_orig"])
                self.build_transac_grp(concept_grp, "modification", author, dates["c_mod"])

                if zh:
                    lgrp_zh = ET.SubElement(concept_grp, "languageGrp")
                    ET.SubElement(lgrp_zh, "language", lang="ZH", type="Chinese")
                    tgrp_zh = ET.SubElement(lgrp_zh, "termGrp")
                    ET.SubElement(tgrp_zh, "term").text = zh
                    self.build_transac_grp(tgrp_zh, "origination", author, dates["zh_orig"])
                    self.build_transac_grp(tgrp_zh, "modification", author, dates["zh_mod"])

                if en:
                    lgrp_en = ET.SubElement(concept_grp, "languageGrp")
                    ET.SubElement(lgrp_en, "language", lang="EN", type="English")
                    tgrp_en = ET.SubElement(lgrp_en, "termGrp")
                    ET.SubElement(tgrp_en, "term").text = en
                    self.build_transac_grp(tgrp_en, "origination", author, dates["en_orig"])
                    self.build_transac_grp(tgrp_en, "modification", author, dates["en_mod"])

            if hasattr(ET, 'indent'): ET.indent(root_mtf, space="  ", level=0)

            # 解决 BOM 问题的核心：直接获取 Unicode 字符串，手动拼接头部
            mtf_content_str = ET.tostring(root_mtf, encoding="unicode")
            final_mtf_xml_str = f"<?xml version='1.0' encoding='UTF-16' ?>\n{mtf_content_str}"

            # 使用 python 的 open 函数指定 utf-16 编码，它会自动在文件最开头放一个合法的 BOM
            # 而不会在 <mtf> 前面产生多余的不可见字符
            with open(out_mtf, "w", encoding="utf-16") as f:
                f.write(final_mtf_xml_str)
                
            self.log(f"💾 MultiTerm XML 已保存: {out_mtf}")
            self.log("🎉 转换圆满完成！")
            
            messagebox.showinfo("成功", f"转换完成！\n成功处理 {len(terms_data)} 条术语。\n文件已存放在:\n{out_dir}")

        except Exception as e:
            self.log(f"❌ 运行中断：{str(e)}")
            messagebox.showerror("错误", f"发生错误：\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVtoXMLConverterApp(root)
    root.mainloop()