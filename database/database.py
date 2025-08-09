import aiosqlite

DB_NAME = 'database.db'


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
        """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                role TEXT,
                bank_card INTEGER,
                level INTEGER,
                rank TEXT,
                balance INTEGER,
                task_compl INTEGER
            )
        """)

        # table - tasks
        await db.execute(
        """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                status TEXT,
                priority TEXT,
                role TEXT,
                total_price INTEGER,
                total_xp INTEGER,
                result_url TEXT
            )
        """)

        await db.execute(
        """
            CREATE TABLE IF NOT EXISTS user_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_id INTEGER NOT NULL,
                status TEXT,
                result_url TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
            )
        """)

        await db.commit()


# додавання нового користувача
async def add_user(user_id, username, role, bank_card):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT INTO users (user_id, username, role, bank_card) VALUES (?, ?, ?, ?)',
            (user_id, username, role, bank_card)
        )
        await db.commit()

# перегляд інформації про користувача
async def get_user_info(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        c = await db.execute(
            'SELECT user_id, username, role, bank_card, current_task_id, level, rank, balance, task_compl FROM users WHERE user_id = ?', 
            (user_id,)
        )
        row = await c.fetchone()
        return row

# редагування інформації про користувача
async def edit_user_info(username, role, bank_card, user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'UPDATE users SET username = ?, role = ?, bank_card = ? WHERE user_id = ?',
            (username, role, bank_card, user_id)
        )
        await db.commit()

# додавання завдання в бд
async def add_tasks(title, description, status, priority, role, total_price, total_xp):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT INTO tasks (title, description, status, priority, role, total_price, total_xp) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (title, description, status, priority, role, total_price, total_xp)
        )
        await db.commit()

# отримання всіх завдань з бд
async def get_all_tasks():
    async with aiosqlite.connect(DB_NAME) as db:
        c = await db.execute(
            'SELECT id, title, description, status, priority, role, total_price, total_xp FROM tasks'
        )
        row = await c.fetchall()
        return row

# оновлення всіх завдань в таблиці
async def update_all_tasks(title, description, priority, total_price, total_xp, task_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'UPDATE tasks SET title = ?, description = ?, priority = ?, total_price = ?, total_xp = ? WHERE id = ?',
            (title, description, priority, total_price, total_xp, task_id)
        )
        await db.commit()

# оновлення рядка status в БД
async def update_status(task_id, task_status):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'UPDATE tasks SET status = ? WHERE id = ?', (task_status, task_id)
        )
        await db.commit()

# запис завдань які взяв користувач
async def user_tasks(user_id, task_id, status, result_url):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT INTO user_tasks (user_id, task_id, status, result_url) VALUES (?, ?, ?, ?)',
            (user_id, task_id, status, result_url)
        )
        await db.commit()

# отримання всіх завдань від користувача які він взяв
async def user_get_tasks(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        c = await db.execute(
            'SELECT tasks.id, tasks.title, tasks.description, tasks.status, tasks.role, tasks.total_price, tasks.total_xp, user_tasks.status FROM user_tasks JOIN tasks ON user_tasks.task_id = tasks.id WHERE user_tasks.user_id = ?', 
            (user_id,)
        )
        row = await c.fetchall()
        return row