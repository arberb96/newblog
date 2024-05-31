import os

AWS_SECRET_KEY_ID=os.environ.get("AWS_SECRET_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME=os.environ.get("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_CUSTOM_DOMAIN=os.environ.get("AWS_S3_CUSTOM_DOMAIN")
AWS_S3_ENDPOINT_URL=os.environ.get("AWS_S3_ENDPOINT_URL")
# AWS_S3_OBJECT_PARAMETERS={
#     "CasheControl": "max-age=86400",
# }

DEFAULT_FILE_STORAGE = "blogproject.cdn.backends.MediaRootS3BotoStorage"
STATICFILES_STORAGE = "blogproject.cdn.backends.StaticRootS3BotoStorage"