from os import getcwd, environ
from typing import cast

from aws_cdk.aws_ecs import ContainerImage, AwsLogDriver, FargateTaskDefinition, Cluster, FargateService
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy, IPrincipal
from aws_cdk.aws_logs import LogGroup
from aws_cdk.core import Stack, Construct, App, Environment


class MainStack(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        task_definition = FargateTaskDefinition(
            self,
            'TaskDefinition',
            cpu=256,
            memory_limit_mib=512,
            execution_role=Role(
                self,
                'ExecutionRole',
                assumed_by=cast(IPrincipal, ServicePrincipal('ecs-tasks.amazonaws.com'))
            ),
            task_role=Role(
                self,
                'TaskRole',
                assumed_by=cast(IPrincipal, ServicePrincipal('ecs-tasks.amazonaws.com')),
                managed_policies=[
                    ManagedPolicy.from_aws_managed_policy_name('AmazonSESFullAccess')
                ]
            )
        )
        task_definition.add_container(
            'Container',
            image=ContainerImage.from_asset(
                getcwd(),
                file='Dockerfile',
                repository_name='jqbx-bot',
                exclude=['cdk.out']
            ),
            command=['pipenv', 'run', 'python', '-u', '-m', 'src.main'],
            environment={
                'SPOTIFY_USER_ID': environ.get('SPOTIFY_USER_ID'),
                'JQBX_ROOM_ID': environ.get('JQBX_ROOM_ID'),
                'JQBX_BOT_DISPLAY_NAME': environ.get('JQBX_BOT_DISPLAY_NAME'),
                'JQBX_BOT_IMAGE_URL': environ.get('JQBX_BOT_IMAGE_URL')
            },
            logging=AwsLogDriver(
                stream_prefix='jqbx-bot',
                log_group=LogGroup(self, 'LogGroup')
            )
        )
        cluster = Cluster(self, '%sCluster' % _id)
        FargateService(self, '%sService' % _id, cluster=cluster, task_definition=task_definition, desired_count=1)


if __name__ == '__main__':
    app = App()
    MainStack(app, 'JqbxBot', env=Environment(region=environ.get('AWS_DEFAULT_REGION')))
    app.synth()
