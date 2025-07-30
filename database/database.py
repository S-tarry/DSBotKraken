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
                current_task_id INTEGER,
                level INTEGER,
                rank TEXT,
                balance INTEGER,
                task_compl INTEGER,
                FOREIGN KEY (current_task_id) REFERENCES tasks (id) ON DELETE CASCADE
            )
        """)

        # table - tasks
        await db.execute(
        """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subtasks_id INTEGER NOT NULL,
                description TEXT,
                total_price INTEGER,
                points INTEGER,
                total_xp INTEGER,
                FOREIGN KEY (subtasks_id) REFERENCES subtasks (id) ON DELETE CASCADE
            )
        """)

        # table - subtasks
        await db.execute(
        """
            CREATE TABLE IF NOT EXISTS subtasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                price INTEGER,
                xp INTEGER
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