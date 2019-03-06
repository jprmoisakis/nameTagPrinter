#Classe com funções auxiliares da Geração de crachás
import os 
from pdfrw import PdfReader, PdfWriter, PageMerge, PdfDict
import fitz
import shutil


def adicionaLogo():
    shutil.copy("resources/pdfs/Crachas-A6/Crachа 01 - A6.pdf", "resources/pdfs/cracha.pdf")  
    doc= fitz.open("resources/pdfs/cracha.pdf")
    page = doc[0]                              # choose some page
    rect = fitz.Rect(170, 210, 400, 300)       # where we want to put the image
    pix = fitz.Pixmap("resources/pngs/logo.png")       # any supported image file
    page.insertImage(rect, pixmap = pix, overlay = True)   # insert image
    doc.saveIncr() 


def adicionaBackground(dadosFormatados):

    ipdf = PdfReader('resources/pdfs/sample.pdf')
    wpdf = PdfReader('resources/pdfs/cracha.pdf')

    wmark = PageMerge().add(wpdf.pages[0])[0]
    writer = PdfWriter()
    blank = wpdf.pages[0]
    PageMerge(ipdf.pages[0]).add(wmark).render()

    for i in range(len(dadosFormatados) -1):
        writer.addpage(blank)

    writer.write('resources/pdfs/newfile.pdf')

def parseExcel(dadosLinha,tags):

    dadosFormatados = []
            
    for linha in dadosLinha:
        tagInfo = linha.split('\t')
        dicObj = {}
        for i in range(len(tags)):
            dicObj[tags[i]] = tagInfo[i]
        dadosFormatados.append(dicObj)    
    return dadosFormatados

def substituirTags(text,dadosFormatados,tags):

    for k in range(len(tags)):
        text = text.replace("{{" + tags[k]+ "}}",dadosFormatados[tags[k]])
        
    return text

def handle_uploaded_file(f):
    with open('resources/pngs/logo.png', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
