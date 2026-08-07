import customtkinter as ctk
from matplotlib.lines import lineStyles
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import datetime


class CustomToolbar(NavigationToolbar2Tk):
    toolitems = (
            ('Home', 'Скинути вигляд', 'home', 'home'),
            ('Pan', 'Переміщення', 'move', 'pan'),
            ('Zoom', 'Лупа', 'zoom_to_rect', 'zoom'),
            ('Save', 'Зберегти', 'filesave', 'save_figure'),
            )



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
                command = self.draw_pl_days
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


        line, = ax.plot(x_values, equity, color = '#2FA572', linewidth = 2, marker = 'o', markersize = 4)

        annot = ax.annotate(
                "", xy=(0,0),
                xytext=(10,10),
                textcoords="offset points",
                bbox = dict(boxstyle="round,pad=0.5", fc = "#2b2b2b",
                ec = "#2FA572", lw = 1),
                color = "white",
                fontsize = 10,
                fontweight = "bold",
                )
        annot.set_visible(False)


        

        def hover(event):
            if event.inaxes == ax:
                cont, ind = line.contains(event)
                if cont:
                    index = ind["ind"][0]
                    x_date, y_date = line.get_data()
                    px, py = x_date[index], y_date[index]

                    annot.xy = (px, py)


                    xlim = ax.get_xlim()
                    ylim = ax.get_ylim()


                    if px > (xlim[0] + xlim[1]) / 2:
                        x_offset = -15
                        ha = "right"
                    else:
                        x_offset = 15
                        ha = "left"

                    if py > (ylim[0] + ylim[1]) / 2:
                        y_offset = -15
                        va = "top"
                    else:
                        y_offset = 15
                        va = "bottom"



                    annot.set_position((x_offset, y_offset))
                    annot.set_ha(ha)
                    annot.set_va(va)



                    txt_trade = self.app.get_text("statistic", "trade")
                    txt_balance = self.app.get_text("statistic", "balance")

                    annot.set_text(f"{txt_trade} {px}\n{txt_balance} {py:.2f}$")
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    if annot.get_visible():
                        annot.set_visible(False)
                        fig.canvas.draw_idle()


            ax.axhline(0, color = 'gray', linestyle = '--', linewidth = 1)

            ax.set_title(f'{self.app.get_text("statistic", "profit_dynamics")}', pad = 15, fontsize = 14, fontweight = "bold")
            ax.set_xlabel(f'{self.app.get_text("statistic", "number_of_trades")}')
            ax.set_ylabel(f'{self.app.get_text("statistic", "equity")}')
            ax.grid(True, color = 'gray', alpha = 0.3)




        fig.canvas.mpl_connect("motion_notify_event", hover)


        fig.tight_layout()


        self.current_canvas = FigureCanvasTkAgg(fig, master = self.chart_frame)
        self.current_canvas.draw()
        widget = self.current_canvas.get_tk_widget()
        widget.pack(fill = "both", expand = True, padx = 10, pady = (10, 0))


        self.current_toolbar = CustomToolbar(self.current_canvas, self.chart_frame)
        self.current_toolbar.update()
        self.current_toolbar.pack(side = "bottom", fill = "x", padx = 10, pady = 5)
        self.current_toolbar.config(background = "#343638")


        for widget in self.current_toolbar.winfo_children():
            widget.config(background = "#343638")
        self.current_toolbar._message_label.config(background = "#343638", foreground = "white")



    def refresh_text(self):
        pass
    




    def draw_pl_days(self):

        self.clear_chart()

        trades = self.app.db.get_all_trades()
        daily_pl = {}

        for trade in trades:
            if trade[10] == 1:
                try:
                    trade_date = datetime.strptime(trade[1], "%d.%m.%Y").date()
                except ValueError:
                    try:
                        trade_date = datetime.strptime(trade[1], "%d.%m.%y").date()
                    except ValueError:
                        continue
                profit = float(trade[12])


                if trade_date not in daily_pl:
                    daily_pl[trade_date] = 0.0
                daily_pl[trade_date] += profit




        sorted_dates = sorted(daily_pl.keys())
        x_labels = [d.strftime("%d.%m.%y") for d in sorted_dates]
        profits = [daily_pl[d] for d in sorted_dates]


        colors = ['#2FA572' if p >= 0 else '#E84A5F' for p in profits]



        fig, ax = plt.subplots(figsize = (8, 5), dpi = 100)
        fig.patch.set_facecolor('#343638')
        ax.set_facecolor('#2b2b2b')



        for spine in ax.spines.values():
            spine.set_color('gray')



        ax.tick_params(color = 'white', which = 'both')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')


        bars = ax.bar(x_labels, profits, color = colors, width = 0.4)

        
        if len(x_labels) == 1:
            ax.set_xlim(-1, 1)


        ax.axhline(0, color = 'gray', linestyle = '--', linewidth = 1)


        ax.set_title(self.app.get_text('statistic', 'pl_chart'), pad = 15, fontsize = 14, fontweight = 'bold')
        ax.set_xlabel(self.app.get_text('statistic', 'date'))
        ax.set_ylabel(self.app.get_text('statistic', 'profit'))


        ax.grid(True, axis = 'y', color = 'gray', alpha = 0.3)
        plt.xticks(rotation = 45)




        annot = ax.annotate(
                text = "",
                xy = (0, 0),
                xytext = (0, 10),
                textcoords = "offset points",
                bbox = dict(boxstyle = "round,pad=0.5", fc = "#2b2b2b", ec = "gray", lw = 1),
                color = "white",
                fontsize = 10,
                fontweight = "bold",
                ha = "center",
                )
        annot.set_visible(False)




        def hover(event):
            if event.inaxes == ax:
                for i, bar in enumerate(bars):
                    cont, _ = bar.contains(event)
                    if cont:
                        x = bar.get_x() + bar.get_width() / 2
                        y = bar.get_height()
                        annot.xy = (x, y)


                        txt_date = x_labels[i]
                        txt_val = profits[i]
                        annot.set_text(f"{txt_date}\n{txt_val:+.2f}$")


                        annot.get_bbox_patch().set_edgecolor(colors[i])
                        annot.set_visible(True)
                        fig.canvas.draw_idle()
                        return
                if annot.get_visible():
                    annot.set_visible(False)
                    fig.canvas.draw_idle()
        fig.canvas.mpl_connect("motion_notify_event", hover)


        fig.tight_layout()


        self.current_canvas = FigureCanvasTkAgg(fig, master = self.chart_frame)
        self.current_canvas.draw()
        widget = self.current_canvas.get_tk_widget()
        widget.pack(fill = "both", expand = True, padx = 10, pady = (10, 0))



        self.current_toolbar = CustomToolbar(self.current_canvas, self.chart_frame)
        self.current_toolbar.update()
        self.current_toolbar.pack(side = "bottom", fill = "x", padx = 10, pady = 5)
        self.current_toolbar.config(background = '#343638')


        for widget in self.current_toolbar.winfo_children():
            widget.config(background = '#343638')
        self.current_toolbar._message_label.config(background = '#343638', foreground = 'white')


