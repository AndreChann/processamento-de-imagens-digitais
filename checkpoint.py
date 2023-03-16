import cv2
import numpy as np

img = cv2.imread('circulo.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Definição dos valores minimo e max da mascara
image_lower_hsv1 = np.array([60,165,225])
image_upper_hsv1 = np.array([87,166,227])
image_lower_hsv2 = np.array([0,130,100])
image_upper_hsv2 = np.array([30,255,255])

mask1 = cv2.inRange(hsv, image_lower_hsv1, image_upper_hsv1)
mask2 = cv2.inRange(hsv, image_lower_hsv2, image_upper_hsv2)

mask = mask1 + mask2

contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i in range(2):

    # Desenho do contorno dos circulos
    cv2.drawContours(img, [contours[i]], -1, (0, 170, 250), 6)

    # Calculo da area
    M = cv2.moments(contours[i])
    area = M['m00']
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

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
   
    cv2.line(img, (cx1, cy1), (cx2, cy2), (255, 0, 0), 3)
    text = "Inclinacao: {:.2f} graus".format(angle)
    cv2.putText(img, text, (cx1-420, cy+200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    print("Objeto {}: Área={} Centro de massa=({}, {})".format(i+1, area, cx, cy)) 

    text = "Area: {:.2f}".format(area)
    cv2.putText(img, text, (cx-65, cy-110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    text = "Centro: ({}, {})".format(cx, cy)
    cv2.putText(img, text, (cx-80, cy-90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

cv2.imshow("Imagem Circulos", img)
cv2.waitKey(0)
cv2.destroyAllWindows()