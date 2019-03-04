from django.shortcuts import render
from django.http import HttpResponse
from geradorCrachas.forms import MyForm
import os 
from pdfrw import PdfReader, PdfWriter, PageMerge, PdfDict
import fitz

# Create your views here.

def index(request):
    if(request.method == 'POST'):
        dadosFormExcel = MyForm(request.POST)    
        if dadosFormExcel.is_valid():
            dadosStr = dadosFormExcel.cleaned_data['tabelaCracha']
            dadosLinha = dadosStr.split('\r\n')
            tags = dadosLinha[0].split('\t')
            dadosFormatados = []
            
            for linha in dadosLinha:
                tagInfo = linha.split('\t')
                dicObj = {}
                for i in range(len(tags)):
                    dicObj[tags[i]] = tagInfo[i]
                dadosFormatados.append(dicObj)
                
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
    image_data = open("newfile.pdf", "rb").read()
    return HttpResponse(image_data, content_type="application/pdf")



def adicionaLogo():
    doc= fitz.open("teste.pdf")
    page = doc[0]                         # choose some page
    rect = fitz.Rect(170, 210, 400, 300)       # where we want to put the image
    pix = fitz.Pixmap("resources/pngs/Untitled.png")        # any supported image file
    page.insertImage(rect, pixmap = pix, overlay = True)   # insert image
    doc.saveIncr() 


def adicionaMarcaDagua():
    ipdf = PdfReader('sample.pdf')
    wpdf = PdfReader('teste.pdf')

    wmark = PageMerge().add(wpdf.pages[0])[0]
    writer = PdfWriter()
    blank = wpdf.pages[0]
    PageMerge(ipdf.pages[0]).add(wmark).render()

    for i in range(10):
        writer.addpage(blank)

    writer.write('newfile.pdf')
