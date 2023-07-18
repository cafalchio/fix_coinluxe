# Gunicorn configuration file

# Set the Gunicorn server bind address
bind = "127.0.0.1:8000"

# Number of worker processes
workers = 6

# Number of worker threads per worker process
threads = 1

# Worker class
worker_class = "sync"

# Maximum number of simultaneous client connections
worker_connections = 1000

# Timeout for graceful worker shutdown
timeout = 10

# Enable or disable daemon mode
daemon = False

# Set the path to Gunicorn error log file
errorlog = "error.log"

# Set the path to Gunicorn access log file
accesslog = "access.log"

# Logging format for Gunicorn access log
access_log_format = "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(D)s"

# Preload application code before forking worker processes
preload_app = True
