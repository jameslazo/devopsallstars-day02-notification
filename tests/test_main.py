from moto import mock_aws # https://docs.getmoto.org/en/latest/docs/getting_started.html
from moto.core import DEFAULT_ACCOUNT_ID
from moto.sns import sns_backends # https://docs.getmoto.org/en/latest/docs/services/sns.html
import boto3
import pytest
from src.main import lambda_handler
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture(scope="function")
def mocked_aws(aws_credentials):
    """
    Mock all AWS interactions
    Requires you to create your own boto3 clients
    """
    with mock_aws():
        yield

@pytest.fixture
def create_sns_topic(mocked_aws):
    sns_client = boto3.client("sns", region_name="us-east-1")
    response = sns_client.create_topic(Name="test-topic")
    os.environ["SNS_TOPIC_ARN"] = response["TopicArn"]
    return response["TopicArn"]

@pytest.fixture
def sns_backend():
    """Access the internal SNS backend for message verification."""
    return sns_backends[DEFAULT_ACCOUNT_ID]["us-east-1"]

def test_lambda_sns_publish(create_sns_topic, sns_backend):
    """Test successful SNS message publishing."""
    # Run the Lambda handler with empty event and context (required arguments)
    response = lambda_handler({}, {})

    # Assertions for successful Lambda execution
    assert response["statusCode"] == 200
    assert "Data processed and sent to SNS" in response["body"]
