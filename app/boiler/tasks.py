from background_task import background
import time

from .models import Programs, CurrentProgram

@background(schedule=1)
def check_programs():
    t = time.localtime()
    now = t.tm_hour*60+t.tm_min
    print(f"dentro de task {now}")
    #-----------------------------------------------------
    # revisa si hay algun programa que deba activarse
    #-----------------------------------------------------
    programs = Programs.objects.filter(day=t.tm_wday+1,startTime__lte = now, endTime__gte = now).order_by('-endTime')
    if programs:
        program = programs.first()
        current = CurrentProgram.objects.all()
        if current:
            current = current.first()
            if current.endTime < program.endTime:
                CurrentProgram.objects.all().delete()
                CurrentProgram.objects.create(
                        day = program.day,
                        hour = program.hour,
                        minutes = program.minutes,
                        duration = program.duration,
                    )
        else:
            CurrentProgram.objects.create(
                    day = program.day,
                    hour = program.hour,
                    minutes = program.minutes,
                    duration = program.duration,
                )
    #-----------------------------------------------------
    # revisa si debe apagarse el boiler
    #-----------------------------------------------------
    current = CurrentProgram.objects.all()
    if current:
        current = current.first()
        if current.endTime < now:
            CurrentProgram.objects.all().delete()
        else:    
            print("Boiler encendido")
            print(f"{current} start = {current.startTime} end = {current.endTime}")
    print("saliendo de task")
    pass

check_programs(repeat=5,remove_existing_tasks=True)