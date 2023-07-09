import pytesseract
import cv2
import matplotlib.pyplot as plt

# import keras_ocr
#path_img = '/kaggle/input/hacatohn/test2.jpg'
path_img = '/kaggle/input/hacatohn/boleto.jpg'

def getTextImage(img_path):
    img = cv2.imread(img_path)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = gray_image.shape[:2]
    center = (width/2, height/2)
    rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=90, scale=1)
    rotated_image = cv2.rotate(gray_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    # call imshow() using plt object
    plt.imshow(rotated_image)
  
    # display that image
    plt.show()
    
    textOfImg = pytesseract.image_to_string(rotated_image,lang='eng')
    #textOfImg = pytesseract.image_to_string(gray_image,lang='eng')
    textOfImg = textOfImg.split('\n')
    
    return textOfImg
    # pipiline = keras_ocr.pipeline.Pipeline()
    # pipeline.recognize(['./boleto_qr_1.jpg'])

text = getTextImage(path_img)
print(text)

import re

def cleanData(data):
    regex = re.compile(r'\s')

    #Remove entradas com espaços em branco
    dataCleaned = [i for i in data if not regex.match(i) ]

    #Remove entradas vazias
    dataCleaned = [i for i in dataCleaned if i != '']
    
    return dataCleaned

data = cleanData(text)
print(data)

def getHeaderInfo(arrayData):
    
    header_info = {'bankName':'',
                 'bankCodeReal':'',
                 'bankCodeBoleto':0,
                 'linhaDigitavel':'',
                'valorLinha':0.0,
                }
    
    # O codigo dos bancos pode ser achado nesse site:
    # https://wise.com/br/codigo-do-banco/
    banks =[
        {'bankName':'c6', 'bankCode': 336 },
        {'bankName':'citybank', 'bankCode': 336 },
        {'bankName':'banco do brasil', 'bankCode': 1},
        {'bankName':'inter', 'bankCode': 77},
        {'bankName':'caixa', 'bankCode':104},
        {'bankName':'nu', 'bankCode':260},    
        {'bankName':'itau', 'bankCode':341}, 
        {'bankName':'bradesco', 'bankCode':237}, 
        {'bankName':'santander', 'bankCode':33},     
    ]
    
    # Normalmente o primeiro item da lista que contem o caracter | é
    # a linha
    regex = re.compile(r'.*\|.*')    
    infos_boleto = [i for i in arrayData if  regex.match(i) ]
    infos_boleto = infos_boleto[0].lower().split('|')
    
    # Pega o nome do banco no boleto
    for bank in banks:
        if infos_boleto[0].find(str(bank['bankName'])) != -1:
            header_info['bankName'] = bank['bankName']
            header_info['bankCodeReal'] = bank['bankCode']
            break
    
    # Pega o codigo da linha digitavel
    linhaDigitavel = infos_boleto[-1]
    linhaDigitavel = linhaDigitavel.replace(",", ".")
    header_info['linhaDigitavel'] = linhaDigitavel
    
    # Pega o codigo do boleto na linha digitavel
    codigoBancoBoleto = re.search(r'\d{3}',linhaDigitavel).group()
    header_info['bankCodeBoleto'] = int(codigoBancoBoleto)
    
    #Pega o valor do boleto na linha digitavel
    valor = linhaDigitavel[-10:]
    valor = int(valor)/100
    header_info['valorLinha'] = valor
    
    return header_info
    
header = getHeaderInfo(data)
print(header)

def getPerson(arrayData, namePerson):
    person = {'name':'', 'cpfs':[]}
    nameRegex = re.compile(f'(?i){namePerson}') 
    #cpfRegex = re.compile(r'\d{7}')
    #cpfRegex = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}')
    #cpfRegex = re.compile(r'\d{3}.\d{3}.\d{3}-\d{2}')

    #Remove entradas com espaços em branco
    #cpfs = [i for i in data if cpfRegex.match(i) ]
    #person['cpfs'] = cpfs
    
    #Acha o nome da pessoa
    name = [i for i in data if nameRegex.match(i) ]
    person['name']  = name
    
    return person
    
    
print(getPerson(data, "Giovani"))


def verificaBoleto(bankInfo, name):
    resultadoChecagem = { 'isValid':False,'message':''}
    
    # Checa se o codigo do banco na linha digitavel é o mesmo do banco
    if bankInfo['bankCodeReal'] != bankInfo['bankCodeReal']:
        resultadoChecagem['isValid'] = False
        resultadoChecagem['message'] = f'''O boleto diz ser do {bankInfo['bankName']} porem isso não condiz com o codigo do banco
        voce pode verificar essa imformação no site http://www.buscabanco.com.br/
        '''   

