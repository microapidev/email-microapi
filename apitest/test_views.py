from django.shortcuts import render
from django.urls import reverse
from rest_framework.test import APITestCase,APIClient
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
import json
import pytest
from api import urls

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.mark.django_db
@pytest.mark.parametrize(
    'sender, recipient, body, subject, cc, bcc, status_code',[
       ("","","hello","hi","","",400),

       ("",'None@none.com',"hello","hi","","",400),

       ("hello@hello.com","","hello","hi","","",400),

       ("None@none.com","hi@hi.com","","hi","","",400),

       ("None@none.com","hi.hi.com","","hi","","",400),

       ("phemmylintry@gmail.com","alabiemmanuelferanmi@gmail.com","","hi","","",400),
       
       ("phemmylintry@gmail.com","alabiemmanuelferanmi@gmail.com","message","hi","","",200),


    ]
)

def test_send_registration(sender, recipient, body, subject, cc, bcc, status_code, api_client):
    '''testing different test cases for sending email with sendmailendpoint'''
    data = {
        "sender":sender,
        "recipient":recipient,
        "body":body,
        "subject":subject,
        "cc":cc,
        "bcc":bcc

        }
    url = reverse("sendmail")
    response = api_client.post(url, data =data)
    assert response.status_code == status_code


