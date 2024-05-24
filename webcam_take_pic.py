import cv2 as cv
def take_pic():
	cam = cv.VideoCapture(0)
	ret, frame = cam.read()
	img = cv.cvtColor(frame, cv.COLOR_RGB2RGBA)
	#cv.namedWindow('Detections', cv.WINDOW_NORMAL)
	cv.imwrite("capture.png", img)