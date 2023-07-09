def checkPdf(something):
    images_from_path = convert_from_path('./boleto.pdf')
    open_cv_image = np.array(images_from_path[0]) 
    open_cv_image = open_cv_image[:, :, ::-1].copy() 
    bd = cv2.barcode.BarcodeDetector()
    # retval_bar, decoded_info_bar, decoded_type, points_bar = bd.detectAndDecode(open_cv_image)
    print(bd.detectAndDecode(open_cv_image))
