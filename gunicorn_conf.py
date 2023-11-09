import os
import os.path as osp
from pathlib import Path

current_file_path = Path(__file__).resolve()
current_dir_path = current_file_path.parent

# SSL
keyfile = 'key.pem'
certfile = 'cert.pem'

# Socket Path
bind = 'unix:' + osp.join(current_dir_path, 'gunicorn.sock')

# Worker Options
workers = 2
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
log_dir = osp.join(current_dir_path, 'logs')
os.makedirs(log_dir, exist_ok=True)
accesslog = osp.join(log_dir, 'access.log')
errorlog = osp.join(log_dir, 'error.log')
