# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# import pandas as pd
# import xml.etree.ElementTree as ET
# import os
# import json
# from xml.dom import minidom

# CONFIG_FILE = "converter_config.json"

# class UniversalConverterApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("全能数据与本地化格式转换器 (CSV/XLSX/TMX/XML/JSON/TSV)")
#         self.root.geometry("600x420")
#         self.root.resizable(False, False)

#         # 加载历史配置（路径记忆）
#         self.config = self.load_config()

#         # 变量声明
#         self.input_file = tk.StringVar()
#         self.output_file = tk.StringVar()
#         self.src_lang = tk.StringVar(value="en-US")
#         self.tgt_lang = tk.StringVar(value="zh-CN")

#         self._build_gui()

#     def load_config(self):
#         """加载历史配置，如果没有则返回默认字典"""
#         if os.path.exists(CONFIG_FILE):
#             try:
#                 with open(CONFIG_FILE, "r", encoding="utf-8") as f:
#                     return json.load(f)
#             except Exception:
#                 pass
#         return {"last_input_dir": "/", "last_output_dir": "/"}

#     def save_config(self):
#         """保存历史配置到本地"""
#         try:
#             with open(CONFIG_FILE, "w", encoding="utf-8") as f:
#                 json.dump(self.config, f, indent=4)
#         except Exception as e:
#             print(f"无法保存配置: {e}")

#     def _build_gui(self):
#         main_frame = ttk.Frame(self.root, padding="20")
#         main_frame.pack(fill=tk.BOTH, expand=True)

#         # --- 输入文件区域 ---
#         ttk.Label(main_frame, text="1. 选择输入文件 (支持 CSV, XLSX, TMX, XML, JSON, TSV/TXT)", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5), columnspan=3)
#         ttk.Entry(main_frame, textvariable=self.input_file, width=50, state="readonly").grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
#         ttk.Button(main_frame, text="浏览...", command=self.browse_input).grid(row=1, column=2, padx=10, pady=(0, 15))

#         # --- TMX 语言代码设置 ---
#         ttk.Label(main_frame, text="2. 语言代码设置 (仅当涉及 TMX 格式转换时生效):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5), columnspan=3)
        
#         lang_frame = ttk.Frame(main_frame)
#         lang_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))
        
#         ttk.Label(lang_frame, text="源语言 (Source):").pack(side=tk.LEFT)
#         ttk.Entry(lang_frame, textvariable=self.src_lang, width=10).pack(side=tk.LEFT, padx=(5, 15))
        
#         ttk.Label(lang_frame, text="目标语言 (Target):").pack(side=tk.LEFT)
#         ttk.Entry(lang_frame, textvariable=self.tgt_lang, width=10).pack(side=tk.LEFT, padx=(5, 0))

#         # --- 输出文件区域 ---
#         ttk.Label(main_frame, text="3. 选择保存位置和目标格式", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=(0, 5), columnspan=3)
#         ttk.Entry(main_frame, textvariable=self.output_file, width=50, state="readonly").grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
#         ttk.Button(main_frame, text="另存为...", command=self.browse_output).grid(row=5, column=2, padx=10, pady=(0, 20))

#         # --- 转换按钮 ---
#         self.convert_btn = ttk.Button(main_frame, text="开始转换", command=self.process_conversion)
#         self.convert_btn.grid(row=6, column=0, columnspan=3, pady=(10, 0), ipadx=30, ipady=5)

#     def browse_input(self):
#         filetypes = (
#             ("All Supported", "*.csv *.xlsx *.xls *.tmx *.xml *.json *.tsv *.txt"),
#             ("Excel Files", "*.xlsx *.xls"),
#             ("CSV Files", "*.csv"),
#             ("TMX Files", "*.tmx"),
#             ("XML Files", "*.xml"),
#             ("JSON Files", "*.json"),
#             ("Text/TSV Files", "*.tsv *.txt"),
#             ("All Files", "*.*")
#         )
#         filename = filedialog.askopenfilename(
#             title="选择输入文件",
#             initialdir=self.config.get("last_input_dir", "/"),
#             filetypes=filetypes
#         )
#         if filename:
#             self.input_file.set(filename)
#             # 更新历史记录
#             self.config["last_input_dir"] = os.path.dirname(filename)
#             self.save_config()

