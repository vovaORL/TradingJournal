import customtkinter as ctk
from tkinter import messagebox
from language_manager import LanguageManager
from ui_header import HeaderFrame, SettingsWindow
from ui_actions import ActionsFrame, AddTradeWindow, EditTradeWindow, ManageAssetsWindow
from ui_table import TradeFrame
from ui_footer import FooterFrame
from db_manager import DatabaseManager
import os


class TradingApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        

        self.db = DatabaseManager()

        self.lang_manager = LanguageManager()
        self.current_lang = self.lang_manager.current_lang


        self.geometry("1000x600")
        self.title("Trading Journal")
        self.minsize(400,300)

        self.setup_layout()
        self.protocol("WM_DELETE_WINDOW", self.close_entrire_app)

        self.trades_frame.load_trades()



    def close_entrire_app(self):
        os._exit(0)


    def setup_layout(self):
        self.settings_frame = HeaderFrame(self)
        self.settings_frame.pack(fill = "x", padx = 5, pady = 10)

        self.main_frame = ActionsFrame(self)
        self.main_frame.pack(fill = "x", padx = 5, pady = 10)

        self.trades_frame = TradeFrame(self)
        self.trades_frame.pack(fill = "both", expand = True, padx = 5, pady = 10)

        self.footer_frame = FooterFrame(self)
        self.footer_frame.pack(fill = "x", padx = 5, pady = 10)
        

    
    def open_add_trade_window(self):
        if hasattr(self, "add_window") and self.add_window.winfo_exists():
            self.add_window.focus()
        else:
            self.add_window = AddTradeWindow(self)

    

    def open_edit_trade_window(self, trade_id):
        if hasattr(self, "edit_window") and self.edit_window.winfo_exists():
            self.edit_window.destroy()
        self.edit_window = EditTradeWindow(self, trade_id)



    def save_edit_trade(self, trade_id, val_date, val_direction, val_assets, val_session, val_lot_size, val_entry_price, val_exit_price, val_sl, val_rr, val_is_closed, val_outcome, val_profit, val_broker, val_image_paths):
        if val_is_closed == 1 and not val_outcome:
            messagebox.showerror(self.get_text("messagebox", "messagebox_error_title"), self.get_text("messagebox", "messagebox_error"))
            return

        try:
            val_lot_size = float(val_lot_size)
            val_entry_price = float(val_entry_price)
            if val_exit_price != 0.0 and val_exit_price != "":
                val_exit_price = float(val_exit_price)
        except ValueError:
            messagebox.showerror(self.get_text("messagebox", "messagebox_error_title"), self.get_text("messagebox", "messagebox_error"))
            return

        self.db.edit_trade(trade_id, val_date, val_assets, val_direction, val_session, val_lot_size, val_entry_price, val_exit_price, val_sl, val_rr, val_is_closed, val_outcome, val_profit, val_broker)

        self.trades_frame.refresh_text()
        self.update_statistics()
        if hasattr(self, "edit_window") and self.edit_window.winfo_exists():
            self.edit_window.destroy()


    



    def open_settings_window(self):
        if hasattr(self, "settings_win") and self.settings_win.winfo_exists():
            self.settings_win.focus()
        else:
            self.settings_win = SettingsWindow(self)

    def open_manage_assets_window(self):
        if hasattr(self, "manage_assets_win") and self.manage_assets_win.winfo_exists():
            self.manage_assets_win.focus()
        else:
            self.manage_assets_win = ManageAssetsWindow(self)

       

        
    def save_trade(self, val_date, val_direction, val_assets, val_session, val_lot_size, val_entry_price, val_exit_price, val_sl, val_rr, val_is_closed, val_outcome, val_profit, val_broker, val_image_paths):
       
        if not val_date.strip() or not val_direction.strip() or not val_assets.strip() or not val_lot_size.strip() or not val_entry_price.strip():
            messagebox.showerror(self.get_text("messagebox", "messagebox_error_title"), self.get_text("messagebox", "messagebox_error"))
            return
        try:
            val_lot_size = float(val_lot_size)
            val_entry_price = float(val_entry_price)
            if val_lot_size <= 0 or val_entry_price <= 0:
                messagebox.showerror(self.get_text("messagebox", "messagebox_error_title"), self.get_text("messagebox", "messagebox_error"))
                return
        except ValueError:
            messagebox.showerror(self.get_text("messagebox", "messagebox_error_title"), self.get_text("messagebox", "messagebox_error"))
            return

        if val_exit_price != 0.0 and val_exit_price != "":
            try:
                val_exit_price = float(val_exit_price)
            except ValueError:
                messagebox.showerror(self.get_text("messagebox", "messagebox_error_title"), self.get_text("messagebox", "messagebox_error"))
                return
        else:
            val_exit_price = 0.0


        if val_is_closed == 1 and not val_outcome:
            messagebox.showerror(self.get_text("messagebox", "messagebox_error_title"), self.get_text("messagebox", "messagebox_error"))
            return


        new_id = self.db.add_trade(val_date, val_assets, val_direction, val_session, val_lot_size, val_entry_price, val_exit_price, val_sl, val_rr, val_is_closed, val_outcome, val_profit, val_broker, val_image_paths)
        self.trades_frame.add_row(new_id, val_date, val_assets, val_direction, val_lot_size, val_entry_price, val_exit_price, val_sl, val_rr, val_is_closed, val_outcome, val_profit, val_broker)




        self.update_statistics()






    def update_statistics(self):

        total_trades = self.db.get_total_trades_count()
        wins = self.db.get_win_trades_count()

        loses = self.db.get_lose_trades_count() 

        if total_trades == 0:
            winrate = 0
        else:
            winrate = (wins/ total_trades) * 100
    
        total_lots = self.db.get_total_lots()
        

        self.footer_frame.update_display(total_trades, winrate, wins, loses, total_lots)


    def refresh_ui(self):

        if hasattr(self, "main_frame"):
            self.main_frame.refresh_text()


        if hasattr(self, "settings_frame"):
            self.settings_frame.refresh_text()

        if hasattr(self, "trades_frame"):
            self.trades_frame.refresh_text()

        if hasattr(self, "footer_frame"):
            self.footer_frame.refresh_text()

        if hasattr(self, "settings_frame"):
            self.settings_frame.refresh_text()

        if hasattr(self, "settings_win") and self.settings_win.winfo_exists():
            self.settings_win.refresh_text()

        self.update_statistics()



    def get_text(self, category, key):
        return self.lang_manager.get_text(category, key)

my_app = TradingApp()
my_app.mainloop() 
