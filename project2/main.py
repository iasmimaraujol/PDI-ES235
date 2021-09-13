import cv2
import numpy as np
import pafy

#abrindo o vídeo
video_capture = cv2.VideoCapture("/home/iasmim/PycharmProjects/projeto2Iasmim/venv/video/Destiny.mp4")

freezeFrame, erase, mouse_event, borracha  = True, False, False, False

point = (0, 0)

video_width = int(video_capture.get(3))  # largura
video_height = int(video_capture.get(4))  # Altura
mask = np.zeros((video_height, video_width), dtype="uint8")

exhibition_mode = "teste"  # Flag to choose exhibition mode

def mouse_click_event(event, x, y, flags, params):
    global erase, mouse_x, mouse_y, mouse_event
    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        mouse_x, mouse_y = x, y
        mouse_event = True

    elif event == cv2.EVENT_MBUTTONDOWN:
        erase = not erase
        mouse_event = False
    else:
        mouse_event = False


cv2.namedWindow(winname='Freeze Frame')
cv2.setMouseCallback("Freeze Frame", mouse_click_event)
ret, frame = video_capture.read()
freeze_frame = frame.copy()

while video_capture.isOpened():

    while freezeFrame:
        cv2.destroyWindow(exhibition_mode)
        aux = np.array(cv2.imread("video.jpg"))

        if aux.all() != None:
            mask = cv2.imread("video.jpg", cv2.IMREAD_GRAYSCALE)
            freezeFrame = False
            cv2.destroyAllWindows()
            break
        else:
            # Create mask manually
            if mouse_event and not erase:
                if borracha == False:
                    cv2.circle(freeze_frame, (mouse_x, mouse_y), 6, (255, 255, 255), -1)
                    cv2.circle(mask, (mouse_x, mouse_y), 6, 255, -1)
                else:
                    cv2.circle(freeze_frame, (mouse_x, mouse_y), 6, (0,0,0), -1)
                    cv2.circle(mask, (mouse_x, mouse_y), 6, 0, -1)



            elif mouse_event and erase:
                x_, y_ = mouse_x - 10, mouse_y - 10
                freeze_frame[y_:(y_ + 2 * 10), x_:(x_ + 2 * 10)] = frame.copy()[y_:(y_ + 2 * 10), x_:(x_ + 2 * 10)]
                cv2.circle(mask, (mouse_x, mouse_y), 12, 0, -1)


            if cv2.waitKey(30) & 0xFF == ord('m'):
                freezeFrame = False
                cv2.destroyAllWindows()
                print("Exhibition Modes Keys:\n")
                print("----- Original/Inpainted press b ----\n")
                print("----- Original press o -----\n")
                print("----- Inpainted press i -----\n")
                break

            mask_show = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

            frame_show = np.hstack((freeze_frame, mask_show))

            cv2.imshow("Freeze Frame", freeze_frame)
            key = cv2.waitKey(25) & 0xFF
            if key & 0xFF == ord('b'):
                borracha = not borracha



    # Key inputs
    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.imwrite("video.jpg", mask)
        break
    if key == ord('p'):
        freezeFrame = True
        freeze_frame = frame.copy()

    if key == ord('o'):
        exhibition_mode = "Original"
        cv2.destroyAllWindows()
    if key == ord('i'):
        exhibition_mode = "Inpainted"
        cv2.destroyAllWindows()
    if key == ord('b'):
        exhibition_mode = "Original/Inpainted"
        cv2.destroyAllWindows()
    ret, frame = video_capture.read()
    frame_painted = cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)

    if exhibition_mode == "teste":
        frame_show = np.hstack((frame, frame_painted))
    elif exhibition_mode == "Original":
        frame_show = frame
    elif exhibition_mode == "Inpainted":
        frame_show = frame_painted

    frame_show = cv2.resize(frame_show, (960, 500))
    cv2.imshow(exhibition_mode, frame_show)

video_capture.release()
cv2.destroyAllWindows()