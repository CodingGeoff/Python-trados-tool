# AGENTS.md - 项目智能上下文文档

> 本文档为 AI 助手提供项目背景信息，帮助快速理解和处理代码相关任务。

---

## 项目概述

**项目名称**: Python Trados Tool - 本地化与翻译工具集  
**项目类型**: Python GUI 应用程序集合  
**主要用途**: 为翻译和本地化工作者提供一站式工具，支持术语库转换、PDF 文本提取、文件格式转换等

**核心技术栈**:

- **Python 3.13** - 主要开发语言
- **tkinter/customtkinter** - GUI 框架
- **PyMuPDF (fitz)** - PDF 解析与文本提取
- **pandas/openpyxl** - 表格数据处理
- **pytesseract** - OCR 文字识别
- **PIL (Pillow)** - 图像处理
- **SpaCy/jieba** - NLP 自然语言处理

---

## 目录结构

```
C:\10_Workspace\Python工具\Python-trados-tool\
├── AGENTS.md                          # 本文件 - 项目上下文文档
├── PDF_Hybrid_Processing_Algorithm.md # PDF 混合处理算法文档
├── PDF_Processing_Algorithm.md        # PDF 文本提取算法文档
├── build_exe.bat                      # PyInstaller 打包脚本
├── clean-pdf.py                       # 高级 PDF 清洗工具（含 NLP）
├── converter_config.json              # 转换器配置（目录记忆）
├── converter_config_v3.json           # 配置 v3 版本
├── csv-tmx-xml-gui.py                 # CSV 转 TMX/XML GUI
├── csv2tmx-gui.py                     # CSV 转 TMX 专用工具
├── csv_to_word_gui.py                 # CSV 转 Word 工具
├── I-LOVE-PDF.py                      # 基础 PDF 处理工具
├── multiterm-convert.py               # ★ 主要工具 - 全能术语转换器
├── ultimate_converter.py              # 术语转换器高级版（含容错引擎）
├── Ultimate_PDF_Extractor.py          # PDF 提取器标准版
├── Ultimate_PDF_Extractor-pro.py      # PDF 提取器专业版
├── text_diff.py                       # 文本对比工具
├── word.py                            # Word 处理工具
├── xml_converter.py                   # XML 转换器
└── venv\                              # Python 虚拟环境
    ├── Lib\site-packages\             # 依赖包
    └── Scripts\                       # 可执行脚本
```

---

## 核心工具详解

### 1. multiterm-convert.py - 全能术语转换中心

**定位**: 项目旗舰工具，功能最全面的术语库转换器

**功能特性**:

- 支持输入格式: CSV, Excel (.xls/.xlsx), TBX, XML
- 支持输出格式:
  - 标准 Simple XML
  - MultiTerm MTF (Trados 术语库格式)
  - TMX 翻译记忆库格式
  - Markdown 表格
- 智能容错引擎: XML 损坏时自动切换到正则提取模式
- 中文/英文双语术语支持

**关键技术实现**:

```python
# 双核 XML 解析 (标准 DOM + 正则容错)
def parse_tbx_xml(self, filepath):
    try:
        tree = ET.parse(filepath)  # 标准解析
    except ET.ParseError:
        return self.parse_xml_fallback(filepath)  # 容错模式

# 正则容错引擎 - 无视标签错误，强制提取数据
def parse_xml_fallback(self, filepath):
    entries = re.findall(r'<termEntry[^>]*>(.*?)</termEntry>', content, flags=re.DOTALL)
```

**UI 设计**:

