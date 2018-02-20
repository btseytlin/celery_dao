import time
from .celery import worker
from .tasks import add

def main():
    print('Running app')
    print('I will wait 3 seconds for celery to connect to brocker')
    time.sleep(3)
    print('I will now call a task')
    time.sleep(10)
    result = add.apply_async((2, 2,))
    print('Task called, waiting for celery to give us the answer')
    print(f'Answer: {result.get()}')

if __name__ == '__main__':
    main()