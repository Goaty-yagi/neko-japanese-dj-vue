from django.shortcuts import render
from rest_framework.views import APIView
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import Http404
from django.utils.html import strip_tags
from django.template.loader import render_to_string
# import smtplib
# import ssl


class SendVerificationEmail(APIView):
    permission_classes = ([AllowAny])
    def post(self, request, format=None):
        print("SENDEV",request)
        context = {}
        rediredtURL = settings.FRONT_ORIGIN
        # message = render_to_string("templates/confirmation_email.html", context)
        # html_message = render_to_string("templates/confirmation_email.html", context)
        message = f'''
        <html>
            <body style="display:flex; justify-content: center; bsckground: gray;">
                <div style="width:auto;margin:1rem;padding:1rem;border:solid gray;display:float; text-align:center;">
                    <h1>You're on your way!
                        Let's confirm your email address.
                    </h1>
                    <p  style="color: gray">
                        You're on your way!
                        Let's confirm your email address.
                        By clicking on the following link, you are confirming your email address.
                    </p>
                    <button style="display:block;margin:auto; padding:0.5rem; background:orange; border:solid naby; font-weight: bold;">
                        <a href="{rediredtURL}" style="text-decoration: none; color:darkblue;">
                            Confirm Email Address
                        </a>
                    </button>
                </div>
            </body>
        </html>
        '''
        print("set", message)
        email_to = request["email"]
        EmInstance = EmailMessage(
            'Hello from EM',
            message,
            settings.EMAIL_HOST_USER,
            [email_to],
            # ['neko222japanese@gmail.com'],
            # reply_to=['another@example.com'],
            # headers={'Message-ID': 'foo'},
        )
        try:
            EmInstance.content_subtype = "html"
            mail_sender = EmInstance.send(fail_silently=True)
            if mail_sender:
                return JsonResponse({"message":"successfully sent"}, status=200)
            else:
                print({"message":"couldn't send message"})
                return JsonResponse({"message":"couldn't send message"}, status=400)

        except Exception as e:
            print("MAIL ERROR", e)
            return JsonResponse({"message":"something went wrong! couldn't send message"}, status=500)

# class SendVerificationEmail(APIView):
#     permission_classes = ([AllowAny])
#     def post(self, request, format=None):
#         try:
#             mail_sender = send_mail(
#                 'Hello',
#                 'Body goes here',
#                 settings.EMAIL_HOST_USER,
#                 ['tw200green@gmail.com'],
#             )
#             print("SEND",mail_sender)
#             if mail_sender:
#                 return JsonResponse({"message":"successfully sent"}, status=200)
#             else:
#                 print({"message":"couldn't send message"})
#                 return JsonResponse({"message":"couldn't send message"}, status=400)

#         except Exception as e:
#             print("MAIL ERROR", e)
#             return JsonResponse({"message":"something went wrong! couldn't send message"}, status=500)


