import sqlite3
import os



class DatabaseManager():
    def __init__(self):

        self.conn = sqlite3.connect("trades.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                assets TEXT,
                direction TEXT,
                session TEXT,
                lot_size REAL,
                entry_price REAL,
                exit_price REAL,
                sl REAL,
                rr REAL,
                is_closed INTEGER,
                outcome TEXT,
                profit REAL,
                broker TEXT,
                image_paths TEXT,
                comment TEXT,
                errors TEXT
            )
        ''')
        self.conn.commit()
        
        
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS assets (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT UNIQUE
                            )
                            ''')
        self.cursor.execute('SELECT COUNT(*) FROM assets')
        if self.cursor.fetchone()[0] == 0:
            default_assets = [("EUR/USD",), ("GBP/USD",), ("EUR/JPY",), ("EUR/CAD",)]
            self.cursor.executemany('INSERT INTO assets (name) VALUES (?)', default_assets)
            self.conn.commit()

        
    def get_all_assets(self):
        self.cursor.execute('SELECT id, name FROM assets ORDER BY name ASC')
        return self.cursor.fetchall()

    def add_asset(self, name):
        try:
            self.cursor.execute('INSERT INTO assets (name) VALUES (?)', (name,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def delete_asset(self, asset_id):
        self.cursor.execute('DELETE FROM assets WHERE id = ?', (asset_id,))
        self.conn.commit()



        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS wallet (id INTEGER PRIMARY KEY, balance REAL)
                            ''')
        self.cursor.execute('SELECT COUNT(*) FROM wallet')
        count = self.cursor.fetchone()[0]

        if count == 0:
            self.cursor.execute('INSERT INTO wallet (balance) VALUES (0.0)')
        self.conn.commit()

    

    def edit_asset(self, asset_id, new_name):
        try:
            self.cursor.execute('UPDATE assets SET name = ? WHERE id = ?', (new_name, asset_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False





    def get_total_trades_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM trades")
        return self.cursor.fetchone()[0]
    
    def get_win_trades_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM trades WHERE outcome = 'Win'")
        return self.cursor.fetchone()[0]
    
    def get_lose_trades_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM trades WHERE outcome = 'Lose'")
        return self.cursor.fetchone()[0]






    def get_total_lots(self):
        self.cursor.execute("SELECT SUM(lot_size) FROM trades")
        result = self.cursor.fetchone()[0]
        return round(result, 2) if result else 0.0




    def edit_trade(self, trade_id, date, assets, direction, session, lot_size, entry_price, exit_price, sl, rr, is_closed, outcome, profit, broker):
        self.cursor.execute('''
                            UPDATE trades
                            SET date = ?, assets = ?, direction = ?, session = ?, lot_size = ?, entry_price = ?, exit_price = ?, sl = ?, rr = ?, is_closed = ?, outcome = ?, profit = ?, broker = ?
                            WHERE id = ?
                            ''',(date, assets, direction, session, lot_size, entry_price, exit_price, sl, rr, is_closed, outcome, profit, broker, trade_id))
        self.conn.commit()
        


    def get_balance(self):
        self.cursor.execute("SELECT balance FROM wallet")
        balance = self.cursor.fetchone()[0]
        return balance
    


    def update_balance(self, new_balance):
        self.cursor.execute("UPDATE wallet SET balance = ?", (new_balance,))
        self.conn.commit()





    def add_trade(self, date, assets, direction, session, lot_size, entry_price, exit_price, sl, rr, is_closed, outcome, profit, broker, image_paths):
        self.cursor.execute('''
            INSERT INTO trades (date, assets, direction, session, lot_size, entry_price, exit_price, sl, rr, is_closed, outcome, profit, broker, image_paths)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (date, assets, direction, session, lot_size, entry_price, exit_price, sl, rr, is_closed, outcome, profit, broker, image_paths))
        self.conn.commit()
        return self.cursor.lastrowid



    def get_all_trades(self):
        self.cursor.execute("SELECT * FROM trades")
        rows = self.cursor.fetchall()
        return rows









    def delete_trade(self, trade_id):
        self.cursor.execute("DELETE FROM trades WHERE id=?", (trade_id,))
        self.conn.commit()


    def get_trade_by_id(self, trade_id):
        self.cursor.execute("SELECT * FROM trades WHERE id=?", (trade_id,))
        return self.cursor.fetchone()


    def update_trade_details(self, trade_id, comment, errors):
        self.cursor.execute(
                """
                UPDATE trades
                SET comment = ?, errors = ?
                WHERE id = ?
                """, (comment, errors, trade_id))
        self.conn.commit()
    








    def quick_update_result(self, trade_if, is_closed, outcome, profit):
        self.cursor.execute("""
                            UPDATE trades
                            SET is_closed = ?, outcome = ?, profit = ?
                            WHERE id = ?
                            """, (is_closed, outcome, profit, trade_if))
        self.conn.commit()



