from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
import getpass

# Add new imports for memory (update here)
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("GOOGLE_API_KEY")

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY")

# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
store_folder = os.path.abspath(os.path.join(BASE_DIR, "../../db_stores"))

print(store_folder)
def load_db(role: str):  
  embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
  # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
  store_path = os.path.join(store_folder, f"vectorstore_{role}")
  print(store_path)

  if not os.path.exists(store_path):
    print(f"Vector store does not exist for {role}")
  return FAISS.load_local(store_path, embeddings=embeddings, allow_dangerous_deserialization=True)

# Create in-memory store for chat histories (update here)
memory_store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in memory_store:
        memory_store[session_id] = ChatMessageHistory()
    return memory_store[session_id]

def get_response(query: str, role: str, session_id: str = "default-session"):  # Keep session_id
  store = load_db(role)
  llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

  # Update prompt to include chat history (FIXED HERE)
  system_prompt = (
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Use three sentence maximum and keep the answer concise. "
    "Context: {context}"
  )
  
  # Create the prompt with history placeholder (FIXED HERE)
  prompt = ChatPromptTemplate.from_messages([
      ("system", system_prompt),
      MessagesPlaceholder(variable_name="history"),
      ("human", "{input}"),
  ])

  retriever = store.as_retriever()
  
  # Create the base chain (update here)
  document_chain = create_stuff_documents_chain(llm, prompt)
  
  # Create retrieval chain (update here)
  retrieval_chain = create_retrieval_chain(retriever, document_chain)

  # Create memory-enabled chain (update here)
  chain_with_memory = RunnableWithMessageHistory(
      retrieval_chain,
      get_session_history,
      input_messages_key="input",
      history_messages_key="history",  # Must match prompt placeholder name
      output_messages_key="answer",    # Add output key
  )

  # Update invocation with session_id (update here)
  result = chain_with_memory.invoke(
      {"input": query},
      config={"configurable": {"session_id": session_id}}
  )

  # Handle response (update here)
  return result.get("answer", "Sorry, I couldn't generate a response.")