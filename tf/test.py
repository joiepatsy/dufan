
# import tensorflow as tf
# import sys
# import cv2
# import datetime
# import imutils
# import pathlib
# from data import jp
# from yolo_v3 import Yolo_v3
# from utils import load_images, load_class_names, draw_boxes, draw_frame
# import pprint
# tf.compat.v1.disable_eager_execution()
# vi = 'C:/Users/Joie/Desktop/ta_dufan/data/video/boulevard.mp4'
# def main(vi):
# 	_MODEL_SIZE = (416, 416)
# 	_MAX_OUTPUT_SIZE = 20
# 	iou_threshold=0.5
# 	confidence_threshold=0.5
# 	class_names = load_class_names('./data/labels/coco.names')
# 	n_classes = len(class_names)    
# 	pp = pprint.PrettyPrinter(indent=4)
# 	frameIndex = 1
# 	ftd = [1]
# 	multiple = 1
# 	while True: 
# 		temp = 160* multiple
# 		ftd.append(temp)
# 		multiple+=1
# 		if(temp>=9600):
# 			break 

# 	model = Yolo_v3(n_classes=n_classes, model_size=_MODEL_SIZE, max_output_size=_MAX_OUTPUT_SIZE, iou_threshold=iou_threshold, confidence_threshold=confidence_threshold)
# 	inputs = tf.compat.v1.placeholder(tf.float32, [1, *_MODEL_SIZE, 3])
# 	detections = model(inputs, training=False)
# 	saver = tf.compat.v1.train.Saver(tf.compat.v1.global_variables(scope='yolo_v3_model'))
# 	with tf.compat.v1.Session() as sess:
# 		saver.restore(sess, './weights/model.ckpt')
# 		cap = cv2.VideoCapture(vi)
		
# 		try:
# 			frm = 1
# 			while True:
# 				ret, frame = cap.read()
# 				if not ret:
# 					break
# 				for f in ftd:
# 					if (frm==int(f)):
# 						resized_frame = cv2.resize(frame, dsize=_MODEL_SIZE[::-1], interpolation=cv2.INTER_NEAREST)
# 						detection_result = sess.run(detections, feed_dict={inputs: [resized_frame]})
# 						pp.pprint(detection_result)
# 						print('--------------------------------------------------------------------------')
# 						pp.pprint(detection_result[0])
# 				cv2.imshow('Tugas Akhir - Joie', frame)
# 				key = cv2.waitKey(1) & 0xFF
# 				break
# 		finally:
# 			cv2.destroyAllWindows()
# 			cap.release()

# main(vi)

# 2 car,7 truck,5 bus,3 motor


# import cv2
# vi = 'C:/Users/Joie/Desktop/TA/ta_dufan/data/videos/video1.mp4'
# def main(vi):
# 	cap = cv2.VideoCapture(vi)
# 	frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# 	print(frame_count)
# main(vi)

# import os, pathlib
# base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"
# base_length = len(base)+12
# videolist = []
# for path in pathlib.Path(base+"data/videos").iterdir():
# 	path = str(path)
# 	videolist.append(path[base_length:])

# print(videolist)



# import os
# base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"

# print(len(base))
# base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\'
# print(base)