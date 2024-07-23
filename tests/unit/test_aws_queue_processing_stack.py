import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_queue_processing.aws_queue_processing_stack import AwsQueueProcessingStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_queue_processing/aws_queue_processing_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsQueueProcessingStack(app, "aws-queue-processing")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
