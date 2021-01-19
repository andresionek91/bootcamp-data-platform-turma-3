from aws_cdk import core

from bootcamp_data_platform_turma_3.data_lake.stack import DataLakeStack

app = core.App()
data_lake = DataLakeStack(app)
app.synth()
