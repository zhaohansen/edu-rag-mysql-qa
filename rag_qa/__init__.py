# 该文件用于帮助 rag_qa这个Python包, 管理包内的脚本, 方便其它包的调用.
# 注意: 这里不做重量级导入(向量库/大模型), 否则只用到文档加载器时也会被迫加载模型.
import os
import sys

# 1. 记录当前目录.
current_dir = os.path.abspath(__file__)

# 2. 记录rag_qa目录 -> Milvus版的问答系统的目录.
rag_qa_path = os.path.dirname(current_dir)

# 3. 添加 rag_qa_path路径到 系统路径变量中.
if rag_qa_path not in sys.path:
    sys.path.insert(0, rag_qa_path)

# 4. 具体的导包动作 -> 改为按需导入, 避免 import rag_qa 时就加载 torch / 模型.
__all__ = ["RAGPrompts", "VectorStore", "RAGSystem"]


def __getattr__(name):
    if name == "RAGPrompts":
        from rag_qa.core.prompts import RAGPrompts
        return RAGPrompts
    if name == "VectorStore":
        from rag_qa.core.vector_store import VectorStore
        return VectorStore
    if name == "RAGSystem":
        from rag_qa.core.new_rag_system import RAGSystem
        return RAGSystem
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
