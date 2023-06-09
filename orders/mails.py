from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

class Mail:

    @staticmethod
    def send_complete_order(order, user):
        subject = 'El pedido ha sido completado y será enviado'
        template = get_template('orders/mails/complete.html')
        content = template.render({
            'user': user,
        })
        message = EmailMultiAlternatives( subject, 'Mensaje importante', settings.EMAIL_HOST_USER, [user.email])
        message.attach_alternative(content, 'text/html')
        message.send()