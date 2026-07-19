import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import shutil
import os


class ActionsFrame(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        


        self.btn_add = ctk.CTkButton(master = self, text = self.app.get_text("menu", "btn_add"), fg_color = "green", command = self.app.open_add_trade_window) 
        self.btn_add.pack(side = "left", pady = 5, padx = 5)

        self.btn_delete = ctk.CTkButton(master = self, text = self.app.get_text("menu", "btn_delete"), fg_color = "red", command = self.delete_selected_trade)
        self.btn_delete.pack(side = "left", pady = 5, padx = 5)

        self.btn_detali = ctk.CTkButton(master = self, 
                                        text = self.app.get_text("menu", "btn_detali"),
                                        fg_color = "blue", 
                                        command = self.open_trade_details_window)
        self.btn_detali.pack(side = "left", pady = 5, padx = 5)

    def open_trade_details_window(self):

        selected_id = self.app.trades_frame.selected_trade_id

        if selected_id is None:
            messagebox.showerror(title = "Error", message = self.app.get_text("menu", "delete_btn_error")) 
            return
        else:
            full_info= self.app.db.get_trade_by_id(selected_id)



        if hasattr(self, "trade_details_win") and self.trade_details_win.winfo_exists():
            self.trade_details_win.focus()
        else:
            self.trade_details_win = TradeDetailsWindow(self.app, full_info)


    def delete_selected_trade(self):

        selected_id = self.app.trades_frame.selected_trade_id
        if selected_id is None:
            messagebox.showerror(title = "Error", message = self.app.get_text("menu", "delete_btn_error"))
        else:
            self.app.db.delete_trade(selected_id)
            self.app.trades_frame.selected_trade_frame.destroy()
            self.app.update_statistics()
            self.app.trades_frame.selected_trade_id = None
            self.app.trades_frame.selected_trade_frame = None


    















    def refresh_text(self):
        self.btn_add.configure(text = self.app.get_text("menu", "btn_add"))
        self.btn_delete.configure(text = self.app.get_text("menu", "btn_delete"))


class AddTradeWindow(ctk.CTkToplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app


        self.selected_images = []


        self.geometry("600x450")
        self.title(self.app.get_text("add_window", "add_window"))


        field_width = 230

        self.form_frame = ctk.CTkFrame(
                self,
                fg_color="transparent",
                )
        self.form_frame.pack(pady = (20, 10))

        
        self.form_frame.grid_columnconfigure((0, 1), weight = 1)



        current_date = datetime.now().strftime("%d.%m.%Y")
        self.entry_date = ctk.CTkEntry(master = self.form_frame, width = field_width, placeholder_text = self.app.get_text("add_window", "entry_date"), fg_color = "#343638")
        self.entry_date.grid(row = 0, column = 0, pady=10, padx=15)
        self.entry_date.insert(0, current_date)






        db_assets = self.app.db.get_all_assets()
        asset_list = [item[1] for item in db_assets] if db_assets else ["No existing assets"]

        self.combo_active = ctk.CTkOptionMenu(master = self.form_frame,
                                              values = asset_list,
                                              width = field_width,
                                             fg_color = "#343638",
                                             button_color = "#343638",
                                             button_hover_color = "#4A4D50",
                                             dropdown_fg_color = "#343638",
                                             dropdown_hover_color = "#4A4D50"
                                              )
        self.combo_active.grid(row = 1, column = 0, pady = 10, padx = 15)







        self.combo_direction = ctk.CTkOptionMenu(master = self.form_frame,
                                                 values = ["Long", "Short"],
                                                 width = field_width,
                                                 fg_color = "#343638",
                                                 button_color = "#343638",
                                                 button_hover_color = "#4A4D50",
                                                 dropdown_fg_color = "#343638",
                                                 dropdown_hover_color = "#4A4D50"
                                                 )
        self.combo_direction.grid(row = 2, column = 0, pady = 10, padx = 15)



        self.combo_session = ctk.CTkOptionMenu(
                master = self.form_frame,
                width = field_width,
                values = ["London", "New York", "Asia"],
                 fg_color = "#343638",
                 button_color = "#343638",
                 button_hover_color = "#4A4D50",
                 dropdown_fg_color = "#343638",
                 dropdown_hover_color = "#4A4D50"
                )
        self.combo_session.grid(row = 3, column = 0, pady = 10, padx = 15)






        self.entry_broker = ctk.CTkEntry(master = self.form_frame,
                                         width = field_width,
                                         placeholder_text = self.app.get_text("add_window", "entry_broker"),
                                            fg_color = "#343638",
                                         )
        self.entry_broker.grid(row = 4, column = 0, pady = 10, padx = 15)





        self.entry_lot_size = ctk.CTkEntry(master = self.form_frame,
                                           placeholder_text = self.app.get_text("add_window", "entry_lot_size"),
                                           width = field_width,
                                            fg_color = "#343638",
                                           )
        self.entry_lot_size.grid(row = 0, column = 1, pady = 10, padx = 15)
        self.entry_lot_size.bind("<KeyRelease>", self.calculate_profit)








        self.entry_entry_price = ctk.CTkEntry(master = self.form_frame,
                                              width = field_width,
                                              placeholder_text = self.app.get_text("add_window", "entry_entry_price"),
                                            fg_color = "#343638",
                                              )
        self.entry_entry_price.grid(row = 1, column = 1, pady = 10, padx = 15)
        self.entry_entry_price.bind("<KeyRelease>", self.calculate_profit)








        self.entry_exit_price = ctk.CTkEntry(master = self.form_frame,
                                             width = field_width,
                                             placeholder_text = self.app.get_text("add_window", "entry_exit_price"),

                                            fg_color = "#343638",
                                             )
        self.entry_exit_price.grid(row = 2, column = 1, pady = 10, padx = 15)
        self.entry_exit_price.bind("<KeyRelease>", self.calculate_profit)



        









        self.entry_sl = ctk.CTkEntry(
                master = self.form_frame,
                width = field_width,
                placeholder_text = "Stop Loss",
                fg_color = "#343638",
                )
        self.entry_sl.grid(row = 3, column = 1, pady = 10, padx = 15)
        self.entry_sl.bind("<KeyRelease>", self.calculate_profit)






        self.entry_profit = ctk.CTkEntry(
                master = self.form_frame,
                width = field_width,
                placeholder_text = self.app.get_text("add_window", "entry_profit"),
                fg_color = "#343638",
                )
        self.entry_profit.grid(row = 4, column = 1, pady = 10, padx = 15)



        self.bottom_frame = ctk.CTkFrame(master = self, fg_color = "transparent")
        self.bottom_frame.pack(pady = (5, 20))


        self.btn_images = ctk.CTkButton(master = self.bottom_frame, width = 350, text = self.app.get_text("add_window", "btn_images"), fg_color = "blue", command = self.open_image_window)
        self.btn_images.pack(pady = 5)

        self.lbl_images = ctk.CTkLabel(master = self.bottom_frame, text = self.app.get_text("add_window", "lbl_images"))
        self.lbl_images.pack(pady = 5)


        self.btn_save = ctk.CTkButton(master = self.bottom_frame, width = 350, text = self.app.get_text("add_window", "btn_save"), fg_color = "green", command = self.collect_and_save)
        self.btn_save.pack(pady = (10, 0))







    



        self.transient(self.app)
        self.focus()


    def open_image_window(self):
        file_paths = filedialog.askopenfilenames(
                title = self.app.get_text("add_window", "open_image_window"),
                filetypes = (("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*"))
                )

        if file_paths:
            self.selected_images = list(file_paths)

            self.lbl_images.configure(text = f"{self.app.get_text('add_window', 'lbl_images')} {len(self.selected_images)}")



    






    def calculate_profit(self, event = None):
        exit_val = self.entry_exit_price.get().strip().replace(',', '.')

        if exit_val == "":
            self.entry_profit.configure(state = "normal")
            self.entry_profit.delete(0, "end")
            return

        

        try:
            asset = self.combo_active.get()
            direction = self.combo_direction.get()

            
            entry_val = self.entry_entry_price.get().strip().replace(',', '.')
            lots_val = self.entry_lot_size.get().strip().replace(',', '.')


            entry_price = float(entry_val)
            exit_price = float(exit_val)
            lots = float(lots_val)


            if direction == "Long":
                price_diff = exit_price - entry_price
            elif direction == "Short":
                price_diff = entry_price - exit_price
            else:
                price_diff = 0.0
            

            if "XAU" in asset:
                contract_size = 100
            elif "BTC" in asset or "ETH" in asset:
                contract_size = 1
            elif "JPY" in asset:
                contract_size = 1000
            else:
                contract_size = 100000

            
            profit = price_diff * contract_size * lots



            self.entry_profit.configure(state = "normal")
            self.entry_profit.delete(0, "end")
            self.entry_profit.insert(0, str(round(profit, 2)))

            
        except ValueError:
            pass





    def collect_and_save(self):
        val_date = self.entry_date.get()
        val_direction = self.combo_direction.get()
        val_assets = self.combo_active.get()
        val_session = self.combo_session.get()

        val_lot_size = self.entry_lot_size.get().strip().replace(',', '.')
        val_entry_price = self.entry_entry_price.get().strip().replace(',', '.')
        exit_val = self.entry_exit_price.get().strip().replace(',', '.')
        val_sl = self.entry_sl.get().strip().replace(',', '.')

        val_broker = self.entry_broker.get()



        if exit_val == "":
            val_exit_price = 0.0
            val_is_closed = 0
            val_outcome = ""
            val_profit = 0.0
            val_rr = "-"
        else:
            val_exit_price = exit_val
            val_is_closed = 1
            profit_str = self.entry_profit.get().strip()
            val_profit_val = float(profit_str) if profit_str else 0.0
            val_profit = val_profit_val
            
            val_rr = "-"
            if val_sl:
                try:
                    sl_price = float(val_sl)
                    entry_price = float(val_entry_price)
                    exit_price = float(val_exit_price)

                    if val_direction == 'Long':
                        risk = entry_price - sl_price
                        reward = exit_price - entry_price
                    else:
                        risk = sl_price - entry_price
                        reward = entry_price - exit_price



                    if risk > 0:
                        val_rr = str(round(reward / risk, 2))
                except ValueError:
                    pass

        if val_profit > 0:
            val_outcome = "Win"
        elif val_profit < 0:
            val_outcome = "Loss"
        else:
            val_outcome = self.app.get_text("table", "lbl_wait_trade")

        




        val_image_paths = ""

        saved_paths = []


        save_folder = "trade_images"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)


        for index, old_path in enumerate(self.selected_images):
            extension = os.path.splitext(old_path)[1]

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"img_{timestamp}_{index}{extension}"

            new_path = os.path.join("trade_images", new_name)

            shutil.copy(old_path, new_path)
            saved_paths.append(new_name)


        val_image_paths = ",".join(saved_paths)
        self.app.save_trade(val_date, val_direction, val_assets, val_session, val_lot_size, val_entry_price, val_exit_price, val_sl, val_rr, val_is_closed, val_outcome, val_profit, val_broker, val_image_paths)
        self.destroy() 



class TradeDetailsWindow(ctk.CTkToplevel):
    def __init__(self, app, trade_date):
        super().__init__(app)
        self.app = app
        self.trade_id = trade_date[0]


        self.geometry("600x700")
        self.title(self.app.get_text("menu", "trade_details"))


        self.lbl_comment = ctk.CTkLabel(
                master = self,
                text=self.app.get_text("menu", "lbl_comment"),
                font = ("Arial", 16, "bold")
                )
        self.lbl_comment.pack(pady = (10, 0), padx = 20, anchor = "w")


        self.text_field = ctk.CTkTextbox(master = self,
                                        font = ("Arial", 16)
                                         )
        self.text_field.pack(pady=10, padx=20, fill="x", expand=True)


        self.lbl_error = ctk.CTkLabel(
                master = self,
                text=self.app.get_text("menu", "lbl_error"),
                font = ("Arial", 16, "bold")
                )
        self.lbl_error.pack(pady = (10, 0), padx = 20, anchor = "w")



        self.error_field_trade = ctk.CTkTextbox(master = self,
                                                font = ("Arial", 16)
                                                )
        self.error_field_trade.pack(pady=10, padx=20, fill="x", expand=True)


        if trade_date[15]:
            self.text_field.insert("1.0", trade_date[15])
        if trade_date[16]:
            self.error_field_trade.insert("1.0", trade_date[16])


        for field in [self.text_field, self.error_field_trade]:
            field.bind("<Control-a>", lambda e, f = field: self.select_all(e,f))
            field.bind("<Control-A>", lambda e, f = field: self.select_all(e,f))

            field.bind("<Control-BackSpace>", lambda e,f = field: self.delete_word(e,f))

    
        self.image_frame = ctk.CTkFrame(master = self, fg_color = "transparent")
        self.image_frame.pack(pady = (10, 0), padx = 20, fill = "x")

        
        image_paths_string = trade_date[14]

        if image_paths_string:
            image_list = image_paths_string.split(",")

            for index, img_name in enumerate(image_list):
                btn_img = ctk.CTkButton(
                        master = self.image_frame,
                        text = f"{self.app.get_text('menu', 'btn_img')} {index + 1}",
                        fg_color = "#D2691E",
                        command = lambda name = img_name: self.open_image(name)
                        )
                btn_img.pack(side = "left", padx = (0, 10))
        

        self.btn_save_change = ctk.CTkButton(master = self,
                                             text = self.app.get_text("menu", "btn_save_change"),
                                             fg_color = "green",
                                             command = self.save_and_close
                                             )
        self.btn_save_change.pack(pady = 20, padx = 20, fill = "x")

        self.transient(self.app)
        self.focus()



    def select_all(self, event, field):
        field.tag_add("sel", "1.0", "end")
        field.mark_set("insert", "1.0")
        field.see("insert")
        return "break"

    def delete_word(self, event, field):
        field.delete("insert - 1c wordstart", "insert")
        return "break"


    def save_and_close(self):
        new_comment = self.text_field.get("1.0", "end-1c")
        new_errors = self.error_field_trade.get("1.0", "end-1c")

        self.app.db.update_trade_details(self.trade_id, new_comment, new_errors)
        self.destroy()

    def open_image(self, img_name):
        full_path = os.path.join("trade_images", img_name)

        if os.path.exists(full_path):
            os.startfile(full_path)
        else:
            messagebox.showerror("Error", f"Image {img_name} not found")








class EditTradeWindow(ctk.CTkToplevel):
    def __init__(self, app, trade_id):
        super().__init__(app)
        self.app = app
        self.trade_id = trade_id


        self.selected_images = []


        self.geometry("600x450")
        self.title(self.app.get_text("add_window", "change_window"))


        field_width = 230

        self.form_frame = ctk.CTkFrame(
                self,
                fg_color="transparent",
                )
        self.form_frame.pack(pady = (20, 10))

        
        self.form_frame.grid_columnconfigure((0, 1), weight = 1)



        current_date = datetime.now().strftime("%d.%m.%Y")
        self.entry_date = ctk.CTkEntry(master = self.form_frame, width = field_width, placeholder_text = self.app.get_text("add_window", "entry_date"), fg_color = "#343638")
        self.entry_date.grid(row = 0, column = 0, pady=10, padx=15)
        self.entry_date.insert(0, current_date)






        db_assets = self.app.db.get_all_assets()
        asset_list = [item[1] for item in db_assets] if db_assets else ["No existing assets"]

        self.combo_active = ctk.CTkOptionMenu(master = self.form_frame,
                                              values = asset_list,
                                              width = field_width,
                                             fg_color = "#343638",
                                             button_color = "#343638",
                                             button_hover_color = "#4A4D50",
                                             dropdown_fg_color = "#343638",
                                             dropdown_hover_color = "#4A4D50"
                                              )
        self.combo_active.grid(row = 1, column = 0, pady = 10, padx = 15)







        self.combo_direction = ctk.CTkOptionMenu(master = self.form_frame,
                                                 values = ["Long", "Short"],
                                                 width = field_width,
                                                 fg_color = "#343638",
                                                 button_color = "#343638",
                                                 button_hover_color = "#4A4D50",
                                                 dropdown_fg_color = "#343638",
                                                 dropdown_hover_color = "#4A4D50"
                                                 )
        self.combo_direction.grid(row = 2, column = 0, pady = 10, padx = 15)



        self.combo_session = ctk.CTkOptionMenu(
                master = self.form_frame,
                width = field_width,
                values = ["London", "New York", "Asia"],
                 fg_color = "#343638",
                 button_color = "#343638",
                 button_hover_color = "#4A4D50",
                 dropdown_fg_color = "#343638",
                 dropdown_hover_color = "#4A4D50"
                )
        self.combo_session.grid(row = 3, column = 0, pady = 10, padx = 15)






        self.entry_broker = ctk.CTkEntry(master = self.form_frame,
                                         width = field_width,
                                         placeholder_text = self.app.get_text("add_window", "entry_broker"),
                                            fg_color = "#343638",
                                         )
        self.entry_broker.grid(row = 4, column = 0, pady = 10, padx = 15)





        self.entry_lot_size = ctk.CTkEntry(master = self.form_frame,
                                           placeholder_text = self.app.get_text("add_window", "entry_lot_size"),
                                           width = field_width,
                                            fg_color = "#343638",
                                           )
        self.entry_lot_size.grid(row = 0, column = 1, pady = 10, padx = 15)
        self.entry_lot_size.bind("<KeyRelease>", self.calculate_profit)







        self.entry_entry_price = ctk.CTkEntry(master = self.form_frame,
                                              width = field_width,
                                              placeholder_text = self.app.get_text("add_window", "entry_entry_price"),
                                            fg_color = "#343638",
                                              )
        self.entry_entry_price.grid(row = 1, column = 1, pady = 10, padx = 15)
        self.entry_entry_price.bind("<KeyRelease>", self.calculate_profit)








        self.entry_exit_price = ctk.CTkEntry(master = self.form_frame,
                                             width = field_width,
                                             placeholder_text = self.app.get_text("add_window", "entry_exit_price"),

                                            fg_color = "#343638",
                                             )
        self.entry_exit_price.grid(row = 2, column = 1, pady = 10, padx = 15)
        self.entry_exit_price.bind("<KeyRelease>", self.calculate_profit)



        









        self.entry_sl = ctk.CTkEntry(
                master = self.form_frame,
                width = field_width,
                placeholder_text = "Stop Loss",
                fg_color = "#343638",
                )
        self.entry_sl.grid(row = 3, column = 1, pady = 10, padx = 15)
        self.entry_sl.bind("<KeyRelease>", self.calculate_profit)






        self.entry_profit = ctk.CTkEntry(
                master = self.form_frame,
                width = field_width,
                placeholder_text = self.app.get_text("add_window", "entry_profit"),
                fg_color = "#343638",
                )
        self.entry_profit.grid(row = 4, column = 1, pady = 10, padx = 15)



        self.bottom_frame = ctk.CTkFrame(master = self, fg_color = "transparent")
        self.bottom_frame.pack(pady = (5, 20))


        self.btn_images = ctk.CTkButton(master = self.bottom_frame, width = 350, text = self.app.get_text("add_window", "btn_images"), fg_color = "blue", command = self.open_image_window)
        self.btn_images.pack(pady = 5)

        self.lbl_images = ctk.CTkLabel(master = self.bottom_frame, text = self.app.get_text("add_window", "lbl_images"))
        self.lbl_images.pack(pady = 5)


        self.btn_save = ctk.CTkButton(master = self.bottom_frame, width = 350, text = self.app.get_text("add_window", "btn_save"), fg_color = "green", command = self.collect_and_save)
        self.btn_save.pack(pady = (10, 0))




        self.load_existing_date()
        self.transient(self.app)
        self.focus()




    def load_existing_date(self):
        data = self.app.db.get_trade_by_id(self.trade_id)

        if not data: return
        self.entry_date.delete(0, "end")
        self.entry_date.insert(0, data[1])

        self.combo_active.set(data[2])
        self.combo_direction.set(data[3])
        self.combo_session.set(data[4])
        

        self.entry_lot_size.insert(0, str(data[5]))
        self.entry_entry_price.insert(0, str(data[6]))
        self.entry_exit_price.insert(0, str(data[7]) if data[7] != 0 else '')

        if data[8] is not None and data[8] != "":
            self.entry_sl.insert(0, str(data[8]))

        
        if data[12] is not None:
            self.entry_profit.configure(state = "normal")
            self.entry_profit.delete(0, "end")
            res_str = f"+{data[12]}" if float(data[12]) > 0 else str(data[12])
            self.entry_profit.insert(0, res_str if data[10] == 1 else "")


        if data[13]:
            self.entry_broker.insert(0, data[13])

    def open_image_window(self):
        file_paths = filedialog.askopenfilenames(
                title = self.app.get_text("add_window", "open_image_window"),
                filetypes = (("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*"))
                )

        if file_paths:
            self.selected_images = list(file_paths)

            self.lbl_images.configure(text = f"{self.app.get_text('add_window', 'lbl_images')} {len(self.selected_images)}")






    def calculate_profit(self, event = None):
        exit_val = self.entry_exit_price.get().strip()

        if exit_val == "":
            self.entry_profit.configure(state = "normal")
            self.entry_profit.delete(0, "end")
            return

        

        try:
            asset = self.combo_active.get()
            direction = self.combo_direction.get()

            
            entry_val = self.entry_entry_price.get().strip().replace(',', '.')
            lots_val = self.entry_lot_size.get().strip().replace(',', '.')


            entry_price = float(entry_val)
            exit_price = float(exit_val)
            lots = float(lots_val)


            if direction == "Long":
                price_diff = exit_price - entry_price
            elif direction == "Short":
                price_diff = entry_price - exit_price
            else:
                price_diff = 0.0


            pip_multiplier = 100 if "JPY" in asset.upper() else 10000
            pips = price_diff * pip_multiplier

            profit = pips * (10.0 * lots)

            self.entry_profit.configure(state = "normal")
            self.entry_profit.delete(0, "end")

            
            res_str = f"{round(profit, 2)}" if profit > 0 else str(round(profit, 2))


            self.entry_profit.insert(0, str(round(profit, 2)))
        except ValueError:
            pass





    def collect_and_save(self):
        val_date = self.entry_date.get()
        val_direction = self.combo_direction.get()
        val_assets = self.combo_active.get()
        val_session = self.combo_session.get()

        val_lot_size = self.entry_lot_size.get().strip().replace(',', '.')
        val_entry_price = self.entry_entry_price.get().strip().replace(',', '.')
        exit_val = self.entry_exit_price.get().strip().replace(',', '.')
        val_sl = self.entry_sl.get().strip().replace(',', '.')

        val_broker = self.entry_broker.get()


        if exit_val == "":
            val_exit_price = 0.0
            val_is_closed = 0
            val_outcome = ""
            val_profit = 0.0
            val_rr = ""
        else:
            val_exit_price = exit_val
            val_is_closed = 1
            profit_str = self.entry_profit.get().strip()
            val_profit_val = float(profit_str) if profit_str else 0.0
            val_profit = val_profit_val
        
            val_rr = "-"
            if val_sl:
                try:
                    sl_price = float(val_sl)
                    entry_price = float(val_entry_price)
                    exit_price = float(val_exit_price)

                    if val_direction == 'Long':
                        risk = entry_price - sl_price
                        reward = exit_price - entry_price
                    else:
                        risk = sl_price - entry_price
                        reward = entry_price - exit_price



                    if risk > 0:
                        val_rr = str(round(reward / risk, 2))
                except ValueError:
                    pass



        if val_profit > 0:
            val_outcome = "Win"
        elif val_profit < 0:
            val_outcome = "Loss"
        else:
            val_outcome = self.app.get_text("table", "lbl_wait_trade")

        




        val_image_paths = ""

        saved_paths = []


        save_folder = "trade_images"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)


        for index, old_path in enumerate(self.selected_images):
            extension = os.path.splitext(old_path)[1]

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"img_{timestamp}_{index}{extension}"

            new_path = os.path.join("trade_images", new_name)

            shutil.copy(old_path, new_path)
            saved_paths.append(new_name)


        val_image_paths = ",".join(saved_paths)
        self.app.save_edit_trade(self.trade_id, val_date, val_direction, val_assets, val_session, val_lot_size, val_entry_price, val_exit_price, val_sl, val_rr, val_is_closed, val_outcome, val_profit, val_broker, val_image_paths)
        self.destroy() 

