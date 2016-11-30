from __future__ import print_function

from datetime import timedelta, datetime
from functools import wraps
import json
import boto3
import os
import inspect
import logging
import pprint
import sys
import time
from datetime import datetime, date
from slackclient import SlackClient
from base64 import b64decode

import yaml

from c7n.credentials import SessionFactory
from c7n.policy import Policy, load as policy_load
from c7n.reports import report as do_report
from c7n.utils import Bag, dumps
from c7n.manager import resources
from c7n.resources import load_resources
from c7n import mu, schema, version

log = logging.getLogger('custodian.commands')

