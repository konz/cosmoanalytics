# Cosmoanalytics

*Work in progress!*

## Installation

## Development

```bash
# Create the bucket for packaged Lambda code:
aws cloudformation deploy --template-file cloudformation/distribution-bucket.yaml --stack-name cosmoanalytics-dist

virtualenv venv
source venv/bin/activate
pip install pybuilder

pyb install_dependencies
pyb lambda_release

aws cloudformation deploy --stack-name cosmoanalytics --template-file cloudformation/cosmoanalytics.yaml --capabilities CAPABILITY_IAM
```