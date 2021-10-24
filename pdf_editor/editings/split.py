import os
from zipfile import ZipFile
import PyPDF2


def PDFsplit(pdf, diapasons, output_nameN, out_path):
    # diapasons = [[start, end], [start, end]]          from 0
    pdfFileObj = open(pdf, 'rb')
    infile = PyPDF2.PdfFileReader(pdfFileObj)

    zipObj = ZipFile(out_path, 'w')
    c = 0
    for start, end in diapasons:
        output = PyPDF2.PdfFileWriter()

        for i in range(start, end+1):
            page = infile.getPage(i)
            output.addPage(page)
        name = output_nameN.format(c)
        with open(name, 'wb') as f:
            output.write(f)
        zipObj.write(name)
        os.remove(name)
        c += 1
    zipObj.close()
