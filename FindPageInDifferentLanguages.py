import requests

def get_wikidata_id(title, source_lang="th"):
    url = f"https://{source_lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": title,
        "prop": "pageprops",
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        if "pageprops" in page and "wikibase_item" in page["pageprops"]:
            return page["pageprops"]["wikibase_item"]
    return None

def get_page_in_language(wikidata_id, target_lang="en"):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetentities",
        "ids": wikidata_id,
        "props": "sitelinks",
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    sitelinks = data.get("entities", {}).get(wikidata_id, {}).get("sitelinks", {})
    lang_key = f"{target_lang}wiki"
    if lang_key in sitelinks:
        return sitelinks[lang_key]["title"]
    return None

def find_page_in_language(title, source_lang="th", target_lang="en"):
    wikidata_id = get_wikidata_id(title, source_lang)
    if not wikidata_id:
        return None
    translated_title = get_page_in_language(wikidata_id, target_lang)
    if translated_title:
        return f"https://{target_lang}.wikipedia.org/wiki/{translated_title.replace(' ', '_')}"
    return None

def process_titles(input_file, output_file, source_lang="th", target_lang="en"):
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            title = line.strip()
            if title:
                translated_page = find_page_in_language(title, source_lang, target_lang)
                outfile.write(f"{title}\t{translated_page}\n")
                print(f"Processed: {title} -> {translated_page}")

input_file = "titles_only.txt"
output_file = "Thai_important_titles_to_English.txt"
process_titles(input_file, output_file)
