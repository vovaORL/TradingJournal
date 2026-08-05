import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import datetime



class ChartsTab(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        
        self.grid_columnconfigure(0, weight = 0, minsize = 200)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)


        self.menu_frame = ctk.CTkFrame(self, fg_color = "#2b2b2b", corner_radius=10)
        self.menu_frame.grid(row = 0, column = 0, sticky = "nsew", padx = (15, 5), pady = 15)


        lbl_menu = ctk.CTkLabel(self.menu_frame, text = self.app.get_text("statistic", "choose_chart"), font = ("Arial", 16, "bold"))
        lbl_menu.pack(pady = (20, 10))




        self.btn_equity = ctk.CTkButton(
                self.menu_frame,
                text = self.app.get_text("statistic", "equity_chart"),
                command = self.draw_equity_curve,
                )
        self.btn_equity.pack(pady = 5, padx = 15, fill = "x")




        self.btn_pl_days = ctk.CTkButton(
                self.menu_frame,
                text = self.app.get_text("statistic", "pl_chart"),
                fg_color = "gray",
                )
        self.btn_pl_days.pack(pady = 5, padx = 15, fill = "x")




        self.btn_drawdown = ctk.CTkButton(
                self.menu_frame,
                text = self.app.get_text("statistic", "drawdown_chart"),
                fg_color = "gray",
                )
        self.btn_drawdown.pack(pady = 5, padx = 15, fill = "x")


        self.chart_frame = ctk.CTkFrame(self, fg_color = "#343638", corner_radius=10)
        self.chart_frame.grid(row = 0, column = 1, sticky = "nsew", padx = (5, 15), pady = 15)


        self.current_canvas = None
        self.current_toolbar = None


        self.draw_equity_curve()



    def clear_chart(self):
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None
        if self.current_toolbar:
            self.current_toolbar.destroy()
            self.current_toolbar = None



        plt.close('all')




    def draw_equity_curve(self):
        self.clear_chart()

        trades = self.app.db.get_all_trades()
        valid_trades = []

        for trade in trades:
            if trade[10] == 1:
                try:
                    trade_date = datetime.strptime(trade[1], "%d.%m.%Y")
                except ValueError:
                    try:
                        trade_date = datetime.strptime(trade[1], "%d.%m.%y")
                    except ValueError:
                        continue
                profit = float(trade[12])
                valid_trades.append((trade_date, profit))




        valid_trades.sort(key = lambda x: x[0]) 


        equity = [0.0]

        for _, profit in valid_trades:
            equity.append(equity[-1] + profit)


        x_values = range(len(equity))


        fig, ax = plt.subplots(figsize = (8, 5), dpi = 100)
        fig.patch.set_facecolor('#343638')
        ax.set_facecolor('#2b2b2b')



        for spine in ax.spines.values():
            spine.set_color('gray')

        ax.tick_params(colors = 'white', which = 'both')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')


        ax.plot(x_values, equity, color = '#2FA572', linewidth = 2, marker = 'o', markersize = 4)

        ax.axhline(0, color = 'gray', linestyle = '--', linewidth = 1)


        ax.set_title(f'{self.app.get_text("statistic", "profit_dynamics")}', pad = 15, fontsize = 14, fontweight = 'bold')
        ax.set_xlabel(f'{self.app.get_text("statistic", "number_of_trades")}')
        ax.set_ylabel(f'{self.app.get_text("statistic", "equity")}')
        ax.grid(True, color = 'gray', alpha = 0.3)


        self.current_canvas = FigureCanvasTkAgg(fig, master = self.chart_frame)
        self.current_canvas.draw()


        widget = self.current_canvas.get_tk_widget()
        widget.pack(fill = "both", expand = True, padx = 10, pady = (10, 0))


        self.current_toolbar = NavigationToolbar2Tk(self.current_canvas, self.chart_frame)
        self.current_toolbar.update()
        self.current_toolbar.pack(side = "bottom", fill = "x", padx = 10, pady = 5)
        self.current_toolbar.config(background='#343638')


    def refresh_text(self):
        pass

