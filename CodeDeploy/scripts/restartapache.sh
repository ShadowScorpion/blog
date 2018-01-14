#!/bin/bash
systemctl restart httpd > /var/log/httpd/codedeploy.log 2>&1
