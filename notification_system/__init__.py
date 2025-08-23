from faststream import FastStream
from faststream.rabbit import RabbitBroker

broker = RabbitBroker('amqp://guest:guest@localhost:5672')

app = FastStream(broker)


@broker.subscriber(
    queue='test',
    retry=2,
)
async def base_handler(body):
    print(body)