#     def browse_output(self):
#         if not self.input_file.get():
#             messagebox.showwarning("提示", "请先选择输入文件！")
#             return
            
#         filetypes = (
#             ("Excel XLSX", "*.xlsx"),
#             ("CSV UTF-8", "*.csv"),
#             ("TMX Translation Memory", "*.tmx"),
#             ("Generic XML", "*.xml"),
#             ("JSON Data", "*.json"),
#             ("TSV (Tab Separated)", "*.tsv")
#         )
#         filename = filedialog.asksaveasfilename(
#             title="保存文件",
#             initialdir=self.config.get("last_output_dir", "/"),
#             defaultextension=".xlsx",
#             filetypes=filetypes
#         )
#         if filename:
#             self.output_file.set(filename)
#             # 更新历史记录
#             self.config["last_output_dir"] = os.path.dirname(filename)
#             self.save_config()

#     def process_conversion(self):
#         in_file = self.input_file.get()
#         out_file = self.output_file.get()

#         if not in_file or not out_file:
#             messagebox.showwarning("提示", "请确保已选择输入和输出文件路径！")
#             return

#         in_ext = os.path.splitext(in_file)[1].lower()
#         out_ext = os.path.splitext(out_file)[1].lower()

#         try:
#             self.convert_btn.config(text="正在处理中...", state=tk.DISABLED)
#             self.root.update()

#             # ==========================================
#             # 步骤 1: 将任意输入格式读取为 DataFrame (df)
#             # ==========================================
#             df = None
#             if in_ext == '.csv':
#                 df = pd.read_csv(in_file, encoding='utf-8')
#             elif in_ext in ['.xlsx', '.xls']:
#                 df = pd.read_excel(in_file)
#             elif in_ext == '.tmx':
#                 df = self.tmx_to_dataframe(in_file)
#             elif in_ext == '.xml':
#                 df = pd.read_xml(in_file)
#             elif in_ext == '.json':
#                 df = pd.read_json(in_file)
#             elif in_ext in ['.tsv', '.txt']:
#                 df = pd.read_csv(in_file, sep='\t', encoding='utf-8')
#             else:
#                 raise ValueError(f"不支持的输入文件格式: {in_ext}")

#             if df is None or df.empty:
#                 raise ValueError("读取到的数据为空或文件内容无法解析。")

#             # 清理 DataFrame，将 NaN 替换为空字符串，防止输出出现 'nan' 文本
#             df = df.fillna("")

#             # ==========================================
#             # 步骤 2: 将 DataFrame (df) 导出为任意目标格式
#             # ==========================================
#             if out_ext == '.csv':
#                 df.to_csv(out_file, index=False, encoding='utf-8')
#             elif out_ext == '.xlsx':
#                 df.to_excel(out_file, index=False)
#             elif out_ext == '.tmx':
#                 self.dataframe_to_tmx(df, out_file)
#             elif out_ext == '.xml':
#                 df.to_xml(out_file, index=False, force_ascii=False)
#             elif out_ext == '.json':
#                 df.to_json(out_file, orient='records', force_ascii=False, indent=4)
#             elif out_ext == '.tsv':
#                 df.to_csv(out_file, index=False, sep='\t', encoding='utf-8')
#             else:
#                 raise ValueError(f"不支持的输出文件格式: {out_ext}")

#             messagebox.showinfo("成功", f"文件转换成功！\n已保存至:\n{out_file}")

#         except Exception as e:
#             messagebox.showerror("错误", f"转换失败。\n原因: {str(e)}\n\n(提示: 确保通用XML结构为扁平表格，或TMX文件格式标准)")
#         finally:
#             self.convert_btn.config(text="开始转换", state=tk.NORMAL)

#     # --- 自定义 TMX 处理逻辑（不受 pandas 限制） ---

#     def tmx_to_dataframe(self, filepath):
#         """解析 TMX 返回含 Source 和 Target 的 DataFrame"""
#         tree = ET.parse(filepath)
#         root = tree.getroot()
        
#         ns = ''
#         if '}' in root.tag:
#             ns = root.tag.split('}')[0] + '}'

#         data = []
#         for tu in root.iter(f'{ns}tu'):
#             tuvs = tu.findall(f'.//{ns}tuv')
#             if len(tuvs) >= 2:
#                 src_node = tuvs[0].find(f'.//{ns}seg')
#                 tgt_node = tuvs[1].find(f'.//{ns}seg')
                
