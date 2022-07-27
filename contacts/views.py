from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic.base import View
from ascons import settings

import os
from twilio.rest import Client

from contacts.models import Contact


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')

    def post(self, request):
        if request.user.is_authenticated:
            _name = request.user.username
            _email = request.user.email
        else:
            _name = request.POST['name']
            _email = request.POST['email']
            _phone = request.POST['phone']
        _message = request.POST['message']
        subject = request.POST['subject']
        context = {'message': _message, 'subject': subject, 'name': _name}
        email_template = render_to_string('includes/support_email.html', context)
        try:
            send_mail = EmailMessage(
                f'Message for ascons.com.ng',
                email_template,
                _email,
                [settings.SUPPORT_EMAIL],
            )
            send_mail.fail_silently = False
            send_mail.send()

            # Send sms message to admin...
            account_sid = os.environ['AC200ea02284b2107f2377c19f48937a63']
            auth_token = os.environ['2a2a62149e79326826a15a4dd9aec306']
            client = Client(account_sid, auth_token)
            twl_message = client.messages.create(
                messaging_service_sid='MG9752274e9e519418a7406176694466fa',
                body='A message was sent from your website visit to check.',
                to='+19786345903'
            )
            print(twl_message.sid)

            # Display message if successful...
            messages.success(request, "Email sent successfully...")
            return render(request, 'contact.html')
        except Exception:
            contact = Contact.objects.create(
                name=_name,
                email=_email,
                phone=_phone,
                subject=subject,
                message=_message,
            )
            contact.save()

            messages.success(request, "Message sent and received successfully")
            return render(request, 'contact.html')
