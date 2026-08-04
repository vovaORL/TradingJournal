import customtkinter as ctk
from datetime import date, datetime, timedelta


class SegmentationTab(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color = "transparent")
        self.app = app


        self.top_frame = ctk.CTkFrame(self, fg_color = "#2b2b2b", corner_radius=10)
        self.top_frame.pack(fill = "x", pady = 15, padx = 15)


        self.var_asset = ctk.BooleanVar(value = True)
        self.var_dir = ctk.BooleanVar(value = False)
        self.var_session = ctk.BooleanVar(value = False)
        self.var_broker = ctk.BooleanVar(value = False)


        self.cb_asset = ctk.CTkCheckBox(
                self.top_frame,
                text = self.app.get_text("statistic", "seg_asset"),
                variable = self.var_asset,
                command = self.calculate_segments
                )
        self.cb_asset.pack(side = "left", padx = 15, pady = 15)


        self.cb_dir = ctk.CTkCheckBox(
                self.top_frame,
                text = self.app.get_text("statistic", "seg_dir"),
                variable = self.var_dir,
                command = self.calculate_segments
                )
        self.cb_dir.pack(side = "left", padx = 15, pady = 15)


        self.cb_session = ctk.CTkCheckBox(
                self.top_frame,
                text = self.app.get_text("statistic", "seg_session"),
                variable = self.var_session,
                command = self.calculate_segments
                )
        self.cb_session.pack(side = "left", padx = 15, pady = 15)




        self.cb_broker = ctk.CTkCheckBox(
                self.top_frame,
                text = self.app.get_text("statistic", "seg_broker"),
                variable = self.var_broker,
                command = self.calculate_segments
                )
        self.cb_broker.pack(side = "left", padx = 15, pady = 15)


        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color = "transparent")
        self.scroll_frame.pack(fill = "both", expand = True, padx = 15, pady = (0, 15))


        self.calculate_segments()







    def calculate_segments(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()


        if not (self.var_asset.get() or self.var_dir.get() or self.var_session.get() or self.var_broker.get()):
            lbl_empty = ctk.CTkLabel(self.scroll_frame, text = self.app.get_text("statistic", "seg_no_selection"), font = ("Arial", 16))
            lbl_empty.pack(pady = 50)
            return

        trades = self.app.db.get_all_trades()



        period_val = self.app.period_var.get()
        now = datetime.now()
        limite_date_start = datetime.min
        limite_date_end = datetime.max


        if period_val == self.app.get_text('settings', 'period_1m'):
            limite_date_start = now - timedelta(days=30)
        elif period_val == self.app.get_text('settings', 'period_3m'):
            limite_date_start = now - timedelta(days=90)
        elif period_val == self.app.get_text('settings', 'period_6m'):
            limite_date_start = now - timedelta(days=180)
        elif period_val == self.app.get_text('settings', 'period_1y'):
            limite_date_start = now - timedelta(days=365)
        elif period_val == self.app.get_text('settings', 'period_custom'):
            if hasattr(self.app, "custom_period_date") and self.app.custom_period_date:
                limite_date_start = self.app.custom_start_date
                limite_date_end = self.app.custom_end_date



        segments_date = {}

        for trade in trades:
            try:
                trade_date = datetime.strptime(trade[1], "%d.%m.%Y")
            except ValueError:
                try:
                    trade_date = datetime.strptime(trade[1], "%d.%m.%y")
                except ValueError:
                    continue




            if limite_date_start <= trade_date <= limite_date_end and trade[10] == 1:
                outcome = trade[11]
                profit = float(trade[12])

                key_parts = []

                if self.var_asset.get(): key_parts.append(str(trade[2]))
                if self.var_dir.get(): key_parts.append(str(trade[3]))
                if self.var_session.get(): key_parts.append(str(trade[4]))
                if self.var_broker.get(): key_parts.append(str(trade[13]))


                segment_name = " | ".join(key_parts)
                
                if segment_name not in segments_date:
                    segments_date[segment_name] = {"profit": 0.0, "wins": 0, "losses": 0}



                segments_date[segment_name]["profit"] += profit
                if outcome == "Win":
                    segments_date[segment_name]["wins"] += 1
                elif outcome == "Loss":
                    segments_date[segment_name]["losses"] += 1





            sorted_segments = sorted(segments_date.items(), key = lambda x: x[1]["profit"], reverse = True)



            for name, date in sorted_segments:
                total_trades = date["wins"] + date["losses"]
                if total_trades == 0: continue


                winrate = (date["wins"] / total_trades) * 100
                net_profit = date["profit"]
                color = "#2FA572" if net_profit >= 0 else "#E84A5F"


                card = ctk.CTkFrame(self.scroll_frame, fg_color = "#343638", corner_radius = 8)
                card.pack(fill = 'x', pady = 5)
                card.grid_columnconfigure(0, weight = 3)
                card.grid_columnconfigure((1, 2, 3), weight = 1)


                lbl_name = ctk.CTkLabel(card, text = name, font = ("Arial", 16, "bold"))
                lbl_name.grid(row = 0, column = 0, padx = 15, pady = 15, sticky = "w")


                lbl_profit = ctk.CTkLabel(card, text = f"{net_profit:+.2f}$", font = ("Arial", 16, "bold"), text_color = color)
                lbl_profit.grid(row = 0, column = 1, padx = 15, pady = 15, sticky = "e")


                lbl_wr = ctk.CTkLabel(card, text = f"{self.app.get_text('statistic', 'seg_wr')} {winrate:.1f}%", font = ("Arial", 14))
                lbl_wr.grid(row = 0, column = 2, padx = 15, pady = 15, sticky = "e")


                lbl_trades = ctk.CTkLabel(card, text = f"{self.app.get_text('statistic', 'seg_trades')} {date['wins']} / {date['losses']}", font = ("Arial", 14))
                lbl_trades.grid(row = 0, column = 3, padx = 15, pady = 15, sticky = "e")




    def refresh_text(self):
        self.cb_asset.configure(text = self.app.get_text("statistic", "seg_asset"))
        self.cb_dir.configure(text = self.app.get_text("statistic", "seg_dir"))
        self.cb_session.configure(text = self.app.get_text("statistic", "seg_session"))
        self.cb_broker.configure(text = self.app.get_text("statistic", "seg_broker"))
        self.calculate_segments()