#                 src_text = src_node.text if (src_node is not None and src_node.text) else ""
#                 tgt_text = tgt_node.text if (tgt_node is not None and tgt_node.text) else ""
                
#                 data.append({"Source": src_text, "Target": tgt_text})
                
#         return pd.DataFrame(data)

#     def dataframe_to_tmx(self, df, filepath):
#         """DataFrame 转 TMX，自动提取前两列"""
#         if len(df.columns) < 2:
#             raise ValueError("转换为 TMX 格式要求数据源至少包含两列（源语和目标语）。")

#         src_col = df.columns[0]
#         tgt_col = df.columns[1]

#         tmx = ET.Element("tmx", version="1.4")
#         header = ET.SubElement(tmx, "header", 
#                                creationtool="UniversalConverter", 
#                                creationtoolversion="2.0",
#                                datatype="PlainText", 
#                                segtype="sentence",
#                                adminlang="en-US", 
#                                srclang=self.src_lang.get().strip())
#         body = ET.SubElement(tmx, "body")

#         for index, row in df.iterrows():
#             src_text = str(row[src_col]).strip()
#             tgt_text = str(row[tgt_col]).strip()
            
#             if not src_text and not tgt_text:
#                 continue 

#             tu = ET.SubElement(body, "tu")
            
#             tuv_src = ET.SubElement(tu, "tuv", {"xml:lang": self.src_lang.get().strip()})
#             seg_src = ET.SubElement(tuv_src, "seg")
#             seg_src.text = src_text
            
#             tuv_tgt = ET.SubElement(tu, "tuv", {"xml:lang": self.tgt_lang.get().strip()})
#             seg_tgt = ET.SubElement(tuv_tgt, "seg")
#             seg_tgt.text = tgt_text

#         xml_string = ET.tostring(tmx, encoding='utf-8')
#         parsed_xml = minidom.parseString(xml_string)
#         pretty_xml = parsed_xml.toprettyxml(indent="  ")

#         # 移除 minidom 生成的多余空白行
#         pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])

#         with open(filepath, "w", encoding="utf-8") as f:
#             f.write(pretty_xml)

# if __name__ == "__main__":
#     root = tk.Tk()
#     style = ttk.Style(root)
#     # 尝试使用系统中更好看的主题
#     if 'clam' in style.theme_names():
#         style.theme_use('clam')
#     app = UniversalConverterApp(root)
#     root.mainloop()


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import xml.etree.ElementTree as ET
import os
import json
from xml.dom import minidom

CONFIG_FILE = "converter_config_v3.json"

