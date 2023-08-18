import configparser

config = configparser.ConfigParser()
config.read('./resource/config.ini')

gpt_access_token = config['gpt_chat']['access_token']