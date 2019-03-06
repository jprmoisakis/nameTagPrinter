#Classe com funções auxiliares da Geração de crachás
import os 
from pdfrw import PdfReader, PdfWriter, PageMerge, PdfDict
import fitz
import shutil

'''
Adiciona o Logo no modelo do crachá em pdf

input:
    File::pdf
    File::png 
output:
    Escrita no arquivo pdf

'''
def adicionaLogo():
    shutil.copy("resources/pdfs/Crachas-A6/Crachа 01 - A6.pdf", "resources/pdfs/cracha.pdf")  
    doc= fitz.open("resources/pdfs/cracha.pdf")
    page = doc[0]                              # página a ser adicionada
    rect = fitz.Rect(170, 210, 400, 300)       # Objeto retangulo onde o logo será adiciona
    pix = fitz.Pixmap("resources/pngs/logo.png")       # imagem
    page.insertImage(rect, pixmap = pix, overlay = True)   # insere imagem
    doc.saveIncr() 

'''
Adiciona e replica o background já com a logo adicionada em um novo pdf, baseado na quantidade
de dados inseridos do form do excel 

input:
    dadosFormatados::string

output:
    Escrita no arquivo

'''
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

'''
Faz o parsing dos dados inseridos, transformando-os em uma lista de dicionarios

Recebe os dados em string linha a linha e a Lista de tags (primeira linha do excel)
retorna uma lista de dicionários com os dados separados por "chave" = "valor" das tags

input:
    dadosLinha::list<string>
    tags :: list<string>
output:
    dadosFormatados ::list<dictionary<string,string>>  ex [{'Nome': 'Abdellatif Bouazza', 'País': 'Brasil', 'Instituição': 'Não Respondeu', 'Email': 'produto+abdellatif@even3.com.br', 'Inscrição': 'Pendente'}]

'''
def parseExcel(dadosLinha,tags):

    dadosFormatados = []
            
    for linha in dadosLinha:
        tagInfo = linha.split('\t')
        dicObj = {}
        for i in range(len(tags)):
            dicObj[tags[i]] = tagInfo[i]
        dadosFormatados.append(dicObj)    
    return dadosFormatados

'''
Substitui o valor das tags no texto que foi inserido pelo usuario 

Recebe o texto, um dicionario dadosFormatadosItem (que corresponde a um item da lista dadosFormatados)
e uma lista de tags, faz a substituição da tag no texto pelo valor das tags
input:
    texto::string
    dadosFormatadosItem:: dictionary<string,string>
    tags :: list<string>
output:
    texto:: string

'''
def substituirTags(texto,dadosFormatadosItem,tags):

    for k in range(len(tags)):
        texto = texto.replace("{{" + tags[k]+ "}}",dadosFormatadosItem[tags[k]])
        
    return texto

'''
Função de tratamento do logo inserido

'''
def handle_uploaded_file(f):
    with open('resources/pngs/logo.png', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)



'''
Substitui o valor das tags no texto que foi inserido pelo usuario para todas as páginas

input:
    dadosFormatados ::list<dictionary<string,string>> 
    textoCracha:: string
    tags::list<string>
output:
    Escrita no arquivo


'''
def adicionaTexto(dadosFormatados,textoCracha,tags):
    doc= fitz.open("resources/pdfs/newfile.pdf")
    for i in range(len(dadosFormatados)):
        if(i >=1):
            itemTextoCracha = substituirTags(textoCracha,dadosFormatados[i],tags)
            #print (itemTextoCracha)
            page = doc[i-1]
            rect = fitz.Rect(170, 350, 430, 700)  
            rc = page.insertTextbox(rect, itemTextoCracha, fontsize = 25,  
                fontname = "Times-Roman",      
                fontfile = None,
                align = 0)     
            doc.saveIncr()
    