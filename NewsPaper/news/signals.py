from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import *

def send_notif(preview, pk, title, subscribers):
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'http://127.0.0.1:8000/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=None,
        to=subscribers
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=Post.category.through)
def notify_new_post_cateogry(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':

        categories = instance.category.all()
        subscribers = []
        for categorysss in categories:
            subscribers = Subscription.objects.filter(category=categorysss.id)
            subscribers = [s.user.email for s in subscribers]
            # for s in subscribers:
            #     mail = s.user.email

            send_notif(instance.preview_text(), instance.pk, instance.title, subscribers)




# @receiver(post_save, sender=Post)
# def subscribe_mails(instance, created, **kwargs):
#     if not created:
#         return
#     print('--------------------------------' * 10)
#     print(instance.category.through.objects.all().last())

    # mails = User.objects.filter(
    #     subscriptions__category=instance.category
    # ).values_list('email', flat=True)
    # print(User.objects.filter(subscriptions__category=instance.category))

    # subject = f'Новый пост в вашей любимой категории!'
    #
    # html_content = (
    #     f'Название: {instance.title}<br>'
    #     f'Категория: {instance.category}<br>'
    #     f'Краткий текст: {instance.preview_text()}<br><br>'
    #     f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
    #     f'Ссылка на пост</a>'
    # )
    #
    # for email in mails:
    #     msg = EmailMultiAlternatives(subject, html_content, None, [email])
    #     msg.attach_alternative(html_content, "text/html")
    #     msg.send()
