import csv
import urllib.request

from bs4 import BeautifulSoup

TARGET_URL = "https://simferopol.hh.ru/search/vacancy?text=django&area=113"


def get_html(url):
	response = urllib.request.urlopen(url)

	return response.read()


def get_page_count(html):
	soup = BeautifulSoup(html, "html.parser")
	paggination = soup.find("div", class_="b-pager m-pager_left-pager HH-Pager")

	return int(paggination.find_all('li')[-2].text)


def parse(html):
	soup = BeautifulSoup(html, "html.parser")
	table = soup.find("div", class_="search-result")
	rows = table.find_all("div", class_="search-result-item search-result-item_standard ")[1:]

	vacancies = []
	for row in rows:
		cols = row.find_all('div')

		vacancies.append({
			'title': cols[0].a.text,
			'about': cols[0].div.text,
			'resp': cols[0].div.text,
			'price': cols[0].a.text,
		})

	return vacancies
#print(parse(get_html(TARGET_URL)))


def save(vacancies, path):
	with open(path, 'w') as csvfile:
		writer = csv.writer(csvfile)

		writer.writerow(('Title', 'About', 'Responsibilies', 'Price'))

		writer.writerows(
			(vacancy['title'], ', '.join(vacancy['about']), vacancy['resp'], vacancy['price']) for vacancy in vacancies
		)


def main():
	total_pages = get_page_count(get_html(TARGET_URL))

	print('Found %s pages' % total_pages)

	projects = []

	for page in range(1, total_pages + 1):
		print('Parsing %d%% (%d/%d)' % (page / total_pages * 100, page, total_pages))
		projects.extend(parse(get_html(TARGET_URL + "page=%d" % page)))

	save(projects, 'data/vacanсies.csv')
	print('Saved!')


if __name__ == '__main__':
	main()
