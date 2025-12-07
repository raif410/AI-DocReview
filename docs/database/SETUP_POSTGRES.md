# 🐘 Настройка PostgreSQL

## 📋 Быстрый старт

### Вариант 1: Docker (рекомендуется)

Если у вас установлен Docker:

```bash
# Запустите PostgreSQL через Docker Compose
docker-compose up -d postgres

# Проверьте статус
docker-compose ps
```

PostgreSQL будет доступен на `localhost:5432` с настройками:
- Пользователь: `postgres`
- Пароль: `postgres`
- База данных: `docreview`

### Вариант 2: Локальная установка

#### Windows

1. **Скачайте PostgreSQL:**
   - https://www.postgresql.org/download/windows/
   - Или через Chocolatey: `choco install postgresql`

2. **Установите PostgreSQL:**
   - Следуйте инструкциям установщика
   - Запомните пароль для пользователя `postgres`

3. **Запустите службу:**
   ```powershell
   # Через службы Windows
   services.msc
   # Найдите "postgresql" и запустите
   
   # Или через PowerShell
   Start-Service postgresql-x64-15  # Версия может отличаться
   ```

4. **Создайте базу данных:**
   ```bash
   # Подключитесь к PostgreSQL
   psql -U postgres
   
   # Создайте базу данных
   CREATE DATABASE docreview;
   
   # Выйдите
   \q
   ```

5. **Обновите `.env` файл:**
   ```env
   DATABASE_URL=postgresql://postgres:ВАШ_ПАРОЛЬ@localhost:5432/docreview
   ```

#### Linux

```bash
# Установка
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Запуск службы
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Создание базы данных
sudo -u postgres psql
CREATE DATABASE docreview;
\q
```

#### macOS

```bash
# Установка через Homebrew
brew install postgresql@15
brew services start postgresql@15

# Создание базы данных
createdb docreview
```

---

## ✅ Проверка установки

### 1. Проверьте, что PostgreSQL запущен

**Windows:**
```powershell
Get-Service -Name "*postgres*"
```

**Linux/macOS:**
```bash
sudo systemctl status postgresql  # Linux
brew services list  # macOS
```

### 2. Проверьте подключение

```bash
psql -h localhost -U postgres -d docreview
```

Если подключение успешно - вы увидите приглашение `postgres=#`

### 3. Инициализируйте базу данных

```bash
python scripts/init_db.py
```

Должно вывести:
```
✅ Database initialized successfully!
Tables created: ['review_tasks', 'issues', 'review_results']
```

### 4. Проверьте структуру БД

```bash
python scripts/tools/view_db_structure.py
```

---

## 🔧 Настройка подключения

### Обновление `.env` файла

Создайте или обновите файл `.env` в корне проекта:

```env
# PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/docreview

# Формат: postgresql://username:password@host:port/database
```

### Проверка настроек

```bash
python -c "from src.config import settings; print(settings.database_url)"
```

---

## 🚀 После настройки

После успешной настройки PostgreSQL:

1. **Инициализируйте БД:**
   ```bash
   python scripts/init_db.py
   ```

2. **Проверьте структуру:**
   ```bash
   python scripts/tools/view_db_structure.py
   ```

3. **Проверьте данные:**
   ```bash
   python scripts/tools/view_db_data.py
   ```

---

## ❓ Решение проблем

### Ошибка: "Connection refused"

**Причина:** PostgreSQL не запущен

**Решение:**
- Windows: Запустите службу через `services.msc`
- Linux: `sudo systemctl start postgresql`
- macOS: `brew services start postgresql@15`
- Docker: `docker-compose up -d postgres`

### Ошибка: "password authentication failed"

**Причина:** Неправильный пароль в `DATABASE_URL`

**Решение:** Обновите пароль в `.env` файле

### Ошибка: "database does not exist"

**Причина:** База данных не создана

**Решение:**
```bash
createdb docreview
# Или через psql:
psql -U postgres
CREATE DATABASE docreview;
```

---

## 📚 Дополнительная информация

- [Официальная документация PostgreSQL](https://www.postgresql.org/docs/)
- [Docker Hub - PostgreSQL](https://hub.docker.com/_/postgres)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Решение проблем

