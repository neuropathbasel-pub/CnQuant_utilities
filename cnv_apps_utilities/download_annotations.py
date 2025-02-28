import requests

DATA_ANNOTATION_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRhQ7Cr3aBo8W9Ne8DAehMvFRxYd395ENIW9giK2ATQ3QSrM8jA2E7xXbnW7CWKMdh0IhN0YqWn37Wr/pub?gid=0&single=true&output=csv"
REFERENCE_DATA_ANNOTATION_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRhQ7Cr3aBo8W9Ne8DAehMvFRxYd395ENIW9giK2ATQ3QSrM8jA2E7xXbnW7CWKMdh0IhN0YqWn37Wr/pub?gid=522048357&single=true&output=csv"


def download_annotation_data(annotation_url: str, reference_data_url: str, annotation_path, reference_annotation_path):
    response = requests.get(url=annotation_url)

    if response.status_code == 200:
        with open(file=annotation_path, mode="wb") as file:
            file.write(response.content)
    else:
        print(f"Failed to fetch the sheet. Status code: {response.status_code}")

    response = requests.get(url=reference_data_url)

    if response.status_code == 200:
        with open(file=reference_annotation_path, mode="wb") as file:
            file.write(response.content)
    else:
        print(f"Failed to fetch the sheet. Status code: {response.status_code}")