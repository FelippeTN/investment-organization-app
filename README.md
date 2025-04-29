# Investment Organization App

Este projeto é uma aplicação Django para gerenciamento de investimentos.


### 1. Crie um ambiente virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o banco de dados

Por padrão, o projeto pode usar SQLite (caso deseje usar PostgreSQL, edite o `settings.py`).

---

### 4. Aplique as migrações

```bash
python manage.py migrate
```

### 5. Rode o servidor de desenvolvimento

```bash
python manage.py runserver
```

