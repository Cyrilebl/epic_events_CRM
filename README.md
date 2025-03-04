![Epic Events banner](images/epic-events-banner.png)

## ⚙️ Install Project

1. Clone the repository

```bash
git clone https://github.com/Cyrilebl/epic_events_CRM.git
cd epic_events_CRM
```

2. Create and activate the virtual environment

- **Windows**

```bash
python -m venv env
env\Scripts\activate
```

- **macOS/Linux**

```bash
python3 -m venv env
source env/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🗄️ Initialize Database

1. Install PostgreSQL

- 🔗 [Download](https://www.postgresql.org/download/)

2. Start PostgreSQL

```bash
sudo systemctl start postgresql
```

3. Check if PostgreSQL is Running

```bash
sudo systemctl status postgresql
```

4. Connect to PostgreSQL

```bash
psql -U postgres -W
```

5. Create a New Database

```bash
CREATE DATABASE my_database;
```

6. Connect to the Database

```bash
\c my_database
```

7. Exit psql

```bash
\q
```

## 🔑 Configure Environment Variables

📄 Create a `.env` file in the project root and add:

```bash
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=my_database
SECRET_KEY=your_secret_key
```

## 🏗 Create Default Models

- Create user roles

```bash
python cli.py create-role
```

- Create a superuser

```bash
python cli.py create-superuser
```

## 🚀 Start the CRM

```bash
python main.py
```

### Terminal Colors

| Message Type       | Color      |
| ------------------ | ---------- |
| Prompt text        | 🟣 Magenta |
| User input prompts | 🔵 Blue    |
| Success messages   | ✅ Green   |
| Errors             | ❌ Red     |
| System status      | 🟡 Yellow  |
