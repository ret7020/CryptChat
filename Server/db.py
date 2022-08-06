class DB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def auth_client(self, user_id, user_pass_hash):
        data = self.cursor.execute("SELECT * FROM `users` WHERE `id` = :user_id AND `password` = :pass_hash", {"pass_hash": user_pass_hash, "user_id": user_id}).fetchall()
        return data
    
    def get_user_convs(self, user_id):
        data = self.cursor.execute("SELECT `chat_id` FROM `chats_users` WHERE `user_id` = :user_id", {"user_id": user_id}).fetchall()
