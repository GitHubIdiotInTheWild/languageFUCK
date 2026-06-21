import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.ndimage import gaussian_filter1d

class GoogleFinancePainter(ctk.CTk):
    # Centralized background color used everywhere
    BG_COLOR = "#000023"

    def __init__(self):
        super().__init__()

        # --- WINDOW CONFIGURATION ---
        self.title("Google Finance")
        self.geometry("800x840") 
        self.resizable(True, True)  
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=self.BG_COLOR) 

        # --- INITIAL DATA STATE MATRIX ---
        self.max_points = 200 
        self.x_data = list(range(self.max_points))
        self.y_data = [50.0] * self.max_points 
        self.yesterday_open_price = 50.0  
        self.is_drawing = False
        self.current_color = "#9aa0a6" 

        # --- ACHIEVEMENTS TRACKING DATABASE ---
        self.unlocked_achievements = set()
        self.achievements_db = {
            "Total Collapse": "Make USD crash so bad it corresponds to 0 of any currency",
            "Sell High, Sell Low, Buy High, Buy Low": "Make an asset the exact amount as the other",
            "Universal Currency": "Make the asset price over a million times worth the other",
            "STONKS UP NOW": "Make the live price double the price of yesterday",
            "Cosmic Fart": "Make the live price .5x the price of yesterday",
            "Downfall": "Make BTC fall below 1,000 USD",
            "WHAT": "Make the live price octuple the price of yesterday"
        }

        # --- TOP HEADER PANEL ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=40, pady=(25, 5))

        self.bread_label = ctk.CTkLabel(self.header_frame, text="Market Summary > USD", 
                                        font=ctk.CTkFont(size=14, family="Arial"), text_color="#9aa0a6")
        self.bread_label.pack(anchor="w")

        self.price_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.price_container.pack(fill="x", anchor="w", pady=2)

        self.price_label = ctk.CTkLabel(self.price_container, text="50.00", 
                                        font=ctk.CTkFont(size=38, weight="bold", family="Arial"), text_color="white")
        self.price_label.pack(side="left")
        
        self.currency_suffix = ctk.CTkLabel(self.price_container, text=" EGP", 
                                            font=ctk.CTkFont(size=18, family="Arial"), text_color="#9aa0a6")
        self.currency_suffix.pack(side="left", anchor="s", padx=5, pady=6)

        self.delta_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.delta_frame.pack(fill="x", padx=40, pady=(0, 15))
        
        self.change_label = ctk.CTkLabel(self.delta_frame, text="0.00 (0.00%) static today", 
                                         font=ctk.CTkFont(size=15, family="Arial"), text_color="#9aa0a6")
        self.change_label.pack(anchor="w")

        # --- MATPLOTLIB STYLING ENGINE ---
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(6, 3), dpi=100)
        self.fig.patch.set_facecolor(self.BG_COLOR)
        self.ax.set_facecolor(self.BG_COLOR)
        
        for spine in ['top', 'right', 'left', 'bottom']:
            self.ax.spines[spine].set_visible(False)
        
        self.ax.grid(True, axis='y', color='#3c4043', linestyle='-', linewidth=0.5)
        self.ax.set_axisbelow(True)
        
        self.ax.set_xlim(0, self.max_points - 1)
        self.ax.set_ylim(0.0, 100.0)
        
        self.ax.set_xticks([0, self.max_points - 1])
        self.ax.set_xticklabels(["Yesterday Open", "Today (Live)"])
        self.ax.tick_params(colors='#9aa0a6', labelsize=10, length=0, pad=10)

        self.line, = self.ax.plot(self.x_data, self.y_data, color=self.current_color, linewidth=2.5)

        self.v_track_line = self.ax.axvline(color='#5f6368', linestyle='--', linewidth=0.8, visible=False)
        self.h_track_line = self.ax.axhline(color='#5f6368', linestyle='--', linewidth=0.8, visible=False)

        self.hover_annotation = self.ax.annotate(
            "", xy=(0, 0), xytext=(15, 15), textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.5", fc="#282a2d", ec="#414448", alpha=0.95),
            fontproperties={"family": "Arial", "size": 10, "weight": "bold"}, color="white"
        )
        self.hover_annotation.set_visible(False)

        # --- CANVAS EMBED PANEL ---
        self.canvas_frame = ctk.CTkFrame(self, fg_color=self.BG_COLOR)
        self.canvas_frame.pack(fill="both", expand=True, padx=25, pady=5)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
        canvas_widget.configure(cursor="cross")

        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('axes_leave_event', self.on_mouse_leave_canvas)

        # --- KEYBOARD SHORTCUT BINDINGS ---
        self.bind("<i>", lambda e: self.adjust_edge_height(index=0, amount=5.0))
        self.bind("<l>", lambda e: self.adjust_edge_height(index=0, amount=-5.0))
        self.bind("<Up>", lambda e: self.adjust_edge_height(index=-1, amount=5.0))
        self.bind("<Down>", lambda e: self.adjust_edge_height(index=-1, amount=-5.0))

        # --- CONVERTER PANEL ---
        self.converter_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.converter_frame.pack(fill="x", padx=40, pady=10)

        self.input_left = ctk.CTkEntry(self.converter_frame, height=54, 
                                       fg_color=self.BG_COLOR, border_color="#3c4043", text_color="white",
                                       font=ctk.CTkFont(size=16))
        self.input_left.insert(0, "1")
        self.input_left.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.input_left.bind("<KeyRelease>", self.on_ticker_or_multiplier_edit)
        
        self.ticker_entry = ctk.CTkEntry(self.input_left, width=70, height=32,
                                         fg_color="#282a2d", border_color="#414448",
                                         text_color="#e8eaed", font=ctk.CTkFont(size=13, weight="bold"),
                                         justify="center")
        self.ticker_entry.insert(0, "USD")
        self.ticker_entry.place(relx=0.96, rely=0.5, anchor="e")
        self.ticker_entry.bind("<KeyRelease>", self.on_ticker_or_multiplier_edit)

        self.input_right = ctk.CTkEntry(self.converter_frame, height=54, 
                                        fg_color=self.BG_COLOR, border_color="#3c4043", text_color="white",
                                        font=ctk.CTkFont(size=16))
        self.input_right.insert(0, "50.00")
        self.input_right.pack(side="left", fill="x", expand=True)
        self.input_right.bind("<KeyRelease>", self.on_value_edit)
        
        self.currency_entry = ctk.CTkEntry(self.input_right, width=70, height=32,
                                           fg_color="#282a2d", border_color="#414448",
                                           text_color="#e8eaed", font=ctk.CTkFont(size=13, weight="bold"),
                                           justify="center")
        self.currency_entry.insert(0, "EGP")
        self.currency_entry.place(relx=0.96, rely=0.5, anchor="e")
        self.currency_entry.bind("<KeyRelease>", self.on_ticker_or_multiplier_edit)

        # --- DYNAMIC NOTIFICATION TOAST FRAME ---
        self.toast_frame = ctk.CTkFrame(self, fg_color="#1d1d1d", border_color="#d4af37", border_width=2, corner_radius=10)
        
        self.toast_title = ctk.CTkLabel(self.toast_frame, text="🏆 ACHIEVEMENT UNLOCKED!", 
                                        font=ctk.CTkFont(size=13, weight="bold", family="Arial"), text_color="#d4af37")
        self.toast_title.pack(anchor="w", padx=15, pady=(8, 2))
        
        self.toast_desc = ctk.CTkLabel(self.toast_frame, text="", 
                                       font=ctk.CTkFont(size=13, family="Arial"), text_color="white", justify="left")
        self.toast_desc.pack(anchor="w", padx=15, pady=(0, 8))

        # --- ADMINISTRATIVE SYSTEM PANEL ---
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.pack(fill="x", padx=40, pady=(10, 20))

        self.reset_btn = ctk.CTkButton(self.controls_frame, text="RESET FLAT LINE", 
                                       fg_color="#3c4043", hover_color="#4f5357", 
                                       width=160, height=38, cursor="hand2",
                                       font=ctk.CTkFont(size=13, weight="bold"),
                                       command=self.reset_chart_to_current_value)
        self.reset_btn.pack(side="right")

    def get_time_string_from_index(self, index):
        total_minutes = int((index / (self.max_points - 1)) * 1440) 
        return f"{total_minutes // 60:02d}:{total_minutes % 60:02d} UTC"

    # --- ENGINE: ACHIEVEMENT CHECKER & EMITTER ---
    def trigger_achievement_toast(self, title):
        if title in self.unlocked_achievements:
            return
        
        self.unlocked_achievements.add(title)
        desc = self.achievements_db[title]
        
        self.toast_desc.configure(text=f"\"{title}\"\n{desc}")
        self.toast_frame.pack(fill="x", padx=40, pady=(0, 10), before=self.controls_frame)
        self.after(4500, lambda: self.toast_frame.pack_forget())

    def run_achievement_evaluation_matrix(self):
        """Checks for all 7 conditions based on asset prices, tickers, and trends."""
        live_price = self.y_data[-1]
        yesterday_price = self.y_data[0]
        ticker_name = self.ticker_entry.get().strip().upper()
        
        try:
            multiplier = float(self.input_left.get()) if self.input_left.get() != "" else 1.0
            total_value = float(self.input_right.get().replace(",", "")) if self.input_right.get() != "" else 0.0
        except ValueError:
            multiplier, total_value = 1.0, 0.0

        # 1. Total Collapse
        if live_price <= 0.0001 or total_value <= 0.0001:
            self.trigger_achievement_toast("Total Collapse")

        # 2. Sell High, Sell Low, Buy High, Buy Low
        if abs(multiplier - 1.0) < 0.00001 and abs(live_price - total_value) < 0.01 and live_price > 0:
            self.trigger_achievement_toast("Sell High, Sell Low, Buy High, Buy Low")

        # 3. Universal Currency (Multiplier makes total value a million times bigger or vice versa)
        if multiplier >= 1000000.0 and live_price > 0:
            self.trigger_achievement_toast("Universal Currency")

        # 4. STONKS UP NOW (Live price is exactly double yesterday's)
        if yesterday_price > 0 and abs(live_price - (yesterday_price * 2.0)) < 0.01:
            self.trigger_achievement_toast("STONKS UP NOW")

        # 5. Cosmic Fart (Live price is half of yesterday's)
        if yesterday_price > 0 and abs(live_price - (yesterday_price * 0.5)) < 0.01:
            self.trigger_achievement_toast("Cosmic Fart")

        # 6. Downfall (BTC falls below 1,000 USD)
        if ticker_name == "BTC" and live_price < 1000.0 and live_price > 0:
            self.trigger_achievement_toast("Downfall")

        # 7. WHAT (Live price octuples / 8x yesterday's price)
        if yesterday_price > 0 and abs(live_price - (yesterday_price * 8.0)) < 0.01:
            self.trigger_achievement_toast("WHAT")

    def update_market_metrics(self, current_price):
        delta = current_price - self.yesterday_open_price
        percentage = (delta / self.yesterday_open_price) * 100.0 if self.yesterday_open_price > 0 else 0.0
        intensity = min(1.0, abs(percentage) / 15.0) 
        
        base_r, base_g, base_b = 0.60, 0.62, 0.65 
        
        if delta > 0:
            r = base_r + (0.11 - base_r) * intensity
            g = base_g + (0.72 - base_g) * intensity
            b = base_b + (0.33 - base_b) * intensity
            self.change_label.configure(text=f"+{delta:,.2f} ({percentage:+.2f}%) ↑ today", text_color="#81c995")
        elif delta < 0:
            r = base_r + (0.95 - base_r) * intensity
            g = base_g + (0.54 - base_g) * intensity
            b = base_b + (0.51 - base_b) * intensity
            self.change_label.configure(text=f"{delta:,.2f} ({percentage:.2f}%) ↓ today", text_color="#f28b82")
        else:
            r, g, b = base_r, base_g, base_b
            self.change_label.configure(text="0.00 (0.00%) static today", text_color="#9aa0a6")

        self.current_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        self.line.set_color(self.current_color)

    def adjust_edge_height(self, index, amount):
        current_val = self.y_data[index]
        new_val = max(0.0, current_val + amount)
        self.y_data[index] = new_val

        if index == 0:
            self.yesterday_open_price = new_val

        self.y_data = list(np.linspace(self.yesterday_open_price, self.y_data[-1], self.max_points))
        self.line.set_ydata(self.y_data)

        base_price = self.y_data[-1]
        try:
            multiplier = float(self.input_left.get()) if self.input_left.get() != "" else 1.0
        except ValueError:
            multiplier = 1.0
        total_calculated_value = base_price * multiplier

        self.price_label.configure(text=f"{base_price:,.2f}")
        self.input_right.delete(0, "end")
        self.input_right.insert(0, f"{total_calculated_value:.2f}")

        self.update_market_metrics(base_price)
        self.run_achievement_evaluation_matrix()

        dynamic_max = max(1.0, max(self.yesterday_open_price, base_price) * 2.0)
        self.ax.set_ylim(0.0, dynamic_max)
        self.canvas.draw_idle()

    def on_value_edit(self, event):
        raw_text = self.input_right.get().replace(",", "")
        if raw_text == "":
            return
        try:
            val_total = float(raw_text)
            multiplier = float(self.input_left.get()) if self.input_left.get() != "" else 1.0
            base_asset_price = max(0.0, val_total / max(0.000001, multiplier))
            
            self.price_label.configure(text=f"{base_asset_price:,.2f}")
            self.yesterday_open_price = self.y_data[0]
            self.y_data = list(np.linspace(self.yesterday_open_price, base_asset_price, self.max_points))
            
            self.line.set_ydata(gaussian_filter1d(self.y_data, sigma=1.5))
            self.update_market_metrics(base_asset_price)
            self.run_achievement_evaluation_matrix()
            
            self.ax.set_ylim(0.0, max(1.0, max(self.yesterday_open_price, base_asset_price) * 2.0))
            self.canvas.draw_idle()
        except ValueError:
            pass

    def on_ticker_or_multiplier_edit(self, event):
        asset_name = self.ticker_entry.get().strip().upper()
        fiat_name = self.currency_entry.get().strip().upper()
        self.bread_label.configure(text=f"Market Summary > {asset_name if asset_name else 'Asset'}")
        self.currency_suffix.configure(text=f" {fiat_name}")
        self.on_value_edit(None)

    def on_press(self, event):
        if event.inaxes == self.ax:
            self.is_drawing = True
            self.paint_point(event.xdata, event.ydata)

    def on_motion(self, event):
        if self.is_drawing and event.inaxes == self.ax:
            self.paint_point(event.xdata, event.ydata)
        
        if event.inaxes == self.ax and not self.is_drawing:
            idx = int(round(event.xdata))
            if 0 <= idx < self.max_points:
                y_val = self.y_data[idx]
                
                self.v_track_line.set_xdata([event.xdata])
                self.h_track_line.set_ydata([y_val])
                self.v_track_line.set_visible(True)
                self.h_track_line.set_visible(True)
                
                fiat_name = self.currency_entry.get().strip().upper()
                try:
                    multiplier = float(self.input_left.get()) if self.input_left.get() != "" else 1.0
                except ValueError:
                    multiplier = 1.0
                
                self.hover_annotation.xy = (event.xdata, y_val)
                self.hover_annotation.set_text(
                    f"Price: {y_val:,.2f}\n"
                    f"Total: {y_val * multiplier:,.2f} {fiat_name}\n"
                    f"Time: {self.get_time_string_from_index(idx)}"
                )
                self.hover_annotation.set_visible(True)
                self.canvas.draw_idle()
        elif event.inaxes != self.ax:
            self.on_mouse_leave_canvas(None)

    def on_mouse_leave_canvas(self, event):
        self.v_track_line.set_visible(False)
        self.h_track_line.set_visible(False)
        self.hover_annotation.set_visible(False)
        self.canvas.draw_idle()

    def on_release(self, event):
        self.is_drawing = False
        self.y_data = list(gaussian_filter1d(self.y_data, sigma=2.0))
        self.line.set_ydata(self.y_data)
        self.update_market_metrics(self.y_data[-1])
        self.run_achievement_evaluation_matrix()
        self.canvas.draw_idle()

    def paint_point(self, mx, my):
        if mx is not None and my is not None:
            idx = int(round(mx))
            if 0 <= idx < self.max_points:
                my_constrained = max(0.0, my)
                self.y_data[idx] = my_constrained
                
                if idx == 0:
                    self.yesterday_open_price = my_constrained

                self.line.set_ydata(self.y_data)
                base_price = self.y_data[-1]
                try:
                    multiplier = float(self.input_left.get()) if self.input_left.get() != "" else 1.0
                except ValueError:
                    multiplier = 1.0
                
                self.price_label.configure(text=f"{base_price:,.2f}")
                self.input_right.delete(0, "end")
                self.input_right.insert(0, f"{base_price * multiplier:.2f}")
                
                self.update_market_metrics(base_price)
                self.v_track_line.set_visible(False)
                self.h_track_line.set_visible(False)
                self.hover_annotation.set_visible(False)
                self.canvas.draw_idle()

    def reset_chart_to_current_value(self):
        current_value = self.y_data[-1]
        self.yesterday_open_price = current_value
        self.y_data = [current_value] * self.max_points
        self.line.set_ydata(self.y_data)
        
        self.ax.set_ylim(0.0, max(1.0, current_value * 2.0))
        try:
            multiplier = float(self.input_left.get()) if self.input_left.get() != "" else 1.0
        except ValueError:
            multiplier = 1.0
        
        self.price_label.configure(text=f"{current_value:,.2f}")
        self.input_right.delete(0, "end")
        self.input_right.insert(0, f"{current_value * multiplier:.2f}")
        
        self.update_market_metrics(current_value)
        self.run_achievement_evaluation_matrix()
        self.canvas.draw_idle()

if __name__ == "__main__":
    app = GoogleFinancePainter()
    app.mainloop()