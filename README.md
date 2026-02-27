# 🌐 Python Trados Tool - 本地化与翻译工具集

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13+-blue.svg" alt="Python 3.13+">
  <img src="https://img.shields.io/badge/Platform-Windows-green.svg" alt="Windows">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
</p>

> 一套专为翻译、本地化工作者和语言服务提供商打造的高效工具集，涵盖术语库转换、PDF 文本提取、格式转换等核心功能。

---

## 📑 目录

- [项目简介](#项目简介)
- [核心功能](#核心功能)
- [快速开始](#快速开始)
- [工具详解](#工具详解)
- [技术架构](#技术架构)
- [安装指南](#安装指南)
- [使用教程](#使用教程)
- [开发指南](#开发指南)
- [常见问题](#常见问题)
- [更新日志](#更新日志)

---

## 项目简介

**Python Trados Tool** 是一个综合性的本地化工具集合，旨在简化和自动化翻译工作流程中的常见任务。无论您是需要处理术语库格式转换、从 PDF 提取可翻译文本，还是进行文件格式转换，这个工具集都能提供高效、可靠的解决方案。

### 设计理念

- **🎯 专业导向**: 针对 SDL Trados、MemoQ 等专业 CAT 工具优化
- **🚀 高效便捷**: 一键式操作，批量处理能力
- **🛡️ 健壮容错**: 智能错误处理，确保任务连续性
- **🎨 友好界面**: 现代化 GUI 设计，实时日志反馈

---

## 核心功能

### 1. 术语库转换中心 🔄

**支持的格式互转**:

| 输入格式 | 输出格式 | 说明 |
|---------|---------|------|
| CSV | XML, MTF, TMX, Markdown | 表格数据转术语库 |
| Excel (.xls/.xlsx) | XML, MTF, TMX, Markdown | 支持多工作表 |
| TBX | CSV, XML, MTF, Markdown | 标准术语交换格式 |
| XML | CSV, MTF, TMX, Markdown | 自定义 XML 格式 |

**输出格式详解**:

- **Simple XML**: 标准双语对照 XML，易于解析
- **MultiTerm MTF**: SDL Trados MultiTerm 术语库格式
- **TMX**: 翻译记忆交换格式，通用标准
- **Markdown**: 便于文档展示的表格格式

### 2. PDF 文本提取引擎 📄

**三种处理模式**:

1. **纯文本模式**: 直接从可编辑 PDF 提取文本
2. **OCR 模式**: 扫描件/图片 PDF 的文字识别
3. **混合模式**: 自动检测并处理文本+扫描混合 PDF

**智能清洗功能**:

- 自动识别并移除页眉/页脚/页码
- 修复连字符断词（如 "ex- ample" → "example"）
- 中文换行智能合并
- 学术水印检测与清除

### 3. 文件格式转换工具 📁

- **CSV ↔ Word**: 表格数据与 Word 文档互转
- **CSV ↔ TMX**: 翻译记忆库格式转换
- **XML 转换器**: 通用 XML 格式处理

---

## 快速开始

### 系统要求

- **操作系统**: Windows 10/11
- **Python 版本**: 3.13 或更高
- **内存**: 建议 4GB 以上（处理大型 PDF 时需要更多）
- **磁盘空间**: 500MB 可用空间

### 一键启动

```powershell
# 1. 进入项目目录
cd Python-trados-tool

# 2. 激活虚拟环境
.\venv\Scripts\activate

# 3. 启动主工具
python multiterm-convert.py
```

### 获取独立 EXE

如果不想安装 Python 环境，可直接使用打包好的可执行文件：

```powershell
# 运行打包脚本生成 EXE
.\build_exe.bat

# 输出位置
dist\TermConverter.exe
```

---

## 工具详解

### 🌟 multiterm-convert.py - 全能术语转换中心

**定位**: 项目旗舰工具，功能全面的术语库转换器

#### 功能特性

**智能解析引擎**:

- **Pandas 引擎**: 处理 CSV/Excel 表格数据
- **XML DOM 引擎**: 标准 XML/TBX 解析
- **正则容错引擎**: 损坏 XML 文件强制提取

**双核 XML 解析**:

```python
# 第一核：标准 DOM 解析
try:
    tree = ET.parse(filepath)
    root = tree.getroot()
except ET.ParseError:
    # 第二核：容错正则解析
    return self.parse_xml_fallback(filepath)
```

**容错正则解析示例**:

```python
def parse_xml_fallback(self, filepath):
    """无视 XML 结构错误，强制提取有效数据"""
    with open(filepath, 'r', encoding='utf-8-sig', errors='ignore') as f:
        content = f.read()
    
    # 匹配 TBX termEntry 块
    entries = re.findall(r'<termEntry[^>]*>(.*?)</termEntry>', content, flags=re.DOTALL)
    
    for entry in entries:
        # 提取中英文术语
        lang_sets = re.findall(r'<langSet[^>]*xml:lang="([^"]+)"[^>]*>(.*?)</langSet>', entry, flags=re.DOTALL)
        # ... 解析逻辑
```

#### 使用界面

1. **数据源选择**: 支持浏览选择 CSV/XLS/TBX/XML 文件
2. **导出目录**: 自定义输出位置
3. **修改人标识**: 设置作者 ID（用于 MTF/TMX 元数据）
4. **格式勾选**: 可同时导出多种格式

#### 日志输出示例

```
[14:32:10] --- 转换任务开始 ---
[14:32:10] ➡️ 检测到 XML/TBX 文件，启用 XML DOM 解析引擎...
[14:32:11] ✅ 成功读取并解析 1,247 条术语数据
[14:32:11] 💾 已导出: 基础 XML
[14:32:12] 💾 已导出: MultiTerm MTF
[14:32:12] 💾 已导出: TMX 记忆库
[14:32:12] 🎉 全部导出完成！
```

---

### 🧹 clean-pdf.py - 高级 PDF 清洗工具

**定位**: 含 NLP 和空间感知的最强 PDF 处理工具

#### 核心特性

**多维 NLP 清洗引擎**:

```python
class UltimateTextCleaner:
    @staticmethod
    def is_noise_block(text, y0, y1, page_height):
        """
        基于空间坐标和 NLP 规则判定干扰块
        
        检测维度:
        1. 空间位置: 页面顶部/底部 12% 区域的短文本
        2. 日期模式: "25 November 2025" 格式的孤立日期
        3. 罗马数字: 页码前缀如 "xvi Series Editor's Introduction"
        4. 下载水印: 学术论文的 "Downloaded from http..."
        5. 人名/书名: 首字母大写密集 + 无标点结尾
        """
        # 空间坐标判定
        is_top = y0 < (page_height * 0.12)
        is_bottom = y1 > (page_height * 0.88)
        
        # NLP 句法试探
        words = text.split()
        title_case_words = sum(1 for w in words if w.istitle())
        if title_case_words / len(words) > 0.6 and len(words) < 6:
            return True  # 判定为署名/书名干扰块
```

**连字符修复**:

```python
@staticmethod
def heal_text(text):
    # 修复断行连字符: "misin-\nformation" → "misinformation"
    text = re.sub(r'([a-zA-Z]+)[-\xad]\s*\n\s*([a-zA-Z]+)', r'\1\2', text)
    # 段内换行转空格
    text = text.replace('\n', ' ')
    return re.sub(r'\s{2,}', ' ', text).strip()
```

**处理流程图**:

```
PDF 输入
    │
    ▼
┌──────────────────────┐
│ PyMuPDF 解析         │
│ - 提取文本块         │
│ - 获取空间坐标       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ 干扰块检测           │
│ - 空间坐标过滤       │
│ - 正则模式匹配       │
│ - NLP 语义分析       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ 文本修复             │
│ - 连字符合并         │
│ - 换行规范化         │
└──────────┬───────────┘
           │
           ▼
    清洗后的纯文本输出
```

---

### 📄 Ultimate_PDF_Extractor.py - PDF 提取器

**定位**: 标准版 PDF 处理工具，支持 OCR

#### 扫描件检测机制

```python
# 基于字符数的启发式检测
SCAN_THRESHOLD = 50  # 字符数阈值

text = page.get_text()
if len(text.strip()) < SCAN_THRESHOLD:
    # 判定为扫描页，启用 OCR
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2倍分辨率
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    text = pytesseract.image_to_string(img, lang='eng')
```

#### Tesseract 自动寻路

```python
def setup_tesseract():
    """自动探测 Tesseract 安装路径"""
    if os.name == 'nt':
        potential_paths = [
            r'C:/Software/Tesseract-OCR/tesseract.exe',
            r'C:/Program Files/Tesseract-OCR/tesseract.exe',
            r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe',
            r'D:/Program Files/Tesseract-OCR/tesseract.exe'
        ]
        for path in potential_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                return True
    return False
```

---

## 技术架构

### 技术栈概览

```
┌─────────────────────────────────────────────────────────────┐
│                        应用层 (GUI)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ tkinter      │  │ customtkinter│  │ 现代化主题        │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                        业务逻辑层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ 术语转换引擎  │  │ PDF处理引擎   │  │ 格式转换引擎      │  │
│  │ (pandas/ET)  │  │ (PyMuPDF)    │  │ (openpyxl)       │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                        基础设施层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ OCR引擎      │  │ 图像处理      │  │ NLP处理          │  │
│  │ (tesseract)  │  │ (PIL)        │  │ (spacy/jieba)    │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 核心依赖

| 库 | 版本 | 用途 |
|---|------|------|
| PyMuPDF | 1.24.x | PDF 解析与渲染 |
| pandas | 2.x | 表格数据处理 |
| openpyxl | 3.x | Excel 文件读写 |
| pytesseract | 0.3.x | OCR 文字识别 |
| Pillow | 10.x | 图像处理 |
| customtkinter | 5.x | 现代化 GUI |
| spacy | 3.8.x | 英文 NLP 处理 |
| jieba | 0.42.x | 中文分词 |

---

## 安装指南

### 方法一：使用虚拟环境（推荐）

```powershell
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
.\venv\Scripts\activate

# 3. 安装依赖
pip install pandas openpyxl PyMuPDF pytesseract Pillow customtkinter

# 4. 安装 NLP 模型（可选）
pip install spacy jieba
python -m spacy download en_core_web_md
```

### 方法二：安装 Tesseract OCR 引擎

**Windows**:

1. 下载安装包: <https://github.com/UB-Mannheim/tesseract/wiki>
2. 安装到默认路径 `C:\Program Files\Tesseract-OCR`
3. 程序会自动探测路径，无需额外配置

**验证安装**:

```powershell
tesseract --version
```

### 方法三：打包为独立 EXE

```powershell
# 运行打包脚本
.\build_exe.bat

# 输出文件
dist\TermConverter.exe
```

---

## 使用教程

### 场景一：术语库格式转换

**需求**: 将客户提供的 Excel 术语表转换为 Trados MultiTerm 格式

**步骤**:

1. 运行 `python multiterm-convert.py`
2. 点击"浏览..."选择 Excel 文件
3. 勾选 "MultiTerm MTF" 格式
4. 点击"一键执行转换"
5. 在输出目录找到 `*_MTF.xml` 文件
6. 在 Trados MultiTerm 中导入该文件

**注意事项**:

- Excel 第一列应为中文，第二列应为英文
- 程序会自动跳过表头行
- 支持 `.xls` 和 `.xlsx` 格式

### 场景二：PDF 文本提取

**需求**: 从扫描版学术论文中提取可编辑文本

**步骤**:

1. 运行 `python clean-pdf.py`
2. 选择 PDF 文件（可多选）
3. 设置扫描阈值（建议 50-100）
4. 选择 OCR 语言（eng/eng+chi_sim）
5. 点击"开始处理"
6. 等待处理完成，输出 TXT 文件

**参数说明**:

- **扫描阈值**: 低于此字符数的页面将触发 OCR（默认 50）
- **OCR 语言**: `eng` 仅英文，`eng+chi_sim` 中英混合
- **DPI 倍数**: 2倍（144 DPI）适合大多数场景

### 场景三：损坏 TBX 文件修复

**需求**: 术语库文件损坏，无法正常导入 CAT 工具

**步骤**:

1. 运行 `python ultimate_converter.py`（容错增强版）
2. 选择损坏的 TBX/XML 文件
3. 程序会自动检测损坏并切换到容错模式
4. 导出为新的 MTF 或 TMX 格式

**容错机制**:

- 无视 XML 标签不匹配
- 强制提取 `<termEntry>` 块
- 正则匹配 `<langSet>` 和 `<term>` 内容

---

## 开发指南

### 项目结构

```
Python-trados-tool/
├── multiterm-convert.py          # 主入口：术语转换
├── ultimate_converter.py         # 增强版：容错处理
├── clean-pdf.py                  # PDF 清洗工具
├── Ultimate_PDF_Extractor.py     # PDF 提取器标准版
├── Ultimate_PDF_Extractor-pro.py # PDF 提取器专业版
├── build_exe.bat                 # 打包脚本
├── converter_config.json         # 用户配置
├── venv/                         # 虚拟环境
└── AGENTS.md                     # AI 助手上下文
```

### 代码规范

**命名约定**:

```python
# 类名: 大驼峰
class UltimateTermConverter:
    
# 方法名: 小写下划线
def parse_tbx_xml(self, filepath):
    
# GUI 变量: var_ 前缀
self.var_export_simple = tk.BooleanVar(value=True)

# 回调函数: _callback 后缀
def log_callback(self, message):
```

**错误处理模式**:

```python
try:
    result = self.process_file()
    self.log("✅ 处理成功")
except FileNotFoundError:
    self.log("❌ 文件不存在")
    messagebox.showerror("错误", "请检查文件路径")
except ET.ParseError as e:
    self.log(f"⚠️ XML 解析失败，启用容错模式: {e}")
    result = self.fallback_parse()  # 降级处理
except Exception as e:
    self.log(f"❌ 未知错误: {e}")
    # 确保不影响其他文件处理
    continue
```

**UI 设计规范**:

```python
# 配色方案
self.colors = {
    "bg": "#F0F4F8",      # 背景色
    "panel": "#FFFFFF",   # 面板色
    "text": "#334155",    # 文字色
    "primary": "#3B82F6", # 主色（蓝）
    "success": "#10B981", # 成功色（绿）
    "warning": "#F59E0B", # 警告色（黄）
    "border": "#E2E8F0"   # 边框色
}

# Emoji 使用规范
"🚀"  # 开始/启动
"✅"  # 成功完成
"❌"  # 错误失败
"⚠️"  # 警告提示
"💾"  # 保存/导出
"📂"  # 文件夹
"🎉"  # 任务完成庆祝
```

### 添加新功能

**步骤 1**: 创建功能模块

```python
# my_new_feature.py
def process_data(input_data):
    """处理逻辑"""
    return processed_data
```

**步骤 2**: 集成到 GUI

```python
# 在主类中添加按钮和回调
def setup_ui(self):
    ttk.Button(parent, text="新功能", command=self.run_new_feature)

def run_new_feature(self):
    try:
        result = process_data(self.input_data)
        self.log("✅ 新功能执行成功")
    except Exception as e:
        self.log(f"❌ 新功能失败: {e}")
```

**步骤 3**: 更新文档

- 在 README.md 中添加功能说明
- 在 AGENTS.md 中添加技术细节

---

## 常见问题

### Q1: 安装 pytesseract 后仍提示找不到 Tesseract 引擎？

**A**: 需要单独安装 Tesseract-OCR 二进制程序：

```powershell
# 1. 下载安装
# 访问 https://github.com/UB-Mannheim/tesseract/wiki
# 下载并安装到 C:\Program Files\Tesseract-OCR

# 2. 验证路径
ls "C:\Program Files\Tesseract-OCR\tesseract.exe"

# 3. 程序会自动探测，无需代码配置
```

### Q2: 处理中文 PDF 时 OCR 识别率低？

**A**: 需要安装中文语言包：

```powershell
# 下载中文语言数据
# 放到 Tesseract 的 tessdata 目录
curl -o chi_sim.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata
copy chi_sim.traineddata "C:\Program Files\Tesseract-OCR\tessdata\"

# 使用双语模式
ocr_lang = 'eng+chi_sim'
```

### Q3: 打包 EXE 后运行时缺少依赖？

**A**: 确保 `build_exe.bat` 中包含所有隐藏导入：

```batch
--hidden-import pandas \\
--hidden-import openpyxl \\
--hidden-import numpy \\
--collect-all pandas \\
--collect-all openpyxl
```

### Q4: 如何处理超大 PDF 文件（1000+ 页）？

**A**: 建议分批处理：

```python
# 修改代码，限制单次处理页数
MAX_PAGES = 500
for i, page in enumerate(doc):
    if i >= MAX_PAGES:
        self.log("⚠️ 已达到最大处理页数，剩余页面跳过")
        break
```

### Q5: XML 文件解析失败，容错模式也无效？

**A**: 文件可能损坏，尝试手动修复：

```python
# 使用正则强制提取所有文本内容
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()
    
# 提取所有可能的术语对
terms = re.findall(r'>([^<]{2,50})<', content)
```

---

## 更新日志

### v4.0 (2026-02)

- ✨ 新增 `ultimate_converter.py` 容错增强版
- 🛡️ 双核 XML 解析引擎（DOM + 正则）
- 🚀 优化 OCR 处理速度（多线程支持）
- 🐛 修复 Excel 空行处理问题

### v3.0 (2026-01)

- ✨ 新增 `clean-pdf.py` NLP 清洗工具
- 🧠 空间感知干扰块检测
- 📄 PDF 扫描件自动识别与 OCR
- 🎨 现代化 UI 界面升级

### v2.0 (2025-12)

- ✨ 新增 TMX 格式支持
- 🔄 术语库双向转换
- 📊 批量文件处理能力
- 📝 Markdown 导出功能

### v1.0 (2025-11)

- 🎉 项目初始发布
- ✨ 基础术语转换功能
- 📄 CSV/Excel/XML 支持
- 🖥️ 图形化界面

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交 Issue

请包含以下信息：

- 操作系统版本
- Python 版本
- 错误复现步骤
- 完整错误日志

### 代码贡献

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 许可证

本项目基于 MIT 许可证开源。

```
MIT License

Copyright (c) 2026 Python Trados Tool Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 联系方式

- **项目主页**: <https://github.com/codinggeoff/python-trados-tool>
- **问题反馈**: <https://github.com/codinggeoff/python-trados-tool/issues>
- **邮件联系**: <399328474@qq.com>

---

<p align="center">
  Made with ❤️ by Translators, for Translators
</p>
