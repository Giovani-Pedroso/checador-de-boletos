import pytesseract
# import keras_ocr

def getTextImage():
    print(pytesseract.image_to_string('./boleto_qr_1.jpg',lang='eng'))
    # pipiline = keras_ocr.pipeline.Pipeline()
    # pipeline.recognize(['./boleto_qr_1.jpg'])
    print("Hellp")

getTextImage()
