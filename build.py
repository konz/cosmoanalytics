import subprocess

from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin('pypi:pybuilder_aws_plugin')


name = "cosmoanalytics"
version = "0.1.dev"
default_task = "package_lambda_code"


@init
def set_properties(project):
    project.depends_on("boto3")
    project.set_property('bucket_name',
                         subprocess.run(['aws', 'cloudformation', 'describe-stacks', '--stack-name', 'cosmoanalytics-dist',
                                         '--query', 'Stacks[0].Outputs[?OutputKey==\'distributionBucket\'].OutputValue',
                                         '--output',  'text'], stdout=subprocess.PIPE).stdout.decode().rstrip())
