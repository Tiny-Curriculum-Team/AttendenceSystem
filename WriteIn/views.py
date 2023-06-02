import cv2
import yaml
import threading
from .models import Number
from ultralytics import YOLO
from datetime import datetime
from django.http import JsonResponse


GLOBAL_DATA = yaml.load(open('./config.yml'), Loader=yaml.FullLoader)
thread_one = None
# def control(num):
#     tmp=num
#     while num == 1:
#         if num == 1:
#             print("111")
#         else :
#             break;


def sub_processor():
    # while True:
    #     now = datetime.now().strftime("%m:%d:%H:%M")
    #     ret, frame = cap.read()
    #     cap = cv2.VideoCapture(GLOBAL_DATA['CAMERA_ID'])
    #     data = inference(frame)
    #     # wirte_into_db(now, data)
    #     print("#" * 255, '\n', now, "-----", data)
    amount = 0
    model = YOLO('../../../ultralytics/models/yolov8.yaml').load("./ultralytics/yolo/v8/models/best.pt")
    try:
        results = model.predict(source=0, stream=True)
    except Exception:
        results = model.predict(source=1, stream=True)

    for n, result in enumerate(results):
        boxes = result.boxes  # Boxes object for bbox outputs
        amount += list(boxes.cls).count(5.)  # The category of person in the tensor is 5.
        # amount = list(boxes.cls).count(5.)  # The category of person in the tensor is 5.
        print(f"Person : {list(boxes.cls).count(5.)}")
    print("!" * 255)


# Create your views here.
def start_record(request):
    global thread_one
    thread_one = threading.Thread(target=sub_processor)
    thread_one.start()
    return JsonResponse({f"Started recording! Thread:{thread_one}"}, safe=False)


def stop_record(request):
    global thread_one
    if thread_one is None:
        return JsonResponse("None threading running!", safe=False)
    else:
        thread_one.stop()
    return JsonResponse({f"Stopped recording! Thread: {thread_one}"}, safe=False)


def wirte_into_db(time, amount: int):
    new_data = Number(count=amount,date_time=time)
    new_data.save()


def inference(stream):
    amount = 0
    model = YOLO('../../../ultralytics/models/yolov8.yaml').load("./ultralytics/yolo/v8/models/best.pt")
    inputs = [stream]  # images data
    print("*" * 255)
    print(type(stream))
    results = model(inputs)  # list of Results objects

    for n, result in enumerate(results):
        boxes = result.boxes  # Boxes object for bbox outputs
        amount += list(boxes.cls).count(5.)  # The category of person in the tensor is 5.
        # amount = list(boxes.cls).count(5.)  # The category of person in the tensor is 5.
        print(f"Person : {list(boxes.cls).count(5.)}")
    print("!" * 255)

    return amount
