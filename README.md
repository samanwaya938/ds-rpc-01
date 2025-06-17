# 📂 Multiple Role-Based Document Retrieval with LLMs

## 🚀 Overview

This project is a **Role-Based Retrieval-Augmented Generation (RAG) System** built with **FastAPI**, **Streamlit**, and **LangChain**, leveraging **OpenAI** and **Google GenAI APIs**. It enables users to log in with a specific role and retrieve relevant answers based only on the data allowed for that role.

### 🔹 Use Case

* ✉️ An HR personnel can retrieve HR-specific data.
* 🏢 A marketing manager can only access marketing-related information.
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
├── resources/               # All the role specific custom data 
│
├── requirements.txt         # Project dependencies
├── Dockerfile               # Docker configuration
├── .env                     # API keys (not included in repo)
├── .dockerignore            # Docker ignore rules
├── setup.py                 # Project Setup File
├── README.md                # Instruction file
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

To create vectore database run the store.py file using the following command. It has to be run only once. Once run the db_stores folder will be created in the root directory and it will be conatains all the role specific vector store.
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
docker pull samanwaya/rag-multirole
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
   
These are sample data to login and test

   * ID: `alice`
   * Password: `1234`
   * Role: `engineering`
---  
   * ID: `bob`
   * Password: `abcd`
   * Role: `hr`
---  
   * ID: `charlie`
   * Password: `xyz`
   * Role: `finance`
---  
   * ID: `harry`
   * Password: `1122`
   * Role: `general`
--- 
   * ID: `jack`
   * Password: `xxyyzz`
   * Role: `marketing`
---
2. ***Ask Questions***

    After successful login, you can ask role-specific questions using the chat input. The application uses the relevant vectorstore for the selected role.

   Example:

       "What are the onboarding steps for new employees?"

3. ***Behind the Scenes***

   * Role general loads vectorstore_general
   * Role finance loads vectorstore_finance
   * Stored vector DBs are in db_stores/

---

## 📈 Example Roles & Vectorstores

| Role    | Folder Path                     |
| ------- | ------------------------------- |
| HR      | `db_stores/vectorstore_hr`      |
| Finance | `db_stores/vectorstore_finance` |
| General | `db_stores/vectorstore_general`   |

---

## 📄 Screenshots
### Login Page
![image](https://github.com/user-attachments/assets/fd6647e7-c238-4ebb-a8fc-bfb356770262)

### Chat Page
![image](https://github.com/user-attachments/assets/40179358-2029-4991-bd01-ce0c2e0cb436)


## 📹 Demo Video

*(To be added)*

---

## 📛 Badges

* Python: 3.10.8
* Docker: Image available on DockerHub

---

## 👉 Contributing

Want to contribute or suggest improvements? Feel free to raise issues or submit pull requests.

---

## 🙏 Acknowledgements

* [LangChain](https://github.com/langchain-ai/langchain)
* [OpenAI](https://openai.com)
* [Google Generative AI](https://aistudio.google.com/)
* [Streamlit](https://streamlit.io)
* [FastAPI](https://fastapi.tiangolo.com)

---

## ✨ License

MIT — feel free to use and modify with attribution.
