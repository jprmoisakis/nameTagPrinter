from django.shortcuts import render
from django.http import HttpResponse
from geradorCrachas.forms import MyForm
import geradorCrachas.utils as util
from pdfrw import PdfReader, PdfWriter, PageMerge, PdfDict
import fitz

def index(request):
    if(request.method == 'POST'):
        dadosFormExcel = MyForm(request.POST,request.FILES)  
  
        if dadosFormExcel.is_valid():
            
            #extracao dos dados do formulário
            textoCracha = dadosFormExcel.cleaned_data['textoCracha']
            dadosStr = dadosFormExcel.cleaned_data['tabelaCracha']
            util.handle_uploaded_file(request.FILES['logoInput'])
            
            #tratamento dos dados
            dadosLinha = dadosStr.split('\r\n')
            tags = dadosLinha[0].split('\t')
            dadosFormatados = util.parseExcel(dadosLinha,tags)
                
            print(dadosFormatados)            
        
            #Manipulação do pdf

            util.adicionaLogo()

            util.adicionaBackground(dadosFormatados)
            doc= fitz.open("resources/pdfs/newfile.pdf")

            for i in range(len(dadosFormatados)):
                if(i >=1):
                    itemTextoCracha = util.substituirTags(textoCracha,dadosFormatados[i],tags)
                    
                    print (itemTextoCracha)
                    
                    page = doc[i-1]
                    rect = fitz.Rect(170, 350, 430, 700)   # rectangle (left, top, right, bottom) in pixels
                    rc = page.insertTextbox(rect, itemTextoCracha, fontsize = 25, # choose fontsize (float) 0- 
                        fontname = "Times-BoldItalic",       # a PDF standard font
                        fontfile = None,                # could be a file on your system
                        align = 0)     
                    doc.saveIncr()

            return render(request,'geradorCrachas/home.html',{'form' :dadosFormExcel})

    else:
        form = MyForm()
        return render(request,'geradorCrachas/home.html', {'form' :form})

def pdfPreview(request):
    image_data = open("resources/pdfs/newfile.pdf", "rb").read()
    return HttpResponse(image_data, content_type="application/pdf")

