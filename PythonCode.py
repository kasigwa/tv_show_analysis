"""

Requirements: Python 3.6+
Library:
	requests

"""


import csv
import datetime
import json
import os
import requests
import traceback


column_names = ["id", "url", "name", "type", "language", "status", "runtime", "premiered", "rating_average", "summary", "network_name", "image_original"]


def exception_logger():
	"""
	This function returns the detailed error informationa and exceptions and errors.
	"""

	exception_log = traceback.format_exc().splitlines()
	exception_log.append(str(datetime.datetime.now()))
	print(exception_log)
	return exception_log


def read_urls_from_file():

	"""
	This function returns the list of tv shows URL's reading from the file tv_show_urls.txt.
	"""

	try:
		with open(os.path.join(os.getcwd(), 'tv_show_urls.txt')) as read_file:
			urls = read_file.readlines()
			urls = [i.strip('\n') for i in urls]

		return urls

	except FileNotFoundError as e:
		print("Error in loading file as it doesn't exist", str(e), str(datetime.datetime.now()))
		exception_logger()
		return []


def get_content(web_url=None):

	"""
	This function returns the content of the tv show url as a dictionary object.
	"""

	try:
		data = requests.get(web_url)
		output = json.loads((data.content).decode('utf-8'))

		return output

	except Exception as e:
		exception_logger()
		print("Error in getting content from the web", str(e), str(datetime.datetime.now()))
		return {}


def expand_json(url_content=None):

	"""
	This function returns the dictionary of expanded and filtered content retrieved from the show url.
	"""

	try:
		
		_id = url_content.get("id")
		url = url_content.get("url")
		name = url_content.get("name")
		_type = url_content.get("type")
		language = url_content.get("language")
		status = url_content.get("status")
		runtime = url_content.get("runtime")
		premiered = url_content.get("premiered")
		rating_average = url_content.get("rating",0).get('average')
		summary = url_content.get("summary")
		network_name = url_content.get("network").get('name')
		image_original = url_content.get("image").get('original')

		url_dict = {"id": _id, "url": url, "name": name, "type": _type, "language": language, "status": status, "runtime": runtime, "premiered": premiered, "rating_average": rating_average, "summary": summary, "network_name": network_name, "image_original": image_original}

		return url_dict

	except Exception as e:
		print("Error in expand_json function", str(e), str(datetime.datetime.now()))
		exception_logger()
		return {}


def write_tab_separated_file(final_url_expanded_contents=None):

	"""
	This function writes the tab separated file with name output_tv_shows.tsv in the current directory.
	"""

	try:
		with open(os.path.join(os.getcwd(), 'output_tv_shows.tsv'), 'w') as out:
			writer = csv.DictWriter(out, fieldnames=column_names, delimiter='\t')
			writer.writeheader()
			writer.writerows(final_url_expanded_contents)

			print(f"Tab Separated File has been saved successfully at path ==> {os.path.join(os.getcwd(), 'output_tv_shows.tsv')}")

			return True

	except Exception as e:
		print("Error in write_tab_separated_file function", str(e), str(datetime.datetime.now()))
		exception_logger()
		return False


def main():

	"""
	This function executes the task and steps mentioned in the README.md file.
	"""

	try:

		final_url_expanded_contents = list()

		url_list = read_urls_from_file()

		if url_list:
			for ind, url in enumerate(url_list):
				try:
					print(f"Getting the URL CONTENT FOR INDEX {ind}")
					url_content = get_content(web_url=url)
					print(f"URL content retrieved successfully for URL==> {url}")
					
					if url_content:
						print("Expanding the results into dictionary")
						expanded_content = expand_json(url_content=url_content)
						print("Results expanded successfully")

					if expanded_content:
						final_url_expanded_contents.append(expanded_content)

					print("*"*150)

				except Exception as e:
					print("Error inside the for loop", str(e))
					print(f"The URL causing Error is == {url}")
					exception_logger()

		else:
			print("The URL's text file is Empty")
			return


		print("=="*75)
		print("=="*75)
		
		if final_url_expanded_contents:
			print("Trying to Save TSV file")
			file_written = write_tab_separated_file(final_url_expanded_contents = final_url_expanded_contents)

			if file_written:
				print("File Written Successfully")
			else:
				print("There is some problem with the writing of the file")

	except Exception as e:
		print("Error in the main function.", str(e), str(datetime.datetime.now()))
		exception_logger()



if __name__ == '__main__':
	main()

