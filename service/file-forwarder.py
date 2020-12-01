"""
Simple service to grab data from an URL and forward it to another URL.
"""
from requests import session
from sesamutils import VariablesConfig, sesam_logger

required_env_vars = ["INPUT_URL", "OUTPUT_URL"]
optional_env_vars = [("INPUT_JWT", None),
                     ("OUTPUT_JWT", None),
                     ("OUTPUT_CONTENT_TYPE", "application/json; charset=utf-8"),
                     ("LOG_TIMESTAMP", True)]

config = VariablesConfig(required_env_vars, optional_env_vars)

if not config.validate():
    exit(1)

logger = sesam_logger("file-transfer-service", timestamp=config.LOG_TIMESTAMP)


def main():
    try:
        input_connection = session()
        try:
            input_connection.headers['Authorization'] = f'bearer {config.INPUT_JWT}'
        except AttributeError:
            pass

        logger.debug(f'Creating stream from input URL "{config.INPUT_URL}"')
        res = input_connection.get(config.INPUT_URL)
        res.raise_for_status()

        output_connection = session()
        try:
            output_connection.headers['Authorization'] = f'bearer: {config.OUTPUT_JWT}'
        except AttributeError:
            pass
        output_connection.headers['Content-Type'] = config.OUTPUT_CONTENT_TYPE

        logger.debug(f'Streaming from input URL to output URL : "{config.OUTPUT_URL}"')
        output_response = output_connection.post(
            config.OUTPUT_URL,
            data=res.content
        )
        output_response.raise_for_status()

    except Exception as exc:
        logger.error(f'Error when transferring data from "{config.INPUT_URL}"->"{config.OUTPUT_URL}"\nMsg: "{exc}"')


if __name__ == "__main__":
    main()
