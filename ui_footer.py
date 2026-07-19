import customtkinter as ctk

class FooterFrame(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app


        self.bls_footer = ctk.CTkLabel(master = self, text = self.app.get_text("footer", "bls_footer"), font = ("Arial", 14, "bold"))
        self.bls_footer.pack(side = "left", padx = 5)

        self.trades_count = ctk.CTkLabel(master = self, text = self.app.get_text("footer", "trades_count"), font = ("Arial", 14, "bold"))
        self.trades_count.pack(side = "left", padx = 5)


        self.win_trades_footer = ctk.CTkLabel(master = self, text = self.app.get_text("footer", "win_trades"), font = ("Arial", 14, "bold"))
        self.win_trades_footer.pack(side = "left", padx = 5)

        self.lose_trades_footer = ctk.CTkLabel(master = self, text = self.app.get_text("footer", "lose_trades"), font = ("Arial", 14, "bold"))
        self.lose_trades_footer.pack(side = "left", padx = 5)

        self.winrate_footer = ctk.CTkLabel(master = self, text = self.app.get_text("footer", "winrate_footer"), font = ("Arial", 14, "bold"))
        self.winrate_footer.pack(side = "left", padx = 5)


        self.total_lots = ctk.CTkLabel(
                master = self,
                text = self.app.get_text("footer", "total_lots"),
                font = ("Arial", 14, "bold"),

                )
        self.total_lots.pack(side = "left", padx = 5)


    
    def update_display(self, total_trades, winrate, wins, loses, total_lots):

        self.trades_count.configure(text= f"{self.app.get_text('footer', 'trades_count')} {total_trades}")

        self.win_trades_footer.configure(text = f"{self.app.get_text('footer', 'win_trades')} {wins}")

        self.lose_trades_footer.configure(text = f"{self.app.get_text('footer', 'lose_trades')} {loses}")

        self.winrate_footer.configure(text = f"{self.app.get_text('footer', 'winrate_footer')} {winrate:.2f}%")

        balance = self.app.db.get_balance()
        self.bls_footer.configure(text = f"{self.app.get_text('footer', 'bls_footer')} {balance:.2f}₴")

        self.total_lots.configure(text = f"{self.app.get_text('footer', 'total_lots')} {total_lots}")



    def refresh_text(self):
        self.bls_footer.configure(text = self.app.get_text("footer", "bls_footer"))
        self.winrate_footer.configure(text = self.app.get_text("footer", "winrate_footer"))
