import zipfile
import shutil
import hashlib
from pathlib import Path
from PIL import Image
from fpdf import FPDF
from docx2pdf import convert


class Files:
    def __init__(self, file_path: str):
        self.file = Path(file_path)
        if not self.file.exists():  raise FileNotFoundError(f"{self.file} not found")

    def exists(self) -> bool:
        return self.file.exists()

    def info(self) -> dict:
        stat = self.file.stat()
        return {
            "name": self.file.name,
            "extension": self.file.suffix,
            "size_kb": round(stat.st_size / 1024, 2),
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "path": str(self.file.resolve()),
        }

    def copy_to(self, destination):
        shutil.copy(self.file, destination)

    def move_to(self, destination):
        new_path = Path(destination)
        self.file = self.file.rename(new_path)

    def rename(self, new_name):
        new_path = self.file.with_name(new_name)
        self.file.rename(new_path)
        self.file = new_path

    def delete(self):
        self.file.unlink()

    def change_extension(self, new_ext):
        new_path = self.file.with_suffix(new_ext)
        self.file.rename(new_path)
        self.file = new_path

    def read(self):
        if self.file.suffix.lower() != ".txt":
            raise ValueError("Read is only supported for text files")
        return self.file.read_text(encoding="utf-8")

    def write(self, text: str, overwrite: bool = True):
        mode = "w" if overwrite else "a"
        with open(self.file, mode, encoding="utf-8") as f:
            f.write(text)

    def convert_to_pdf(self, output_pdf):
        ext = self.file.suffix.lower()
        if ext == ".docx":
            convert(self.file, output_pdf)
        elif ext in (".png", ".jpg", ".jpeg"):
            image = Image.open(self.file)
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            image.save(output_pdf, "PDF", resolution=100)
        elif ext == ".txt":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
            with open(self.file, "r", encoding="utf-8") as f:
                for line in f:
                    pdf.multi_cell(0, 8, line)
            pdf.output(output_pdf)
        else:
            raise ValueError(f"Format {ext} is not supported")

    def to_zip(self, zip_name="file.zip"):
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(str(self.file), arcname=self.file.name)

    def hash(self, algo="sha256"):
        h = hashlib.new(algo)
        with open(self.file, "rb") as f:
            h.update(f.read())
        return h.hexdigest()

    def is_same(self, other_file):  return self.hash() == Files(other_file).hash()
