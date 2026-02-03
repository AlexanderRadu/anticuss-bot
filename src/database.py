import json
import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        with self.connection:
            self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS groups_info (
                                                                           chat_id INTEGER PRIMARY KEY,
                                                                           group_name TEXT,
                                                                           mat_counter INTEGER DEFAULT 0,
                                                                           ban_list TEXT DEFAULT '[]',
                                                                           bot_switch INTEGER DEFAULT 1,
                                                                           ban_words TEXT DEFAULT '[]'
                                )
                                """)

    def add_group(self, chat_id, group_name):
        with self.connection:
            self.cursor.execute("SELECT chat_id FROM groups_info WHERE chat_id = ?", (chat_id,))
            if not self.cursor.fetchone():
                self.cursor.execute(
                    "INSERT INTO groups_info (chat_id, group_name, mat_counter, ban_list, bot_switch, ban_words) VALUES (?, ?, 0, '[]', 1, '[]')",
                    (chat_id, group_name)
                )
            else:
                self.cursor.execute("UPDATE groups_info SET bot_switch = 1 WHERE chat_id = ?", (chat_id,))

    def get_group_data(self, chat_id):
        self.cursor.execute("SELECT * FROM groups_info WHERE chat_id = ?", (chat_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "chat_id": row[0],
                "group_name": row[1],
                "mat_counter": row[2],
                "ban_list": json.loads(row[3]),
                "bot_switch": row[4],
                "ban_words": json.loads(row[5])
            }
        return None

    def update_ban_list(self, chat_id, ban_list):
        with self.connection:
            self.cursor.execute("UPDATE groups_info SET ban_list = ? WHERE chat_id = ?", (json.dumps(ban_list), chat_id))

    def update_ban_words(self, chat_id, ban_words):
        with self.connection:
            self.cursor.execute("UPDATE groups_info SET ban_words = ? WHERE chat_id = ?", (json.dumps(ban_words), chat_id))

    def set_bot_switch(self, chat_id, status):
        with self.connection:
            self.cursor.execute("UPDATE groups_info SET bot_switch = ? WHERE chat_id = ?", (status, chat_id))

    def increment_mat_counter(self, chat_id):
        with self.connection:
            self.cursor.execute("UPDATE groups_info SET mat_counter = mat_counter + 1 WHERE chat_id = ?", (chat_id,))

    def get_stats(self):
        self.cursor.execute("SELECT mat_counter FROM groups_info")
        all_counts = [row[0] for row in self.cursor.fetchall()]
        total_mat = sum(all_counts)

        import pandas as pd
        df = pd.read_sql_query("SELECT group_name, mat_counter FROM groups_info ORDER BY mat_counter DESC LIMIT 10", self.connection)
        return total_mat, df
