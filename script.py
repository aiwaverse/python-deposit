import requests as req
from concurrent.futures import *
import time
from multiprocessing import cpu_count

def submit_form(link, params):
    response = req.post(link, params)
    return response

if __name__ == "__main__":
    # add here the form link, everything before /formResponse, without any of the viewform part
    # example: form_link = "https://docs.google.com/forms/d/e/[string of numbers and letters]"
    form_link = ""
    form_link_full = form_link + "/formResponse"
    # add here the entries, each entry may be an array of strings if an entry allows multiple answers
    # example: {"entry.123456789" : ["A", "B", "C"]} or {"entry.123456789" : "D"}
    params = {}
    count = 0
    tic = time.perf_counter()
    # this controls the number of cpu cores used, by default it uses every core available since it's a simple script
    # feel free to change this if you so desire
    cpu_number = cpu_count()
    print("Starting script, press Ctrl+C to stop!")
    try:
        while True:
            with ThreadPoolExecutor(max_workers = cpu_number) as executor:
                futures = [executor.submit(submit_form, form_link_full, params) for i in range(0,cpu_number)]
                if not all([f.result().ok for f in futures]):
                    print("Not all responses were 200. Aborting.")
                    break
                count += 2
                if count % 100 == 0:
                    toc = time.perf_counter()
                    print(f"Votes so far: {count}.\nTime to do: {toc - tic:0.4f} seconds")
                    tic = toc
    except KeyboardInterrupt:
        print("Done!")
