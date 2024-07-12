#!/usr/bin/python3
import sys
import logging
import json
import cv2 as cv
import pyzbar.pyzbar as pyzbar

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(level=logging.INFO)
    cap = cv.VideoCapture(0)

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

        cv.imshow('frame',cv.flip(frame,flipCode=1))
        detect_and_decode(frame, read_codes)

    print(json.dumps(read_codes))

    cap.release()
    cv.destroyAllWindows()

    
    sys.exit(0)

def detect_and_decode(frame, read_codes):
    decoded = pyzbar.decode(frame)
    for obj in decoded:
        url = str(obj.data, "utf-8")
        if "http" not in url:
            continue
        if url not in read_codes:
            read_codes[url] = url
            logger.info(f"New code added. Total count: {len(read_codes)}. Code added: {url}")
    

if __name__ == "__main__":
    main()
