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
    messagebox.showerror("缺少依赖环境", "系统缺少处理 Excel 的组件。\n\n请在命令行运行：pip install pandas openpyxl")
    exit()

class UltimateTermConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("🌈 全能术语转换中心 Ultra (防弹最终版)")
        self.root.geometry("780x680")
        self.root.resizable(False, False)
        
        # UI 配色
        self.colors = {
            "bg": "#F0F4F8", "panel": "#FFFFFF", "text": "#334155", 
            "primary": "#3B82F6", "success": "#10B981", "warning": "#F59E0B", "border": "#E2E8F0"
        }
        self.root.configure(bg=self.colors["bg"])

        # 界面输入变量
        self.input_file_path = tk.StringVar()
        self.output_dir_path = tk.StringVar()
        self.author_id = tk.StringVar(value="msm16")
        
        # 【核心修复】：复选框变量名增加 var_ 前缀，严格与函数名区分
        self.var_export_simple = tk.BooleanVar(value=True)
        self.var_export_mtf = tk.BooleanVar(value=True)
        self.var_export_tmx = tk.BooleanVar(value=False)
        self.var_export_md = tk.BooleanVar(value=False)

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

        ttk.Label(main_container, text="智能术语转换工作台", style="Header.TLabel").pack(anchor="w", pady=(0, 15))

        # 文件配置面板
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

        # 格式选项面板
        panel_format = tk.Frame(main_container, bg=self.colors["panel"], highlightbackground=self.colors["border"], highlightthickness=1, padx=15, pady=15)
        panel_format.pack(fill="x", pady=(0, 15))
        
        ttk.Label(panel_format, text="✨ 勾选导出格式 (支持破损文件自动修复提取):", font=("Microsoft YaHei", 10, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))
        ttk.Checkbutton(panel_format, text="标准 XML", variable=self.var_export_simple).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(panel_format, text="MultiTerm MTF", variable=self.var_export_mtf).grid(row=1, column=1, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(panel_format, text="TMX 记忆库", variable=self.var_export_tmx).grid(row=1, column=2, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(panel_format, text="Markdown", variable=self.var_export_md).grid(row=1, column=3, sticky="w", padx=10, pady=5)

        # 按钮区
        btn_frame = tk.Frame(main_container, bg=self.colors["bg"])
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="🚀 一 键 执 行 转 换", style="Primary.TButton", command=self.start_conversion).pack(ipady=8, fill="x", padx=120)

        # 日志区
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
        """控制台日志打印"""
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

    # ==========================
    # 数据解析引擎 (Pandas & XML)
    # ==========================
    def load_data_smart(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        if ext in ['.csv', '.xls', '.xlsx']:
            self.log("➡️ 检测到表格文件，启用 Pandas 解析引擎...")
            return self.load_data_via_pandas(filepath)
        elif ext in ['.tbx', '.xml']:
            self.log("➡️ 检测到 XML/TBX 文件，启用 XML DOM 解析引擎...")
            return self.parse_tbx_xml(filepath)
        else:
            raise ValueError(f"系统不认识这种文件格式: {ext}，请重新选择。")

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

    def parse_tbx_xml(self, filepath):
        try:
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
            
            for row in list(root.iter('row')):
                zh, en = row.find('Chinese'), row.find('English')
                z_txt = zh.text.strip() if zh is not None and zh.text else ""
                e_txt = en.text.strip() if en is not None and en.text else ""
                if z_txt or e_txt: data_list.append((z_txt, e_txt))
            return data_list

        except ET.ParseError as e:
            self.log(f"⚠️ 源文件结构损坏 ({str(e).split(':')[0]})")
            self.log("🛡️ 自动切换至【强力正则容错提取引擎】...")
            return self.parse_xml_fallback(filepath)

    def parse_xml_fallback(self, filepath):
        """正则容错引擎，无视标签错误"""
        with open(filepath, 'r', encoding='utf-8-sig', errors='ignore') as f:
            content = f.read()

        data_list = []
        entries = re.findall(r'<termEntry[^>]*>(.*?)</termEntry>', content, flags=re.DOTALL)
        if entries:
            for entry in entries:
                zh_term, en_term = "", ""
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

        rows = re.findall(r'<row[^>]*>(.*?)</row>', content, flags=re.DOTALL)
        if rows:
            for row in rows:
                zh_m = re.search(r'<Chinese[^>]*>(.*?)</Chinese>', row, flags=re.DOTALL)
                en_m = re.search(r'<English[^>]*>(.*?)</English>', row, flags=re.DOTALL)
                zh = zh_m.group(1).strip() if zh_m else ""
                en = en_m.group(1).strip() if en_m else ""
                if zh or en: data_list.append((zh, en))
            return data_list

        raise ValueError("容错提取失败：在文件中未能找到有效的术语对照内容。")

    # ==========================
    # 格式生成引擎 (名称全部重构)
    # ==========================
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

    def generate_simple_xml(self, data, out_path):
        root = ET.Element("root")
        for zh, en in data:
            row = ET.SubElement(root, "row")
            ET.SubElement(row, "Chinese").text, ET.SubElement(row, "English").text = zh, en
        if hasattr(ET, 'indent'): ET.indent(root, space="  ", level=0)
        ET.ElementTree(root).write(out_path, encoding="utf-8", xml_declaration=True)

    def generate_mtf_xml(self, data, author, out_path):
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

    def generate_tmx_memory(self, data, author, out_path):
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

    def generate_md_table(self, data, out_path):
        lines = ["# 术语对照表\n", "| 序号 | 中文 (ZH-CN) | 英文 (EN-US) |", "|:---:|:---|:---|"]
        for i, (zh, en) in enumerate(data, 1): lines.append(f"| {i} | {zh.replace('|', '&#124;')} | {en.replace('|', '&#124;')} |")
        with open(out_path, "w", encoding="utf-8") as f: f.write("\n".join(lines))

    # ==========================
    # 主控制流程
    # ==========================
    def start_conversion(self):
        file_path, out_dir, author = self.input_file_path.get(), self.output_dir_path.get(), self.author_id.get() or "System"
        
        # 拦截：用户没选文件
        if not file_path or not out_dir: 
            return messagebox.showwarning("操作提示", "请先点击右上角的【浏览...】选择要处理的文件和导出位置。")
            
        # 拦截：用户一个格式都没勾选
        if not any([self.var_export_simple.get(), self.var_export_mtf.get(), self.var_export_tmx.get(), self.var_export_md.get()]): 
            return messagebox.showwarning("操作提示", "请至少勾选一种中间面板的【导出格式】。")

        self.log("--- 转换任务开始 ---")
        try:
            # 1. 提取数据
            data = self.load_data_smart(file_path)
            self.log(f"✅ 成功从损坏文件中抢救/提取出 {len(data)} 条数据！")
            
            bn = os.path.splitext(os.path.basename(file_path))[0]
            cnt = 0
            
            # 2. 生成文件（调用已重命名的函数，杜绝冲突）
            if self.var_export_simple.get(): 
                self.generate_simple_xml(data, os.path.join(out_dir, f"{bn}_Simple.xml"))
                cnt += 1; self.log("💾 已导出: 基础 XML")
                
            if self.var_export_mtf.get(): 
                self.generate_mtf_xml(data, author, os.path.join(out_dir, f"{bn}_MTF.xml"))
                cnt += 1; self.log("💾 已导出: MultiTerm MTF")
                
            if self.var_export_tmx.get(): 
                self.generate_tmx_memory(data, author, os.path.join(out_dir, f"{bn}_Memory.tmx"))
                cnt += 1; self.log("💾 已导出: TMX 记忆库")
                
            if self.var_export_md.get(): 
                self.generate_md_table(data, os.path.join(out_dir, f"{bn}_Table.md"))
                cnt += 1; self.log("💾 已导出: Markdown")
            
            self.log("🎉 全部导出完成！")
            
            # 成功的“人话”弹窗
            messagebox.showinfo("转换成功", f"太棒了！数据抢救与转换已完成。\n\n• 成功提取：{len(data)} 条数据\n• 导出文件：{cnt} 种格式\n\n文件已存放在您指定的文件夹中。")
            
        except Exception as e:
            # 失败的“人话”弹窗，避免代码暴雷给小白
            self.log(f"❌ 任务中断: {str(e)}")
            messagebox.showerror("遇到了一点小麻烦", f"转换过程中出现了问题，可能是由于文件内容过于特殊。\n\n具体原因：\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    UltimateTermConverter(root)
    root.mainloop()