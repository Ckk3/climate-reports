import logging.config

def setup_logging():
    # Setup logging configuration
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'filename': 'climate_reports_generator/app.log',
                'maxBytes': 5242880, # 5MB
                'backupCount': 5
            },
        },
        'loggers': {
            '__main__': {
                'level': 'DEBUG',
                'handlers': ['console', 'file'],
                'propagate': False
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
    }
    logging.config.dictConfig(logging_config)

setup_logging()
