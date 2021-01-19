from enum import Enum
from aws_cdk import core
from aws_cdk import (
    aws_s3 as s3,
)

from bootcamp_data_platform_turma_3.environment import Environment


class DataLakeLayer(Enum):
    RAW = 'raw'
    PROCESSED = 'processed'
    CURATED = 'curated'


class BaseDataLakeBucket(s3.Bucket):

    def __init__(self, scope: core.Construct, deploy_env: Environment, layer: DataLakeLayer, **kwargs):
        self.layer = layer
        self.deploy_env = deploy_env
        self.obj_name = f's3-belisco-{self.deploy_env.value}-data-lake-{self.layer.value}'

        super().__init__(
            scope,
            id=self.obj_name,
            bucket_name=self.obj_name,
            block_public_access=self.default_block_public_access,
            encryption=self.default_encryption,
            versioned=True,
            **kwargs
        )

        self.set_default_lifecycle_rules()

    @property
    def default_encryption(self):
        return s3.BucketEncryption.S3_MANAGED

    @property
    def default_block_public_access(self):
        return s3.BlockPublicAccess(
                ignore_public_acls=True,
                block_public_acls=True,
                block_public_policy=True,
                restrict_public_buckets=True
            )

    def set_default_lifecycle_rules(self):
        """
        Sets lifecycle rule by default
        """
        self.add_lifecycle_rule(
            abort_incomplete_multipart_upload_after=core.Duration.days(7),
            enabled=True
        )

        self.add_lifecycle_rule(
            noncurrent_version_transitions=[
                s3.NoncurrentVersionTransition(
                    storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                    transition_after=core.Duration.days(30)
                ),
                s3.NoncurrentVersionTransition(
                    storage_class=s3.StorageClass.GLACIER,
                    transition_after=core.Duration.days(60)
                )
            ]
        )

        self.add_lifecycle_rule(
            noncurrent_version_expiration=core.Duration.days(360)
        )
