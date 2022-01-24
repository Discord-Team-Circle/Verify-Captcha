def createLogger(name: str, level: int = 20):
    import sys
    import logging
    from Webhook import WebhookHandler

    LOGGER = logging.getLogger(name)
    FORMATTER = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setFormatter(FORMATTER)
    fileHandler = logging.FileHandler(
        filename=f"./{name}.log", mode="w", encoding="utf8"
    )
    webhookHandler = WebhookHandler(
        "https://canary.discord.com/api/webhooks/935064191365160990/wLRlqyMJdd0KYbAaJFkuWeNz22MwE0nGzaWzOwCc1yhpX_VvXfCbUhbqGGohFKgxutln"
    )
    webhookHandler.setLevel(level)
    fileHandler.setFormatter(FORMATTER)
    LOGGER.setLevel(level)
    LOGGER.addHandler(streamHandler)
    LOGGER.addHandler(fileHandler)
    LOGGER.addHandler(webhookHandler)
    return LOGGER
