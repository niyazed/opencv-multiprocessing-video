'''
Multithreaded video processing sample.
Usage:
   video_threaded.py {<video device number> | default set to 0}

   Shows how python threading capabilities can be used
   to organize parallel captured frame processing pipeline
   for smoother playback.

Keyboard shortcuts:

   Press 'q' to  exit
   
'''


import argparse
import os
import cv2
import imutils

from VideoGet import VideoGet
from VideoShow import VideoShow
import multiprocessing as mp


def threadBoth(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = imutils.resize(frame, width=1080)
        video_shower.frame = frame

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", "-s", default=0,
        help="Path to video file or integer representing webcam index"
            + " (default 0).")
    args = vars(ap.parse_args())

    # If source is a string consisting only of integers, check that it doesn't
    # refer to a file. If it doesn't, assume it's an integer camera ID and
    # convert to int.
    if (
        isinstance(args["source"], str)
        and args["source"].isdigit()
        and not os.path.isfile(args["source"])
    ):
        args["source"] = int(args["source"])


    # Paralle the execution of a function across multiple input values
    num_processes = mp.cpu_count()
    p = mp.Pool(num_processes)
    p.map(threadBoth(args["source"]), range(num_processes))
    

if __name__ == "__main__":
    print(__doc__)
    main()
