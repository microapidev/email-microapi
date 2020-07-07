'''import os
import binascii
import random
from importlib import import_module

from django.conf import settings


def get_token_generator():
    token_class = RandomStringTokenGenerator
    options = {}

    DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = getattr(settings, 'DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG', None)

    if DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG:
        if "CLASS" in DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG:
            class_path_name = DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG["CLASS"]
            module_name, class_name = class_path_name.rsplit('.', 1)

            mod = import_module(module_name)
            token_class = getattr(mod, class_name)

        if "OPTIONS" in DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG:
            options = DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG["OPTIONS"]
    
    #initialize the token class and pass options
    return token_class(**options)


class BaseTokenGenerator:
    #this is the base class for token generators which can take arbitrary args/kwargs and work with

    def __init__(self, *args, **kwargs):
        pass

    def generate_token(self, *args, **kwargs):
        raise NotImplementedError


class RandomStringTokenGenerator(BaseTokenGenerator):
    """
    Generates a random string with min and max length using os.urandom and binascii.hexlify
    """

    def __init__(self, min_length=10, max_length=50, *args, **kwargs):
        self.min_length = min_length
        self.max_length = max_length

    def generate_token(self, *args, **kwargs):
        """generate a pseudorandom code of random length using os.urandom and binascii.hexlify"""
        #determine the length based on min_length and max_length
        length = random.randint(self.min_length, self.max_length)

        #generate the token using os.urandom and hexlify
        return binascii.hexlify(
            os.urandom(self.max_length)
        ).decode()[0:length]


class RandomNumberTokenGenerator(BaseTokenGenerator):
    """
    Generate a random number using random.SystemRandom()
    """
    def __init__(self, min_number=10000, max_number=99999, *args, **kwargs):
        self.min_number = min_number
        self.max_number = max_number

    def generate_token(self, *args, **kwargs):
        r = random.SystemRandom()
        return str(r.randint(self.min_number, self.max_number))

'''