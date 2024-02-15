from classes.Selenium_Exec import *
from classes.Trello_Manager import *
from datetime import datetime
import re


whats_automate = Selenium_Manager("web.whatsapp.com")

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



if __name__ == "__main__":
	groups = whats_automate.access_field(By.XPATH, "//div[@class='to2l77zo gfz4du6o ag5g9lrv bze30y65 kao4egtt qh0vvdkp']/p[@class='selectable-text copyable-text iq0m558w g0rxnol2']", 60)
	whats_automate.do_action(groups, "send_keys", "Notas", True)
	while(True):
		data = monitoring_req()
		sleep(10)
		if data != False:
			chat_text = whats_automate.access_field(By.XPATH, "//div[@class='to2l77zo gfz4du6o ag5g9lrv bze30y65 kao4egtt']/p[@class='selectable-text copyable-text iq0m558w g0rxnol2']", 60)
			list_data = re.split("\n|\t", data)
			for i in list_data:
				print(i)
				whats_automate.do_action(chat_text, "send_keys", i, False)
				whats_automate.do_presskeys(Keys.LEFT_SHIFT, Keys.RETURN)
			whats_automate.do_action(chat_text, "send_keys", '', True)



