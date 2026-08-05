import customtkinter as ctk
from stats_module.tab_general import GeneralStatLab
from stats_module.tab_segments import SegmentationTab
from stats_module.tab_charts import ChartsTab


class StatisticsWindow(ctk.CTkToplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        self.title(self.app.get_text('settings', 'btn_statistic'))
        self.geometry("900x700")

        self.transient()
        self.grab_set()

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_1_name = self.app.get_text('settings', 'general_diagnoz')
        self.tab_2_name = self.app.get_text('settings', 'segments')
        self.tab_3_name = self.app.get_text('settings', 'charts')

        self.tabview.add(self.tab_1_name)
        self.tabview.add(self.tab_2_name)
        self.tabview.add(self.tab_3_name)


        self.general_tab = GeneralStatLab(master = self.tabview.tab(self.tab_1_name), app = self.app)
        self.general_tab.pack(fill = "both", expand = True)

        self.segments_tab = SegmentationTab(master = self.tabview.tab(self.tab_2_name), app = self.app)
        self.segments_tab.pack(fill = "both", expand = True)

        self.charts_tab = ChartsTab(master = self.tabview.tab(self.tab_3_name), app = self.app)
        self.charts_tab.pack(fill = "both", expand = True)





    def refresh_text(self):
        self.title(self.app.get_text('settings', 'btn_statistic'))

        self.tabview.rename(self.tab_1_name, self.app.get_text('settings', 'general_diagnoz'))
        self.tabview.rename(self.tab_2_name, self.app.get_text('settings', 'segments'))
        self.tabview.rename(self.tab_3_name, self.app.get_text('settings', 'charts'))

        self.tab_1_name = self.app.get_text('settings', 'general_diagnoz')
        self.tab_2_name = self.app.get_text('settings', 'segments')
        self.tab_3_name = self.app.get_text('settings', 'charts')

        if hasattr(self, "segments_tab") and self.segments_tab.winfo_exists():
            self.general_tab.refresh_text()
        if hasattr(self, "charts_tab") and self.charts_tab.winfo_exists():
            self.charts_tab.refresh_text()
