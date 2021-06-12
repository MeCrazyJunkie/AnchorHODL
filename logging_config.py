# Logging setup
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S '
        },
        'repay_logger_format': {
            'format': '%(asctime)s %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S '
        },
        'info_logger_format': {
            'format': '%(asctime)s %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S '
        },
    },
    'handlers': {
        'out' : {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/default.log',
            'maxBytes': 1024*1024*5,  # 5MB
            'backupCount': 5,
            'formatter': 'standard'
        },
        'repay_logger': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/repay.log',
            'maxBytes': 1024*1024*5,  # 5MB
            'backupCount': 5,
            'formatter': 'repay_logger_format'
        },
        'apscheduler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/apscheduler.log',
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 5,
        },
        'werkzeug': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/werkzeug.log',
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 5,
        },
        'info_logger': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/info.log',
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 5,
            'formatter': 'info_logger_format'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'out'],
            'level': 'INFO',
            'propagate': True,
        },
        'repay_logger': {
            'handlers': ['repay_logger', 'out'],
            'level': 'INFO',
            'propagate': False,
        },
        'apscheduler': {
            'handlers': ['apscheduler', 'out'],
            'level': 'INFO',
            'propagate': False,
        },
        'werkzeug': {
            'handlers': ['werkzeug', 'out'],
            'level': 'INFO',
            'propagate': False,
        },
        'info_logger': {
            'handlers': ['info_logger', 'out'],
            'level': 'INFO',
            'propagate': False,
        },
        'urllib3.connectionpool': {
            'level': 'WARNING',
        }
    },
}

