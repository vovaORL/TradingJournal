import json
import os

class LanguageManager:
    def __init__(self):
        self.translations = {
                "uk": {
                    "menu":{
                        "btn_add": "➕ Додати угоду",
                        "btn_delete": "➖ Видалити угоду",
                        "delete_btn_error": "Виділіть угоду", 
                        "btn_detali": "Деталі",
                        "input_comment": "Додайте коментарі до угоди",
                        "input_comment_error": "Додайте помилки",
                        "btn_save_change": "Зберегти зміни",
                        "trade_details": "Деталі угоди",
                        "delete_btn_error": "Оберіть угоду",
                        "lbl_comment": "Коментарі:",
                        "lbl_error": "Помилки:",
                        "btn_img": "Скріншот",
                        "manage_assets": "Керування парами",
                        "btn_add_asset": "Додати",
                        "btn_edit_asset": "Редагувати",
                        "btn_delete_asset": "Видалити",
                        "add_asset_name": "Введіть назву пари",
                        "add_asset": "Додати пару",
                        "edit_asset_name": "Введіть нову назву",
                        "edit_asset": "Редагування пари",
                        },
                    "settings":{
                        "currency_pair": "Валютні пари",
                        "error_amount": "Введіть коректне число",
                        "suma_mai_mare": "Сума має бути більшою за 0!",
                        "balance_deposit_btn_entry": "Підтвердити",
                        "balance_deposit_entry": "Введіть суму",
                        "btn_deposit": "Поповнити",
                        "btn_withdraw": "Вивести",
                        "btn_adjust": "Скоригувати",
                        "current_balance": "Поточний баланс",
                        "tabview_other": "Інше",
                        "tabview_balance": "Баланс",
                        "btn_file": "📂 Файл",
                        "btn_statistic": "📊 Статистика",
                        "btn_settings": "⚙️ Налаштування",
                        "combo_lang": "Мова"
                        },
                    "footer":{
                        "winrate_footer": "Вінрейт: ",
                        "bls_footer": "Баланс: ",
                        "trades_count": "Угоди: ",
                        "win_trades": "Угод в плюс",
                        "lose_trades": "Угод в мінус",
                        "total_lots": "Сума лотів:"
                        },
                    "table":{
                        "lbl_result": "P/L",
                        "lbl_date": "Дата",
                        "lbl_asset": "Актив",
                        "lbl_direction": "Напрямок",
                        "lbl_lot_size": "Лот",
                        "lbl_entry_price": "Ціна входу",
                        "lbl_pips": "Піпси",
                        "lbl_broker": "Брокер",
                        "lbl_wait_trade": "Відк.⏳",
                        "win": "Виграш",
                        "lose": "Програш",
                    },
                    "add_window":{
                        "add_window": "Додати нову угоду",
                        "entry_date": "Дата. Напр: 22.03.26",
                        "entry_lot_size": "Кількість лотів: (Прик: 0.12)",
                        "entry_entry_price": "Ціна входу: (Прик: 1.0000)",
                        "entry_exit_price": "Ціна виходу: (Прик: 1.0010)",
                        "entry_result_box": "Угода закрита",
                        "entry_result": "Результат (+50 або -20)",
                        "entry_profit": "Результат (Прибуток/Збиток)",
                        "entry_broker": "Ex: Binarium",
                        "btn_images": "Додати фото",
                        "lbl_images": "Вибрано фото: ",
                        "open_image_window": "Виберіть скріншоти угод",
                        "change_window": "Редагування угоди",
                        "btn_save": "💾 Зберегти угоду",
                        },
                    "messagebox":{
                        "messagebox_error": "Будь ласка, заповніть усі поля",
                        "messagebox_error_title": "Помилка",
                        "add_asset_error": "Така пара вже існує в базі",
                        "select_asset": "Виберіть пару для редагування",
                        "edit_asset_error": "Така пара вже існує в базі",
                        "delete_asset": "Точно видалити цю пару?",
                        }
                },
                "en":{
                    "menu":{
                        "btn_add": "➕ Add trade",
                        "btn_delete": "➖ Delete trade",
                        "delete_btn_error": "Choose trade to delete", 
                        "btn_detali": "Details",
                        "input_comment": "Add comments to the trade",
                        "input_comment_error": "Include errors",
                        "btn_save_change": "Save changes",
                        "trade_details": "Details of the trade",
                        "delete_btn_error": "Choose trade",
                        "lbl_comment": "Comments:",
                        "lbl_error": "Errors:",
                        "btn_img": "Screenshot",
                        "manage_assets": "Pair management",
                        "btn_add_asset": "Add",
                        "btn_edit_asset": "Edit",
                        "btn_delete_asset": "Remove",
                        "add_asset_name": "Input pair name",
                        "add_asset": "Add pair",
                        "edit_asset_name": "Input new pair name",
                        "edit_asset": "Change pair",
                        },
                    "settings":{
                        "currency_pair": "Currency pair",
                        "error_amount": "Input amount is not valid!",
                        "suma_mai_mare": "Deposit amount must be bigger than 0!",
                        "balance_deposit_btn_entry": "Confirm",
                        "balance_deposit_entry": "Enter the amount",
                        "btn_deposit": "Deposit",
                        "btn_withdraw": "Withdraw",
                        "btn_adjust": "Adjust",
                        "current_balance": "Current balance",
                        "tabview_other": "Other",
                        "tabview_balance": "Balance",
                        "btn_file": "📂 File",
                        "btn_statistic": "📊 Statistics",
                        "btn_settings": "⚙️ Settings",
                        "combo_lang": "Language",
                        },
                    "footer":{
                        "winrate_footer": "Winrate: ",
                        "bls_footer": "Balance: ",
                        "trades_count": "Trades: ",
                        "win_trades": "Trades in plus",
                        "lose_trades": "Trades in minus",
                        "total_lots": "Suma lots:"
                        },
                    "table":{
                        "lbl_result": "P/L",
                        "lbl_date": "Date",
                        "lbl_asset": "Asset",
                        "lbl_direction": "Direction",
                        "lbl_lot_size": "Lot",
                        "lbl_entry_price": "Price entry",
                        "lbl_exit_price": "Price exit",
                        "lbl_pips": "Pips",
                        "lbl_broker": "Broker",
                        "lbl_wait_trade": "Open ⏳",
                        "win": "Win",
                        "lose": "Lose",
                    },
                    "add_window":{
                        "add_window": "Add New Trade",
                        "entry_date": "Date (eg: 22.03.26)",
                        "entry_bet": "Stake Amount ($)",
                        "entry_result_box": "Trade is closed",
                        "entry_result": "Result (+50 or -20)",
                        "entry_profit": "Result (Profit/Loss)",
                        "entry_broker": "Ex: Binarium",
                        "entry_expiration": "Ex: 10 (In min)",
                        "entry_percent": "Ex: 86",
                        "btn_images": "Add photos",
                        "lbl_images": "Chose photos: ",
                        "open_image_window": "Choose trade screenshots",
                        "change_window": "Edit trade",
                        "btn_save": "💾 Save Trade",
                        },
                    "messagebox":{
                        "messagebox_error": "Please fill in all fields",
                        "messagebox_error_title": "Error",
                        "add_asset_error": "This pair already exists in the database",
                        "select_asset": "Select pair for the change",
                        "edit_asset_error": "This pair already exists in the database",
                        "delete_asset": "Are you sure you want to delete this pair?",
                    }
                }
            }
        self.current_lang = self.load_language() 
        

    def load_language(self):
        if os.path.exists("language.json"):
            with open("language.json", "r") as f:
                config =  json.load(f)
            return config.get("language", "en")
        return "en"



    
    def save_language(self, lang):
        self.current_lang = lang
        with open("language.json", "w") as f:
            json.dump({"language": self.current_lang}, f)




    def get_text(self, category, key):
       return self.translations[self.current_lang][category][key] 


