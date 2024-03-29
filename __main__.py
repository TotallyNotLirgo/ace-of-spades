import uvicorn
from general.config import get_config
import logging

config = get_config()

if __name__ == '__main__':
    uvicorn.run(
        'api:app',
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEVELOPMENT_MODE,
        log_level=logging.CRITICAL,
        ssl_keyfile=config.SSL_KEY_PATH,
        ssl_certfile=config.SSL_CERT_PATH,
    )
