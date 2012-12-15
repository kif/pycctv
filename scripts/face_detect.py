import sys
import cv

def detect(image):
    image_size = cv.GetSize(image)

    # create grayscale version
    if image.nChannels == 3:
        grayscale = cv.CreateImage(image_size, 8, 1)
        cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
    else:
        grayscale = image
    # create storage
    storage = cv.CreateMemStorage()
#    cv.ClearMemStorage(storage)

    # equalize histogram
    cv.EqualizeHist(grayscale, grayscale)

    # detect objects
    cascade = cv.Load('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
    faces = cv.HaarDetectObjects(grayscale, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (50, 50))

    if faces:
        print 'face detected!'
        for i, j in faces:
            print i, j
            cv.Rectangle(image, (int(i[0]), int(i[1])),
                         (int(i[0] + i[2]), int(i[1] + i[3])),
                         (0, 255, 0), 3, 8, 0)

if __name__ == "__main__":

    # create windowsc
    cv.NamedWindow('Camera', cv.CV_WINDOW_AUTOSIZE)

    # create capture device
    device = 0  # assume we want first device
    capture = cv.CaptureFromCAM(device)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

    # check if capture device is OK
    if not capture:
        print "Error opening capture device"
        sys.exit(1)

    while 1:
        # do forever

        # capture the current frame
        frame = cv.QueryFrame(capture)
        if frame is None:
            break

        # mirror
#        cv.Flip(frame, None, 1)

        # face detection
        detect(frame)

        # display webcam image
        cv.ShowImage('Camera', frame)

        # handle events
        k = cv.WaitKey(10)

        if k == 0x1b:  # ESC
            print 'ESC pressed. Exiting ...'
            break
