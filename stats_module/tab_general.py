import customtkinter as ctk


class GeneralStatLab(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        self.lbl_title_pf, self.lbl_pf = self.create_stat_card(self.app.get_text("settings", "stats_pf"), "0.00", 0, 0)
        self.lbl_title_exp, self.lbl_exp = self.create_stat_card(self.app.get_text("settings", "stats_exp"), "0.00$", 0, 1) 


        self.lbl_title_net, self.lbl_net = self.create_stat_card(self.app.get_text("settings", "stats_net_profit"), "0.00$", 1, 0)
        self.lbl_title_wr, self.lbl_wr = self.create_stat_card(self.app.get_text("settings", "stats_win_rate"), "0.0%", 1, 1)


        self.lbl_title_avg_win, self.lbl_avg_win = self.create_stat_card(self.app.get_text("settings", "stats_avg_win"), "+0.00$", 2, 0)
        self.lbl_title_avg_loss, self.lbl_avg_loss = self.create_stat_card(self.app.get_text("settings", "stats_avg_loss"), "-0.00$", 2, 1)


        self.lbl_title_total, self.lbl_total = self.create_stat_card(self.app.get_text("settings", "stats_total_trades"), "0", 3, 0)
        self.lbl_title_max, self.lbl_max = self.create_stat_card(self.app.get_text("settings", "stats_max_trades"), "+0.00$ / -0.00$", 3, 1)


        self.calculate_statistics()




    def create_stat_card(self, title, default_val, row, col):
        card = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=10)
        card.grid(row = row, column = col, padx = 15, pady = 15, sticky="ew")


        lbl_title = ctk.CTkLabel(card, text = title, font = ("Arial", 16, "bold"), text_color="gray")
        lbl_title.pack(pady = (15, 5))

        lbl_val = ctk.CTkLabel(card, text = default_val, font = ("Arial", 32, "bold"))
        lbl_val.pack(pady = (5, 15))

        return lbl_title, lbl_val







    def calculate_statistics(self):
        from datetime import datetime, timedelta


        trades = self.app.db.get_all_trades()


        gross_profit = 0.0
        gross_loss = 0.0
        win_count = 0
        loss_count = 0

        max_win = 0.0
        max_loss = 0.0

        
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
            if hasattr(self.app, "custom_start_date") and self.app.custom_start_date:
                limite_date_start = self.app.custom_start_date
                limite_date_end = self.app.custom_end_date


        for t in trades:
            try:
                trade_date = datetime.strptime(t[1], "%d.%m.%Y")
            except ValueError:
                try:
                    trade_date = datetime.strptime(t[1], "%d.%m.%y")
                except ValueError:
                    continue


            if limite_date_start <= trade_date <= limite_date_end:
                is_closed = t[10]
                if is_closed == 1:
                    outcome = t[11]
                    profit = float(t[12])

                    if outcome == "Win":
                        gross_profit += profit
                        win_count += 1
                        if profit > max_win:
                            max_win = profit
                    elif outcome == "Loss":
                        gross_loss += abs(profit)
                        loss_count += 1
                        if abs(profit) > max_loss:
                            max_loss = abs(profit)

        if gross_loss > 0:
            pf = gross_profit / gross_loss
        else:
            pf = gross_profit if gross_profit > 0 else 0.0


        avg_win = gross_profit / win_count if win_count > 0 else 0.0
        avg_loss = gross_loss / loss_count if loss_count > 0 else 0.0

        
        total_trades = win_count + loss_count


        net_profit = gross_profit - gross_loss
        

        if total_trades > 0:
            win_rate = win_count / total_trades
            loss_rate = loss_count / total_trades
            expected_payoff = (win_rate * avg_win) - (loss_rate * avg_loss)
            win_rate_pct = win_rate * 100
        else:
            expected_payoff = 0
            win_rate_pct = 0.0

        
        self.lbl_pf.configure(text = f"{pf:.2f}", text_color = "#2FA572" if pf >= 1.0 else "#E84A5F")
        self.lbl_avg_win.configure(text = f"+{avg_win:.2f}$", text_color = "#2FA572")
        self.lbl_avg_loss.configure(text = f"-{avg_loss:.2f}$", text_color = "#E84A5F")
        self.lbl_exp.configure(text = f"{expected_payoff:.2f}$", text_color = "#2FA572" if expected_payoff > 0 else "#E84A5F")

        self.lbl_net.configure(text = f"{net_profit:.2f}$", text_color = "#2FA572" if net_profit > 0 else "#E84A5F")
        self.lbl_wr.configure(text = f"{win_rate_pct:.1f}%", text_color = "#2FA572" if win_rate_pct > 50 else "#E84A5F")
        self.lbl_total.configure(text = f"{total_trades}", text_color = "white")
        self.lbl_max.configure(text = f"+{max_win:.2f}$ / -{max_loss:.2f}$", text_color = "white")


    def refresh_text(self):
        self.lbl_title_pf.configure(text = self.app.get_text("settings", "stats_pf"))
        self.lbl_title_exp.configure(text = self.app.get_text("settings", "stats_exp"))
        self.lbl_title_avg_win.configure(text = self.app.get_text("settings", "stats_avg_win"))
        self.lbl_title_avg_loss.configure(text = self.app.get_text("settings", "stats_avg_loss"))
        self.lbl_title_net.configure(text = self.app.get_text("settings", "stats_net_profit"))
        self.lbl_title_wr.configure(text = self.app.get_text("settings", "stats_win_rate"))
        self.lbl_title_total.configure(text = self.app.get_text("settings", "stats_total_trades"))
        self.lbl_title_max.configure(text = self.app.get_text("settings", "stats_max_trades"))

