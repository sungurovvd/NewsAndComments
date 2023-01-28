from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals
        # from .tasks import send_week_mails
        # from  .scheduler import appointment_scheduler
        # print('start')
        #
        # appointment_scheduler.add_job(
        #     id='send_week_mails',
        #     func= send_week_mails,
        #     trigger='interval',
        #     seconds= 604800,
        # )
        # appointment_scheduler.start()
