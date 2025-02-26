import tkinter as tk
from tkinter import filedialog, messagebox
from stegano.lsb import hide, reveal
from PIL import Image, ImageTk

class StegoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Steganography Tool")
        self.master.geometry("800x600")
        self.master.configure(bg="#1E1E1E")

        # Main Frame
        main_frame = tk.Frame(master, bg="#252526", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title Label
        tk.Label(main_frame, text="Image Steganography", font=("Arial", 22, "bold"), fg="#61DAFB", bg="#252526").pack(pady=10)
        
        # Image Display Area
        self.image_frame = tk.Frame(main_frame, bg="#2D2D30", relief=tk.RIDGE, bd=3)
        self.image_frame.pack(pady=10)
        self.img_label = tk.Label(self.image_frame, bg="#2D2D30", width=50, height=15)
        self.img_label.pack()

        # Buttons and Entry Field
        control_frame = tk.Frame(main_frame, bg="#252526")
        control_frame.pack(pady=10)
        
        self.btn_load = tk.Button(control_frame, text="Choose Image", command=self.load_image, font=("Arial", 12), bg="#007ACC", fg="white", width=20)
        self.btn_load.grid(row=0, column=0, padx=10, pady=5)
        
        self.message_box = tk.Entry(control_frame, width=50, font=("Arial", 12))
        self.message_box.grid(row=1, column=0, padx=10, pady=5)
        self.message_box.insert(0, "Enter your secret message...")
        
        self.btn_encrypt = tk.Button(control_frame, text="Hide Message", command=self.encode_message, font=("Arial", 12), bg="#E74C3C", fg="white", width=20)
        self.btn_encrypt.grid(row=2, column=0, padx=10, pady=5)
        
        self.btn_decrypt = tk.Button(control_frame, text="Extract Message", command=self.decode_message, font=("Arial", 12), bg="#2ECC71", fg="white", width=20)
        self.btn_decrypt.grid(row=3, column=0, padx=10, pady=5)
        
        self.image_path = None

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg;*.jpeg")])
        if self.image_path:
            img = Image.open(self.image_path).resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            self.img_label.config(image=img_tk, bg="#2D2D30")
            self.img_label.image = img_tk  # Prevent garbage collection

    def encode_message(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first!")
            return

        message = self.message_box.get().strip()
        if not message or message == "Enter your secret message...":
            messagebox.showerror("Error", "Please enter a valid message!")
            return
        
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if not save_path:
            return

        try:
            hidden_img = hide(self.image_path, message)
            hidden_img.save(save_path)
            messagebox.showinfo("Success", "Message hidden successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encrypt: {e}")

    def decode_message(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
        
        try:
            extracted_msg = reveal(self.image_path)
            if extracted_msg:
                messagebox.showinfo("Hidden Message", extracted_msg)
            else:
                messagebox.showwarning("Warning", "No hidden message found!")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()
