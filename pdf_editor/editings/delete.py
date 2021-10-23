import PyPDF2


def PDFdelete(pdf, pages_to_delete, output_name):
    pdfFileObj = open(pdf, 'rb')
    infile = PyPDF2.PdfFileReader(pdfFileObj)

    output = PyPDF2.PdfFileWriter()
    for i in range(infile.getNumPages()):
        if i not in pages_to_delete:
            p = infile.getPage(i)
            output.addPage(p)

    with open(output_name, 'wb') as f:
        output.write(f)
