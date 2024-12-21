from twitchio.ext import commands
from twitchio import Message
from KafkaManager import KafkaManager
from typing import Optional

def check_connection_kafka_activated(kafkaManager) -> bool:
    return kafkaManager is not None and isinstance(kafkaManager, KafkaManager)


class TwitchChatListener(commands.Bot):
    def __init__(
        self, 
        token: str, 
        channel: str, 
        kafkaManager: Optional[KafkaManager] = None, 
        verbose: Optional[bool] = False
    ):
        """
        Initialise our TwitchChatListener with our access token, prefix and a list of channels to join on boot...
        prefix can be a callable, which returns a list of strings or a string...
        initial_channels can also be a callable which returns a list of strings...
        """
        super().__init__(token=f'oauth:{token}', prefix='!', initial_channels=[channel])
        self.kafkaManager = kafkaManager
        self.verbose = verbose

        print(f"[*] Twitch chat listener ready on the channel: {channel}")
        print(f"[*] Verbose mode: {"Enable" if self.verbose else "Disabled"}.")
        print(f"[*] Connection to Kafka: {"Actived" if check_connection_kafka_activated(self.kafkaManager) else "Not activated"}\n")


    async def event_ready(self):
        print(f'[*] Logged as (Username, User-id): ({self.nick},{self.user_id})')
        if check_connection_kafka_activated(self.kafkaManager):
            print(f"[*] Sending comments on the kafka topic: {self.kafkaManager.topic}")
        
        if self.verbose:
            print("[**] Comment:")

    async def event_message(self, message: Message):
        # We check if it is a reply message
        if 'reply-parent-user-id' in message.tags:
            reply = f"{message.tags['reply-parent-user-id']};{message.tags['reply-parent-user-login']};{message.tags['reply-parent-msg-id']};{message.tags['reply-parent-msg-body'].replace("\\s", " ")};"
        else:
            reply = f";;;;"

        # Selection of interesting fields in a message
        comment_data = f"{message.id};{message.timestamp.time()};{message.channel.name};{message.author.name};{message.author.is_mod};{message.author.is_subscriber};{message.author.is_turbo};{message.author.is_vip};{message.content};{message.first};{message.tags['user-id']};{message.tags['subscriber']};{message.tags['emotes']};{message.tags['flags']};{message.tags['returning-chatter']};" + reply

        if check_connection_kafka_activated(self.kafkaManager):
            self.kafkaManager.send_comment_to_kafka(comment_data)
        
        if self.verbose:
            print(f"{comment_data}")


if __name__ == '__main__':
    TOKEN_TWITCH = 'XXX'
    CHANNEL = 'channel'

    twitchChatListener = TwitchChatListener(TOKEN_TWITCH, CHANNEL, verbose=True)

    twitchChatListener.run()
    # TwitchChatListener.run() is blocking and will stop execution of any below code here until stopped or closed.
