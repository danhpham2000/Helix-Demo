# Title:
Build the AI-powered recruiting outreach that combines chatbot and workspace

### Description:
The main purpose is to generate outreach with all the steps, user can edit dynamically or ask AI agent to do that

### Frontend:
- React, TypeScript, CSS 

### Backend:
- Python, Flask: Build API server endpoints

### Databases:
- PostgreSQL: Store user preferences, and sequence generation

### AI infrastructure
- OpenAI: for API_KEY
- LangGraph: building workflow of the agents
- LangSmith: for debugging and tracing
- Pinecone (not implement): For storing relevant information, chat history


### How to run
- First, clone the repository
```
git clone https://github.com/danhpham2000/Helix-Demo.git
```

- Second, navigate to each folder


#### Frontend
```
bun install 
```
or 

```
npm install
```
Then, run
```
bun run dev
```

or 

```
npm run dev
```

#### Backend 
```
pip3 install -r requirements.txt
```

Then,
```
flask --debug run
```
### Note:
- .env file to store all credential database# Helix-Demo
