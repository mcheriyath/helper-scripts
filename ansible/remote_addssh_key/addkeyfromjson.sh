#!/bin/bash
cat /tmp/github/ansiblessh/sample.json| python -c "import sys, json; print json.load(sys.stdin)['ssh']['key']" >> /home/vagrant/.ssh/authorized_keys
