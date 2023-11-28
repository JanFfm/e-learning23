import matplotlib
from matplotlib import pyplot as plt
from matplotlib.dates import date2num, DateFormatter
from matplotlib.ticker import StrMethodFormatter
from django.contrib.auth import get_user_model
from PIL import Image

from io import BytesIO
import base64
from datetime import datetime, timedelta

from .models import ProgressPerHour, TimeStamp, Streaks

matplotlib.use('Agg') 

def get_time_char(user_stat_over_time: ProgressPerHour):
    times = []
    correct = []
    total =[]
    for u in user_stat_over_time:
        times.append(u.time_stamp)
        correct.append(u.correct_count)
        total.append(u.count)        
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


def get_best_of_this_hour(this_user):
    time_stamp,_ = TimeStamp.objects.get_or_create(date=datetime.now().today().date(), hour=datetime.now().hour) 
    users = get_user_model().objects.all()
    nearest_progresses = []
    for user in users:
        try:
            progress_list = ProgressPerHour.objects.filter(user=user)
            nearest_progresses.append(min(progress_list, key=lambda p: time_stamp.calculate_time_difference(p.time_stamp)))
        except:
            dummy_progress = ProgressPerHour(user=user, time_stamp=time_stamp)
            nearest_progresses.append(dummy_progress)
    ratios_per_user =[]
    this_users_ratio = 0
    for p in nearest_progresses:
        try:
           
            if p.user.username == this_user.username:
                ratios_per_user.append((p.correct_count/p.count, p.user.username, "r"))
                this_users_ratio = p.correct_count/p.count
            else: 
                ratios_per_user.append((p.correct_count/p.count, p.user.username, "g"))
        except ZeroDivisionError:
                if p.user.username == this_user.username:
                    ratios_per_user.append((0, p.user.username, "r"))
                    this_users_ratio =0
                else: 
                    ratios_per_user.append((0, p.user.username, "g"))
    try:
        ratios_and_users = sorted(ratios_per_user, key=lambda x: x[0])
        if len(ratios_per_user) > 5:
            ratios_and_users  = ratios_and_users[-5:]
        ratios, users, color   = zip(*ratios_and_users)
   
        if len(ratios) > 1: 
            print(this_users_ratio)
            if this_user.username not in users:
                ratios= (this_users_ratio,) + ratios 
                users = (this_user.username,) + users
            plt.bar(users, ratios, color=color)
            #plt.xticks(users)

            image_stream = BytesIO()
            plt.savefig(image_stream, format='png')
            plt.close()
            
            image = base64.b64encode(image_stream.getvalue()).decode('utf-8')
            return image
    except Exception as e:
        print(e)
        return None
    

def get_streak_list(user):            
    all_users = get_user_model().objects.all()
    all_streaks = []
    my_streaks = []
    for u in all_users:
        streak,_ = Streaks.objects.get_or_create(user=u)
      
        longest, act = streak.count_streaks()
        
        if u == user:
            my_streaks.append((u.username + " (aktuell)",act, 'r'))
            if longest != act:
                my_streaks.append((u.username+ " (bestes)",longest, 'r'))
        else:
            all_streaks.append((u.username,longest, 'g'))
    print(all_streaks)
    print(my_streaks)
    all_streaks = sorted(all_streaks, key=lambda x: x[1])
    if len(all_streaks) > 5:
        all_streaks = all_streaks[-5:]
    all_streaks +=  my_streaks
    all_streaks = sorted(all_streaks, key=lambda x: x[1])
    users, score, color = zip(*all_streaks)
    print(users, score, color)

    plt.bar(users, score, color=color)
    #plt.gca().xaxis.set_major_formatter(StrMethodFormatter())
    #plt.xticks(users)

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    
    image = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image

    
        
        
        
    

       
    return None
    