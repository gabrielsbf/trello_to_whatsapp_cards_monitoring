from srcs.classes.Selenium_Exec import *
from srcs.classes.Trello_Manager import *
from datetime import datetime
import re
from utils.env_p import *

def monitoring_req():
	move_wspc = TrelloManager("MOVEMENTES")
	print("MONITORING NEW REQUISITIONS")
	info = move_wspc.have_new_inputs("cards")

	if info[0] == False:
		print("You don't have new data, at : ", datetime.now())
		return False

	else:
		data = move_wspc.trello_text(info[1])
		print(f"New data is: {data}")
		move_wspc.write_or_load("write", "cards")
		return str(data)

whats_automate = Selenium_Manager("web.whatsapp.com")
if __name__ == "__main__":
	print("iniciando processo")

	whats_automate.access_url()
	groups = whats_automate.access_field(By.XPATH, WP_AUTO["FIND_CHAT"] , 60)
	whats_automate.do_action(groups, "send_keys", "Notas", True)
	data = monitoring_req()
	if data != False:
		chat_text = whats_automate.access_field(By.XPATH, WP_AUTO["MESSAGE_BOX"], 60)
		list_data = re.split("\n|\t", data)
		for i in list_data:
			print(i)
			whats_automate.do_action(chat_text, "send_keys", i, False)
			whats_automate.do_presskeys(Keys.LEFT_SHIFT, Keys.RETURN)
		whats_automate.do_action(chat_text, "send_keys", '', True)
	else:
		print("no data")
		sleep(5)
	whats_automate.driver.quit()
	sleep(10)


