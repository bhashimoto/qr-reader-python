import cv2 as cv
from qreader import QReader
from datetime import datetime


def main():
    last_capture = datetime(2000,1,1)
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FPS,30)
    qreader = QReader(model_size='n', min_confidence=0.8)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    read_codes = {}

    while True:
        if cv.waitKey(1) == ord('q'):
            break

        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting...")
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        cv.imshow('frame',cv.flip(gray,flipCode=1))
        last_capture = detect_and_decode(qreader, gray, read_codes, last_capture)

    print(read_codes)

    cap.release()
    cv.destroyAllWindows()

def detect_and_decode(qreader, image, read_codes, last_capture):
    detected = qreader.detect(image=image)
    if len(detected) == 0:
        return last_capture

    if (datetime.now() - last_capture).total_seconds() < 5.0:
        return last_capture
    
    decoded = qreader.decode(image, detected[0])

    if not decoded:
        return last_capture

    if decoded not in read_codes:
        read_codes[decoded] = decoded
        print(f"New code detected. Number of read codes: {len(read_codes)}")
    else:
        print("Code already detected")

    return datetime.now()


if __name__ == "__main__":
    main()
