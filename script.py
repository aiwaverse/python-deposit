import requests as req
import time

form_link = "https://docs.google.com/forms/d/e/1FAIpQLSekuFgcsplzVCaRDKi52g3GQcMGPxqUmXB84XHfBmh8wSxZ0A"
form_link_full = form_link + "/formResponse"
params = {"entry.2066924173" : ["3YE", "Busters", "K/DA"]}

print("Starting script, press Ctrl+C to stop!")
count = 0
tic = time.perf_counter()
try:
    while True:
        response = req.post(form_link_full, params)
        if not response.ok:
            print("The response was not 200, aborting.")
            break
        count += 1
        if count % 100 == 0:
            toc = time.perf_counter()
            print(f"Votes so far: {count}\nTime to do: {toc - tic:0.4f} seconds")
            tic = toc
except KeyboardInterrupt:
    print("Done!")
