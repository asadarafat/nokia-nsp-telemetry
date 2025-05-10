#!/bin/sh
sed "s|\${NSP_IP}|$NSP_IP|g; s|\${NSP_KAFKA_PORT}|$NSP_KAFKA_PORT|g" \
  /root/.kaf/config.template > /root/.kaf/config