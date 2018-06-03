def list_urls(filename):
    persistence_file = open(filename,'r')
    urllist = persistence_file.readlines()
    persistence_file.close()
    return urllist

def append_url(filename,url):
    persistence_file = open(filename,'a')
    persistence_file.write(url)
    persistence_file.write("\n")
    persistence_file.close()
