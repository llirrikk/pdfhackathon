import PyPDF2


def PDFmerge(pdfsAndPositions, output_name):  # pdfsAndPlaces[0] - pdf, pdfsAndPlaces[1] - position
    # pdfsAndPositions = [[pdf, position], [pdf, position], [pdf, position]]

    pdfsAndPositions.sort(key = lambda x: x[1])  # сортируем по номеру

    pdfs = []
    for pdf_pos in pdfsAndPositions:
        pdfs.append(pdf_pos[0])

    pdfWriter = PyPDF2.PdfFileWriter()
    for filename in pdfs:
        pdfFileObj = open(filename, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        for pageNum in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            pdfWriter.addPage(pageObj)

    pdfOutput = open(output_name, 'wb')
    pdfWriter.write(pdfOutput)

    pdfOutput.close()
    pdfFileObj.close()
