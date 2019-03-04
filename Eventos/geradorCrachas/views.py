from django.shortcuts import render
from django.http import HttpResponse
from geradorCrachas.forms import MyForm
import os 

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
        
            return render(request,'geradorCrachas/home.html',{'form' :dadosFormExcel})

    else:
        form = MyForm()
        return render(request,'geradorCrachas/home.html', {'form' :form})


