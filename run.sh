#!/bin/bash -e
python status.py&
watch -n10 python gateway.py
