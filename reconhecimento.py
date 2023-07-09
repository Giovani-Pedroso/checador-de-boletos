import re
import cv2
import pytesseract

def t():
    print("afds")

def y():
    print("afds")

def test(hello):
    y()
    t()
    print(f'voce digitou {hello}')

def getTextImage(img_path):
    #Processa a imagem
    img = cv2.imread(img_path)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = gray_image.shape[:2]

    # Roda a imagem para a analize 
    center = (width/2, height/2)
    rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=90, scale=1)
    rotated_image = cv2.rotate(gray_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Essas linhas serven apenas para teste
    # call imshow() using plt object
    # plt.imshow(rotated_image)
    # display that image
    #vplt.show()

    #Pega o texto da imagem
    textOfImg = pytesseract.image_to_string(rotated_image,lang='eng')
    textOfImg = textOfImg.split('\n')

    #Retrona o texto do boleto 
    return textOfImg

# Tira os espaços em branco 
def cleanData(data):
    regex = re.compile(r'\s')

    #Remove entradas com espaços em branco
    dataCleaned = [i for i in data if not regex.match(i) ]

    #Remove entradas vazias
    dataCleaned = [i for i in dataCleaned if i != '']
    
    return dataCleaned

#Pega a informação do header do boleto como o nome do banco e a linha digitavel
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


