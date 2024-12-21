from KafkaManager import KafkaManager
from TwitchChatListener import TwitchChatListener

import argparse
import multiprocessing
import time
import signal
import sys


def get_args():
	# Initializing the argument parser
	parser = argparse.ArgumentParser(
		description="A tool to retrieve live comments from a Twitch channel and send them to a Kafka topic."
	)
	
	parser.add_argument(
		"-s", "--server",
		type=str,
		required=True,
		help="Address of the server (e.g., localhost:8080)."
	)
	parser.add_argument(
		"-c", "--channel",
		nargs='+',  # Multiple values
		type=str,
		required=True,
		help="Name(s) of the Twitch channel(s) where you want to retrieve live comments."
	)
	parser.add_argument(
		"-t", "--topic",
		type=str,
		required=True,
		help="Name of your Kafka topic to receive the data."
	)
	parser.add_argument(
		"-tt", "--twitch_token",
		type=str,
		required=True,
		help="OAuth Twitch token for authentication."
	)
	parser.add_argument(
		"-v", "--verbose",
		action="store_true",
		default=False,
		help="Enable verbose mode for detailed logging (default: False)."
	)
    

	return parser.parse_args()


if __name__ == '__main__':
	# Retrieve arguments
	args = get_args()

	# Constantes
	SERVER = args.server
	TOPIC_KAFKA = args.topic

	TOKEN_TWITCH = args.twitch_token
	CHANNELS = args.channel


	# Launching connection to Kafka server
	kafkaManager = KafkaManager(SERVER, TOPIC_KAFKA)


	# Launching Twitch Listener
	twitchChatListener = TwitchChatListener(TOKEN_TWITCH, CHANNELS[0], kafkaManager=kafkaManager, verbose=args.verbose)
	twitchChatListener.run()
	# TwitchChatListener.run() is blocking and will stop execution of any below code here until stopped or closed.

