from typing import Tuple, Any, List, Union, Dict
import random
from learnware import learnware
import lib.database_operations as dbops
import itsdangerous
import smtplib
import ssl
import multiprocessing as mp
import socks
import socket


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


def dump_learnware(learnware: learnware.Learnware, matching: int = None, last_modify: str = None):
    ret = {
        "learnware_id": learnware.id,
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
        return serializer.loads(code, max_age=3600 * 24)
    except itsdangerous.SignatureExpired:
        return None
    except itsdangerous.BadSignature:
        return None
    pass


def send_email_worker(sender_email, password, receiver_email, message, smtp_server, port, proxy_host, proxy_port):
    if len(smtp_server) == 0:
        return

    if len(proxy_host) > 0 and proxy_port > 0:
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy_host, proxy_port)
        original_socket = socket.socket
        socket.socket = socks.socksocket
        pass

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        pass

    if len(proxy_host) > 0 and proxy_port > 0:
        socket.socket = original_socket
        pass
    pass


def send_verification_email(email: str, verification_code: str, email_config: dict) -> bool:
    port = email_config["smtp_port"]
    smtp_server = email_config["smtp_server"]
    sender_email = email_config["sender_email"]
    receiver_email = email
    password = email_config["smtp_password"]
    confirm_url = email_config["verification_url"] + "?code=" + verification_code
    proxy_host = email_config.get("proxy_host", "")
    proxy_port = email_config.get("proxy_port", 0)

    message = f"""\
From: {sender_email}\r\n\
Subject: Please activate your account\r\n\
\r\n
        Welcome! Thanks for signing up. Please follow this link to activate your account:

            { confirm_url }

        Cheers!
        BeiMing Group
"""

    thread = mp.Process(
        target=send_email_worker,
        args=(sender_email, password, receiver_email, message, smtp_server, port, proxy_host, proxy_port),
    )
    thread.start()
    return thread


def send_reset_password_email(email: str, verification_code: str, user_id: str, email_config: dict) -> bool:
    port = email_config["smtp_port"]
    smtp_server = email_config["smtp_server"]
    sender_email = email_config["sender_email"]
    receiver_email = email
    password = email_config["smtp_password"]
    confirm_url = email_config["reset_password_url"] + "?code=" + verification_code + "&user_id=" + user_id
    proxy_host = email_config.get("proxy_host", "")
    proxy_port = email_config.get("proxy_port", 0)

    message = f"""\
From: {sender_email}\r\n\
Subject: Reset your password\r\n\
\r\n
        Please follow this link to reset your password:

            { confirm_url }

        Cheers!

        BeiMing Group
"""

    thread = mp.Process(
        target=send_email_worker,
        args=(sender_email, password, receiver_email, message, smtp_server, port, proxy_host, proxy_port),
    )
    thread.start()
    return thread
