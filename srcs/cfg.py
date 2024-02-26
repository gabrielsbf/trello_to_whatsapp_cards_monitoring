from configparser import ConfigParser
from utils.env_p import *

def cred(section):
	config = ConfigParser()
	config.read(CONFIG_PATH)
	tuple_items = config.items(section)
	object = {i[0] : i[1] for i in tuple_items}
	return object
