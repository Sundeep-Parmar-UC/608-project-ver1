import requests

def Obtain(EBSpath,fileName):

    url = "https://database.lichess.org/standard/"+ fileName
    downloadedFilePath = EBSpath + fileName

    # 1. Download the file
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status() # Ensure the download was successful

        with open(downloadedFilePath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=None):
                f.write(chunk)

    except requests.exceptions.RequestException as e:
        return "Failed"

    return downloadedFilePath
