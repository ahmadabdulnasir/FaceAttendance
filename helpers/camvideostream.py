# import the necessary packages
from threading import Thread
import cv2
import time

class CamVideoStream:
	def __init__(self, src=0, name="CameraVideoFeed", loop=False):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.ret, self.frame) = self.stream.read()

		# initialize the thread name
		self.name = name
		self.loop = loop

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, name=self.name, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.ret, self.frame) = self.stream.read()
			if self.loop and not self.ret:
			    print('Video Ends')
			    self.stream.set(cv2.cv2.CAP_PROP_POS_FRAMES, 1)
			time.sleep(1/30)

	def read(self):
		# return the frame most recently read
		return (self.ret, self.frame)

	def stop(self):
	    self.stream.release()
	    # indicate that the thread should be stopped
	    self.stopped = True
