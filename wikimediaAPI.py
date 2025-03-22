import requests
import csv
from datetime import date, timedelta
from urllib.parse import quote
from tqdm import tqdm
import time
import logging

def encodeTitle(title):
    return quote(title.strip(), safe="")

def getViewCounts(page_title, start_date, end_date, retry=3):
    encoded_title = encodeTitle(page_title)

    api_url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/th.wikipedia.org/all-access/user/{encoded_title}/daily/{start_date.strftime('%Y%m%d')}/{end_date.strftime('%Y%m%d')}"

    for attempt in range(retry):
        try:
            response = requests.get(api_url, headers={"User-Agent": "Wikipedia Page View Analysis"})
            response.raise_for_status()
            data = response.json()
            daily_counts = {item["timestamp"][:8]: item["views"] for item in data.get("items", [])}
            return [
                daily_counts.get((start_date + timedelta(days=i)).strftime("%Y%m%d"), -1)
                for i in range((end_date - start_date).days + 1)
            ]

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logging.error(f"Page '{page_title}' not found on Thai Wikipedia.")
                return [-1] * ((end_date - start_date).days + 1)
            else:
                logging.warning(f"Attempt {attempt + 1} failed for '{page_title}': {e}")
                if attempt < retry - 1:
                    time.sleep(2)
                else:
                    logging.error(f"Skipping '{page_title}' after {retry} failed attempts.")
                    return [-1] * ((end_date - start_date).days + 1)
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} failed for '{page_title}': {e}")
            if attempt < retry - 1:
                time.sleep(2)
            else:
                logging.error(f"Skipping '{page_title}' after {retry} failed attempts.")
                return [-1] * ((end_date - start_date).days + 1)

def downloadData(input_file_path, output_file_path, start_date, end_date):
    try:
        with open(input_file_path, "r", encoding="utf-8") as infile:
            titles = [line.strip() for line in infile if line.strip()] 
    except FileNotFoundError:
        logging.error(f"Input file '{input_file_path}' not found.")
        return

    total_titles = len(titles)
    print(f"Total titles to process: {total_titles}")

    with open(output_file_path, "w", encoding="utf-8", newline="") as outfile:
        all_days = [
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((end_date - start_date).days + 1)
        ]
        writer = csv.writer(outfile)
        writer.writerow(["Page Title"] + all_days)

        processed_titles = 0
        for title in tqdm(titles, desc="Downloading data", unit="page"):
            viewCounts = getViewCounts(title, start_date, end_date)
            writer.writerow([title] + viewCounts)
            processed_titles += 1

        print(f"Processed {processed_titles}/{total_titles} titles")

    input_file = "titles_only.txt"
    output_file = "wikimedia-dataset-for-2016-to-2024.csv"
    start_date = date(2016, 1, 1)
    end_date = date(2024, 12, 31)

    downloadData(input_file, output_file, start_date, end_date)

    print(f"File saved to {output_file}")