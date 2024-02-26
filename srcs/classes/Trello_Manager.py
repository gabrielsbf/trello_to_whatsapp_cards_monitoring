from configparser import ConfigParser
import requests
import json
from srcs.cfg import cred
from datetime import datetime
from utils.env_p import *

class TrelloManager:

	def __init__(self, workspace):
		self.workspace_name = workspace
		self.id = self.fetch_specific_elem(str('/members/'
											+ self.basic_info['creds']['username']
											+ '/boards'),
											'name',
											workspace)[0]['id']
		self.cards = self.fetch_endpoints_url('cards')
		self.lists = self.fetch_endpoints_url('lists')
		self.board = self.fetch_endpoints_url('workspace')
		self.board_path = BOARDS_JSON_PATH + '/' + self.workspace_name

	basic_info = {
			'creds': cred('trello_api'),
			'endpoints' :
			{
				'workspace' : '/boards',
				'lists' : '/lists',
				'cards' : '/cards'
			}
		}

	def fetch_any_url(self, endpoint):
		headers = {
			"Accept":"application/json"
		}
		completeUrl = self.basic_info['creds']['domain'] + endpoint + "?key=" + self.basic_info['creds']['key'] + "&token=" + self.basic_info['creds']['token'];
		response = requests.get(url=completeUrl,headers=headers)
		return (response.json())

	def fetch_endpoints_url(self, child, father='workspace', list_name=''):

		if child == 'workspace':
			data = self.fetch_specific_elem('/members/'
											+ self.basic_info['creds']['username']
											+ '/boards',
											'name',
											self.workspace_name)
			return data

		elif child == 'cards' and father == 'lists':
			element_id = self.fetch_specific_elem(self.basic_info['endpoints']['workspace'] +
								'/' +
								self.id +
								self.basic_info['endpoints']['lists'],
								'name',
								list_name)['id']
		else:
			element_id = self.id

		data = self.fetch_any_url(self.basic_info['endpoints'][father] +
						'/' +
						element_id +
						self.basic_info['endpoints'][child]
						)
		return data

	def fetch_specific_elem(self, endpoint, key, element):
		if self.basic_info['endpoints'].get(endpoint) == None:
			json_el = self.fetch_any_url(endpoint)
		else:
			json_el = self.fetch_endpoints_url(endpoint, 'workspace')
		ans = list(filter(lambda x :(x[key] == element) , json_el))

		return ans

	def definig_types(self, type):
		data = type
		match data:
			case 'cards':
				json_obj = self.cards
			case 'lists':
				json_obj = self.lists
			case 'board':
				json_obj = self.board
		return json_obj

	def write_or_load(self, method, type):

		def write_json_file(json_obj, file_name, folder='.'):
			json_parse = json.dumps(json_obj)
			with open(folder + '/' + file_name + '.json', 'w') as json_file:
				json_file.write(json_parse)

		def load_json_file(file_name, folder='.'):
			with open(folder + '/' +  file_name + '.json') as json_obj:
				data = json.load(json_obj)
				return data

		if method == 'write':
			write_json_file(self.definig_types(type), self.workspace_name + "_" + type, self.board_path)
		elif method == 'load':
			return load_json_file(self.workspace_name + "_" + type, self.board_path)

	#that definition can be used to display any changes on a field - may show an old card that has been changed
	def have_new_data(self, type):
		new_json_req = self.definig_types(type)
		json_file = self.write_or_load('load', type)

		result = list(filter(lambda x : x not in json_file, new_json_req))
		if result == []:
			return [False, result]
		else:
			return [True, result]

	def have_new_inputs(self, type):
		new_json_req = self.definig_types(type)
		json_file = self.write_or_load('load', type)
		result = []
		for field in new_json_req:
			is_equal = list(filter(lambda x : x['id'] == field['id'], json_file))
			if is_equal == []:
				result.append(field)
		if result == []:
			return [False, result]
		else:
			return [True, result]


	def trello_text(self, json_obj):
		separator = '-----------------------------------------------------'
		text = f"""{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - NOVO(s) CARD(s) TRELLO\n{separator}
		"""


		for cat in json_obj:
			header = "Título do Card: " + cat['name']
			# desc = "descrição: " + cat['desc']
			list_obj = self.lists
			get_list_by_id = str([n['name'] for n in list_obj if n['id'] == cat['idList']])
			list_name = "Responsável: " + get_list_by_id.replace('[','').replace(']','')
			url_trello = "Job: " + cat["shortUrl"]

			entire_text = '\n'.join([header, url_trello, list_name])
			text = '\n'.join([text, entire_text, separator])
			# print(entire_text)
		return text
