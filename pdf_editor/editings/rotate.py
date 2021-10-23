import PyPDF2


def PDFrotate(origFileName, rotation, output_name): 
    pdfFileObj = open(origFileName, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pdfWriter = PyPDF2.PdfFileWriter()
    for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page)
        pageObj.rotateClockwise(rotation)
        pdfWriter.addPage(pageObj)

    newFile = open(output_name, 'wb')
    pdfWriter.write(newFile)

    pdfFileObj.close()
    newFile.close()
