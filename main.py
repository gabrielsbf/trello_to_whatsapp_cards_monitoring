from srcs.classes.Selenium_Exec import *
from srcs.classes.Trello_Manager import *
from datetime import datetime
from time import sleep
from srcs.obs import *
from utils.env_p import *


trello_manager = TrelloManager("MOVEMENTES")
whats_automate = Selenium_Manager("web.whatsapp.com")
if __name__ == "__main__":
	print("iniciando processo")

	whats_automate.access_url()
	print("url acessada com sucesso")
	groups = whats_automate.access_field(By.XPATH, WP_AUTO["FIND_CHAT"] , 60)
	whats_automate.do_action(groups, "send_keys", "Notas", True)
	observer = observe_file_change(BOARD_MOVEMENTES_PATH + "new_card_fd", trello_manager, whats_automate)
	observer.start()
	try:
		while True:
			sleep(1)
	except KeyboardInterrupt:
		observer.unschedule_all()
		observer.stop()
	observer.join()
	whats_automate.driver.quit()


