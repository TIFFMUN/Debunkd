import os
from langchain_community.document_loaders import CSVLoader, WebBaseLoader, MergedDataLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def precompute_verify_vectors(persist_directory="chroma_verify_db"):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Current directory: {current_dir}")
        
        file_path = os.path.join(current_dir, "COVID Fake News Data.csv")
        print(f"Checking for file: {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found at: {file_path}")
        
        print("Loading CSV file...")
        csv_loader = CSVLoader(file_path=file_path, encoding="utf-8")
        docs1 = csv_loader.load()
        print(f"Loaded {len(docs1)} documents from CSV")
        
        print("Loading web data from https://theonion.com/...")
        web_loader = WebBaseLoader(
            "https://theonion.com/",
            requests_kwargs={"headers": {"User-Agent": "YourAppName/1.0"}}
        )
        docs2 = web_loader.load()
        print(f"Loaded {len(docs2)} documents from web")
        
        print("Merging datasets...")
        merged_loader = MergedDataLoader(loaders=[csv_loader, web_loader])
        docs = merged_loader.load()
        print(f"Total documents merged: {len(docs)}")
        
        print("Splitting documents...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        print(f"Created {len(splits)} splits")
        
        print("Generating embeddings and building vector store...")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        print(f"Verify vector store precomputed and saved to {persist_directory}")
        
    except Exception as e:
        print(f"Error in precompute_verify_vectors: {str(e)}")

def precompute_teacher_vectors(persist_directory="chroma_teacher_db"):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Current directory: {current_dir}")
        
        file_path1 = os.path.join(current_dir, "COVID Fake News Data.csv")
        file_path2 = os.path.join(current_dir, "tips.csv")
        
        for fp in [file_path1, file_path2]:
            print(f"Checking for file: {fp}")
            if not os.path.exists(fp):
                raise FileNotFoundError(f"CSV file not found at: {fp}")
        
        print("Loading CSV files...")
        csv_loader1 = CSVLoader(file_path=file_path1, encoding="utf-8")
        csv_loader2 = CSVLoader(file_path=file_path2, encoding="utf-8")
        
        docs1 = csv_loader1.load()
        docs2 = csv_loader2.load()
        print(f"Loaded {len(docs1)} from {file_path1}, {len(docs2)} from {file_path2}")
        
        combined_docs = docs1 + docs2
        print(f"Total combined documents: {len(combined_docs)}")
        
        print("Splitting documents...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        splits = text_splitter.split_documents(combined_docs)
        print(f"Created {len(splits)} splits")
        
        print("Generating embeddings and building vector store...")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        print(f"Teacher vector store precomputed and saved to {persist_directory}")
        
    except Exception as e:
        print(f"Error in precompute_teacher_vectors: {str(e)}")

if __name__ == "__main__":
    print("Starting precomputation...")
    precompute_verify_vectors()
    precompute_teacher_vectors()
    print("Precomputation complete.")