"""
文档解析模块
支持 PDF、Markdown、TXT 等格式
"""
import os
import re
from typing import List, Dict, Optional


def parse_file(filepath: str) -> str:
    """解析单个文件，返回文本内容"""
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == '.txt':
        return _parse_txt(filepath)
    elif ext == '.md':
        return _parse_md(filepath)
    elif ext == '.pdf':
        return _parse_pdf(filepath)
    else:
        return f"不支持的文件格式：{ext}"


def _parse_txt(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def _parse_md(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def _parse_pdf(filepath: str) -> str:
    """解析 PDF 文件"""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except ImportError:
        return "错误：需要安装 PyPDF2 (pip install PyPDF2)"
    except Exception as e:
        return f"PDF 解析错误：{str(e)}"


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    将文本切分为固定大小的块
    优先按段落切分，段落过长时按句子切分
    """
    if not text.strip():
        return []
    
    # 先按段落切分
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        if len(para) <= chunk_size:
            chunks.append(para)
        else:
            # 段落过长，按句子切分
            sentences = re.split(r'(?<=[。！？.!?])\s*', para)
            current = ""
            for sent in sentences:
                sent = sent.strip()
                if not sent:
                    continue
                if len(current) + len(sent) <= chunk_size:
                    current += sent
                else:
                    if current:
                        chunks.append(current)
                    # 如果单个句子超过 chunk_size，强制切分
                    if len(sent) > chunk_size:
                        for i in range(0, len(sent), chunk_size - overlap):
                            chunks.append(sent[i:i + chunk_size - overlap])
                    else:
                        current = sent
            if current:
                chunks.append(current)
    
    return chunks


def load_documents(data_dir: str) -> List[Dict]:
    """
    加载目录下所有文档，返回结构化的文档列表
    返回格式：[{"filename": str, "content": str, "chunks": [str]}, ...]
    """
    documents = []
    
    if not os.path.exists(data_dir):
        return documents
    
    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1].lower()
            if ext in ('.txt', '.md', '.pdf'):
                content = parse_file(filepath)
                chunks = chunk_text(content)
                documents.append({
                    "filename": filename,
                    "filepath": filepath,
                    "content": content,
                    "chunks": chunks,
                    "chunk_count": len(chunks),
                })
    
    return documents