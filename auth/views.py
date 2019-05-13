# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import requests
import uuid
@api_view(['POST'])
def login_redirect(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'POST':
        login_url = settings.LMS_URL + '/oauth2/access_token/'
        data = {"client_id": settings.LMS_CLIENT_ID, "client_secret": settings.LMS_CLIENT_SECRET,
                 "username": request.data['username'], "password": request.data['password'], "token_type": "JWT", "grant_type":"password"}
        login_reply = requests.post(login_url, data=(data))
        if login_reply.ok:
            return Response(login_reply.json(), status=login_reply.status_code)
        else:
            return Response(login_reply.json(), status=login_reply.status_code)

@api_view(['POST'])
def register_redirect(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'POST':
        print("came here")
        url = settings.LMS_URL + "/youngsphere/api/v1/registrations/"
        data = request.data
        headers = {'Content-type': 'application/json', 'Authorization':'Token '+ settings.LMS_TOKEN }
        print(json.dumps(data))
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if r.ok:
            login_url = settings.LMS_URL + '/oauth2/access_token/'
            data = {"client_id": settings.LMS_CLIENT_ID, "client_secret": settings.LMS_CLIENT_SECRET,
                    "username": request.data['username'], "password": request.data['password'], "token_type": "JWT",
                    "grant_type": "password"}
            login_reply = requests.post(login_url, data=(data))
            return Response({'email': request.data['email'], 'token_object': login_reply.json() }, status=status.HTTP_201_CREATED)
        else:
            return Response(r, status=r.status_code)

@api_view(['POST'])
def register_site(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'POST':
        url = settings.LMS_URL + "/youngspheresite/api/register/"
        data = request.data
        data['organization']['edx_uuid'] = str(uuid.uuid4())
        headers = {'Content-type': 'application/json', 'Authorization':'Token ' + settings.LMS_TOKEN }
        print(json.dumps(data))
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if r.ok:
            return Response(r.json(), status=status.HTTP_201_CREATED)
        else:
            print(r)
            return Response(r, status=r.status_code)
