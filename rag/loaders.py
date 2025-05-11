import os
import glob
from typing import List
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain.schema import Document


def load_documents(base_path: str) -> List[Document]:
    """
    Recursively load .md files with front-matter metadata and structured parsing.
    """
    documents: List[Document] = []
    subfolders = [f for f in glob.glob(os.path.join(base_path, "*")) if os.path.isdir(f)]

    loader_cls = UnstructuredMarkdownLoader
    if subfolders:
        for folder in subfolders:
            doc_type = os.path.basename(folder)
            loader = DirectoryLoader(
                folder,
                glob="**/*.md",
                loader_cls=loader_cls,
                loader_kwargs={}
            )
            for doc in loader.load():
                doc.metadata.setdefault("doc_type", doc_type)
                documents.append(doc)
    else:
        for file_path in glob.glob(os.path.join(base_path, "*.md")):
            loader = loader_cls(file_path)
            doc = loader.load()[0]
            doc.metadata.setdefault("doc_type", os.path.basename(base_path))
            documents.append(doc)
    print(f"[load_documents] {len(documents)} documentos carregados de {base_path}")
    return documents
