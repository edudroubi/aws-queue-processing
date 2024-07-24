def handler(event, lambda_context):
    raise Exception("Erro de processamento")
    print(f'event: {event}')
    print(f'context: {lambda_context}')
