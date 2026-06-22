# NexusSQL AI System Architecture

## Overview
NexusSQL AI is an enterprise-grade Generative AI platform that bridges non-technical business users and relational databases. It translates plain English or Arabic questions into optimized, executable SQL queries with real-time results using Google's Gemini 2.5 Flash model. The application features a robust Role-Based Access Control (RBAC) layer to secure data modifications.

## System Architecture Diagram

```mermaid
flowchart TD
    subgraph UI ["🖥️ Streamlit Frontend (app.py)"]
        Login["Login Screen (src/auth.py)"]
        Dashboard["Main Dashboard"]
        AdminView["Admin Workspace\n(src/admin_view.py)"]
        UserView["User Workspace\n(src/user_view.py)"]
        Input["Natural Language Query Input"]
    end

    subgraph Core ["⚙️ Core Logic"]
        AIEngine["AI Engine & RBAC Guardrails\n(src/ai_engine.py)"]
        DBManager["Database Manager\n(src/db_manager.py)"]
    end

    subgraph External ["🌐 External APIs"]
        Gemini["Google Gemini 2.5 Flash\n(Google GenAI SDK)"]
    end

    subgraph Data ["🗄️ Database"]
        DB[(SQLite3: Faculty.db)]
        UsersT[Users Table]
        StudentsT[Students Table]
        MarksT[Marks Table]
    end

    %% Flow Details
    Login --"Verifies Credentials"--> UsersT
    Login --"Routes by Role"--> Dashboard
    
    Dashboard --"If Admin"--> AdminView
    Dashboard --"If User"--> UserView
    
    AdminView -.->|"Direct Data Operations\n(Insert, Update, Delete)"| DBManager
    UserView -.->|"Read-Only Schema View"| Dashboard
    
    Dashboard --> Input
    Input --"Question + Role Context"--> AIEngine
    
    AIEngine --"Constructs Prompt\n(Enforces Read-Only for Users)"--> Gemini
    Gemini --"Returns SQL Query\n(or FORBIDDEN)"--> AIEngine
    
    AIEngine --"Passes Valid SQL"--> DBManager
    DBManager --"Executes SQL"--> DB
    
    DB --"Returns Records"--> DBManager
    DBManager --"Pandas DataFrame"--> Dashboard
    
    %% DB Structure Link
    DB --- UsersT
    DB --- StudentsT
    DB --- MarksT
    StudentsT -.- MarksT

    %% Styling Elements for Visual Appeal
    classDef ui fill:#E1F5FE,stroke:#0288D1,stroke-width:2px,color:#01579B,rx:8,ry:8
    classDef core fill:#EDE7F6,stroke:#5E35B1,stroke-width:2px,color:#311B92,rx:8,ry:8
    classDef external fill:#E8F5E9,stroke:#388E3C,stroke-width:2px,color:#1B5E20,rx:8,ry:8
    classDef db fill:#FFF8E1,stroke:#FFA000,stroke-width:2px,color:#FF6F00,rx:8,ry:8
    classDef dbFile fill:#FFEBEE,stroke:#D32F2F,stroke-width:3px,color:#B71C1C,rx:8,ry:8

    class Login,Dashboard,AdminView,UserView,Input ui
    class AIEngine,DBManager core
    class Gemini external
    class UsersT,StudentsT,MarksT db
    class DB dbFile
```

## Component Breakdown

### 1. Frontend & User Interface (`app.py`, `admin_view.py`, `user_view.py`)
- **`app.py`**: The main entry point of the Streamlit application. It handles session state, coordinates the login flow, routes users based on their role, and displays the query input and results.
- **`src/auth.py`**: Validates the user's credentials against the `Users` table in the database and assigns a session role (`admin` or `user`).
- **`src/admin_view.py`**: Provides full access capabilities. Admins can view live schema limits and perform direct database modifications (Insert, Update, Delete) via UI controls without writing SQL.
- **`src/user_view.py`**: Restricts the user to a secure read-only mode, providing sample database views for reference while relying entirely on the AI for querying.

### 2. AI Engine & Security (`src/ai_engine.py`)
- Acts as the translation layer between plain text and SQL.
- Constructs a highly contextual prompt for **Gemini 2.5 Flash** containing the target database schema (`Students` and `Marks` tables).
- **Role-Based Access Control (RBAC):** Dynamically alters the instructions based on the user's role. If a `user` attempts a destructive command (e.g., `DROP`, `DELETE`), the LLM is instructed to bypass generation and return a strict `FORBIDDEN` flag.

### 3. Database Management (`src/db_manager.py` & `db.py`)
- **`db.py`**: A one-time setup script that drops old tables, creates the schemas (`Students`, `Marks`, `Users`), and seeds the database with initial records to support immediate testing.
- **`src/db_manager.py`**: A centralized connection manager that receives raw SQL queries, connects to `Faculty.db`, executes the operations securely, and returns tuples of data back to the Streamlit frontend.

### Data Flow Execution
1. A user asks: *"Give me the marks of Ahmed Akram."*
2. The UI sends this to `ai_engine.py` along with the user's role.
3. The engine builds a prompt mapping schema relationships and sends it to **Gemini**.
4. Gemini translates this into: `SELECT Marks.Subject, Marks.Score FROM Marks JOIN Students ON ...`
5. The UI calls `db_manager.py` to execute the SQL.
6. The returned data is wrapped in a Pandas DataFrame and rendered on the Streamlit dashboard.
