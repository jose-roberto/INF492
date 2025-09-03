import cv2 as cv
import sys

img = cv.imread(cv.samples.findFile("images/starry_night.jpg"))

if img is None:
    sys.exit("Não foi possível ler a imagem.")

cv.imshow("First image", img)
k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite("images/starry_night.png", img)
    print("Imagem salva com sucesso.")