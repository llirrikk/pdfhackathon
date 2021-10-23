from pdf2image import convert_from_path
import os
from zipfile import ZipFile


def PDFtoZIP(pdf: str, output_nameN: str, out_path: str) -> None:

    def get_file_name_without_extension(full_name):
        return os.path.splitext(output_nameN)[0]

    pages = convert_from_path(pdf)
    pdf_name_without_extension = get_file_name_without_extension(output_nameN)

    output_names = []
    zipObj = ZipFile(out_path, 'w')
    c = 0
    for page in pages:
        _name = f'{pdf_name_without_extension.format(c)}.jpg'
        output_names.append(_name)
        page.save(_name, 'JPEG')
        zipObj.write(_name)
        os.remove(_name)
        c += 1
    zipObj.close()
