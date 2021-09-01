import pickle
from typing import Any
import boto3
import os

boto3.set_stream_logger("botocore", level="DEBUG")


def write(model: Any, filename: str):
    # pickle the model into file
    with open(filename, "wb") as f:
        pickle.dump(model, f)

    # send file to s3 bucket
    s3 = boto3.resource("s3")
    s3.Object("nikolaratinac-1030-2019", filename).put(
        Body=open(filename, "rb"),
    )

    os.remove(filename)


def read(filename: str):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("nikolaratinac-1030-2019")
    for obj in bucket.objects.all():
        if obj.key == filename:
            body = obj.get()["Body"].read()
            print(body)
            return body
