import tkinter as tk
from tkinter import filedialog, messagebox
from encoder import encode_image
from decoder import decode_image
from PIL import ImageTk, Image

# ---------- MAIN APP SETUP ----------
app = tk.Tk()
app.title("StegaX - Image Steganography Tool")
app.geometry("700x650")
app.resizable(False, False)
app.config(bg="#121212")  # Modern Dark Background

selected_file = ""

# ---------- FUNCTIONS (Original Logic Preserved) ----------
def choose_file():
    global selected_file
    file_path = filedialog.askopenfilename(filetypes=[("PNG Images", ".png"), ("JPEG Images", ".jpg *.jpeg")])
    if file_path:
        selected_file = file_path
        # Clean up the filename for display
        filename = file_path.split('/')[-1]
        file_label.config(text=f"Selected: {filename}", fg="#00E676") # Green text on selection
        try:
            img = Image.open(file_path)
            img = img.resize((200, 200), Image.Resampling.LANCZOS) # Better quality resize
            img = ImageTk.PhotoImage(img)
            image_preview.config(image=img, width=200, height=200)
            image_preview.image = img
            image_preview.config(bg="#121212", relief="flat") # Remove borders
        except:
            pass

def encode():
    global selected_file
    if not selected_file:
        messagebox.showwarning("Error", "Please select an image first!")
        return
    secret_message = secret_entry.get()
    if not secret_message:
        messagebox.showwarning("Error", "Please enter a secret message!")
        return
    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    if not output_path:
        return
    try:
        encode_image(selected_file, secret_message, output_path)
        messagebox.showinfo("Success", f"Message encoded successfully!\nSaved at: {output_path}")
        secret_entry.delete(0, tk.END) # Clear input after success
    except Exception as e:
        messagebox.showerror("Error", f"Encoding failed: {str(e)}")

def decode():
    file_path = filedialog.askopenfilename(filetypes=[("PNG Images", ".png"), ("JPEG Images", ".jpg *.jpeg")])
    if not file_path:
        return
    try:
        message = decode_image(file_path)
        messagebox.showinfo("Decoded Message", f"Secret Message:\n\n{message}")
    except Exception as e:
        messagebox.showerror("Error", f"Decoding failed: {str(e)}")

# ---------- HELPER FOR HOVER EFFECTS ----------
def on_enter(e, color):
    e.widget['bg'] = color

def on_leave(e, color):
    e.widget['bg'] = color

# ---------- UI ELEMENTS (Styled & Centered) ----------

# 1. Title (Perfectly Centered)
# We use a container frame to ensure perfect centering
title_frame = tk.Frame(app, bg="#121212")
title_frame.pack(pady=30)

title = tk.Label(title_frame, text="STEGA", font=("Segoe UI", 32, "bold"), fg="#FFFFFF", bg="#121212")
title.pack(side="left")

title_x = tk.Label(title_frame, text="X", font=("Segoe UI", 32, "bold"), fg="#FFD700", bg="#121212") # Gold X
title_x.pack(side="left")

# 2. Image Area
image_preview = tk.Label(app, text="[ Preview Area ]", font=("Consolas", 10), bg="#1E1E1E", fg="gray", width=40, height=15)
image_preview.pack(pady=10)

# 3. File Selection Button
file_btn = tk.Button(app, text="📂 Choose Image", font=("Segoe UI", 12, "bold"), 
                     bg="#333333", fg="white", relief="flat", padx=20, pady=5, command=choose_file)
file_btn.pack(pady=10)
# Hover effect
file_btn.bind ("<Enter>", lambda e: on_enter(e="#444444"))
file_btn.bind ("<Leave>", lambda e: on_leave(e="#333333"))

file_label = tk.Label(app, text="No file selected", font=("Segoe UI", 10), bg="#121212", fg="#888888")
file_label.pack(pady=5)

# 4. Secret Message Input
secret_label = tk.Label(app, text="Enter Secret Message:", font=("Segoe UI", 12), bg="#121212", fg="#FFD700")
secret_label.pack(pady=(20, 5))

secret_entry = tk.Entry(app, font=("Consolas", 12), width=40, bg="#2D2D2D", fg="white", insertbackground="white", relief="flat")
secret_entry.pack(pady=5, ipady=5)

# 5. Action Buttons (Side by Side for better look, or stacked if preferred)
button_frame = tk.Frame(app, bg="#121212")
button_frame.pack(pady=30)

# Encode Button
encode_btn = tk.Button(button_frame, text="🔒 ENCODE", font=("Segoe UI", 12, "bold"), 
                       bg="#00B894", fg="white", relief="flat", width=15, pady=8, command=encode)
encode_btn.pack(side="left", padx=15)
encode_btn.bind ("<Enter>", lambda e: on_enter(e="#00A383"))
encode_btn.bind ("<Leave>", lambda e: on_leave(e="#00B894"))

# Decode Button
decode_btn = tk.Button(button_frame, text="🔓 DECODE", font=("Segoe UI", 12, "bold"), 
                       bg="#6C5CE7", fg="white", relief="flat", width=15, pady=8, command=decode)
decode_btn.pack(side="left", padx=15)
decode_btn.bind ("<Enter>", lambda e: on_enter (e="#5849BE"))
decode_btn.bind ("<Leave>", lambda e: on_leave (e="#6C5CE7"))

# Start the App
app.mainloop()