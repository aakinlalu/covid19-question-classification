import datetime
import boto3
from moto import mock_s3
from loggings.logger import S3Logger


@mock_s3
def test_logging():
    file_value = f'{datetime.date.today().strftime("%Y%m%d")}'
    conn = boto3.resource("s3", region_name="us-east-1")

    conn.create_bucket(Bucket="mybucket")

    s3Log = S3Logger("tests/202107031647.log", "mybucket")

    res = s3Log.upload_log_s3()

    assert res == True
