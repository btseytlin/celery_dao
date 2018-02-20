from celery import Celery

worker = Celery('tasks',
             broker='amqp://rabbitmq',
             backend='amqp://rabbitmq',
             include=['celery_dao.tasks'])

if __name__ == '__main__':
    worker.start()