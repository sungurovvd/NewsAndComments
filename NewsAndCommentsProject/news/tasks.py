from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Subscribers
from datetime import datetime
from celery import shared_task
import time


@shared_task
def send_week_mails():
    subscribers = Subscribers.objects.all()
    for subs in subscribers:
        author = subs.author.user
        posts = subs.category.post_set.all().order_by('-create_time')
        post_count = 0
        name_of_new_posts = ''
        for post in posts:
            if datetime.now().timestamp() - post.create_time.timestamp() < 604800:
                name_of_new_posts = name_of_new_posts + post.article + ' ,'
                post_count = post_count + 1
            else:
                break

        html_content = render_to_string(
            'week_message.html',
            {
                'username': author.username,
                'category': subs.category.name,
                'count': post_count,
                'names': name_of_new_posts
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{subs.category.name}',
            body=name_of_new_posts,
            from_email='viktorsung@yandex.ru',
            to=[author.email]
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def hello():
    # >celery -A NewsAndCommentsProject worker -l info --pool=solo
    #celery - A NewsAndCommentsProject beat - l info

    html_content = render_to_string(
        'week_message.html',
        {
            'username': '',
            'category': '',
            'count': '',
            'names': ''
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'',
        body='name_of_new_posts',
        from_email='viktorsung@yandex.ru',
        to=['sungurovvictor@gmail.com']
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print("Hello, world!")


