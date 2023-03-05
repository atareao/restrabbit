#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika


class Publisher:
    def __init__(self, app_id, host, port, queue):
        self._app_id = app_id
        self._queue = queue
        self._host = host
        self._port = port

    def _connect(self):
        self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self._host,
                                          port=self._port)
                )
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue)

    def _disconnect(self):
        self._connection.close()

    def send(self, headers, content):
        self._connect()
        properties = pika.BasicProperties(
                app_id=self._app_id,
                content_type="application/json",
                headers=headers
                )
        self._channel.basic_publish(
                exchange="",
                routing_key=self._queue,
                body=content,
                properties=properties)
        self._disconnect()



