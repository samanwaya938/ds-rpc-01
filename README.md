# 📂 Multiple Role-Based Document Retrieval with LLMs

## 🚀 Overview

This project is a **Role-Based Retrieval-Augmented Generation (RAG) System** built with **FastAPI**, **Streamlit**, and **LangChain**, leveraging **OpenAI** and **Google GenAI APIs**. It enables users to log in with a specific role and retrieve relevant answers based only on the data allowed for that role.

### 🔹 Use Case

* ✉️ An HR personnel can retrieve HR-specific data.
* 🏢 A finance officer can only access finance-related information.
* 🎓 Custom roles with isolated document knowledgebases.

Each role has a dedicated **vectorstore** created with **FAISS** using pre-uploaded documents. At query time, only the appropriate store is used to generate a context-aware response.

---

## 📊 Tech Stack

| Category      | Tools Used                      |
| ------------- | ------------------------------- |
| Backend       | FastAPI, Uvicorn                |
| Frontend      | Streamlit                       |
| LLM Interface | LangChain, OpenAI API           |
| Embeddings    | Google Generative AI Embeddings |
| Vector DB     | FAISS                           |
| Environment   | Python 3.10.8, Docker           |
| Secrets Mgmt  | dotenv (.env)                   |

---

## 📁 Folder Structure

```
my_project/
├── app/
│   ├── backend/
│   │   ├── main.py          # FastAPI backend entrypoint
│   │   ├── auth.py          # Authentication logic
│   │   ├── chat.py          # Chat + Retrieval logic
│   │   └── store.py         # Vectorstore retrieval logic
│   └── frontend/
│       └── app.py           # Streamlit frontend app
├── db_stores/               # Contains vectorstore_hr, vectorstore_finance, etc.
│
├── requirements.txt         # Project dependencies
├── Dockerfile               # Docker configuration
├── .env                     # API keys (not included in repo)
├── .dockerignore            # Docker ignore rules
```

---

## 🔧 Local Setup Instructions

### ✅ Create virtual environment

```bash
python -m venv venv
```

### ✅ Activate the virtual environment

* **Windows:**

```bash
venv\Scripts\activate
```

* **Unix/macOS:**

```bash
source venv/bin/activate
```

### ✅ Install dependencies

```bash
pip install -r requirements.txt
```

### Create .env file
Create .env file in the root directory and save your own OPENAI_API_KEY and GGOGLE_API_KEY. Make sure their should not be any whitespace around "="

### Run the store.py file
To create vectore database run the store.py file using the following command. It has to be run only once.
```bash
python app/backend/store.py
```

### 🌐 Run the application

* **Backend (FastAPI)**

```bash
uvicorn app.backend.main:app --reload
```

* **Frontend (Streamlit)**

```bash
streamlit run app/frontend/app.py
```

---

## 🚧 Docker Usage

### 📦 Build Image

```bash
docker buildx build -t rag-multirole:latest .
```

### 🚚 Pull from DockerHub

```bash
docker pull your-dockerhub-username/rag-multirole:latest
```

### 🔄 Run Docker Container with User API Keys

```bash
docker run -p 8000:8000 -p 8501:8501 \
  --env OPENAI_API_KEY="your_openai_key" \
  --env GOOGLE_API_KEY="your_google_key" \
  your-dockerhub-username/rag-multirole:latest
```

> ⚠️ `.env` file should NOT be part of the Docker image. Users must pass their own keys during runtime using `--env`.

---

## ⚖️ Environment Variables

| Variable Name    | Required | Description                           |
| ---------------- | -------- | ------------------------------------- |
| `OPENAI_API_KEY` | Yes      | OpenAI GPT models                     |
| `GOOGLE_API_KEY` | Yes      | Google GenAI embeddings (vectorstore) |

---

## 📅 Usage Instructions

1. **Login First**

   * ID: `Sam`
   * Password: `123`
   * Role: `hr`

2. **Query Input**

   * Ask questions relevant to your assigned role.
   * Example: "What are the onboarding steps for new employees?"

3. **Role-Based Vectorstores**

   * e.g., `vectorstore_hr` is used for the HR role.
   * All vectorstores are loaded from `db_stores/` directory.

---

## 📈 Example Roles & Vectorstores

| Role    | Folder Path                     |
| ------- | ------------------------------- |
| HR      | `db_stores/vectorstore_hr`      |
| Finance | `db_stores/vectorstore_finance` |
| Legal   | `db_stores/vectorstore_legal`   |

---

## 📄 Screenshots

*(To be added)*

## 📹 Demo Video

*(To be added)*

---

## 🌐 Badges

* Python:&#x20;
* Docker:&#x20;

---

## 👉 Contributing

Want to contribute or suggest improvements? Feel free to raise issues or submit pull requests.

---

## 🙏 Acknowledgements

* [LangChain](https://github.com/langchain-ai/langchain)
* [OpenAI](https://openai.com)
* [Google Generative AI](https://ai.google/discover/generative-ai/)
* [Streamlit](https://streamlit.io)
* [FastAPI](https://fastapi.tiangolo.com)

---

## ✨ License

MIT — feel free to use and modify with attribution.
