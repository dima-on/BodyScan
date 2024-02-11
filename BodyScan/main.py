import cv2
import mediapipe as mp
import time
import numpy
from PIL import ImageFont, ImageDraw, Image

fontpath = "./CeraProBold.ttf"



mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
cap = cv2.VideoCapture(0)
capVideo = cv2.VideoCapture("Other/DontScan.mp4")

pTime = 0

cap.set(3, 720)
cap.set(3, 480)
dim = (1600, 800)

Tl = 0
Tr = 0
Bl = 0
Br = 0

Timer = 0
pTime = 0
timeCheck = 0

FirstFrameTimer = 0

AnUnCorr = 0


Gl, Gr, Ml, Md = 0, 0, 0, 0

View = 0

print("Запуск Системы")

def calculate_angle(a, b, c, Top, TextPos):
    radians = numpy.arctan2(c.y - b.y, c.x - b.x) - numpy.arctan2(a.y - b.y, a.x - b.x)
    angle = numpy.abs(radians * 180.0 / numpy.pi)

    if angle > 180.0:
        angle = 360 - angle



    if Top == 1:
        vuvodText = int(85 - angle)
    else:
        vuvodText = int(95 - angle)

    if vuvodText < 0:
        vuvodText *= -1

    if TextPos == 0:
        pos = int(b.x * w) - 20, int(b.y * h) - 5
    if TextPos == 1:
        pos = int(b.x * w) - 20, int(b.y * h) - 5
    if TextPos == 2:
        pos = int(b.x * w) - 20, int(b.y * h) + 30
    if TextPos == 3:
        pos = int(b.x * w) - 10, int(b.y * h) + 30

    cv2.putText(img, str(int(angle)),
                (pos), cv2.FONT_HERSHEY_PLAIN, 1.5,
                (0, 242 - vuvodText * 200, vuvodText * 200), 3)


    return angle

def BodyScan():
    return \
        calculate_angle(Point[11], Point[12], Point[24], 1, 0), \
        calculate_angle(Point[12], Point[11], Point[23], 1, 1),\
        calculate_angle(Point[12], Point[24], Point[23], 0, 2), \
        calculate_angle(Point[24], Point[23], Point[11], 0, 3)






while True:
    success, imgDontRevert = cap.read()
    img = cv2.flip(imgDontRevert, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    h, w, c = img.shape


    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        Point = results.pose_landmarks.landmark


        if AnUnCorr == 1:
            Check = 0


            AnTrTl = Gr - Gl
            AnBrBl = Md - Ml

            if AnTrTl < 0:
                AnTrTl *= -1

            if AnBrBl < 0:
                AnBrBl *= -1

            if AnTrTl > 3 and AnTrTl < 9:

                Check = 1

            if AnBrBl > 3 and AnBrBl < 9:

                if Check == 1:
                    Check = 5
                else:
                    Check = 2

            if AnBrBl > 9:
                Check = 3

            if AnTrTl > 9:
                if Check == 3:
                    Check = 6
                else:
                    Check = 4



            if Check == 1:
                View = cv2.imread("Other/Top.png", 1)


            if Check == 2:
                View = cv2.imread("Other/But.png", 1)

            if Check == 3:
                View = cv2.imread("Other/ButF.png", 1)

            if Check == 4:
                View = cv2.imread("Other/TopF.png", 1)

            if Check == 5:
                View = cv2.imread("Other/All.png", 1)

            if Check == 6:
                View = cv2.imread("Other/AllF.png", 1)


            if Check == 0:
                View = cv2.imread("Other/Ok.png", 1)


            timeCheck = 0


        else:
            oldTl = Tl
            oldTr = Tr

            oldBl = Bl
            oldBr = Br

            Tl, Tr, Bl, Br = BodyScan()

            TlSpeed = Tl - oldTl
            if TlSpeed < 0:
                TlSpeed *= -1

            TrSpeed = Tr - oldTr
            if TrSpeed < 0:
                TrSpeed *= -1

            BlSpeed = Bl - oldBl
            if BlSpeed < 0:
                BlSpeed *= -1

            BrSpeed = Br - oldBr
            if BrSpeed < 0:
                BrSpeed *= -1

            font = ImageFont.truetype(fontpath, 70)
            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            draw.text((90, 300), "Не рухайтесь", font=font, fill=(155, 55, 255))
            img = numpy.array(img_pil)

            if TlSpeed < 1.3 and TrSpeed < 1.3 and BlSpeed < 1.3 and BrSpeed < 1.3:

                Timer = time.time()
                timeCheck += Timer - pTime
                pTime = Timer

                if FirstFrameTimer == 1:

                    if timeCheck >= 3 and timeCheck < 5:

                        timeCheck = 0
                        Gl, Gr, Ml, Md = BodyScan()
                        AnUnCorr = 1


                    if 3 - int(timeCheck) > -1:
                        font = ImageFont.truetype(fontpath, 100)
                        img_pil = Image.fromarray(img)
                        draw = ImageDraw.Draw(img_pil)
                        draw.text((280, 380), str(3 - int(timeCheck)), font=font, fill=(155, 55, 255))
                        img = numpy.array(img_pil)

                else:
                    FirstFrameTimer = 1
            else:
                timeCheck = 0
                FirstFrameTimer = 0
            View = img
    else:

        AnUnCorr = 0
        timeCheck = 0

        FirstFrameTimer = 0

        ret, imgVideo = capVideo.read()
        if ret:
            View = imgVideo
        else:

            capVideo.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue





    cv2.imshow("Detect", cv2.resize(View, dim))
    cv2.waitKey(1)