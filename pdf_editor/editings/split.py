def PDFsplit(pdf, diapasons, output_nameN):
    # diapasons = [[start, end], [start, end]]          from 0
    pdfFileObj = open(pdf, 'rb')
    infile = PyPDF2.PdfFileReader(pdfFileObj)

    c = 0
    for start, end in diapasons:
        output = PyPDF2.PdfFileWriter()

        for i in range(start, end+1):
            page = infile.getPage(i)
            output.addPage(page)
        with open(output_nameN.format(c), 'wb') as f:
            output.write(f)
        c += 1

    # to ZIP ???????????????