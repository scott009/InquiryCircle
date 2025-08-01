# Gunicorn configuration file for InquiryCircle
# gunicorn.conf.py

import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/gunicorn/inquirycircle_access.log"
errorlog = "/var/log/gunicorn/inquirycircle_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "inquirycircle"

# Daemon mode (set to True for production)
daemon = False

# User/group to run as (uncomment for production)
# user = "www-data"
# group = "www-data"

# Preload application for better performance
preload_app = True

# Graceful timeout
graceful_timeout = 30

# Temporary directory
tmp_upload_dir = None
