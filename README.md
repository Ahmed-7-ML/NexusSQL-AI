
# 🗄️ Enterprise Text-to-SQL AI Engine

> An enterprise-grade GenAI platform that bridges non-technical business users and relational databases — translating plain English or Arabic questions into optimized, executable SQL queries with real-time results.

Powered by **Gemini 2.5 Flash** (2026 Google GenAI SDK),  **Streamlit** , and a robust **Role-Based Access Control (RBAC)** security layer.

---

## 📸 Application Previews

### 1. Secure Login Gateway

Authentication enforced at startup — verifies identity and maps user permissions before granting access.

![Authentication Gateway](login.png)

### 2. Admin Workspace (Full Access)

Administrators get read, write, update, and delete capabilities, including a live row-preview slider and direct database modification panels.

![Admin Dashboard](admin.png)

### 3. Standard User Workspace (Read-Only)

Employees access a restricted analytical viewport. All destructive operations are blocked at both the UI and LLM prompt layers.

![User Dashboard](user.png)

---

## ✨ Key Features

* **Natural Language → SQL:** Converts complex English/Arabic questions into optimized SQL commands via Gemini 2.5 Flash.
* **Dual-Layer RBAC Security:** If a standard user injects phrases like  *"drop table"* , strict LLM system prompts override execution and surface a `🚫 SECURITY VIOLATION` error.
* **Decoupled Modular Architecture:** Business logic is cleanly separated into `src/auth.py`, `src/ai_engine.py`, and `src/db_manager.py` for maintainability and easy scaling.
* **Admin CRUD Operations:** Admins can insert records, cascade-delete entries, and perform safe upsert score adjustments directly from the UI.
* **Dynamic Live Previews:** A live slider lets admins adjust table row limits (`LIMIT {n}`) on the fly, rendered as clean Pandas DataFrames.
* **Multi-Table Relational Schema:** Supports `FOREIGN KEY` constraints and cross-table `JOIN` operations out of the box.

---

## 🏢 Business Value

In enterprise environments, data is locked inside massive databases that non-technical decision-makers can't access without a data analyst. This platform achieves **Data Democratization** — letting anyone in the organization "text their database" in plain language for instant, secure business insights.

---

## 🏗️ System Architecture

```
[User Input]          Plain-text question + session role (User / Admin)
       ↓
[AI Engine]           Embeds schema context + dynamic RBAC guardrails
(src/ai_engine.py)
       ↓
[Gemini 2.5 Flash]    Translates input into a sanitized, executable SQL query
       ↓
[DB Manager]          Executes query securely against Faculty.db (SQLite3)
(src/db_manager.py)
       ↓
[Streamlit UI]        Wraps results in a DataFrame and renders the dashboard
```

---

## 🗄️ Database Schema

### `Students` Table

| Column      | Type        | Attributes                 |
| :---------- | :---------- | :------------------------- |
| `Id`      | INTEGER     | PRIMARY KEY, AUTOINCREMENT |
| `Name`    | VARCHAR(25) | UNIQUE, NOT NULL           |
| `DoB`     | TEXT        | Date of Birth              |
| `Section` | INTEGER     | Class Section Number       |

### `Marks` Table

| Column        | Type        | Attributes                     |
| :------------ | :---------- | :----------------------------- |
| `MarkId`    | INTEGER     | PRIMARY KEY, AUTOINCREMENT     |
| `StudentId` | INTEGER     | FOREIGN KEY →`Students(Id)` |
| `Subject`   | VARCHAR(50) | Subject Title                  |
| `Score`     | INTEGER     | Exam Grade                     |

---

## 🔒 Production Scaling & Security Roadmap

### 1. On-Premises Local LLM (Zero Data Leakage)

To comply with GDPR/HIPAA, the engine is architected to cut over from Cloud APIs to **locally hosted LLMs** (e.g., Llama 3.1, Qwen, Mistral) via **Ollama** or **vLLM** — ensuring no company data ever leaves the internal firewall.

### 2. Role-Based Access Control (RBAC)

| Role                    | Permissions                                                                                      |
| :---------------------- | :----------------------------------------------------------------------------------------------- |
| **Admin**         | Full read, write, update, delete + schema-level operations                                       |
| **Standard User** | Strict read-only via SQL Views;`DROP`,`DELETE`,`TRUNCATE`,`ALTER`blocked at prompt level |

### 3. Enterprise Database Migration

The `src/db_manager.py` driver abstraction allows a one-line connection string swap from SQLite3 to  **PostgreSQL** ,  **MySQL** ,  **Microsoft SQL Server** , or **Amazon RDS** — zero changes required in the UI layer.

---

## 🚀 Getting Started

### Prerequisites

* Python `^3.10` or `^3.11`
* [Poetry](https://python-poetry.org/) installed
* Google AI Studio API key — [get one here](https://aistudio.google.com/)

### Installation

**1. Clone the repository:**

```bash
git clone https://github.com/your-username/text-to-sql-ai-engine.git
cd text-to-sql-ai-engine
```

**2. Install dependencies:**

```bash
poetry install
```

**3. Configure your API key:**

Create a `.env` file in the project root:

```
GEMINI_API_KEY=AIzaSyYourActualAPIKeyHere
```

**4. Initialize the database:**

```bash
poetry run python db_setup.py
```

**5. Launch the app:**

```bash
poetry run streamlit run app.py
```

---

## 🛠️ Tech Stack

| Layer            | Technology                         |
| :--------------- | :--------------------------------- |
| Core Language    | Python 3.11                        |
| GenAI SDK        | `google-genai`(2026 Release)     |
| Foundation Model | Gemini 2.5 Flash                   |
| Web Interface    | Streamlit (Wide Layout + Dark CSS) |
| Data Engineering | Pandas & SQLite3                   |
| Dependency Mgmt  | Poetry & Pyenv                     |

---

## 📝 License

Distributed under the [MIT License](https://claude.ai/chat/LICENSE).

---

*Developed by **Ahmed Akram Amer** — Triple AI Portfolio Systems.*
