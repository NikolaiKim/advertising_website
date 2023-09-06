import requests
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from djoser.conf import django_settings


class ActivateUserEmail(APIView):
    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/activation/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data=post_data)
        message = result.text
        return Response(message)


def reset_user_password(request, uid, token):
    if request.POST:
        password = request.POST.get('password1')
        payload = {'uid': uid, 'token': token, 'new_password': password}

        url = '{0}://{1}{2}'.format(
            django_settings.PROTOCOL, django_settings.DOMAIN, reverse('password_reset_confirm'))

        response = requests.post(url, data=payload)
        if response.status_code == 204:
            messages.success(request, 'Your password has been reset successfully!')
            return redirect('home')
        else:
            return Response(response.json())
    else:
        return render(request, 'templates/reset_password.html')
