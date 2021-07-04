import datetime
import os
from pathlib import Path
from zipfile import ZipFile
from dataclasses import dataclass

from eliot import to_file
import schedule
import boto3
from botocore.exceptions import ClientError


@dataclass
class S3Logger:
    folder: str
    bucket: str

    def zip_file(self) -> None:
        """[summary]

        Raises:
            ValueError: [description]
        """
        try:
            with ZipFile(f"{self.folder}.zip") as zip_obj:
                for folder_name, sub_folders, file_names in os.walk(self.folder):
                    for filename in file_names:
                        file_path = f"{folder_name}/{filename}"
                        zip_obj.write(file_path, os.path.basename(file_path))
        except Exception as e:
            raise ValueError(e)

    def upload_log_s3(self, object_name: str = None) -> bool:
        """[summary]

        Args:
            object_name (None): [description]

        Raises:
            ClientError: [description]

        Returns:
            bool: [description]
        """
        self.zip_file()

        if object_name is None:
            object_name = f"covid19_question_classification/{self.folder}.zip"

        s3 = boto3.client("s3")

        try:
            response = s3.upload_file(f"{self.folder}.zip", self.bucket, object_name)
        except ClientError as e:
            raise e
            return False
        return True


folder = f'{datetime.date.today().strftime("%Y%m%d")}'
log_file = f'{datetime.datetime.today().strftime("%Y%m%d%H%M")}.log'

if not Path(folder).exists():
    Path(folder).mkdir()

loc = f"{folder}/{log_file}"

__LOGGER__ = to_file(open(loc, "w"))

s3Log = S3Logger(loc, "street-code-ai-logs")
schedule.every().day.at("23.30").do(s3Log.upload_log_s3).tag(
    "daily-tasks", "covid19-classication"
)
