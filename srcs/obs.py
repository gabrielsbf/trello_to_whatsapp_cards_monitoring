from watchdog.observers import Observer
from watchdog.observers.api import ObservedWatch
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from utils.env_p import *
from srcs.classes.Trello_Manager import TrelloManager
from srcs.classes.Selenium_Exec import *
from time import sleep
import re
from datetime import datetime

class Event_Handler(FileSystemEventHandler):
	def __init__(self, social: TrelloManager, sl: Selenium_Manager):
		self.social = social
		self.sl = sl
	def catch_all_handler(self, event):
		pass

	def on_modified(self, event):
		chat_text = self.sl.access_field(By.XPATH, WP_AUTO["MESSAGE_BOX"], 60)
		data = self.social.load_json_file("new_cards", BOARD_MOVEMENTES_PATH + "new_card_fd")
		text = self.social.trello_text(data)
		list_text = re.split("\n|\t", text)
		for i in list_text:
			self.sl.do_action(chat_text, 'send_keys', i, False)
			self.sl.do_presskeys(Keys.LEFT_SHIFT, Keys.RETURN)
		self.sl.do_action(chat_text, "send_keys", '', True)

def observe_file_change(file_path, social: TrelloManager, sl: Selenium_Manager):
	print("listening at: " + file_path)
	observer = Observer()
	event_handler = Event_Handler(social, sl)
	observer.schedule(event_handler,file_path, recursive=True)
	return observer


def monitoring_req(wspace: TrelloManager):
	print("MONITORING NEW REQUISITIONS")
	info = wspace.have_new_inputs("cards")

	if info[0] == False:
		print("You don't have new data, at : ", datetime.now())
		return False

	else:
		print("new data encountered at : ", datetime.now())
		wspace.write_or_load("write", "cards")
		wspace.write_json_file(info[1], "new_cards",  BOARD_MOVEMENTES_PATH + "new_card_fd")


# observe_file_change(BOARD_MOVEMENTES_PATH + "new_card_fd/")
