"""
Simple service to grab a stream of data and stream it to an URL.
"""
from requests import session
from sesamutils import VariablesConfig, sesam_logger

required_env_vars = ["INPUT_URL", "OUTPUT_URL"]  # ["OUTPUT_URL"]
optional_env_vars = [("CHUNK_SIZE", 262144 * 4 * 10),
                     ("INPUT_JWT", None),
                     ("OUTPUT_JWT", None),
                     ("OUTPUT_CONTENT_TYPE", "application/json; charset=utf-8"),
                     ("LOG_TIMESTAMP", True)]

config = VariablesConfig(required_env_vars, optional_env_vars)

if not config.validate():
    exit(1)

logger = sesam_logger("file-transfer-service", timestamp=config.LOG_TIMESTAMP)


def main():
    file_url = config.INPUT_URL

    try:
        input_connection = session()
        try:
            input_connection.headers['Authorization'] = f'bearer {config.INPUT_JWT}'
        except AttributeError:
            pass

        logger.debug(f'Creating stream from input URL "{file_url}"')
        res = input_connection.get(file_url, stream=True)
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
            data=res.iter_content(chunk_size=int(config.CHUNK_SIZE))
         )
        output_response.raise_for_status()

    except Exception as exc:
        logger.error(f'Error when transferring request data from "{config.INPUT_URL}"->"{config.OUTPUT_URL}"\n"{exc}"')


if __name__ == "__main__":
    main()