- 现代扁平化配色方案 (#F0F4F8 背景, #3B82F6 主色)
- 实时日志输出框
- 多格式复选框支持批量导出

---

### 2. ultimate_converter.py - 术语转换器防弹版

**定位**: multiterm-convert.py 的增强版本，增加了更多容错处理

**额外特性**:

- 更强的 XML 损坏修复能力
- 变量命名严格区分（`var_export_*` 前缀）避免命名冲突
- 更友好的错误提示信息

---

### 3. clean-pdf.py - 高级 PDF 清洗工具

**定位**: 含 NLP 和空间感知的 PDF 文本清洗工具

**核心功能**:

- **多维 NLP 清洗引擎**: 自动识别并移除页眉/页脚/页码/日期/署名
- **空间感知**: 基于 Y 坐标判断干扰块位置（页面顶部 12% 或底部 88% 区域）
- **连字符修复**: 自动修复断行单词 "ex-\nample" → "example"
- **OCR 支持**: 扫描件自动识别（需 Tesseract）

**智能干扰块检测算法**:

```python
def is_noise_block(text, y0, y1, page_height):
    # 1. 空间坐标判定：页眉页脚区域 + 短文本
    is_top = y0 < (page_height * 0.12)
    is_bottom = y1 > (page_height * 0.88)
    
    # 2. 正则模式：日期、罗马数字、下载水印
    if re.fullmatch(r'^(?:[0-3]?\d\s+)?[A-Z][a-z]{2,8}\s+\d{4}$', text):  # 日期
    if re.search(r'Downloaded from http', text):  # 学术水印
    
    # 3. NLP 判定：人名/书名（首字母大写密集 + 无标点结尾）
    title_case_ratio = title_case_words / len(words)
    if title_case_ratio > 0.6 and word_count < 6:
        return True  # 判定为干扰块
```

---

### 4. Ultimate_PDF_Extractor.py / -pro.py

**定位**: PDF 文本提取工具（标准版与专业版）

**处理流程**:

1. **直接提取**: 使用 PyMuPDF `page.get_text()`
2. **扫描检测**: 字符数 < 阈值(默认50) 判定为扫描页
3. **OCR 识别**: PDF → Pixmap → PIL Image → pytesseract
4. **文本清洗**: 连字符修复、空格压缩

**Tesseract 自动寻路**:

```python
def setup_tesseract():
    potential_paths = [
        r'C:/Software/Tesseract-OCR/tesseract.exe',
        r'C:/Program Files/Tesseract-OCR/tesseract.exe',
        # ... 多路径尝试
    ]
```

---

## 技术文档

### PDF 处理算法详解 (PDF_Processing_Algorithm.md)

**英文 PDF 处理流程**:

```
PDF → PyMuPDF → 直接文本提取 → 四步清洗 → 结构化输出
```

**四步清洗**:

1. 连字符修复: `ex-\nample` → `example`
2. 引用标记移除: `[1], [12-14]`
3. 特殊字符过滤
4. 空格压缩 + 小写化

**中文 PDF 特殊处理**:

- 中文换行合并: `翻译家\n群体` → `翻译家群体`
- 保持中文标点符号

### PDF 混合处理算法 (PDF_Hybrid_Processing_Algorithm.md)

**适用场景**: 同时包含文本页和扫描页的 PDF

**智能检测逻辑**:

```python
if len(text.strip()) < 50:  # 字符数阈值
    # 启用 OCR 流程
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2倍分辨率
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    text = pytesseract.image_to_string(img, lang='eng')
```

---

## 构建与打包

### 使用 build_exe.bat 打包 EXE

```batch
:: 清理旧构建
rmdir /s /q "build"
rmdir /s /q "dist"

:: PyInstaller 打包
pyinstaller ^
    --name "TermConverter" ^
    --onefile ^
    --windowed ^
    --collect-all pandas ^
    --collect-all openpyxl ^
    --collect-all numpy ^
    --hidden-import tkinter ^
    multiterm-convert.py
```

**输出**: `dist\TermConverter.exe` - 独立运行的 Windows 可执行文件

---

## 开发约定

### 代码风格

- **中文优先**: 用户界面和日志全部使用中文
- **Emoji 增强**: 日志和标题使用 Emoji 提升可读性 (`🚀`, `✅`, `❌`, `⚠️`)
- **防御式编程**: 大量使用 try-except 块，确保单文件失败不影响整体

### 命名规范

- GUI 类名: `Ultimate*Converter`, `*Processor`
- 回调函数: `*_callback`
- 变量前缀区分: `var_export_*` 用于复选框变量

### 错误处理模式

```python
try:
    result = process_file()
    self.log("✅ 处理成功")
except FileNotFoundError as e:
    self.log(f"❌ 文件不存在: {e}")
except ET.ParseError as e:
    self.log(f"⚠️ XML 损坏，启用容错模式")
    result = fallback_parse()
except Exception as e:
    self.log(f"❌ 未知错误: {e}")
    # 绝不让单个文件影响批量处理
    continue
```

---

## 依赖安装

```bash
# 激活虚拟环境
venv\Scripts\activate.bat

# 核心依赖
pip install pandas openpyxl
pip install PyMuPDF
pip install pytesseract pillow
pip install customtkinter
pip install spacy jieba

# Tesseract-OCR 引擎 (需单独安装)
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
```

---

## 常见任务速查

| 任务 | 入口文件 | 关键函数/类 |
|------|----------|-------------|
| 术语格式转换 | `multiterm-convert.py` | `UltimateTermConverter.load_data_smart()` |
| PDF 文本提取 | `clean-pdf.py` | `PDFProcessorWorker._process_single_pdf()` |
| PDF OCR 识别 | `Ultimate_PDF_Extractor.py` | `page.get_pixmap()` + `pytesseract.image_to_string()` |
| XML 容错解析 | `ultimate_converter.py` | `parse_xml_fallback()` |
| 打包 EXE | `build_exe.bat` | PyInstaller |

---

## 项目历史与演进

1. **初代**: 基础 CSV/TMX 转换 (`csv2tmx-gui.py`)
2. **第二代**: 引入 XML/TBX 支持 (`csv-tmx-xml-gui.py`)
3. **第三代**: 全能术语转换器 (`multiterm-convert.py`)
4. **第四代**: 容错引擎 + 防弹版 (`ultimate_converter.py`)
5. **并行发展**: PDF 处理工具链 (`clean-pdf.py`, `Ultimate_PDF_Extractor*.py`)

---

## 注意事项

1. **Tesseract 依赖**: PDF OCR 功能需要预先安装 Tesseract-OCR 引擎，程序会自动探测常见安装路径
2. **内存管理**: 超长 PDF (1000+ 页) 建议分批处理，防止内存溢出
3. **字符编码**: Windows 批处理脚本使用 `chcp 65001` 确保 UTF-8 编码
4. **虚拟环境**: 开发/运行前确保激活 `venv`，打包脚本会自动检测并激活

---

*文档版本: 1.0*  
*最后更新: 2026-02-27*  
*项目路径: C:\10_Workspace\Python工具\Python-trados-tool*
