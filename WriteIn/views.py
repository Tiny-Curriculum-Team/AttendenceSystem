import cv2
import yaml
from .models import Number
from ultralytics import YOLO
from datetime import datetime
from django.http import JsonResponse


GLOBAL_DATA = yaml.load(open('../config.yml'), Loader=yaml.FullLoader)
AMOUNT = 0
STATE = 1


# Create your views here.
def start_record(request):
    global STATE
    STATE = 1
    while STATE == 1:
        now = datetime.now().strftime("%m:%d:%H:%M")
        cap = cv2.VideoCapture(GLOBAL_DATA['CAMERA_ID'])
        ret, frame = cap.read()
        data = inference(frame)
        wirte_into_db(now, data)
        print("#" * 255, '\n', now, "-----", data)
    return JsonResponse({
        "Finished recording."
    })


def stop_record(request):
    global STATE
    STATE = 0
    return JsonResponse({f"Stopped recording! State: {STATE}"})


def wirte_into_db(time, amount: int):
    new_data = Number(count=amount,date_time=time)
    new_data.save()


def inference(stream):
    amount = 0
    model = YOLO('./ultralytics/models/yolov8n.yaml').load("./ultralytics/yolo/v8/models/best.pt")
    inputs = [stream]  # images data
    results = model(inputs)  # list of Results objects

    for n, result in enumerate(results):
        boxes = result.boxes  # Boxes object for bbox outputs
        amount += list(boxes.cls).count(5.)  # The category of person in the tensor is 5.
        # amount = list(boxes.cls).count(5.)  # The category of person in the tensor is 5.
        print(f"Person : {list(boxes.cls).count(5.)}")

    return amount
