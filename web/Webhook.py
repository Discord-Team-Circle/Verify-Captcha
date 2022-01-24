# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import logging

import requests

try:
    from django.conf import settings
except ImportError:
    settings = None


class WebhookHandler(logging.Handler):
    """Logging handler to post to Slack to the webhook URL"""

    def __init__(self, hook_url=None, *args, **kwargs):
        super(WebhookHandler, self).__init__(*args, **kwargs)
        self._hook_url = hook_url
        self.formatter = SimpleFormatter()

    @property
    def hook_url(self):
        if self._hook_url is None:
            self._hook_url = getattr(settings, "SLACK_WEBHOOK_URL", "")
        return self._hook_url

    def emit(self, record):
        """
        Submit the record with a POST request
        """
        try:
            slack_data = self.format(record)
            requests.post(self.hook_url, slack_data)
        except Exception:
            self.handleError(record)

    def filter(self, record):
        """
        Disable the logger if hook_url isn't defined,
        we don't want to do it in all environments (e.g local/CI)
        """
        if not self.hook_url:
            return 0
        return super(WebhookHandler, self).filter(record)


class SimpleFormatter(logging.Formatter):
    """Basic formatter without styling"""
    def format(self, record):
        return {'content': record.getMessage()}