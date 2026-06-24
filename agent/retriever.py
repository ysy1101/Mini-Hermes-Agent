"""
向量检索模块
基于 ChromaDB 实现语义搜索
"""
import os
from typing import List, Dict, Optional, Tuple

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False


class VectorRetriever:
    """向量检索器"""
    
    def __init__(
        self,
        persist_dir: str = "chroma_db",
        collection_name: str = "knowledge_base",
    ):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.collection = None
        
        if not CHROMA_AVAILABLE:
            self._available = False
            return
        
        self._available = True
        self.client = chromadb.Client(Settings(
            persist_directory=persist_dir,
            is_persistent=True,
        ))
        
        # 获取或创建 collection
        try:
            self.collection = self.client.get_collection(collection_name)
        except Exception:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
    
    @property
    def available(self) -> bool:
        return self._available if CHROMA_AVAILABLE else False
    
    def add_documents(
        self,
        chunks: List[str],
        source: str,
        metadatas: Optional[List[Dict]] = None,
    ):
        """添加文档块到向量库"""
        if not self.available:
            return "ChromaDB 未安装，无法添加文档"
        
        if not chunks:
            return "没有可添加的文档块"
        
        ids = [f"{source}_{i}" for i in range(len(chunks))]
        
        if metadatas is None:
            metadatas = [{"source": source, "chunk_index": i} for i in range(len(chunks))]
        
        try:
            # 删除同一来源的旧数据
            existing = self.collection.get(where={"source": source})
            if existing["ids"]:
                self.collection.delete(ids=existing["ids"])
            
            self.collection.add(
                documents=chunks,
                ids=ids,
                metadatas=metadatas,
            )
            return f"已添加 {len(chunks)} 个文档块（来源：{source}）"
        except Exception as e:
            return f"添加文档失败：{str(e)}"
    
    def search(
        self, query: str, top_k: int = 5
    ) -> List[Tuple[str, str, float]]:
        """
        搜索相关文档
        返回: [(文档内容, 来源, 相似度), ...]
        """
        if not self.available:
            return []
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
            )
            
            items = []
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    source = ""
                    distance = 0.0
                    if results["metadatas"] and results["metadatas"][0]:
                        source = results["metadatas"][0][i].get("source", "")
                    if results["distances"] and results["distances"][0]:
                        distance = results["distances"][0][i]
                    
                    # 将距离转换为相似度 (cosine distance -> similarity)
                    similarity = 1 - min(distance, 1.0)
                    items.append((doc, source, similarity))
            
            return items
        except Exception as e:
            print(f"搜索错误：{str(e)}")
            return []
    
    def get_stats(self) -> Dict:
        """获取向量库统计信息"""
        if not self.available:
            return {"状态": "不可用"}
        
        try:
            count = self.collection.count()
            return {
                "文档块总数": count,
                "集合名称": self.collection_name,
                "存储位置": self.persist_dir,
            }
        except Exception as e:
            return {"错误": str(e)}
    
    def clear(self):
        """清空向量库"""
        if self.available and self.collection:
            try:
                ids = self.collection.get()["ids"]
                if ids:
                    self.collection.delete(ids=ids)
                return "向量库已清空"
            except Exception as e:
                return f"清空失败：{str(e)}"
        return "向量库不可用"


def build_index(data_dir: str, persist_dir: str = "chroma_db") -> str:
    """
    构建索引：解析 data_dir 下所有文档，建立向量索引
    """
    from .document import load_documents
    
    docs = load_documents(data_dir)
    if not docs:
        return "未找到任何文档（支持 .txt, .md, .pdf）"
    
    retriever = VectorRetriever(persist_dir=persist_dir)
    if not retriever.available:
        return "ChromaDB 未安装，请运行 pip install chromadb"
    
    total_chunks = 0
    for doc in docs:
        result = retriever.add_documents(
            chunks=doc["chunks"],
            source=doc["filename"],
        )
        total_chunks += doc["chunk_count"]
    
    return f"索引构建完成：{len(docs)} 个文档，共 {total_chunks} 个文本块"