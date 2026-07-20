import customtkinter as ctk 
from datetime import datetime, timedelta


class TradeFrame(ctk.CTkScrollableFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        
        self.pack(fill = "both", expand = True, pady = 5, padx = 5)
        self.grid_columnconfigure(0, weight = 1)

        self.selected_trade_id = None
        self.selected_trade_frame = None

        self.filter_frame = ctk.CTkFrame(
                master = self,
                fg_color="transparent",
                )
        self.filter_frame.grid(row = 0, column = 0, columnspan = 11, sticky = "ew", padx = 2, pady = (0, 10))


        self.sort_var = ctk.StringVar(value = self.app.get_text("table", "sort_date_new"))
        self.period_var = ctk.StringVar(value = self.app.get_text("table", "period_all"))



        self.header_frame = ctk.CTkFrame(master = self, fg_color = "transparent")
        self.header_frame.grid(row = 0, column = 0, columnspan = 11, sticky = "ew", padx = 2, pady = 5)

        for i in range(11):
            self.header_frame.grid_columnconfigure(i, weight = 1, uniform = "col")



        self.lbl_date = ctk.CTkLabel(master = self.header_frame, text = self.app.get_text("table", "lbl_date"), font = ("Arial", 14, "bold"), anchor = "center")
        self.lbl_date.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "ew")



        self.lbl_asset = ctk.CTkLabel(master = self.header_frame, text = self.app.get_text("table", "lbl_asset"), font = ("Arial", 14, "bold"), anchor = "center")
        self.lbl_asset.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "ew")



        self.lbl_direction = ctk.CTkLabel(master = self.header_frame, text = self.app.get_text("table", "lbl_direction"), font = ("Arial", 14, "bold"), anchor = "center")
        self.lbl_direction.grid(row = 0, column = 2, padx = 5, pady = 5, sticky = "ew")


        self.lbl_lot_size = ctk.CTkLabel(master = self.header_frame, text = self.app.get_text("table", "lbl_lot_size"), font = ("Arial", 14, "bold"), anchor = "center")
        self.lbl_lot_size.grid(row = 0, column = 3, padx = 5, pady = 5, sticky = "ew")

        
        self.lbl_entry_price = ctk.CTkLabel(
                master = self.header_frame,
                text = self.app.get_text("table", "lbl_entry_price"),
                font = ("Arial", 14, "bold"),
                anchor = "center",
                )
        self.lbl_entry_price.grid(row = 0, column = 4, padx = 5, pady = 5, sticky = "ew")





        self.lbl_exit_price = ctk.CTkLabel(master = self.header_frame, text = "TP", font = ("Arial", 14, "bold"), anchor = "center")
        self.lbl_exit_price.grid(row = 0, column = 5, padx = 5, pady = 5, sticky = "ew")


        self.lbl_stop_price = ctk.CTkLabel(
                master = self.header_frame,
                text = "SL",
                font = ("Arial", 14, "bold"),
                anchor = "center",
                )
        self.lbl_stop_price.grid(row = 0, column = 6, padx = 5, pady = 5, sticky = "ew")

        self.lbl_pips = ctk.CTkLabel(
                master = self.header_frame,
                text = self.app.get_text("table", "lbl_pips"),
                font = ("Arial", 14, "bold"),
                anchor = "center",
                )
        self.lbl_pips.grid(row = 0, column = 7, padx = 5, pady = 5, sticky = "ew")

        


        self.lbl_rr = ctk.CTkLabel(
                master = self.header_frame,
                text = "RR",
                font = ("Arial", 14, "bold"),
                anchor = "center",
                )
        self.lbl_rr.grid(row = 0, column = 8, padx = 5, pady = 5, sticky = "ew")





        self.lbl_result = ctk.CTkLabel(master = self.header_frame, text = self.app.get_text("table", "lbl_result"), font = ("Arial", 14, "bold"), anchor = "center")
        self.lbl_result.grid(row = 0, column = 9, padx = 5, pady = 5, sticky = "ew")




        self.lbl_broker = ctk.CTkLabel(master = self.header_frame, text = self.app.get_text("table", "lbl_broker"), font = ("Arial", 14, "bold"), anchor = "center")
        self.lbl_broker.grid(row = 0, column = 10, padx = 5, pady = 5, sticky = "ew")




        self.current_row = 1

    def add_row(self, trade_id, val_date, val_assets, val_direction, val_lot_size, val_entry_price, val_exit_price, val_sl, val_rr, val_is_closed, val_outcome, val_profit, val_broker):

        row_frame = ctk.CTkFrame(master = self, fg_color = "transparent")
        row_frame.grid(row = self.current_row, column = 0, columnspan = 11, sticky = "ew", padx = 2, pady = 5)


        for i in range(11):
            row_frame.grid_columnconfigure(i, weight = 1, uniform = "col")
        
        if "JPY" in val_assets.upper():
            str_entry = f"{float(val_entry_price):.3f}"
            str_exit = "-" if val_exit_price == 0.0 else f"{float(val_exit_price):.3f}"
        else:
            str_entry = f"{float(val_entry_price):.5f}"
            str_exit = "-" if val_exit_price == 0.0 else f"{float(val_exit_price):.5f}"


        if val_is_closed == 0:
            display_result = self.app.get_text("table", "lbl_wait_trade")
            res_color = "gray"
            display_pips = "-"
        else:
            price_diff = float(val_exit_price) - float(val_entry_price)
            if val_direction == "Short":
                price_diff = -price_diff

            pip_mult = 100 if "JPY" in val_assets.upper() else 10000 
            pips_calc = round(price_diff * pip_mult, 1)
            display_pips = f"+{pips_calc}" if pips_calc > 0 else str(pips_calc)



            if val_outcome == "Win":
                display_result = f"+{val_profit}"
                res_color = "#2FA572"
            elif val_outcome == "Loss":
                display_result = str(val_profit)
                res_color = "#E84A5F"
            else:
                display_result = str(val_profit)
                res_color = "white"





        new_lbl_date = ctk.CTkLabel(master = row_frame, text = val_date, font = ("Arial", 14, "bold"), anchor = "center")
        new_lbl_date.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "ew")


        new_lbl_direction = ctk.CTkLabel(master = row_frame, text = val_direction, font = ("Arial", 14, "bold"), anchor = "center")
        new_lbl_direction.grid(row = 0, column = 2, padx = 5, pady = 5, sticky = "ew")


        new_lbl_assets = ctk.CTkLabel(master = row_frame, text = val_assets, font = ("Arial", 14, "bold"), anchor = "center")
        new_lbl_assets.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "ew")


        new_lbl_lot_size = ctk.CTkLabel(master = row_frame, text = val_lot_size, font = ("Arial", 14, "bold"), anchor = "center")
        new_lbl_lot_size.grid(row = 0, column = 3, padx = 5, pady = 5, sticky = "ew")


        new_lbl_entry_price = ctk.CTkLabel(master = row_frame, text = str_entry, font = ("Arial", 14, "bold"), anchor = "center")
        new_lbl_entry_price.grid(row = 0, column = 4, padx = 5, pady = 5, sticky = "ew")



        new_lbl_exit_price = ctk.CTkLabel(master = row_frame, text = str_exit, font = ("Arial", 14, "bold"), anchor = "center")
        new_lbl_exit_price.grid(row = 0, column = 5, padx = 5, pady = 5, sticky = "ew")
        

        new_lbl_sl = ctk.CTkLabel(master = row_frame, text = str(val_sl), font = ("Arial", 14, "bold"), anchor = "center")
        new_lbl_sl.grid(row = 0, column = 6, padx = 5, pady = 5, sticky = "ew")
        
        new_lbl_pips = ctk.CTkLabel(master = row_frame, text = display_pips, font = ("Arial", 14, "bold"), anchor = "center")
        new_lbl_pips.grid(row = 0, column = 7, padx = 5, pady = 5, sticky = "ew")

        display_rr = str(val_rr) if val_rr else "-" 
        new_lbl_rr = ctk.CTkLabel(master = row_frame, text = display_rr, font = ("Arial", 14, "bold"), anchor = "center")
        new_lbl_rr.grid(row = 0, column = 8, padx = 5, pady = 5, sticky = "ew")



        new_lbl_result = ctk.CTkLabel(master = row_frame, text = display_result, font = ("Arial", 14, "bold"), text_color = res_color, anchor = "center")
        new_lbl_result.grid(row = 0, column = 9, padx = 5, pady = 5, sticky = "ew")


        new_lbl_broker = ctk.CTkLabel(master = row_frame, text = str(val_broker), font = ("Arial", 14, "bold"), anchor = "center")
        new_lbl_broker.grid(row = 0, column = 10, padx = 5, pady = 5, sticky = "ew")

        

        self.current_row += 1

        row_frame.bind("<Button-1>", lambda _, t_id = trade_id, f=row_frame: self.select_trade(t_id, f))

        for child in row_frame.winfo_children():
            child.bind("<Button-1>", lambda _, t_id = trade_id, f=row_frame: self.select_trade(t_id, f))



        row_frame.bind("<Double-Button-1>", lambda _, t_id = trade_id: self.app.open_edit_trade_window(t_id))
        for child in row_frame.winfo_children():
            child.bind("<Double-Button-1>", lambda _, t_id = trade_id: self.app.open_edit_trade_window(t_id))





    def select_trade(self, trade_id, f):
        if self.selected_trade_frame is not None and self.selected_trade_frame.winfo_exists():
            self.selected_trade_frame.configure(fg_color = "transparent")
        f.configure(fg_color = "#3a3a3a")
        self.selected_trade_id = trade_id
        self.selected_trade_frame = f






    def load_trades(self):
        
        rows = self.app.db.get_all_trades()
        for row in rows:
            self.add_row(
                    trade_id = row[0],
                    val_date = row[1],
                    val_assets = row[2],
                    val_direction = row[3],
                    val_lot_size = row[5],
                    val_entry_price = row[6],
                    val_exit_price = row[7],
                    val_sl = row[8],
                    val_rr = row[9],
                    val_is_closed = row[10],
                    val_outcome = row[11],
                    val_profit = row[12],
                    val_broker = row[13],
                    )

        self.app.update_statistics()




    def clear_table(self):
        for widget in self.winfo_children():
            if widget != self.header_frame:
                widget.destroy()

        self.current_row = 1



    def refresh_text(self):
        self.lbl_date.configure(text = self.app.get_text("table", "lbl_date"))
        self.lbl_asset.configure(text = self.app.get_text("table", "lbl_asset"))
        self.lbl_direction.configure(text = self.app.get_text("table", "lbl_direction"))
        self.lbl_lot_size.configure(text = self.app.get_text("table", "lbl_lot_size"))
        self.lbl_entry_price.configure(text = self.app.get_text("table", "lbl_entry_price"))
        self.lbl_result.configure(text = self.app.get_text("table", "lbl_result"))
        self.lbl_broker.configure(text = self.app.get_text("table", "lbl_broker"))

        self.clear_table()
        self.load_trades()






