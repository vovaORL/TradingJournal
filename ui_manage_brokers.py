import customtkinter as ctk


class ManageBrokersFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color = "transparent")
        self.app = app



        self.entry_broker = ctk.CTkEntry(master = self, placeholder_text = self.app.get_text("menu", "broker_name"))
        self.entry_broker.pack(pady = (20, 10), padx = 20, fill = "x")


        self.btn_add = ctk.CTkButton(master = self, text = self.app.get_text("menu", "btn_add"), fg_color = "green", command = self.add_broker)
        self.btn_add.pack(pady = 5, padx = 20, fill = "x")


        self.scroll_frame = ctk.CTkScrollableFrame(master = self)
        self.scroll_frame.pack(pady = 15, padx = 20, fill = "both", expand = True)

        self.load_brokers()





    def load_brokers(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        
        brokers = self.app.db.get_all_brokers()


        for broker in brokers:
            frame = ctk.CTkFrame(self.scroll_frame, fg_color = "transparent")
            frame.pack(fill = "x", pady = 2)

            lbl = ctk.CTkLabel(frame, text = broker, font = ("Arial", 14))
            lbl.pack(side = "left", padx = 10)

            btn_del = ctk.CTkButton(frame, text = "x", width = 30, fg_color = "red", command = lambda name = broker: self.delete_broker(name))
            btn_del.pack(side = "right", padx = 10)





    def add_broker(self):
        broker_name = self.entry_broker.get().strip()
        if broker_name:
            self.app.db.add_broker(broker_name)
            self.entry_broker.delete(0, "end")
            self.load_brokers()

    
    def delete_broker(self, name):
        self.app.db.delete_broker(name)
        self.load_brokers()











