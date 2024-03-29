from bs4 import BeautifulSoup
import requests
from constants.constants import URL


def scrape_schedule_table() -> list:
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    table_data = []

    for row in table.find_all('tr'):
        row_data = [cell.text for cell in row.find_all(['td'])]
        table_data.append(row_data)

    return table_data


async def execute_day_schedule(date) -> list:
    data = scrape_schedule_table()[2:]
    result_list = [
        f"""
{sublist[0].strip("-")} ({sublist[1]}), пара: {sublist[2]}.
Аудитория: {sublist[6]}
{sublist[3]} ({sublist[4]})
Преподаватель: {sublist[5]}
"""
        for sublist in data if sublist[0].strip("-") == date and sublist[-1] != "+"]
    return result_list
