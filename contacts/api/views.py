import email
from rest_framework import permissions
from rest_framework.views import APIView
from contacts.models import Contact
from django.core.mail import send_mail
from rest_framework.response import Response


class ContactCreateView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        try:
            send_mail(
                data['subject'],
                "Name: "
                + data['name']
                + '\nEmail: '
                + data['email']
                + '\n\nMessage:\n'
                + data['message'],
                "ascons.edu@gmail.com",
                ["ascons.edu@gmail.com"],
                fail_silently=False
            )
            contact = Contact(
                name=data['name'],
                email=data['email'],
                subject=data['subject'],
                message=data['message']
            )
            contact.save()
            return Response({'success': 'Message sent successfully'})
        except Exception:
            return Response({'error': 'Message not sent'})
