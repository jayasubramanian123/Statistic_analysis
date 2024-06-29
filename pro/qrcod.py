import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import qrcode
from PIL import Image, ImageTk

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")

        # Text input for QR code data
        self.label = ttk.Label(root, text="Enter text or URL:", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.text_entry = ttk.Entry(root, width=50, font=("Helvetica", 12))
        self.text_entry.pack(pady=10)

        # Button to generate QR code
        self.generate_button = ttk.Button(root, text="Generate QR Code", command=self.generate_qr_code)
        self.generate_button.pack(pady=10)

        # Button to save QR code
        self.save_button = ttk.Button(root, text="Save QR Code", command=self.save_qr_code)
        self.save_button.pack(pady=10)

        # Canvas to display QR code
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white", bd=2, relief="sunken")
        self.canvas.pack(pady=10)

        # Placeholder for the generated QR code image
        self.img = None

    def generate_qr_code(self):
        # Get the input text
        text = self.text_entry.get()
        if not text:
            messagebox.showwarning("Input Error", "Please enter text or URL to generate QR code.")
            return

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        self.img = qr.make_image(fill_color="black", back_color="white")

        # Convert image to PhotoImage
        img_tk = ImageTk.PhotoImage(self.img.convert("RGB"))

        # Clear previous image
        self.canvas.delete("all")

        # Add image to canvas
        self.canvas.create_image(150, 150, image=img_tk)
        self.canvas.image = img_tk

    def save_qr_code(self):
        if self.img is None:
            messagebox.showwarning("Save Error", "No QR code image to save. Please generate a QR code first.")
            return

        # Ask the user for the file path to save the image
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", ".png"), ("All files", ".*")])
        if file_path:
            self.img.save(file_path)
            messagebox.showinfo("Save Success", f"QR code image saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", background="#f0f0f0")

    app = QRCodeGenerator(root)
    root.mainloop()
