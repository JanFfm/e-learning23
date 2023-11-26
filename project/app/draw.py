import matplotlib
from matplotlib import pyplot as plt
from matplotlib.dates import date2num, DateFormatter

from io import BytesIO
import base64
from datetime import datetime, timedelta

from .models import ProgressPerHour, TimeStamp

matplotlib.use('Agg') 

def get_time_char(user_stat_over_time: ProgressPerHour):
    times = []
    correct = []
    total =[]
    for u in user_stat_over_time:
        times.append(u.time_stamp)
        correct.append(u.correct_count)
        total.append(u.count)
        
    maximum = max(total)
    datetimes = [datetime.combine(timestamp.date, datetime.min.time()) + timedelta(hours=timestamp.hour) for timestamp in times]


    
    plt.plot(datetimes, correct, label='Richtige Antworten')
    plt.plot(datetimes, total, label='Beantwortete Fragen Insgesamt')


    plt.gca().xaxis.set_major_formatter(DateFormatter('%d.%m %H:00'))
    plt.xticks(datetimes)


    plt.legend()
    
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    
    image = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image


def get_best_of_this_hour(user):
    time_stamp,_ = TimeStamp.objects.get_or_create(date=datetime.now().today().date(), hour=datetime.now().hour) 
    progress = ProgressPerHour.objects.filter(time_stamp=time_stamp)
    
    ratios_per_user =[]
    for p in progress:
        try:
            ratios_per_user.append((p.correct_count/p.count, p.user.username))
        except ZeroDivisionError:
            ratios_per_user.append((0, p.user.username))
    ratios, users  = zip(*sorted(ratios_per_user, key=lambda x: x[0]))
    
    plt.bar(users, ratios)
    #plt.xticks(users)

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    
    image = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image