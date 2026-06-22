import customtkinter as ctk
import subprocess
import os

# Set the overall theme to Dark
ctk.set_appearance_mode("Dark")

# File to keep track of lifetime stats
STATS_FILE = "farm_stats.txt"

def get_lifetime_commits():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def update_lifetime_commits(amount):
    current = get_lifetime_commits()
    new_total = current + amount
    with open(STATS_FILE, "w") as f:
        f.write(str(new_total))
    return new_total

def start_farming():
    try:
        count = int(entry.get())
        
        if count <= 0:
            status_label.configure(text="⚠️ Enter a number > 0!", text_color="#ff9900")
            return
            
        status_label.configure(text="⚡ Farming in progress...", text_color="#ff9900")
        log_box.configure(state="normal")
        log_box.delete("1.0", "end")
        log_box.insert("end", f" >>> Launching high-speed commit sequence: targeting {count} iterations...\n\n")
        root.update()
        
        progress_bar.set(0)
        
        for i in range(count):
            current_step = i + 1
            
            # Write to file
            with open("green_farm.txt", "w") as f:
                f.write(f"CustomGUI Farm Pack: {i}\n")
                
            # SAFE SPEED HACK: subprocess.run ensures Windows safely cycles handles 
            # without running out of system memory, while keeping it lightning fast.
            subprocess.run(["git", "add", "green_farm.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "commit", "-m", f"GUI Turbo Pack #{i}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Update GUI progress bar math
            target_progress = current_step / count
            progress_bar.set(target_progress)
            
            # Console logs
            log_box.insert("end", f"[DEPLOYED] Commit #{current_step}/{count}\n")
            log_box.see("end")
            
            # Batch UI updates to keep performance smooth
            if current_step % 5 == 0 or current_step == count:
                root.update()
            
        # Update Stats
        new_total = update_lifetime_commits(count)
        stats_label.configure(text=f"Lifetime Farmed: {new_total}")
        
        status_label.configure(text=f"✅ Farmed {count} commits successfully!", text_color="#1DB954")
        log_box.insert("end", f"\n >>> Operation successful. Tree updated with {count} local commits.\n")
        log_box.configure(state="disabled")
        
    except ValueError:
        status_label.configure(text="⚠️ Please enter a valid number!", text_color="#ff9900")

# --- UI Setup ---
root = ctk.CTk()
root.title("GitHub Graph Planter Pro")
root.geometry("550x520") 
root.configure(fg_color="#121212")

# Header (Deep Violet)
title_label = ctk.CTkLabel(
    root, 
    text="🚀 GITHUB COMMIT FARMER", 
    font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
    text_color="#8a2be2"
)
title_label.pack(pady=20)

# Lifetime Stats
stats_label = ctk.CTkLabel(
    root,
    text=f"Lifetime Farmed: {get_lifetime_commits()}",
    font=ctk.CTkFont(size=14, weight="bold"),
    text_color="#8a2be2"
)
stats_label.pack(pady=5)

# Input Frame
input_frame = ctk.CTkFrame(root, fg_color="transparent")
input_frame.pack(pady=15)

entry_label = ctk.CTkLabel(
    input_frame, 
    text="Number of Commits:", 
    font=ctk.CTkFont(size=13),
    text_color="#ffffff"
)
entry_label.pack(side="left", padx=10)

entry = ctk.CTkEntry(
    input_frame, 
    width=100, 
    font=ctk.CTkFont(size=14),
    border_color="#8a2be2",
    fg_color="#1e1e1e",
    text_color="#ffffff"
)
entry.insert(0, "100")
entry.pack(side="left", padx=10)

# Wider but Thinner Rounded Cyan Progress Bar
progress_bar = ctk.CTkProgressBar(
    root, 
    width=420,                
    height=6,                 
    progress_color="#00ffff", 
    fg_color="#2d2d2d",       
    corner_radius=3           
)
progress_bar.set(0)
progress_bar.pack(pady=10)

# Status Label (Fixed 'slant' keyword argument)
status_label = ctk.CTkLabel(
    root, 
    text="Ready to launch", 
    font=ctk.CTkFont(size=12, slant="italic"),
    text_color="#888888"
)
status_label.pack(pady=5)

# Log Console
log_label = ctk.CTkLabel(root, text="System Log:", font=ctk.CTkFont(size=11), text_color="#aaaaaa")
log_label.pack(anchor="w", padx=50)

log_box = ctk.CTkTextbox(root, width=450, height=130, fg_color="#1e1e1e", border_color="#2d2d2d", text_color="#cccccc", font=ctk.CTkFont(family="Courier", size=11))
log_box.insert("1.0", "System idle. Awaiting user input...\n")
log_box.configure(state="disabled")
log_box.pack(pady=5)

# Farm Button (Spotify Green)
farm_button = ctk.CTkButton(
    root, 
    text="START FARMING", 
    font=ctk.CTkFont(size=14, weight="bold"),
    fg_color="#1DB954",      
    hover_color="#1ed760",  
    text_color="#ffffff",
    height=40,
    corner_radius=8,
    command=start_farming
)
farm_button.pack(pady=20)

root.mainloop()