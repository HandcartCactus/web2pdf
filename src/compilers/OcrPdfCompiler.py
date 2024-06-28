from f_is_for_freedom.compilers.Compiler import Compiler


import img2pdf
import ocrmypdf


from typing import List


class OcrPdfCompiler(Compiler):
    def __init__(self, export_path) -> None:
        self.export_path = export_path

    def compile_content(self, content:List[str]):
        with open(self.export_path, 'wb') as file:
            file.write(img2pdf.convert(content))

        ocrmypdf.ocr(self.export_path, self.export_path)

        return self.export_path