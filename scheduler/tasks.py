# from datetime import timedelta
# from django.utils import timezone
# from django_q.tasks import async_task, schedule
# from django_q.models import Schedule


# def send_mail(subject, body, sender, recipient):
#     body = 'This is a scheduled email, you will receive another email in 5 minutes'
#     # # send this message right away
#     async_task('django.core.mail.send_mail',
#             subject,
#             body,
#             sender,
#             [recipient])
#     # and this follow up email in one hour
#     msg = 'Here are some tips to get you started...'
#     schedule('django.core.mail.send_mail',
#              'Follow up',
#              msg,
#              sender,
#              [recipient],
#              schedule_type=Schedule.ONCE,
#              next_run=timezone.now() + timedelta(minutes=5))
    
