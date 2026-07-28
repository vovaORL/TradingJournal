import customtkinter as ctk


class GeneralStatLab(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        

        self.lbl_title = ctk.CTkLabel(self, text = self.app.get_text('statistic', 'main_metrics'), font = ('Arial', 20, 'bold'))
        self.lbl_title.pack(pady = 20)
