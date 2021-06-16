# downloads the latest data from just eat cycles api
import os
import wget

# dic that maps filename to url ("filename":"url")
json_urls = {
    "station_status.json": "https://gbfs.urbansharing.com/edinburghcyclehire.com/station_status.json",
    "station_information.json": "https://gbfs.urbansharing.com/edinburghcyclehire.com/station_information.json",
}


def download_json(json_urls):
    for file, url in json_urls.items():
        print(f"Checking:{file}")
        if os.path.exists(file):
            # if file exist, remove it
            print(f"Exists:{file}")
            os.remove(file)
        wget.download(
            url, out=f"json_data/{file}", bar=None
        )
    print(f"Downloading:{file}")


download_json(json_urls)