class ManageAssetsWindow(ctk.CTkToplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        
        self.title(self.app.get_text("menu", "manage_assets"))
        self.geometry("350x450")

        
        self.top_frame = ctk.CTkFrame(
                master = self,
                fg_color = "transparent",
                )
        self.top_frame.pack(fill = "x", pady = 10, padx = 10)




        self.btn_add_asset = ctk.CTkButton(
                master = self.top_frame,
                text = self.app.get_text("menu", "btn_add_asset"),
                width = 90,
                fg_color="green",
                command = self.add_new_asset
                )
        self.btn_add_asset.pack(side = "left", padx = 5)




        self.btn_edit_asset = ctk.CTkButton(
                master = self.top_frame,
                text = self.app.get_text("menu", "btn_edit_asset"),
                width = 90,
                fg_color="blue",
                command = self.edit_selected_asset
                )
        self.btn_edit_asset.pack(side = "left", padx = 5)




        self.btn_delete_asset = ctk.CTkButton(
                master = self.top_frame,
                text = self.app.get_text("menu", "btn_delete_asset"),
                width = 90,
                fg_color="red",
                command = self.delete_selected_asset
                )
        self.btn_delete_asset.pack(side = "left", padx = 5)




        self.list_frame = ctk.CTkScrollableFrame(
                master = self,
                fg_color = "#2b2b2b",
                )
        self.list_frame.pack(fill = "both", expand = True, padx = 10, pady = (0,10))


        self.selected_asset_id = None
        self.selected_asset_frame = None

        self.load_assets()

        self.transient(self.app)
        self.focus()

    

    def load_assets(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.selected_asset_id = None
        self.selected_asset_frame = None

        assets = self.app.db.get_all_assets()


        for asset_id, asset_name in assets:
            row = ctk.CTkFrame(
                    master = self.list_frame,
                    fg_color = "transparent",
                    corner_radius = 5,
                    )
            row.pack(fill = "x", pady = 2, padx = 2)

            lbl = ctk.CTkLabel(
                    master = row, 
                    text = asset_name,
                    font = ("Arial", 16, "bold"),
                    anchor = "w"
                    )
            lbl.pack(side = "left", pady = 5, padx = 10)

            
            row.bind("<Button-1>", lambda event, r = row, a_id = asset_id: self.select_asset(r, a_id))
            lbl.bind("<Button-1>", lambda event, r = row, a_id = asset_id: self.select_asset(r, a_id))







    def select_asset(self, row_frame, asset_id):
        if self.selected_asset_frame is not None and self.selected_asset_frame.winfo_exists():
            self.selected_asset_frame.configure(fg_color = "transparent")


        row_frame.configure(fg_color = "#4A4D50")
        self.selected_asset_id = asset_id
        self.selected_asset_frame = row_frame



    


    def add_new_asset(self):
        dialog = ctk.CTkInputDialog(
                text = self.app.get_text("menu", "add_asset_name"),
                title = self.app.get_text("menu", "add_asset"),
                )
        new_name = dialog.get_input()

        if new_name:
            new_name = new_name.strip().upper()
            success = self.app.db.add_asset(new_name)
            if success:
                self.load_assets()
            else:
                messagebox.showerror("Error", self.app.get_text("messagebox", "add_asset_error"))






    def edit_selected_asset(self):
        if self.selected_asset_id is None:
            messagebox.showwarning("Atention", self.app.get_text("messagebox", "select_asset"))
            return

        dialog = ctk.CTkInputDialog(
                text =  self.app.get_text("menu", "edit_asset_name"),
                title = self.app.get_text("menu", "edit_asset"),
                )
        new_name = dialog.get_input()
        

        if new_name:
            new_name = new_name.strip().upper()
            success = self.app.db.edit_asset(self.selected_asset_id, new_name)
            if success:
                self.load_assets()
            else:
                messagebox.showerror("Error", self.app.get_text("messagebox", "edit_asset_error"))






    def delete_selected_asset(self):
        if self.selected_asset_id is None:
            messagebox.showwarning("Atention", self.app.get_text("messagebox", "select_asset"))
            return

        confirm = messagebox.askyesno("Atention", self.app.get_text("messagebox", "delete_asset"))
        if confirm:
            self.app.db.delete_asset(self.selected_asset_id)
            self.load_assets()



