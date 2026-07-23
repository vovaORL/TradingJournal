import customtkinter as ctk
import tkinter as ct
from PIL import Image

class HeaderFrame(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        
        
        header_font = ("Arial", 15, "bold")

        self.icon_image = ctk.CTkImage(
                light_image = Image.open("Image_for_app/add_pair.png"),
                dark_image = Image.open("Image_for_app/add_pair.png"),
                size = (24, 24)
                )
         
        self.btn_file = ctk.CTkButton(master = self,
                                      text = self.app.get_text("settings", "btn_file"),
                                      font = header_font,
                                      fg_color = "transparent",
                                      command=self.show_file_menu)
        self.btn_file.pack(side = "left", padx = 2)

        self.btn_statistic = ctk.CTkButton(master = self,
                                           text = self.app.get_text("settings", "btn_statistic"),
                                           font = header_font,
                                           fg_color = "transparent")
        self.btn_statistic.pack(side = "left", padx = 2)

        self.btn_settings = ctk.CTkButton(master = self,
                                          text = self.app.get_text("settings", "btn_settings"),
                                          font = header_font,
                                          fg_color = "transparent",
                                          command = self.app.open_settings_window)
        self.btn_settings.pack(side = "left", padx = 2)


        self.btn_add_pair = ctk.CTkButton(
                master = self,
                text = "",
                image = self.icon_image,
                width = 24,
                height = 24,
                fg_color = "transparent",
                hover_color = "#4A4D50",
                command = self.app.open_manage_assets_window
                )
        self.btn_add_pair.pack(side = "left", padx = 15, pady = 5)
        self.btn_add_pair.bind("<Enter>", self.show_tooltip)
        self.btn_add_pair.bind("<Leave>", self.hide_tooltip)



        self.combo_period = ctk.CTkOptionMenu(
                master = self,
                values = [self.app.get_text('table', 'period_all'), self.app.get_text('settings', 'period_1m'), self.app.get_text('settings', 'period_3m'), self.app.get_text('settings', 'period_6m'), self.app.get_text('settings', 'period_1y'), self.app.get_text('settings', 'period_custom')],
                variable = self.app.period_var,
                command = self.handle_period_change,
                fg_color = "#343638",
                button_color = "#343638",
                button_hover_color = "#4A4D50",
                )
        self.combo_period.pack(side = "right", padx = 10, pady = 5)


        self.combo_sort = ctk.CTkOptionMenu(
                master = self,
                values =[self.app.get_text('table', 'sort_date_new'), self.app.get_text('table', 'sort_date_old')],
                variable = self.app.sort_var,
                command = lambda val: self.app.trades_frame.apply_filters(),
                fg_color = "#343638", button_color = "#343638", button_hover_color = "#4A4D50",
                )
        self.combo_sort.pack(side = "right", padx = 10, pady = 5)


    def show_tooltip(self, Event):
        try:
            if not self.btn_add_pair.winfo_exists():
                return
            if hasattr(self, "tooltip_win") and self.tooltip_win.winfo_exists():
                self.destroy()


            self.tooltip_win = ct.Toplevel(self.app)
            self.tooltip_win.overrideredirect(True)
            self.tooltip_win.attributes("-topmost", True)
            self.tooltip_win.configure(bg = "#4A4D50")

            x = self.btn_add_pair.winfo_rootx() - 40
            y = self.btn_add_pair.winfo_rooty() + self.btn_add_pair.winfo_height() + 5
            self.tooltip_win.geometry(f"+{x}+{y}")

            lbl = ctk.CTkLabel(
                    master = self.tooltip_win,
                    text = self.app.get_text("settings", "currency_pair"),
                    fg_color = "#4A4D50",
                    text_color = "white",
                    corner_radius = 6,
                    padx = 10,
                    pady = 5,
                    font = ("Arial", 12)
                    )
            lbl.pack()
        except Exception:
            pass

    def hide_tooltip(self, Event):
        try:
            if hasattr(self, "tooltip_win") and self.tooltip_win.winfo_exists():
                self.tooltip_win.destroy()
        except Exception:
            pass


    

    def handle_period_change(self, val):
        from datetime import datetime
        if val == self.app.get_text('settings', 'period_custom'):
            self.open_custom_period_window()
        else:
            self.app.trades_frame.apply_filters()


    


    def open_custom_period_window(self):
        from datetime import datetime
        if hasattr(self, "custom_period_win") and self.custom_period_win.winfo_exists():
            self.custom_period_win.focus()


        self.custom_period_win = ctk.CTkToplevel(self)
        self.custom_period_win.title(self.app.get_text("settings", "period_custom"))
        self.custom_period_win.geometry("300x250")
        self.custom_period_win.transient()
        self.custom_period_win.grab_set()

        lbl = ctk.CTkLabel(
                self.custom_period_win,
                text = self.app.get_text("settings", "select_date"),
                font = ("Arial", 14, "bold"),
                )
        lbl.pack(pady = (20, 10))




        self.entry_start_date = ctk.CTkEntry(
                self.custom_period_win,
                placeholder_text = self.app.get_text("settings", "start_date"),
                width = 200,
                )
        self.entry_start_date.pack(pady = 10)





        self.entry_end_date = ctk.CTkEntry(
                self.custom_period_win,
                text = f'self.app.get_text("settings", "finish_date") {datetime.now().strftime('%d.%m.%Y')}',
                width = 200,
                )
        self.entry_end_date.pack(pady = 10)



        btn_apply = ctk.CTkButton(
                self.custom_period_win,
                text = self.app.get_text("header", "save_period"),
                fg_color = "green",
                command = self.apply_custom_period,
                )
        btn_apply.pack(pady = (10, 20))
        

        self.custom_period_win.protocol("WM_DELETE_WINDOW", self.cancel_custom_period)





    def apply_custom_period(self):
        from datetime import datetime
        start_str = self.entry_start_date.get().strip()
        ent_str = self.entry_end_date.get().strip()


        try:
            start_date = datetime.strptime(start_str, "%d.%m.%Y")
            end_date = datetime.strptime(ent_str, "%d.%m.%Y")

            self.app.custom_start_date = start_date
            self.app.custom_end_date = end_date.replace(hour = 23, minute = 59, second = 59)

            self.app.trades_frame.apply_filters()
            self.custom_period_win.destroy()
        except ValueError:
            import tkinter.messagebox as mb
            mb.showerror("Error", "error_date", parent = self.custom_period_win)



    def cancel_custom_period(self):
        self.app.period_var.set(self.app.get_text("settings", "period_all"))
        self.custom_period_win.destroy()
        self.app.trades_frame.apply_filters()





    def show_file_menu(self):
        if hasattr(self, "dropdown_window") and self.dropdown_window.winfo_exists():
            self.dropdown_window.destroy()
            return

        self.dropdown_window = ctk.CTkToplevel(self.app)
        self.dropdown_window.overrideredirect(True)
        self.dropdown_window.configure(fg_color = "#2b2b2b")

        x = self.btn_file.winfo_rootx()
        y = self.btn_file.winfo_rooty() + self.btn_file.winfo_height()
        self.dropdown_window.geometry(f"150x80+{x}+{y}")


        self.lang_switch = ctk.CTkSwitch(
                master = self.dropdown_window,
                text = "UKR / ENG",
                progress_color = "#1f538d",
                command = self.toggle_language
                )

        self.lang_switch.pack(pady = 15, padx = 15)

        if self.app.current_lang == "en":
            self.lang_switch.select()
        else:
            self.lang_switch.deselect()


        self.dropdown_window.focus()
        self.dropdown_window.bind("<FocusOut>", lambda _: self.dropdown_window.destroy())

    def toggle_language(self):
        if self.lang_switch.get() == 1:
            new_lang = "en"
        else:
            new_lang = "uk"


        self.app.lang_manager.save_language(new_lang)
        self.app.current_lang = new_lang
        self.app.refresh_ui()


    def refresh_text(self):
        self.btn_file.configure(text = self.app.get_text("settings", "btn_file"))
        self.btn_statistic.configure(text = self.app.get_text("settings", "btn_statistic"))
        self.btn_settings.configure(text = self.app.get_text("settings", "btn_settings"))











class SettingsWindow(ctk.CTkToplevel):

    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.geometry("500x600")
        self.title(self.app.get_text("settings", "combo_lang"))

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill = "both", expand = True, padx = 10, pady = 10)

        self.current_name_balance = self.app.get_text("settings", "tabview_balance")
        self.tab_balance = self.tabview.add(self.current_name_balance)

        self.current_name_other = self.app.get_text("settings", "tabview_other")
        self.tab_other = self.tabview.add(self.current_name_other)



        self.lbl_current_balance = ctk.CTkLabel(
                                            master = self.tab_balance,
                                            text = self.app.get_text("settings", "current_balance"),
                                            font = ("Arial", 24, "bold")
                                            )
        self.lbl_current_balance.pack(pady = (20, 30))

    



        self.balance_view = ctk.CTkEntry(master = self.tab_balance, state = "readonly")
        self.balance_view.pack(pady = 20, padx = 20, fill = "x")
        
        self.btns_frame = ctk.CTkFrame(
                master = self.tab_balance,
                fg_color = "transparent"
                )
        self.btns_frame.pack(pady = 10, fill = "x")


        self.btn_deposit = ctk.CTkButton(
                master = self.btns_frame,
                fg_color = "green",
                text = self.app.get_text("settings", "btn_deposit"),
                command = self.open_deposit
                )
        self.btn_deposit.pack(pady = 10, padx = 5, expand = True, side = 'left')

        self.btn_withdraw = ctk.CTkButton(
                master = self.btns_frame,
                text = self.app.get_text("settings", "btn_withdraw"),
                fg_color = "red",
                command = self.open_withdraw
                )
        self.btn_withdraw.pack(pady = 10, padx = 5, expand = True, side = 'left')


        self.btn_adjust = ctk.CTkButton(
                master = self.btns_frame,
                text = self.app.get_text("settings", "btn_adjust"),
                command = self.open_adjust
                )
        self.btn_adjust.pack(pady = 10, padx = 5, expand = True, side = 'left')

        self.update_balance_display()

        self.combo_change_lang = ctk.CTkComboBox(master = self.tab_other, 
                                                 values = ["English", "Ukrainian"],
                                                 command = self.change_language,
                                                 state = "readonly")
        if self.app.current_lang == "uk":
            self.combo_change_lang.set("Ukrainian")
        elif self.app.current_lang == "en":
            self.combo_change_lang.set("English")

        self.combo_change_lang.pack(pady = 20, padx = 20, fill = "x")
        self.transient(self.app)
        self.grab_set()
        self.focus()



    def update_balance_display(self):
        balance = self.app.db.get_balance()

        self.balance_view.configure(state = "normal")
        self.balance_view.delete(0, "end")
        self.balance_view.insert(0, f"{balance:.2f}₴")
        self.balance_view.configure(state = "readonly")

    def change_language(self, choice):
        if choice == "Ukrainian":
            new_lang = "uk"
        else:
            new_lang = "en"

        self.app.lang_manager.save_language(new_lang)
        self.app.current_lang = new_lang
        self.app.refresh_ui()
        self.title(self.app.get_text("settings", "combo_lang"))



    def refresh_text(self):
        new_name_balance = self.app.get_text("settings", "tabview_balance")
        new_name_other = self.app.get_text("settings", "tabview_other")

        active_tab = self.tabview.get()
        tab_to_set = active_tab


        if new_name_balance != self.current_name_balance:
            self.tabview.rename(self.current_name_balance, new_name_balance)
            if active_tab == self.current_name_balance:
                tab_to_set = new_name_balance
            self.current_name_balance = new_name_balance

        if new_name_other != self.current_name_other:
            self.tabview.rename(self.current_name_other, new_name_other)
            if tab_to_set == self.current_name_other:
                tab_to_set = new_name_other
            self.current_name_other = new_name_other

        self.tabview.set(tab_to_set)

        self.lbl_current_balance.configure(text = self.app.get_text("settings", "current_balance"))
        self.btn_deposit.configure(text = self.app.get_text("settings", "btn_deposit"))
        self.btn_withdraw.configure(text = self.app.get_text("settings", "btn_withdraw"))
        self.btn_adjust.configure(text = self.app.get_text("settings", "btn_adjust"))

    def open_deposit(self):
        if hasattr(self, "deposit_win") and self.deposit_win.winfo_exists():
            self.deposit_win.focus()
        else:
            self.deposit_win = ctk.CTkToplevel(self)
            self.deposit_win.geometry("300x200")
            self.deposit_win.title(self.app.get_text("settings", "btn_deposit"))
            self.deposit_win.focus()
            self.deposit_win.transient(self)
            self.deposit_win.grab_set()
            self.deposit_win.attributes("-topmost", True)

            self.deposit_entry = ctk.CTkEntry(
                    master = self.deposit_win,
                    placeholder_text = self.app.get_text("settings", "balance_deposit_entry")
                    )
            self.deposit_entry.pack(pady = 20, padx = 20, fill = "x")

            self.deposit_btn = ctk.CTkButton(
                    master = self.deposit_win,
                    text = self.app.get_text("settings", "balance_deposit_btn_entry"),
                    command = self.confirm_deposit
                    )
            self.deposit_btn.pack(pady = 10)


    def open_withdraw(self):
        if hasattr(self, "withdraw_win") and self.withdraw_win.winfo_exists():
            self.withdraw_win.focus()
        else:
            self.withdraw_win = ctk.CTkToplevel(self)
            self.withdraw_win.geometry("300x200")
            self.withdraw_win.title(self.app.get_text("settings", "btn_withdraw"))
            self.withdraw_win.focus()
            self.withdraw_win.transient(self)
            self.withdraw_win.grab_set()
            self.withdraw_win.attributes("-topmost", True)

            
            self.withdraw_entry = ctk.CTkEntry(
                    master = self.withdraw_win,
                    placeholder_text = self.app.get_text("settings", "balance_deposit_entry")
                    )
            self.withdraw_entry.pack(pady = 20, padx = 20, fill = "x")

            self.withdraw_btn = ctk.CTkButton(
                    master = self.withdraw_win,
                    text = self.app.get_text("settings", "balance_deposit_btn_entry"),
                    command = self.confirm_withdraw
                    )
            self.withdraw_btn.pack(pady = 10)

    def open_adjust(self):
        if hasattr(self, "adjust_win") and self.adjust_win.winfo_exists():
            self.adjust_win.focus()
        else:
            self.adjust_win = ctk.CTkToplevel(self)
            self.adjust_win.geometry("300x200")
            self.adjust_win.title(self.app.get_text("settings", "btn_adjust"))
            self.adjust_win.focus()
            self.adjust_win.transient(self)
            self.adjust_win.grab_set()
            self.adjust_win.attributes("-topmost", True)


            self.adjust_entry = ctk.CTkEntry(
                    master = self.adjust_win,
                    placeholder_text = self.app.get_text("settings", "balance_deposit_entry")
                    )
            self.adjust_entry.pack(pady = 20, padx = 20, fill = "x")

            self.adjust_btn = ctk.CTkButton(
                    master = self.adjust_win,
                    text = self.app.get_text("settings", "balance_deposit_btn_entry"),
                    command = self.confirm_adjust
                    )
            self.adjust_btn.pack(pady = 10)




    def confirm_deposit(self):
        amount_str = self.deposit_entry.get()

        try: 
            amount = float(amount_str)

            if amount <= 0:
                print(self.app.get_text("settings", "suma_mai_mare"))
                return
            current_balance = self.app.db.get_balance()
            new_balance = current_balance + amount

            self.app.db.update_balance(new_balance)
            self.update_balance_display()

            self.app.update_statistics()

            self.deposit_win.destroy()
        except ValueError:
            print(self.app.get_text("settings", "error_amount"))



    def confirm_withdraw(self):
        amount_str = self.withdraw_entry.get()

        try: 
            amount = float(amount_str)

            if amount <= 0:
                print(self.app.get_text("settings", "suma_mai_mare"))
                return
            current_balance = self.app.db.get_balance()
            new_balance = current_balance - amount

            self.app.db.update_balance(new_balance)
            self.update_balance_display()

            self.app.update_statistics()


            self.withdraw_win.destroy()

        except ValueError:
            print(self.app.get_text("settings", "error_amount"))



    def confirm_adjust(self):
        amount_str = self.adjust_entry.get()

        try: 
            amount = float(amount_str)

            if amount <= 0:
                print(self.app.get_text("settings", "suma_mai_mare"))
                return

            self.app.db.update_balance(amount)
            self.update_balance_display()

            self.app.update_statistics()

            self.adjust_win.destroy()

        except ValueError:
            print(self.app.get_text("settings", "error_amount"))



