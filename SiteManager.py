
import time
import sys
from processOutput import parseReturn
import json
print sys.version_info
import httplib2
from multiprocessing import Lock, Process, Queue, current_process


def worker(work_queue, done_queue):
    try:
        for url in iter(work_queue.get, 'STOP'):
            status_code = print_site_status(url)
            done_queue.put("%s | %s | %s" % (current_process().name, url, status_code))
    except Exception, e:
        done_queue.put("%s | %s | %s | %s" % (current_process().name, url,5000,e.message))
    return True


def print_site_status(url):
    http = httplib2.Http(timeout=10)
    headers, content = http.request(url)
    time.sleep(6)


    return headers.get('status', 'no response')


def main():

    sites_json = open("sites.json")
    siteData = json.load(sites_json)
    sites = siteData["sites"]
    sites_json.close()

    print "looking at ", len(sites), " sites"
    workers = 4
    outputFileBad = "./output/bad.json"
    work_queue = Queue()
    done_queue = Queue()
    processes = []

    for url in sites:
        work_queue.put(url)

    for w in xrange(workers):
        p = Process(target=worker, args=(work_queue, done_queue))
        p.start()
        processes.append(p)
        work_queue.put('STOP')

    for p in processes:
        p.join()

    done_queue.put('STOP')


    statusOutput = { "results":[]}

    for status in iter(done_queue.get, 'STOP'):

        statusOutput["results"].append(status)

    good,bad = parseReturn( statusOutput["results"] )

    if len(bad) > 0:
        print "found {0} bad sites ".format(len(bad))
        f = open(outputFileBad,'w')
        f.write( json.dumps( bad ))
        f.close()

if __name__ == '__main__':
    main()