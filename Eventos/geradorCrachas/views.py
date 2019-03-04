from django.shortcuts import render
from django.http import HttpResponse
from geradorCrachas.forms import MyForm
import os 
from pdfrw import PdfReader, PdfWriter, PageMerge, PdfDict
import fitz
import shutil
# Create your views here.

def handle_uploaded_file(f):
    with open('resources/pngs/logo.png', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):
    if(request.method == 'POST'):
        dadosFormExcel = MyForm(request.POST,request.FILES)  
  
        if dadosFormExcel.is_valid():
            print("shurheuahiua")

            dadosStr = dadosFormExcel.cleaned_data['tabelaCracha']
            handle_uploaded_file(request.FILES['logoInput'])
            dadosFormatados = parseExcel(dadosStr)
                
            print(dadosFormatados)            
        

            #Manipulação do pdf

            adicionaLogo()

            adicionaMarcaDagua()







            return render(request,'geradorCrachas/home.html',{'form' :dadosFormExcel})

    else:
        form = MyForm()
        return render(request,'geradorCrachas/home.html', {'form' :form})


def pdfPreview(request):
    #aa =os.getcwd 
    #print (aa)
    image_data = open("resources/pdfs/newfile.pdf", "rb").read()
    return HttpResponse(image_data, content_type="application/pdf")



def adicionaLogo():
    shutil.copy("resources/pdfs/Crachas-A6/Crachа 01 - A6.pdf", "resources/pdfs/cracha.pdf")  
    doc= fitz.open("resources/pdfs/cracha.pdf")
    page = doc[0]                              # choose some page
    rect = fitz.Rect(170, 210, 400, 300)       # where we want to put the image
    pix = fitz.Pixmap("resources/pngs/logo.png")       # any supported image file
    page.insertImage(rect, pixmap = pix, overlay = True)   # insert image
    doc.saveIncr() 


def adicionaMarcaDagua():
    #os.remove("resources/pdfs/teste.pdf")


    ipdf = PdfReader('resources/pdfs/sample.pdf')
    wpdf = PdfReader('resources/pdfs/cracha.pdf')

    wmark = PageMerge().add(wpdf.pages[0])[0]
    writer = PdfWriter()
    blank = wpdf.pages[0]
    PageMerge(ipdf.pages[0]).add(wmark).render()

    for i in range(10):
        writer.addpage(blank)

    writer.write('resources/pdfs/newfile.pdf')

def parseExcel(dadosStr):
    dadosLinha = dadosStr.split('\r\n')
    tags = dadosLinha[0].split('\t')
    dadosFormatados = []
            
    for linha in dadosLinha:
        tagInfo = linha.split('\t')
        dicObj = {}
        for i in range(len(tags)):
            dicObj[tags[i]] = tagInfo[i]
        dadosFormatados.append(dicObj)    
    return dadosFormatados
