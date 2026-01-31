import zipfile
from PIL import Image
from fpdf import FPDF
from docx2pdf import convert
from pathlib import Path


class Files:
    def __init__(self, file_path: str):
        self.file = Path(file_path)
        if not self.file.exists():  raise FileNotFoundError(f"{self.file} not found")

    def to_zip(self, zip_name="file.zip"):
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:  zipf.write(str(self.file), arcname=self.file.name)

    def convert_to_pdf(self, output_pdf):
        ext = self.file.suffix.lower()
        if ext == ".docx":  convert(self.file, output_pdf)
        elif ext in (".png", ".jpg", ".jpeg"):
            image = Image.open(self.file)
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            image.save(output_pdf, "PDF", resolution=100)
        elif ext == ".txt":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
            with open(self.file, "r", encoding="utf-8") as file:
                for line in file:
                    pdf.multi_cell(0, 8, line)
            pdf.output(output_pdf)
        else:   raise ValueError(f"Format {ext} is not supported")
