import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import xml.etree.ElementTree as ET
import os
from xml.dom import minidom

class FormatConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV / XLSX / TMX 格式转换工具")
        self.root.geometry("550x380")
        self.root.resizable(False, False)

        # 变量声明
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.src_lang = tk.StringVar(value="en-US")
        self.tgt_lang = tk.StringVar(value="zh-CN")

        self._build_gui()

    def _build_gui(self):
        # 整体内边距
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- 输入文件区域 ---
        ttk.Label(main_frame, text="第一步：选择输入文件 (CSV, XLSX, TMX)", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5), columnspan=3)
        ttk.Entry(main_frame, textvariable=self.input_file, width=45, state="readonly").grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        ttk.Button(main_frame, text="浏览...", command=self.browse_input).grid(row=1, column=2, padx=10, pady=(0, 15))

        # --- TMX 语言代码设置 (转换到 TMX 时需要) ---
        ttk.Label(main_frame, text="TMX 语言代码 (仅当导出为 TMX 时生效):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5), columnspan=3)
        
        lang_frame = ttk.Frame(main_frame)
        lang_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))
        
        ttk.Label(lang_frame, text="源语言:").pack(side=tk.LEFT)
        ttk.Entry(lang_frame, textvariable=self.src_lang, width=10).pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(lang_frame, text="目标语言:").pack(side=tk.LEFT)
        ttk.Entry(lang_frame, textvariable=self.tgt_lang, width=10).pack(side=tk.LEFT, padx=(5, 0))

        # --- 输出文件区域 ---
        ttk.Label(main_frame, text="第二步：选择保存位置和格式", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=(0, 5), columnspan=3)
        ttk.Entry(main_frame, textvariable=self.output_file, width=45, state="readonly").grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        ttk.Button(main_frame, text="另存为...", command=self.browse_output).grid(row=5, column=2, padx=10, pady=(0, 20))

        # --- 转换按钮 ---
        self.convert_btn = ttk.Button(main_frame, text="开始转换", command=self.process_conversion, style="Accent.TButton")
        self.convert_btn.grid(row=6, column=0, columnspan=3, pady=(10, 0), ipadx=20, ipady=5)

    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="选择输入文件",
            filetypes=(("Supported files", "*.csv *.xlsx *.tmx"), ("All files", "*.*"))
        )
        if filename:
            self.input_file.set(filename)

    def browse_output(self):
        if not self.input_file.get():
            messagebox.showwarning("提示", "请先选择输入文件！")
            return
            
        filename = filedialog.asksaveasfilename(
            title="保存文件",
            defaultextension=".xlsx",
            filetypes=(("Excel XLSX", "*.xlsx"), ("CSV UTF-8", "*.csv"), ("TMX Translation Memory", "*.tmx"))
        )
        if filename:
            self.output_file.set(filename)

    def process_conversion(self):
        in_file = self.input_file.get()
        out_file = self.output_file.get()

        if not in_file or not out_file:
            messagebox.showwarning("提示", "请确保已选择输入和输出文件！")
            return

        in_ext = os.path.splitext(in_file)[1].lower()
        out_ext = os.path.splitext(out_file)[1].lower()

        try:
            self.convert_btn.config(text="转换中...", state=tk.DISABLED)
            self.root.update()

            # 1. 统一将输入文件读取为 Pandas DataFrame
            df = None
            if in_ext == '.csv':
                df = pd.read_csv(in_file, encoding='utf-8')
            elif in_ext == '.xlsx':
                df = pd.read_excel(in_file)
            elif in_ext == '.tmx':
                df = self.tmx_to_dataframe(in_file)
            else:
                raise ValueError("不支持的输入格式")

            if df is None or df.empty:
                raise ValueError("读取到的数据为空或格式不正确。")

            # 2. 将 DataFrame 导出为目标格式
            if out_ext == '.csv':
                df.to_csv(out_file, index=False, encoding='utf-8')
            elif out_ext == '.xlsx':
                df.to_excel(out_file, index=False)
            elif out_ext == '.tmx':
                self.dataframe_to_tmx(df, out_file)
            else:
                raise ValueError("不支持的输出格式")

            messagebox.showinfo("成功", f"文件已成功转换为:\n{out_file}")

        except Exception as e:
            messagebox.showerror("错误", f"转换过程中发生错误:\n{str(e)}")
        finally:
            self.convert_btn.config(text="开始转换", state=tk.NORMAL)

    # --- 核心处理逻辑：TMX 解析与生成 ---

    def tmx_to_dataframe(self, filepath):
        """解析 TMX 文件并返回包含 Source 和 Target 的 DataFrame"""
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # 处理可能存在的命名空间 (namespace)
        ns = ''
        if '}' in root.tag:
            ns = root.tag.split('}')[0] + '}'

        data = []
        # 查找所有的 <tu> (Translation Unit)
        for tu in root.iter(f'{ns}tu'):
            tuvs = tu.findall(f'.//{ns}tuv')
            if len(tuvs) >= 2:
                # 提取前两个 tuv 中的 seg 文本
                src_node = tuvs[0].find(f'.//{ns}seg')
                tgt_node = tuvs[1].find(f'.//{ns}seg')
                
                src_text = src_node.text if src_node is not None else ""
                tgt_text = tgt_node.text if tgt_node is not None else ""
                
                data.append({"Source": src_text, "Target": tgt_text})
                
        return pd.DataFrame(data)

    def dataframe_to_tmx(self, df, filepath):
        """将 DataFrame 转换为标准的 TMX XML 格式"""
        if len(df.columns) < 2:
            raise ValueError("CSV/XLSX 文件至少需要两列数据才能转换为 TMX。")

        src_col = df.columns[0]
        tgt_col = df.columns[1]

        # 创建 XML 根节点
        tmx = ET.Element("tmx", version="1.4")
        header = ET.SubElement(tmx, "header", 
                               creationtool="PythonConverter", 
                               creationtoolversion="1.0",
                               datatype="PlainText", 
                               segtype="sentence",
                               adminlang="en-US", 
                               srclang=self.src_lang.get().strip())
        body = ET.SubElement(tmx, "body")

        # 遍历 DataFrame 填充数据
        for index, row in df.iterrows():
            src_text = str(row[src_col]) if pd.notna(row[src_col]) else ""
            tgt_text = str(row[tgt_col]) if pd.notna(row[tgt_col]) else ""
            
            if not src_text and not tgt_text:
                continue # 跳过空行

            tu = ET.SubElement(body, "tu")
            
            # Source 节点
            tuv_src = ET.SubElement(tu, "tuv", {"xml:lang": self.src_lang.get().strip()})
            seg_src = ET.SubElement(tuv_src, "seg")
            seg_src.text = src_text
            
            # Target 节点
            tuv_tgt = ET.SubElement(tu, "tuv", {"xml:lang": self.tgt_lang.get().strip()})
            seg_tgt = ET.SubElement(tuv_tgt, "seg")
            seg_tgt.text = tgt_text

        # 格式化 XML 并写入文件 (使用 minidom 增加缩进美化)
        xml_string = ET.tostring(tmx, encoding='utf-8')
        parsed_xml = minidom.parseString(xml_string)
        pretty_xml = parsed_xml.toprettyxml(indent="  ")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

if __name__ == "__main__":
    root = tk.Tk()
    # 简单的样式优化
    style = ttk.Style(root)
    style.theme_use('clam')
    app = FormatConverterApp(root)
    root.mainloop()