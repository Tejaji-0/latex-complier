import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import subprocess
import os

class LatexCompilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LaTeX Compiler with Preview")
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        self.filename = "document"

        # Text Area
        self.text_area = scrolledtext.ScrolledText(root, width=80, height=20)
        self.text_area.pack(padx=10, pady=10)

        # Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.compile_btn = tk.Button(self.button_frame, text="Compile & Preview", command=self.compile_and_preview)
        self.compile_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(self.button_frame, text="Save PDF", command=self.save_pdf)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        # Preview Area
        self.preview_label = tk.Label(root)
        self.preview_label.pack(pady=10)

    def compile_and_preview(self):
        latex_code = self.text_area.get("1.0", tk.END)
        tex_file = os.path.join(self.output_dir, f"{self.filename}.tex")
        pdf_file = os.path.join(self.output_dir, f"{self.filename}.pdf")

        with open(tex_file, 'w') as f:
            f.write(latex_code)

        try:
            subprocess.run(
                [r'C:\Users\psmsw\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe', '-interaction=nonstopmode', f"{self.filename}.tex"],
                cwd=self.output_dir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            messagebox.showinfo("Success", "Compiled successfully!")
            self.show_preview(pdf_file)
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Compilation failed. Check your LaTeX code!")

    def show_preview(self, pdf_path):
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)  # Load first page
        pix = page.get_pixmap()
        img_data = pix.tobytes("png")

        # Load image into PIL then Tkinter
        img = Image.open(fitz.open("png", img_data))
        img.thumbnail((600, 800))
        self.tk_img = ImageTk.PhotoImage(img)
        self.preview_label.config(image=self.tk_img)
        doc.close()

    def save_pdf(self):
        src_pdf = os.path.join(self.output_dir, f"{self.filename}.pdf")
        if not os.path.exists(src_pdf):
            messagebox.showwarning("No PDF", "Please compile first!")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")])
        if save_path:
            with open(src_pdf, 'rb') as src, open(save_path, 'wb') as dst:
                dst.write(src.read())
            messagebox.showinfo("Saved", f"PDF saved to {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LatexCompilerApp(root)
    root.mainloop()
