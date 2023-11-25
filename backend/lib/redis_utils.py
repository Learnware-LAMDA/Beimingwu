import context


def subscribe():
    channel = context.redis_client.pubsub()
    channel.subscribe("learnware")

    for message in channel.listen():
        if message["type"] == "message":
            message_data = message["data"]
            if message_data.startswith("reload"):
                learnware_id = message_data.split(" ")[1]
                context.logger.info(f"sub Reload learnware {learnware_id}")
                context.engine.reload_learnware(learnware_id)
                pass
            elif message_data.startswith("delete"):
                learnware_id = message_data.split(" ")[1]
                context.logger.info(f"sub Delete learnware {learnware_id}")
                context.engine.delete_learnware(learnware_id)
            pass
        pass
    pass


def publish_reload_learnware(learnware_id):
    context.redis_client.publish("learnware", f"reload {learnware_id}")
    pass


def publish_delete_learnware(learnware_id):
    context.redis_client.publish("learnware", f"delete {learnware_id}")
    pass


def add_learnware_download_token(learnware_ids, token):
    if isinstance(learnware_ids, str):
        learnware_ids = [learnware_ids]
        pass

    key = f"learnware:download_token:{token}"
    value = "|".join(learnware_ids)
    context.redis_client.set(key, value, ex=60 * 30)
    pass


def get_learnware_id_from_download_token(token):
    key = f"learnware:download_token:{token}"
    learnware_id = context.redis_client.get(key)
    if learnware_id is None:
        return None
    return learnware_id.split("|")


def delete_learnware_download_token(token):
    key = f"learnware:download_token:{token}"
    context.redis_client.delete(key)
    pass


def set_key(key, value, expire=60 * 60):
    key = f"learnware:{key}"
    context.redis_client.set(
        key,
        value,
        ex=expire,
    )
    pass


def get_key(key, default=None):
    key = f"learnware:{key}"
    value = context.redis_client.get(key)
    if value is None:
        return default
    return value
