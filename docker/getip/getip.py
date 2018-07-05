#!/usr/bin/env python

import urllib2

print(urllib2.urlopen('http://ip.42.pl/raw').read())
