import jieba
import jieba.posseg as pseg
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

bucket = os.environ.get('user_dict_bucket')
s3_path = os.environ.get('user_dict_path')
local_file = '/tmp/user_dict.txt' # /tmp 只有这个路径是可以写的

# 下载文件
try:
    s3.download_file(bucket, s3_path, local_file)
    print(f'File downloaded successfully: {local_file}')
except Exception as e:
    print(f'Error downloading file: {e}')

class APIException(Exception):
    def __init__(self, message, code: str = None):
        if code:
            super().__init__("[{}] {}".format(code, message))
        else:
            super().__init__(message)


def handle_error(func):
    """Decorator for exception handling"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIException as e:
            logger.exception(e)
            raise e
        except Exception as e:
            logger.exception(e)
            raise RuntimeError(
                "Unknown exception, please check Lambda log for more details"
            )

    return wrapper


# 对文本进行分词
@handle_error
def lambda_handler(event, context):
    jieba.load_userdict(local_file)

    text = event.get('text')
    if not text:
        return {'error': 'Text is required'}
    
    result = pseg.cut(text.replace(' ', '_'))
    words = list(set([ item.word.replace('_', ' ') for item in result if item.flag == 'term' ]))
    return {'words': words}