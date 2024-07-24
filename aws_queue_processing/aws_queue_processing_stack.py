from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_event_sources
)
from constructs import Construct

class AwsQueueProcessingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create DLQ to handle with errors processing message
        dlq = sqs.Queue(
            self,
            'NewQueueDLQ'
        )

        # Create SQS
        new_queue = sqs.Queue(
            self,
            'NewQueue',
            # Attach dlq to handle with errors
            dead_letter_queue=sqs.DeadLetterQueue(
                max_receive_count=123,
                queue=dlq
            )
        )

        # Create SNS topic
        new_topic = sns.Topic(
            self,
            'NewTopic'
        )

        new_topic.add_subscription(subscriptions.SqsSubscription(new_queue))

        # Create lambda function (this will be our topic consumer)
        fn = _lambda.Function(
            scope=self,
            id='SqsProcessor',
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler='lambda_handler.handler',
            code=_lambda.Code.from_asset('aws_queue_processing/lambda'),
            timeout=Duration.seconds(15),
            memory_size=128,
        )

        # Create event source from new queue to be attached to lambda function consumer
        event_source = lambda_event_sources.SqsEventSource(new_queue)

        # Attach lambda to event source
        fn.add_event_source(event_source)
