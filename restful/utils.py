from typing import Tuple, Any, List, Union, Dict
import random
from learnware import learnware
import lib.database_operations as dbops
import itsdangerous
import smtplib
import ssl


__all__ = ["get_parameters", "generate_random_str", "dump_learnware"]


def get_parameters(request, parameters: List[str]) -> bool:
    try:
        data = request.get_json()
    except:
        return None
    for param in parameters:
        if param not in data:
            return None
    return data


def generate_random_str(randomlength: int) -> str:
    random_str = ""
    base_str = "ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789"
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def dump_learnware(learnware: learnware.Learnware, matching: int=None, last_modify: str=None):
    ret = {
        "learnware_id": learnware.id,
        "username": dbops.get_learnware_owner(learnware.id),
        "semantic_specification": learnware.get_specification().get_semantic_spec(),
    }

    if last_modify is not None: 
        ret["last_modify"] = last_modify
        pass
    if matching is not None: 
        ret["matching"] = matching
        pass
    return ret


def generate_email_verification_code(email: str, secret_key) -> str:
    serializer = itsdangerous.URLSafeTimedSerializer(secret_key=secret_key)
    return serializer.dumps(email)


def decode_email_verification_code(code: str, secret_key) -> Union[str, None]:
    serializer = itsdangerous.URLSafeTimedSerializer(secret_key=secret_key)
    
    try:
        return serializer.loads(code, max_age=3600*24)
    except itsdangerous.SignatureExpired:
        return None
    except itsdangerous.BadSignature:
        return None
    pass


def send_verification_email(email: str, verification_code: str, email_config: dict) -> bool:

    port = email_config['smtp_port']
    smtp_server = email_config['smtp_server']
    sender_email = email_config['sender_email']
    receiver_email = email
    password = email_config['smtp_password']
    confirm_url = email_config['verification_url'] + "?code=" + verification_code

    message = f"""\
From: {sender_email}\r\n\
Subject: Please activate your account\r\n\
\r\n
        Welcome! Thanks for signing up. Please follow this link to activate your account:

            { confirm_url }

        Cheers!
"""

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        pass
    pass