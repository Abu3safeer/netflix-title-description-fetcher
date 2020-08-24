import requests
from bs4 import BeautifulSoup
import csv

# Set link variable
link = 'https://www.netflix.com/'

# Supported languages
languages = ['ar', 'en']

# Ask user for show ID and language code
show_id = input("Title/Show ID: ")
print(f"Supported languages are {languages}")
language_code = input("Type language code: ")

# Check if language code is supported
if language_code not in languages:
    input('langauge code not supported. press any key to exit...')
    exit()

# Format the link based on language code
if language_code == 'en':
    link += f'title/{show_id}'
else:
    link += f'{language_code}/title/{show_id}'

# Fetch HTML page from netflix
pagedata = requests.get(
    link,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
)

# parse fetched html
parsed_html = BeautifulSoup(pagedata.text, features='html.parser')

# Find title using query selector
title = BeautifulSoup.select_one(parsed_html, ".title-title")
if not title:
    input("Show not found. press any key to exit...")
    exit()
# Set title variable
title = title.text
print("Fetching " + title)

# Prepare csv file
csv_target = open(f'{title}.csv', 'w', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(csv_target)

# Find seasons using query selector
seasons_count = BeautifulSoup.select_one(parsed_html, ".test_dur_str")

if seasons_count is None:
    input("No seasons found. press any key to exit...")
    exit()

seasons_count = seasons_count.text.split(" ", 1)[0]

print(f"Show {title} has {seasons_count} seasons.")

# parse seasons blocks in html
seasons = BeautifulSoup.select(parsed_html, '.season')

# Start parsing each season
for season in enumerate(seasons):
    print(f"Processing season {season[0] + 1}")

    # Find episodes using query selector
    episodes = BeautifulSoup.select(season[1], '.episode')
    print(f"Season {season[0] + 1} has {len(episodes)} Episodes")

    # Write season number to csv file
    csv_writer.writerow([f"Season {season[0] + 1}"])
    csv_writer.writerow([' '])

    # Start parsing each episode
    for episode in episodes:

        # Find episode number and title using query selector
        episode_name = BeautifulSoup.select_one(episode, '.episode-title').text.split('.', 1)
        episode_number = episode_name[0]
        episode_title = episode_name[1]
        print(f"Episode {episode_number}'s title is: {episode_title}")

        # Find episode synopsis using query selector
        episode_description = BeautifulSoup.select_one(episode, '.epsiode-synopsis').text
        print(episode_description)

        # Write data to csv file
        csv_writer.writerow([episode_number])
        csv_writer.writerow([episode_title])
        csv_writer.writerow([episode_description])
        csv_writer.writerow([' '])

# Close csv file
csv_target.close()