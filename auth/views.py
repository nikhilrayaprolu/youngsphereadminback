# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import uuid
@api_view(['POST'])
def login_redirect(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'POST':
        login_url = 'http://localhost:18000/oauth2/access_token/'
        data = {"client_id": "3186b101a338f7a985fe", "client_secret": "c56bf390a42c0f163081a70690a7fba8b24e15d6",
                 "username": request.data['username'], "password": request.data['password'], "token_type": "JWT", "grant_type":"password"}
        login_reply = requests.post(login_url, data=(data))
        return Response(login_reply.json(), status=status.HTTP_201_CREATED)

@api_view(['POST'])
def register_redirect(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'POST':
        print("came here")
        url = "http://localhost:18000/youngsphere/api/v1/registrations/"
        data = request.data
        headers = {'Content-type': 'application/json', 'Authorization':'Token fe8df44d58eb9e5a757fd92e10c0e0de05c8ea67' }
        print(json.dumps(data))
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if r.ok:
            login_url = 'http://localhost:18000/oauth2/access_token/'
            data = {"client_id": "3186b101a338f7a985fe", "client_secret": "c56bf390a42c0f163081a70690a7fba8b24e15d6",
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
        url = "http://localhost:18000/youngspheresite/api/register/"
        data = request.data
        data['organization']['edx_uuid'] = str(uuid.uuid4())
        headers = {'Content-type': 'application/json', 'Authorization':'Token fe8df44d58eb9e5a757fd92e10c0e0de05c8ea67' }
        print(json.dumps(data))
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if r.ok:
            return Response(r.json(), status=status.HTTP_201_CREATED)
        else:
            return Response(r.json(), status=r.status_code)

