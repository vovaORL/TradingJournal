import customtkinter as ctk


class GeneralStatLab(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        self.lbl_pf = self.create_stat_card("Profit Factor", "0.00", 0, 0)
        self.lbl_exp = self.create_stat_card("Математичне очікування", "0.00$", 0, 1)
        self.lbl_avg_win = self.create_stat_card("Середній Плюс (Avg Win)", "+0.00$", 1, 0)
        self.lbl_avg_loss = self.create_stat_card("Середній Мінус (Avg Loss)", "-0.00$", 1, 1)


        self.calculate_statistics()




    def create_stat_card(self, title, default_val, row, col):
        card = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=10)
        card.grid(row = row, column = col, padx = 15, pady = 15, sticky="ew")


        lbl_title = ctk.CTkLabel(card, text = title, font = ("Arial", 16, "bold"), text_color="gray")
        lbl_title.pack(pady = (15, 5))

        lbl_val = ctk.CTkLabel(card, text = default_val, font = ("Arial", 32, "bold"))
        lbl_val.pack(pady = (5, 15))

        return lbl_val







    def calculate_statistics(self):
        trades = self.app.db.get_all_trades()


        gross_profit = 0.0
        gross_loss = 0.0
        win_count = 0
        loss_count = 0

        for t in trades:
            is_closed = t[10]
            if is_closed == 1:
                outcome = t[11]
                profit = float(t[12])

                if outcome == "Win":
                    gross_profit += profit
                    win_count += 1
                elif outcome == "Loss":
                    gross_loss += abs(profit)
                    loss_count += 1

        if gross_loss > 0:
            pf = gross_profit / gross_loss
        else:
            pf = gross_profit if gross_profit > 0 else 0.0


        avg_win = gross_profit / win_count if win_count > 0 else 0.0
        avg_loss = gross_loss / loss_count if loss_count > 0 else 0.0

        
        total_trades = win_count + loss_count
        if total_trades > 0:
            win_rate = win_count / total_trades
            loss_rate = loss_count / total_trades
            expected_payoff = (win_rate * avg_win) - (loss_rate * avg_loss)
        else:
            expected_payoff = 0

        
        self.lbl_pf.configure(text = f"{pf:.2f}", text_color = "#2FA572" if pf >= 1.0 else "#E84A5F")
        self.lbl_avg_win.configure(text = f"+{avg_win:.2f}$", text_color = "#2FA572")
        self.lbl_avg_loss.configure(text = f"-{avg_loss:.2f}$", text_color = "#E84A5F")
        self.lbl_exp.configure(text = f"{expected_payoff:.2f}$", text_color = "#2FA572" if expected_payoff > 0 else "#E84A5F")
