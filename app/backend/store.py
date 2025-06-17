from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
import getpass
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    UnstructuredMarkdownLoader,
    CSVLoader,
    TextLoader,
    PyPDFLoader,
    UnstructuredFileLoader
)
import os

load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("GOOGLE_API_KEY")

# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
# os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

# Use raw strings for Windows paths
role_docs = {
    "engineering": r"resources\data\engineering",
    "finance": r"resources\data\finance",
    "general": r"resources\data\general",
    "hr": r"resources\data\hr",
    "marketing": r"resources\data\marketing"
}

def vector_store_db():
    role_vectorstores = {}
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
  
    for role, folder_path in role_docs.items():
        # Normalize path for Windows
        folder_path = os.path.normpath(folder_path)
        
        if not os.path.exists(folder_path):
            print(f"⚠️ Warning: Directory '{folder_path}' does not exist. Skipping role '{role}'.")
            continue
            
        print(f"🔍 Processing role '{role}': {folder_path}")
        documents = []
        
        # Process all files in the directory
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # Skip directories
            if not os.path.isfile(file_path):
                continue
                
            try:
                # Handle different file types
                if filename.lower().endswith(".md"):
                    md_loader = UnstructuredMarkdownLoader(file_path)
                    docs = md_loader.load()
                
                elif filename.lower().endswith(".csv"):
                    csv_loader = CSVLoader(file_path)
                    docs = csv_loader.load()
                
                elif filename.lower().endswith(".txt"):
                    txt_loader = TextLoader(file_path)
                    docs = txt_loader.load()
                
                elif filename.lower().endswith(".pdf"):
                    pdf_loader = PyPDFLoader(file_path)
                    docs = pdf_loader.load()
                
                # Fallback for other file types
                else:
                    print(f"   ⚠️ Trying unstructured loader for: {filename}")
                    file_loader = UnstructuredFileLoader(file_path)
                    docs = file_loader.load()
                
                documents.extend(docs)
                print(f"   ✅ Loaded {filename} ({len(docs)} documents)")
                
            except Exception as e:
                print(f"   ❌ Failed to load {filename}: {str(e)}")
                continue
        
        # Skip role if no documents loaded
        if not documents:
            print(f"   ⚠️ No documents found for {role}")
            continue
            
        # Split documents into chunks
        chunks = text_splitter.split_documents(documents)
        print(f"   📚 Split into {len(chunks)} chunks")
        
        # Create vector store
        try:
            vectorstore = FAISS.from_documents(chunks, embeddings)
            role_vectorstores[role] = vectorstore
            print(f"   🧠 Created vector store for {role} with {len(chunks)} chunks")
        except Exception as e:
            print(f"   ❌ Failed to create vector store for {role}: {str(e)}")
    
    return role_vectorstores

# Usage example
if __name__ == "__main__":
    vectorstores = vector_store_db()
    
    # Save vector stores to disk
    for role, store in vectorstores.items():
        safe_role = "".join(c for c in role if c.isalnum() or c in "_-").rstrip()
        store.save_local(f"db_stores/vectorstore_{safe_role}")
        print(f"💾 Saved vector store for {role}")
    
    print("\nCompleted processing all roles!")