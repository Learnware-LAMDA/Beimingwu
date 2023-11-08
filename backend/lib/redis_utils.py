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
