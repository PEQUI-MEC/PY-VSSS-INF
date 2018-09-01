import Apolo as Vision
import cv2

apolo = Vision.Apolo()

cap = cv2.VideoCapture(0)

while(True):
    #Captura o frame
    ret, frame = cap.read()

	'''
	Chama as funções do Apolo
	'''
	
	
	#Mostra a imagem
	cv2.namedWindow("ImgPrincipal")
    cv2.imshow('ImgPrincipal',frame)
    
	
	#Encerramento da captura
	if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Faz o release da camera
cap.release()