class UltimateConverterApp:
    def __init__(self, root):
        self.root = root
        # 默认语言设置
        self.lang = tk.StringVar(value="zh")
        
        # 国际化语言字典
        self.i18n = {
            "title": {
                "zh": "终极本地化与数据格式转换器 (智能容错版)",
                "en": "Ultimate Localization & Data Converter (Smart Fallback)"
            },
            "btn_lang": {"zh": "English (Switch Language)", "en": "中文 (切换语言)"},
            "step1": {"zh": "第一步：选择输入文件 (支持各类数据和翻译文件)", "en": "Step 1: Select Input File"},
            "browse": {"zh": "浏览文件...", "en": "Browse..."},
            "step2": {"zh": "第二步：TMX 语言代码 (仅针对 TMX 导出)", "en": "Step 2: TMX Lang Codes (For TMX Output Only)"},
            "src_lang": {"zh": "源语言:", "en": "Source Lang:"},
            "tgt_lang": {"zh": "目标语言:", "en": "Target Lang:"},
            "step3": {"zh": "第三步：选择保存位置和目标格式", "en": "Step 3: Select Save Location & Format"},
            "save_as": {"zh": "另存为...", "en": "Save As..."},
            "convert": {"zh": "立即开始转换", "en": "Start Conversion"},
            "converting": {"zh": "正在拼命转换中...", "en": "Converting, please wait..."},
            "msg_empty": {"zh": "请先选择完整的输入和输出路径！", "en": "Please select input and output paths first!"},
            "msg_success": {"zh": "🎉 转换成功！\n文件已保存至:\n", "en": "🎉 Conversion Successful!\nSaved to:\n"},
            "msg_error": {"zh": "转换失败，可能原因：\n", "en": "Conversion Failed, possible reasons:\n"}
        }

        self.root.geometry("640x450")
        self.root.resizable(False, False)

        self.config = self.load_config()

        # UI 绑定变量
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.src_lang_var = tk.StringVar(value="en-US")
        self.tgt_lang_var = tk.StringVar(value="zh-CN")

        self._build_gui()
        self.update_ui_texts() # 初始化语言

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: pass
        return {"last_in": "/", "last_out": "/", "lang": "zh"}

    def save_config(self):
        try:
            self.config["lang"] = self.lang.get()
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except: pass

    def toggle_language(self):
        new_lang = "en" if self.lang.get() == "zh" else "zh"
        self.lang.set(new_lang)
        self.update_ui_texts()
        self.save_config()

    def swap_languages(self):
        """一键互换源语言和目标语言"""
        src = self.src_lang_var.get()
        tgt = self.tgt_lang_var.get()
        self.src_lang_var.set(tgt)
        self.tgt_lang_var.set(src)

    def get_text(self, key):
        return self.i18n.get(key, {}).get(self.lang.get(), key)

    def _build_gui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 语言切换按钮
        self.btn_lang_switch = ttk.Button(main_frame, command=self.toggle_language)
        self.btn_lang_switch.grid(row=0, column=2, sticky=tk.E, pady=(0, 10))

        # --- 第一步 ---
        self.lbl_step1 = ttk.Label(main_frame, font=("Arial", 10, "bold"))
        self.lbl_step1.grid(row=1, column=0, sticky=tk.W, pady=(0, 5), columnspan=3)
        ttk.Entry(main_frame, textvariable=self.input_file, width=54, state="readonly").grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        self.btn_browse = ttk.Button(main_frame, command=self.browse_input)
        self.btn_browse.grid(row=2, column=2, padx=10, pady=(0, 15), sticky=tk.E)

        # --- 第二步 ---
        self.lbl_step2 = ttk.Label(main_frame, font=("Arial", 10, "bold"))
        self.lbl_step2.grid(row=3, column=0, sticky=tk.W, pady=(0, 5), columnspan=3)
        
        lang_frame = ttk.Frame(main_frame)
        lang_frame.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))
        
        # 常用语言代码列表
        self.common_langs = [
            "en-US", "en-GB", "zh-CN", "zh-TW", "zh-HK",
            "ja-JP", "ko-KR", "de-DE", "fr-FR", "es-ES",
            "ru-RU", "it-IT", "pt-BR", "ar-SA", "th-TH",
            "vi-VN", "id-ID", "ms-MY", "tr-TR", "pl-PL"
        ]
        
        self.lbl_src = ttk.Label(lang_frame)
        self.lbl_src.pack(side=tk.LEFT)
        self.src_combo = ttk.Combobox(lang_frame, textvariable=self.src_lang_var, width=12, values=self.common_langs)
        self.src_combo.pack(side=tk.LEFT, padx=(5, 5))
        self.src_combo.set("en-US")
        
        # 互换按钮
        self.btn_swap = ttk.Button(lang_frame, text="⇄", width=3, command=self.swap_languages)
        self.btn_swap.pack(side=tk.LEFT, padx=(0, 5))
        
        self.lbl_tgt = ttk.Label(lang_frame)
        self.lbl_tgt.pack(side=tk.LEFT)
        self.tgt_combo = ttk.Combobox(lang_frame, textvariable=self.tgt_lang_var, width=12, values=self.common_langs)
        self.tgt_combo.pack(side=tk.LEFT, padx=(5, 0))
        self.tgt_combo.set("zh-CN")

        # --- 第三步 ---
        self.lbl_step3 = ttk.Label(main_frame, font=("Arial", 10, "bold"))
        self.lbl_step3.grid(row=5, column=0, sticky=tk.W, pady=(0, 5), columnspan=3)
        ttk.Entry(main_frame, textvariable=self.output_file, width=54, state="readonly").grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        self.btn_save = ttk.Button(main_frame, command=self.browse_output)
        self.btn_save.grid(row=6, column=2, padx=10, pady=(0, 20), sticky=tk.E)

        # --- 转换按钮 ---
        self.btn_convert = ttk.Button(main_frame, command=self.process_conversion)
        self.btn_convert.grid(row=7, column=0, columnspan=3, pady=(10, 0), ipadx=40, ipady=6)

    def update_ui_texts(self):
        """刷新界面语言"""
        self.root.title(self.get_text("title"))
        self.btn_lang_switch.config(text=self.get_text("btn_lang"))
        self.lbl_step1.config(text=self.get_text("step1"))
        self.btn_browse.config(text=self.get_text("browse"))
        self.lbl_step2.config(text=self.get_text("step2"))
        self.lbl_src.config(text=self.get_text("src_lang"))
        self.lbl_tgt.config(text=self.get_text("tgt_lang"))
        self.lbl_step3.config(text=self.get_text("step3"))
        self.btn_save.config(text=self.get_text("save_as"))
        self.btn_convert.config(text=self.get_text("convert"))

    def browse_input(self):
        ft = (("All Supported", "*.csv *.xlsx *.xls *.tmx *.xml *.json *.txt *.tsv"), ("All Files", "*.*"))
        filename = filedialog.askopenfilename(initialdir=self.config.get("last_in", "/"), filetypes=ft)
        if filename:
            self.input_file.set(filename)
            self.config["last_in"] = os.path.dirname(filename)
            self.save_config()

    def browse_output(self):
        if not self.input_file.get():
            messagebox.showwarning("Warning", self.get_text("msg_empty"))
            return
            
        ft = (("Excel XLSX", "*.xlsx"), ("CSV UTF-8", "*.csv"), ("TMX Translation Memory", "*.tmx"), 
              ("JSON Data", "*.json"), ("XML Data", "*.xml"), ("TSV Text", "*.tsv"))
        filename = filedialog.asksaveasfilename(initialdir=self.config.get("last_out", "/"), defaultextension=".xlsx", filetypes=ft)
        if filename:
            self.output_file.set(filename)
            self.config["last_out"] = os.path.dirname(filename)
            self.save_config()

    # ================= 核心：智能容错读取引擎 =================
    def smart_read_csv(self, filepath, is_tsv=False):
        """智能尝试多种编码读取 CSV/TSV，避免因为带中文导致报错"""
        encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb18030', 'latin1']
        separator = '\t' if is_tsv else ','
        
        last_error = None
        for enc in encodings:
            try:
                # 首先尝试自动嗅探分隔符 (engine='python', sep=None)
                if not is_tsv:
                    return pd.read_csv(filepath, encoding=enc, engine='python', sep=None, skipinitialspace=True)
                else:
                    return pd.read_csv(filepath, encoding=enc, sep=separator)
            except Exception as e:
                # 回退：使用强制分隔符尝试
                try:
                    return pd.read_csv(filepath, encoding=enc, sep=separator, skipinitialspace=True)
                except Exception as e2:
                    last_error = e2
                    continue
                    
        raise ValueError(f"无法读取表格。尝试了所有编码均失败。最后的错误: {str(last_error)}")

    def smart_read_json(self, filepath):
        """智能解析 JSON，不管结构多复杂都尝试拍平"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # 如果是列表嵌套字典，直接转 DataFrame
            if isinstance(data, list):
                return pd.json_normalize(data)
            # 如果是单层字典，转置
            elif isinstance(data, dict):
                return pd.DataFrame([data])
            return pd.read_json(filepath)
        except Exception as e:
             raise ValueError(f"JSON 结构异常或不合规: {e}")

    # ================= 业务逻辑：开始转换 =================
    def process_conversion(self):
        in_file = self.input_file.get()
        out_file = self.output_file.get()

        if not in_file or not out_file:
            messagebox.showwarning("Warning", self.get_text("msg_empty"))
            return

        in_ext = os.path.splitext(in_file)[1].lower()
        out_ext = os.path.splitext(out_file)[1].lower()

        try:
            self.btn_convert.config(text=self.get_text("converting"), state=tk.DISABLED)
            self.root.update()

            # ---------------------------
            # 第一阶段：智能解析为 DataFrame
            # ---------------------------
            df = None
            if in_ext == '.csv':
                df = self.smart_read_csv(in_file, is_tsv=False)
            elif in_ext in ['.tsv', '.txt']:
                df = self.smart_read_csv(in_file, is_tsv=True)
            elif in_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(in_file)
            elif in_ext == '.tmx':
                df = self.tmx_to_dataframe(in_file)
            elif in_ext == '.json':
                df = self.smart_read_json(in_file)
            elif in_ext == '.xml':
                try:
                    df = pd.read_xml(in_file)
                except Exception:
                    raise ValueError("此 XML 不是扁平结构 (非二维表)。请转换为标准的数据表格 XML 或 TMX格式。")
            else:
                raise ValueError("不支持的输入格式！")

            if df is None or df.empty:
                raise ValueError("读取成功，但是文件里没有数据 (空文件)。")

            # 清洗数据：处理 NaN 确保导出不出错
            df = df.fillna("")

            # ---------------------------
            # 第二阶段：稳定导出
            # ---------------------------
            if out_ext == '.csv':
                df.to_csv(out_file, index=False, encoding='utf-8-sig') # 使用 utf-8-sig 让 Excel 默认正常打开中文
            elif out_ext == '.xlsx':
                df.to_excel(out_file, index=False)
            elif out_ext == '.tmx':
                self.dataframe_to_tmx(df, out_file)
            elif out_ext == '.json':
                df.to_json(out_file, orient='records', force_ascii=False, indent=4)
            elif out_ext == '.xml':
                # 防止 XML 列名存在非法字符 (比如空格)
                df.columns = [str(c).replace(" ", "_").replace("/", "_") for c in df.columns]
                df.to_xml(out_file, index=False, force_ascii=False)
            elif out_ext == '.tsv':
                df.to_csv(out_file, index=False, sep='\t', encoding='utf-8')

            messagebox.showinfo("Success", f"{self.get_text('msg_success')}{out_file}")

        except Exception as e:
            messagebox.showerror("Error", f"{self.get_text('msg_error')}{str(e)}")
        finally:
            self.btn_convert.config(text=self.get_text("convert"), state=tk.NORMAL)

    # ---------------------------
    # 第三阶段：TMX 解析器 (不依赖外部格式，原生安全解析)
    # ---------------------------
    def tmx_to_dataframe(self, filepath):
        tree = ET.parse(filepath)
        root = tree.getroot()
        ns = root.tag.split('}')[0] + '}' if '}' in root.tag else ''

        data = []
        for tu in root.iter(f'{ns}tu'):
            tuvs = tu.findall(f'.//{ns}tuv')
            if len(tuvs) >= 2:
                src_node = tuvs[0].find(f'.//{ns}seg')
                tgt_node = tuvs[1].find(f'.//{ns}seg')
                
                # 安全获取文本
                src_text = "".join(src_node.itertext()) if src_node is not None else ""
                tgt_text = "".join(tgt_node.itertext()) if tgt_node is not None else ""
                
                data.append({"Source": src_text.strip(), "Target": tgt_text.strip()})
        return pd.DataFrame(data)

    def dataframe_to_tmx(self, df, filepath):
        if len(df.columns) < 2:
            raise ValueError("导出为 TMX 格式要求数据源至少包含 2 列（源语和目标语）！")

        src_col, tgt_col = df.columns[0], df.columns[1]

        tmx = ET.Element("tmx", version="1.4")
        header = ET.SubElement(tmx, "header", creationtool="SmartConverter", creationtoolversion="3.0", datatype="PlainText", segtype="sentence", adminlang="en-US", srclang=self.src_lang_var.get().strip())
        body = ET.SubElement(tmx, "body")

        for _, row in df.iterrows():
            src_text = str(row[src_col]).strip()
            tgt_text = str(row[tgt_col]).strip()
            
            if not src_text and not tgt_text: continue 

            tu = ET.SubElement(body, "tu")
            
            tuv_src = ET.SubElement(tu, "tuv", {"xml:lang": self.src_lang_var.get().strip()})
            ET.SubElement(tuv_src, "seg").text = src_text
            
            tuv_tgt = ET.SubElement(tu, "tuv", {"xml:lang": self.tgt_lang_var.get().strip()})
            ET.SubElement(tuv_tgt, "seg").text = tgt_text

        # 写入文件并美化排版
        xml_string = ET.tostring(tmx, encoding='utf-8')
        pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")
        # 清除由 minidom 产生的多余空行
        clean_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(clean_xml)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    if 'clam' in style.theme_names():
        style.theme_use('clam')
    app = UltimateConverterApp(root)
    root.mainloop()