import threading
import time
import requests

URLS = [
  "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
  "https://images.unsplash.com/photo-1519681393784-d120267933ba",
  "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
  "https://images.unsplash.com/photo-1498050108023-c5249f4df085",
  "https://images.unsplash.com/photo-1522202176988-66273c2fd55f"
]

def download_image(url):
    print(f"Started download from {url}")
    resp = requests.get(url)
    print(f"Finished downloading from {url}, Size: {len(resp.content)} bytes")

start = time.time()

threads = []

for url in URLS:
    # WITHOUT THREAD: It takes more time
    # download_image(url)

    # IN this you spread image downloading on different threads which gave you faster result
    t = threading.Thread(target=download_image, args=(url,))
    t.start()
    threads.append(t)


for t in threads:
    t.join()

end = time.time()

print(f"Ended downloading in {end-start} time")