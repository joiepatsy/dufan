# dufan joie patsy manajang 16021106116


# import package
import tensorflow as tf
import sys
import cv2
import datetime
import imutils
import pathlib
from data import jp
from yolo_v3 import Yolo_v3
from utils import load_images, load_class_names, draw_boxes, draw_frame
import os

# menonaktifkan eager execution
tf.compat.v1.disable_eager_execution()

base = os.path.dirname(os.path.realpath(__file__)) + '/'

# fungsi inti
def main(vi):

	#mendefinisikan variabel" yang diperlukan  
	
	# variabel tentang ukuran model, batas nilai confidence, lokasi file yang berisi label
	_MODEL_SIZE = (416, 416)
	_MAX_OUTPUT_SIZE = 20
	iou_threshold=0.5
	confidence_threshold=0.5
	class_names = load_class_names(base+'data/labels/coco.names')
	n_classes = len(class_names)    
	
	# variabel yang akan menyimpan jumlah kendaraaan pada seluruh frame yang dideteksi
	buss = 0 
	trucks = 0
	motors = 0
	cars = 0
    
    # variabel yang menyimpan waktu deteksi
	currentDT = datetime.datetime.now()
	now = str(currentDT.day) + "/" + str(currentDT.month) + "/" + str(currentDT.year) + " " + str(currentDT.hour) + ":" + str(currentDT.minute) + ":" +  str(currentDT.second)
    
    # variabel yang menyimpan hasil histori deteksi sebelumnya dan fungsi JP untuk menyimpan hasil deteksi yang baru
	joie = jp()
	datatxt = ''
	datatxt = datatxt + joie.read()
	datatxt = datatxt[0:-1]
	frameIndex = 1

	# mengambil id deteksi saat ini dengan cara menghitung jumlah deteksi yang telah dilakukan sebelumnya
	IDDetection = 1
	for path in pathlib.Path(base + "tf/static/detections").iterdir():
		if path.is_file():
			IDDetection += 1

    #mempersiapkan model untuk melakukan deteksi 
	model = Yolo_v3(n_classes=n_classes, model_size=_MODEL_SIZE, max_output_size=_MAX_OUTPUT_SIZE, iou_threshold=iou_threshold, confidence_threshold=confidence_threshold)
	inputs = tf.compat.v1.placeholder(tf.float32, [1, *_MODEL_SIZE, 3])
	detections = model(inputs, training=False)
	saver = tf.compat.v1.train.Saver(tf.compat.v1.global_variables(scope='yolo_v3_model'))
	with tf.compat.v1.Session() as sess:
		# mengambil pretrain model yolov3 yang telah dikonversi ke dalam model tensorflow
		saver.restore(sess, base + 'weights/model.ckpt')

		# mengambil frame dari file video dan mengambil informasi tentang file video
		cap = cv2.VideoCapture(vi)
		frame_size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		fourcc = cv2.VideoWriter_fourcc(*'X264')
		fps = cap.get(cv2.CAP_PROP_FPS)
		file_name = vi[11:]
		frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
		file_duration = frame_count/fps
		minutes = round(file_duration/60)
		seconds = round(file_duration%60)
		out = cv2.VideoWriter(base + 'tf/static/detections/result-'+str(IDDetection)+'.mp4', fourcc, fps,
                              (int(frame_size[0]), int(frame_size[1])))		

		    # teknik untuk melakukan deteksi pada setiap 160 frame dalam file video
		ftd = [1]
		multiple = 1
		while True: 
			temp = (fps*5) * multiple
			ftd.append(temp)
			multiple+=1
			if(temp>=9600):
				break 

		try:
			# frm merujuk pada setiap frame dalam file video
			# frm2 merujuk pada id dari frame yang akan dilakukan proses deteksi
			frm = 1
			frm2 = 1
			# mengambil setiap frame dalam file video
			while True:
				ret, frame = cap.read()
				if not ret:
					break
				for f in ftd:
					if (frm==int(f)):
						# melakukan resizing
						resized_frame = cv2.resize(frame, dsize=_MODEL_SIZE[::-1], interpolation=cv2.INTER_NEAREST)
						# melakukan deteksi
						detection_result = sess.run(detections, feed_dict={inputs: [resized_frame]})
						# menyimpan jumlah kendaraan yang terdeteksi
						bus, car, truck, motor = draw_frame(frame, frame_size, detection_result, class_names, _MODEL_SIZE)
						cars+=car
						buss+=bus
						trucks+=truck
						motors+=motor
						# menyimpan frame yang dilakukan proses deteksi
						cv2.imwrite(base + "tf/static/frames/frame-"+str(frm2)+"."+str(frm)+"."+str(IDDetection)+".png", frame)
						frm2+=1
				# menampilkan pop up window proses deteksi
				cv2.imshow('Tugas Akhir - Joie', frame)
				# menyimpan video hasil deteksi
				out.write(frame)
				key = cv2.waitKey(1) & 0xFF
				if key == ord('q'):
					break
				frm += 1
		finally:
			cv2.destroyAllWindows()
			cap.release()
			# menyimpan hasil deteksi
			base_length = len(base)+12
			vi = vi[base_length:]
			datatxttemp = ',{"id": "'+str(IDDetection)+'","file_name": "'+str(vi)+'", "date": "'+now+'", "duration": "'+str(minutes)+':'+str(seconds)+'", "cars": "'+str(cars)+'", "truck": "'+str(trucks)+'", "bus": "'+str(buss)+'", "motor": "'+str(motors)+'"}]'
			datatxt = datatxt+datatxttemp
			joie.save(datatxt)

if __name__ == '__main__':
    main(sys.argv[1])