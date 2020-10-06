# import cv2


# videoCaptureObject = cv2.VideoCapture(0)
# result = True
# while(result):
#     ret,frame = videoCaptureObject.read()
#     cv2.imwrite("NewPicture.jpg",frame)
#     result = False
# videoCaptureObject.release()
# cv2.destroyAllWindows()




import cv2
import random

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    # if k%256 == 27:
    #     # ESC pressed
    #     print("Escape hit, closing...")
    #     break
    if k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(random.randint(0, 22))
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        break

cam.release()
cv2.destroyAllWindows()
