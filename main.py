#!/usr/bin/python3
import sys
import logging
import json
import cv2 as cv
from qreader import QReader
from datetime import datetime

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(level=logging.INFO)
    last_capture = datetime(2000,1,1)
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FPS,30)
    qreader = QReader(model_size='n', min_confidence=0.8)

    if not cap.isOpened():
        logger.info("Cannot open camera")

        exit()

    read_codes = {}

    while True:
        if cv.waitKey(1) == ord('q'):
            break

        ret, frame = cap.read()

        if not ret:
            logger.info("Can't receive frame (stream end?). Exiting...")
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        cv.imshow('frame',cv.flip(gray,flipCode=1))
        last_capture = detect_and_decode(qreader, gray, read_codes, last_capture)

    print(json.dumps(read_codes))

    cap.release()
    cv.destroyAllWindows()

    
    sys.exit(0)

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
        logger.info(f"New code detected. Number of read codes: {len(read_codes)}")
    else:
        logger.info("Code already detected")

    return datetime.now()


if __name__ == "__main__":
    main()
