
# from collections import OrderedDict
# from tempfile import SpooledTemporaryFile
# import math
# import os
# import re
# import six
# from django.core.paginator import InvalidPage
# from django.http import QueryDict
# from django.template import loader
# from django.template.loader import render_to_string
# from itsdangerous import URLSafeTimedSerializer, TimestampSigner
# from itsdangerous.exc import SignatureExpired
# from django.template.defaultfilters import slugify
# from oauth2_provider.models import AccessToken, RefreshToken
# from oauth2_provider.settings import oauth2_settings
# from oauthlib import common
# from rest_framework.pagination import PageNumberPagination
# from storages.backends.s3boto3 import S3Boto3Storage
# from choices import OWNERSHIP_TYPE
# from strings import *
# from constants import *
# import firebase_admin
# from firebase_admin import credentials, auth

# import MailChecker

# import phonenumbers
import requests
from functools import reduce
import random
import string
from django.conf import settings
from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def get_object_or_redirect(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist as e:
        print(f"ObjectDoesNotExist: {e}")
        print(f"Query parameters: {kwargs}")
        return None
    

def clean_name(name):
    # Remove symbols and brackets
    cleaned_name = ''.join(e for e in name if e.isalnum() or e.isspace())
    # Remove extra spaces and capitalize the first letter of each word
    return ' '.join(cleaned_name.split()).title()

def random_file_name(extension, name:str=None):
    if name is not None:
        random_name = name
    else:
        random_name = ''.join(random.choice(string.ascii_letters) for _ in range(12)) + timezone.localdate().strftime('%Y%m%d')
    return random_name + extension


# def validate_image(value):
#     if hasattr(value, 'content_type'):
#         if value.content_type.split('/')[0] != 'image':
#             raise serializers.ValidationError(detail='Please upload a valid image file')
#     if value.size > settings.MAX_UPLOAD_SIZE:
#         raise serializers.ValidationError(
#             detail=f'File size should be less than {settings.MAX_UPLOAD_SIZE / (1024 * 1024)} Megabytes')


# class CustomS3Boto3Storage(S3Boto3Storage):
#     def _save_content(self, obj, content, parameters):
#         content.seek(0, os.SEEK_SET)
#         content_autoclose = SpooledTemporaryFile()
#         content_autoclose.write(content.read())
#         super(CustomS3Boto3Storage, self)._save_content(obj, content_autoclose, parameters)
#         if not content_autoclose.closed:
#             content_autoclose.close()


class CustomException(Exception):
    pass


# def custom_password_validator(password, user=None, password_validators=None):
#     errors = []
#     if ' ' in password:
#         errors.append('Password cannot contain blank space')
#     if password_validators is None:
#         password_validators = get_default_password_validators()
#     for validator in password_validators:
#         try:
#             validator.validate(password, user)
#         except ValidationError as error:
#             errors.extend(error.messages)

#     if errors:
#         if user:
#             raise serializers.ValidationError(detail={'password': errors})
#         else:
#             raise serializers.ValidationError(detail=errors)


def google_user_details(token):
    result = requests.get(url='https://www.googleapis.com/oauth2/v2/userinfo', params={'atl': 'json', 'access_token': token}).json()
    if result.get('email'):
        return {
            'uid': result['id'],
            'email': result['email'],
            'first_name': result['given_name'],
            'last_name': result.get('family_name', ''),
            'token': token
        }
    return {
        'error': 'Please add email or mobile number in your profile',
        'uid': result['id'],
        'first_name': result['given_name'],
        'last_name': result.get('family_name', ''),
        'token': token
    }


def facebook_user_details(token):
    result = requests.get(url='https://graph.facebook.com/me', params={'access_token': token, 'fields': 'id,email,first_name,last_name'}).json()
    if result.get('email'):
        return {
            'uid': result['id'],
            'email': result['email'],
            'first_name': result['first_name'],
            'last_name': result['last_name'],
            'token': token
        }
    return {
        'error': 'Please add email or mobile number in your profile',
        'uid': result['id'],
        'first_name': result['first_name'],
        'last_name': result['last_name'],
        'token': token
    }


def check_social_user_details(token, backend):
    if backend == 'google-oauth2':
        result = google_user_details(token)
    else:
        result = facebook_user_details(token)
    return result







# def phonenumber_validator(value):
#     try:
#         z = phonenumbers.parse(value, None)
#         if not phonenumbers.is_valid_number(z):
#             raise ValidationError('Please enter a valid phone number')
#         return phonenumbers.format_number(z, phonenumbers.PhoneNumberFormat.E164)
#     except Exception:
#         raise ValidationError('Please enter a valid phone number must start with country code')


def google_user_details(token):
    result = requests.get(url='https://www.googleapis.com/oauth2/v2/userinfo', params={'atl': 'json', 'access_token': token}).json()
    if result.get('email'):
        return {
            'uid': result['id'],
            'email': result['email'],
            'first_name': result['given_name'],
            'last_name': result.get('family_name', ''),
            'token': token
        }
    return {
        'error': 'Please add email or mobile number in your profile',
        'uid': result['id'],
        'first_name': result['given_name'],
        'last_name': result.get('family_name', ''),
        'token': token
    }


def get_pincode_from_address(address):
    if not address:
        return None

    address = address.lower()
    pin_code_text = ""

    if 'pincode' in address:
        pin_code_text = address.split('pincode')[-1]
    elif 'zipcode' in address:
        pin_code_text = address.split('zipcode')[-1]
    elif 'pin code' in address:
        pin_code_text = address.split('pin code')[-1]
    elif 'zip code' in address:
        pin_code_text = address.split('zip code')[-1]
    elif 'pin' in address:
        pin_code_text = address.split('pin')[-1]
    elif 'zip' in address:
        pin_code_text = address.split('zip')[-1]
    elif 'code' in address:
        pin_code_text = address.split('code')[-1]

    pin_code = ""
    for char in pin_code_text:
        if char.isdigit():
            pin_code += char

    return pin_code if pin_code else None


# def is_valid_phone_number(value):
#     try:
#         phonenumber_validator(value)
#         return True
#     except Exception:
#         return False
    

def get_multiple_list_matching(matching_key_mappings: dict):
    matching_maps = []
    for key, value in matching_key_mappings.items():
        matching_maps.extend([{key: x} for x in set(value)])
    q_objs = map(lambda x: Q(**x), matching_maps)
    q_or_obj = reduce(lambda i, j: i | j, q_objs)
    return q_or_obj


# def success_response(data=None, message=None, extra_data={}):
#     result = {'status': {'code': status.HTTP_200_OK,
#                          'message': message},
#               'data': data
#               }
#     result.update(extra_data)
#     return Response(result)


# def error_response(data=None, message=None, code=status.HTTP_403_FORBIDDEN):
#     return Response({'status': {'code': code,
#                                 'message': message},
#                      'data': data
#                      })






def cleanupPhoneNumber(mobile: str):
    if mobile is not None:
        if len(mobile) >= 10:
            mobile = mobile[(len(mobile)-10):]
    return '+91' + str(mobile)

def namesplit(fullname):
    split_name=fullname.strip().split(" ")
    if(len(split_name) > 1):
        first_name = ' '.join(split_name[0: len(split_name) - 1])
        return first_name, split_name[-1]
    return split_name[0], ""