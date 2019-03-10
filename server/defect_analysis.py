from pydarknet import Detector, Image
import cv2

test_img = "defect/waiting/o_24.7078_120.8954_2019_3_10_18_8_4.jpg"
cfg_path = "cfg.road_server/yolov3.cfg"
weights_path = "cfg.road_server/weights/yolov3_20000.weights"
class_path = "cfg.road_server/obj.names"


net = Detector(bytes(cfg_path, encoding="utf-8"), bytes(weights_path, encoding="utf-8"), 0,
               bytes(class_path, encoding="utf-8"))

start_time = time.time()
img = Image(cv2.imread(test_img))
results = net.detect(img)

end_time = time.time()

print("Elapsed Time:",end_time-start_time)

for cat, score, bounds in results:
    x, y, w, h = bounds
    cv2.rectangle(img, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0))
    cv2.putText(img, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

cv2.imwrite("test.jpg", img)
