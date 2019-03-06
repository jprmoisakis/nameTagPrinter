from django.shortcuts import render
from django.http import HttpResponse
from geradorCrachas.forms import MyForm
import geradorCrachas.utils as util

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
                
            #print(dadosFormatados)            
        
            #Manipulação do pdf

            util.adicionaLogo()

            util.adicionaBackground(dadosFormatados)
            
            util.adicionaTexto(dadosFormatados,textoCracha,tags)
            image_data = open("resources/pdfs/newfile.pdf", "rb").read()

            return HttpResponse(image_data, content_type="application/pdf")

    else:
        form = MyForm()
        return render(request,'geradorCrachas/home.html', {'form' :form})

#preview do pdf
def pdfPreview(request):
    image_data = open("resources/pdfs/newfile.pdf", "rb").read()
    return HttpResponse(image_data, content_type="application/pdf")

