import cv2
import numpy as np

cap = cv2.VideoCapture("video.mp4")

# Pega o primeiro frame
if cap.isOpened(): 
    rval, frame = cap.read()
else:
    rval = False

while rval:

    img = frame

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definição dos valores minimo e max da mascara
    pink_low = np.array([140, 100, 100])
    pink_high = np.array([180, 255, 255])
    yellow_low = np.array([20, 70, 100])
    yellow_high = np.array([40, 255, 255])

    pink_mask = cv2.inRange(hsv, pink_low, pink_high)
    yellow_mask = cv2.inRange(hsv, yellow_low, yellow_high)

    mask = cv2.bitwise_or(pink_mask, yellow_mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB) 

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

    for i in range(2):
        # Desenho do contorno
        cv2.drawContours(img, [contours[i]], -1, (0, 255, 0), 2)

        # Calculo da area
        M = cv2.moments(contours[i])
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            area = cv2.contourArea(contours[i])

            # Calculo das coordenadas do centro de massa
            def calcula_centro_massa(contours):
                M = cv2.moments(contours)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                return cx, cy
            cx1, cy1 = calcula_centro_massa(contours[0])
            cx2, cy2 = calcula_centro_massa(contours[1])

            # Calculo do angulo de inclinação da reta
            delta_y = cy2 - cy1
            delta_x = cx2 - cx1
            angle = np.degrees(np.arctan2(delta_y, delta_x))

            # indicação do centro +
            size = 15
            color = (0, 0, 0)
            cv2.line(img, (cx - size, cy), (cx + size, cy), color, 2)
            cv2.line(img, (cx, cy - size), (cx, cy + size), color, 2)

            # reta entre os centros
            cv2.line(img, (cx1, cy1), (cx2, cy2), (0, 255, 0), 2)
            text = "Angulo de inclinacao: {:.2f} graus".format(angle)
            cv2.putText(frame, text, (170, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            
            print("Objeto {}: Área={} Centro de massa=({}, {})".format(i+1, area, cx, cy))

            text = "Area: {:.2f}".format(area)
            cv2.putText(img, text, (cx-75, cy-130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            text = "Centro: ({}, {})".format(cx, cy)
            cv2.putText(img, text, (cx-80, cy-110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)  

    cv2.imshow("original", frame)
    rval, frame = cap.read()
    key = cv2.waitKey(20)
    if key == 27: # ESC para fechar a janela
        break

cv2.destroyAllWindows()
cap.release()