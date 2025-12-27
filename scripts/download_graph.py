import requests

def download_graph():
    url = "https://huggingface.co/datasets/nasa-gesdisc/nasa-eo-knowledge-graph/resolve/main/graph.json?download=true"
    filename = "graph.json"

    print("starting download")
    
    # Stream the download to handle the large file size without using all your RAM
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("finished download")
    else:
        print(f"Failed to download. Status code: {response.status_code}")

if __name__ == "__main__":
    download_graph()