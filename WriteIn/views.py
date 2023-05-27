from django.http import JsonResponse
from datetime import datetime
import cv2
import yaml

from .models import  Number

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
    return amount
