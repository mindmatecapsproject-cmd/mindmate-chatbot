"""
Knowledge Base Management
Handles ingestion of MindMate content from website links into Chroma vector database
"""

import os
from typing import List
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import settings

class KnowledgeBaseManager:
    """Manages knowledge base ingestion and retrieval"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.openai_api_key
        )
        self.db_path = settings.chroma_db_path
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        self.vectorstore = self._load_or_create_vectorstore()
    
    def _load_or_create_vectorstore(self):
        """Load existing vectorstore or create new one"""
        os.makedirs(self.db_path, exist_ok=True)
        
        try:
            vectorstore = Chroma(
                embedding_function=self.embeddings,
                persist_directory=self.db_path
            )
            return vectorstore
        except Exception as e:
            print(f"Creating new vectorstore: {e}")
            return Chroma(
                embedding_function=self.embeddings,
                persist_directory=self.db_path
            )
    
    def scrape_website(self, url: str) -> str:
        """Scrape content from a website URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator='\n', strip=True)
            return text
        
        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return ""
    
    def ingest_from_urls(self, urls: List[str]):
        """Ingest content from multiple URLs into the knowledge base"""
        documents = []
        
        for url in urls:
            print(f"Scraping: {url}")
            content = self.scrape_website(url)
            
            if content:
                # Split text into chunks
                chunks = self.text_splitter.split_text(content)
                
                # Create documents with metadata
                for i, chunk in enumerate(chunks):
                    doc = {
                        "page_content": chunk,
                        "metadata": {"source": url, "chunk": i}
                    }
                    documents.append(doc)
        
        # Add to vectorstore
        if documents:
            texts = [doc["page_content"] for doc in documents]
            metadatas = [doc["metadata"] for doc in documents]
            
            self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
            print(f"Ingested {len(texts)} chunks into knowledge base")
    
    def search(self, query: str, k: int = 5) -> List[str]:
        """Search the knowledge base for relevant content"""
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def add_custom_content(self, content: str, metadata: dict = None):
        """Add custom content to the knowledge base"""
        chunks = self.text_splitter.split_text(content)
        metadatas = [metadata or {}] * len(chunks)
        
        self.vectorstore.add_texts(texts=chunks, metadatas=metadatas)
        print(f"Added {len(chunks)} chunks to knowledge base")

# Initialize knowledge base manager
kb_manager = KnowledgeBaseManager()
