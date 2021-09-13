import cv2 as cv
import numpy as np
import imutils

# começamos definindo o espaço de cores para os vertices
verde = ([0, 200, 110], [50, 240, 150])
green = np.array(verde)

azul = ([0, 220, 120], [13, 250, 170])
blue = np.array(azul)

vermelho = ([100, 230, 200], [130, 255, 240])
red = np.array(vermelho)

roxo = ([130, 210, 200], [168, 255, 230])
purple = np.array(roxo)

# agora abrindo o vídeo
video = cv.VideoCapture("/home/iasmim/UFPE/PDI/projeto1/ProjetoPdi.mp4")
newvideo = cv.VideoCapture("/home/iasmim/UFPE/PDI/projeto1/Destiny.mp4")

(cxp, cyp), (cxg, cyg), (cxb, cyb), (cxr, cyr) = (0, 0), (0, 0), (0, 0), (0, 0)

# definimos os pontos iniciais da imagem
rows1, cols1 = newvideo.get(4), newvideo.get(3)
pts1 = np.float32(
    [[0, 0],
     [cols1, 0],
     [cols1, rows1],
     [0, rows1]]
)

while video.isOpened() and newvideo.isOpened():
    (ret, frame), (ret1, newframe) = video.read(), newvideo.read()

    inputimage1 = frame
    inputimage2 = newframe

    # redimensionando o vídeo
    frame = imutils.resize(frame, 640, 480)

    # aplicando uma gaussiana para suavizar
    frame = cv.GaussianBlur(frame, (15, 15), 0)

    # TRANSFORMANDO para hsv
    frameHsv = cv.cvtColor(frame, cv.COLOR_RGB2HSV)

    # definindo range imagem, minimo, máximo a ser encontrado
    rSeg = cv.inRange(frameHsv, red[0], red[1])
    gSeg = cv.inRange(frameHsv, green[0], green[1])
    bSeg = cv.inRange(frameHsv, blue[0], blue[1])
    pSeg = cv.inRange(frameHsv, purple[0], purple[1])


    #agora vai vou ve se encontro o contorno desejado
    cnt, hred = cv.findContours(rSeg.copy(), cv.RETR_EXTERNAL,
                                cv.CHAIN_APPROX_SIMPLE)
    cntb, hblue = cv.findContours(bSeg.copy(), cv.RETR_EXTERNAL,
                                  cv.CHAIN_APPROX_SIMPLE)
    cntg, hgreen = cv.findContours(gSeg.copy(), cv.RETR_EXTERNAL,
                                   cv.CHAIN_APPROX_SIMPLE)
    cntp, hpurple = cv.findContours(pSeg.copy(), cv.RETR_EXTERNAL,
                                    cv.CHAIN_APPROX_SIMPLE)

    # vamos encontrar a região central e gerar o contorno na circunf
    for pic, cnt in enumerate(cnt):
        arear = cv.contourArea(cnt)
        if arear > 0:
            # It is a circle which completely covers the object with minimum area.
            (xr, yr), raior = cv.minEnclosingCircle(cnt)

            cv.drawContours(frameHsv, cnt, -1, (100, 100, 100), 1)
            # desenhar efetivamente o circulo
            cv.circle(frameHsv, (int(xr), int(yr)), int(raior), (0, 0, 200), 3)
            # pegar o centroide
            R = cv.moments(cnt)
            if R['m00'] == 0:
                cxr = np.nan
                cyr = np.nan
            else:
                cxr = int(R['m10'] / R['m00'])
                cyr = int(R['m01'] / R['m00'])
        cv.imshow('testando', frame)
    for pic, cntb in enumerate(cntb):
        areab = cv.contourArea(cntb)
        if areab > 0:
            # It is a circle which completely covers the object with minimum area.
            (xb, yb), raiob = cv.minEnclosingCircle(cntb)

            cv.drawContours(frameHsv, cntb, -1, (200, 200, 200), 1)

            # desenhar efetivamente o circulo
            cv.circle(frameHsv, (int(xb), int(yb)), int(raiob), (255, 0, 0), 3)
            # pegar o centroide
            b = cv.moments(cntb)
            if b['m00'] == 0:
                cxb = np.nan
                cyb = np.nan
            else:
                cxb = int(b['m10'] / b['m00'])
                cyb = int(b['m01'] / b['m00'])

        cv.imshow('testando', frame)
    for pic, cntg in enumerate(cntg):
        areag = cv.contourArea(cntg)
        if areag > 0:
            # It is a circle which completely covers the object with minimum area.
            (xg, yg), raiog = cv.minEnclosingCircle(cntg)
            cv.drawContours(frameHsv, cntg, -1, (50, 50, 50), 1)
            # desenhar efetivamente o circulo
            cv.circle(frameHsv, (int(xg), int(yg)), int(raiog), (0, 255, 0), 3)
            # pegar o centroide
            g = cv.moments(cntg)
            if g['m00'] == 0:
                cxg = np.nan
                cyg = np.nan
            else:
                cxg = int(g['m10'] / g['m00'])
                cyg = int(g['m01'] / g['m00'])
        cv.imshow('testando', frame)
    for pic, cntp in enumerate(cntp):
        areap = cv.contourArea(cntp)
        if areap > 0:
            # It is a circle which completely covers the object with minimum area.
            (xp, yp), raiop = cv.minEnclosingCircle(cntp)

            cv.drawContours(frameHsv, cntp, -1, (100, 100, 100), 1)

            # desenhar efetivamente o circulo
            cv.circle(frameHsv, (int(xp), int(yp)), int(raiop), (110, 255, 0), 3)
            # pegar o centroide
            p = cv.moments(cntp)
            if p['m00'] == 0:
                cxp = np.nan
                cyp = np.nan
            else:
                cxp = int(p['m10'] / p['m00'])
                cyp = int(p['m01'] / p['m00'])

    # tem que pensar no encerramento do vídeo
    # falta colocar a imagem na região desejada
    pts2 = np.float32(([cxp, cyp], [cxg, cyg], [cxb, cyb], [cxr, cyr]))
    #if pts2.any != np.nan:
    G = cv.getPerspectiveTransform(pts1, pts2)
    # apresentando a perspectiva na tela

    dst = cv.warpPerspective(inputimage2, G, (frame.shape[1], frame.shape[0]), frame,
                             borderMode=cv.BORDER_TRANSPARENT)

    cv.imshow('testando', dst)

    # encerrar o loop
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

# para encerrar o vídeo
video.release()
cv.destroyAllWindows()