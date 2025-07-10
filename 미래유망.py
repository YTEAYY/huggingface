import requests
from bs4 import BeautifulSoup

def huggingface_scraper(user_id):
    url = f"https://huggingface.co/{user_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    print(f"== Huggingface User: {user_id} ==")
    print(f"URL: {url}\n")

    model_cards = soup.find_all("a", href=True)
    model_list = []

    for card in model_cards:
        href = card['href']
        if href.startswith(f"/{user_id}/") and '/datasets/' not in href:
            full_name = href.strip('/')
            text = card.get_text(separator=' ', strip=True)

            parent = card.find_parent('article')
            if parent:
                span_tags = parent.find_all('span')
                task = "Text Classification"
                size = "Unknown"
                updated = "Unknown"

                for tag in span_tags:
                    content = tag.text.strip()
                    if 'B' in content:
                        size = content
                    elif 'ago' in content:
                        updated = content

                model_info = f"{full_name} | {task} | Size: {size} | Updated: {updated}"
                model_list.append(model_info)

    if model_list:
        for idx, model in enumerate(model_list, start=1):
            print(f"[{idx}] {model}")
            print("-" * 60)
    else:
        print("모델 정보를 찾지 못했습니다.")

huggingface_scraper("YTEAYY")
