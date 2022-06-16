from background_task import background

@background(schedule=10)
def demo_task():
    pass