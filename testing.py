import requests
import time
from tqdm import tqdm

def get_wikidata_id(title, source_lang="th"):
    url = f"https://{source_lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": title,
        "prop": "pageprops",
        "format": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "pageprops" in page and "wikibase_item" in page["pageprops"]:
                return page["pageprops"]["wikibase_item"]
    except requests.exceptions.RequestException as e:
        tqdm.write(f"Error fetching Wikidata ID for {title}: {e}")
    return None

def get_page_in_language(wikidata_id, target_lang="my"):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetentities",
        "ids": wikidata_id,
        "props": "sitelinks",
        "format": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        sitelinks = data.get("entities", {}).get(wikidata_id, {}).get("sitelinks", {})
        lang_key = f"{target_lang}wiki"
        if lang_key in sitelinks:
            return sitelinks[lang_key]["title"]
    except requests.exceptions.RequestException as e:
        tqdm.write(f"Error fetching page in {target_lang} for {wikidata_id}: {e}")
    return None

def find_page_in_language(title, source_lang="th", target_lang="my"):
    wikidata_id = get_wikidata_id(title, source_lang)
    if not wikidata_id:
        return None
    time.sleep(1)  # Prevent hitting API limits
    translated_title = get_page_in_language(wikidata_id, target_lang)
    if translated_title:
        return f"https://{target_lang}.wikipedia.org/wiki/{translated_title.replace(' ', '_')}"
    return None

def process_titles(input_file, output_file, missing_file, source_lang="th", target_lang="my"):
    with open(input_file, "r", encoding="utf-8") as infile:
        titles = [line.strip() for line in infile if line.strip()]
    
    with open(output_file, "w", encoding="utf-8") as outfile, open(missing_file, "w", encoding="utf-8") as missfile:
        for title in tqdm(titles, desc="Processing Titles", unit="title"):
            translated_page = find_page_in_language(title, source_lang, target_lang)
            if translated_page:
                outfile.write(f"{title}\t{translated_page}\n")
            else:
                missfile.write(f"{title}\n")

# Example Usage
input_file = "titles_only.txt"  # File containing 20,000 Wikipedia titles (one per line)
output_file = "Thai_important_titles_to_Laos.txt"  # Output file for successful translations
missing_file = "Thai_titles_without_translations_for_Laos.txt"  # File for titles that couldn't be translated
process_titles(input_file, output_file, missing_file)
