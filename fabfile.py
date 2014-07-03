from fabric.api import *
import requests
import json

CLIENT_ID="XXXXXXXX"
API_KEY="XXXXXX"


API_DO_DROPLETS = "https://api.digitalocean.com/droplets?client_id="+CLIENT_ID+"&api_key="+API_KEY
API_DO_IMAGES = "https://api.digitalocean.com/images?client_id="+CLIENT_ID+"&api_key="+API_KEY
API_DO_REGIONS = "https://api.digitalocean.com/regions?client_id="+CLIENT_ID+"&api_key="+API_KEY
API_DO_SIZES = "https://api.digitalocean.com/sizes?client_id="+CLIENT_ID+"&api_key="+API_KEY
API_DO_DROPLET_ACTION = "https://api.digitalocean.com/droplets/{0}/{1}?client_id="+CLIENT_ID+"&api_key="+API_KEY
API_DO_DROPLET_NEW = "https://api.digitalocean.com/droplets/new?client_id="+CLIENT_ID+"&api_key="+API_KEY+"&name={0}&size_id={1}&image_id={2}&region_id={3}"
API_DO_DROPLET_DESTROY = "https://api.digitalocean.com/droplets/destroy?client_id="+CLIENT_ID+"&api_key="+API_KEY+"&name={0}&size_id={1}&image_id={2}&region_id={3}"


# 2 - Amsterdam 1, 1 - New York 1, 3 - San Francisco 1, 4 -  New York 2, 5- Amsterdam 2
DEFAULT_REGION_ID = 5
# 62 - 2GB, 63 - 1GB, 66 - 500Mb, 64 - 4GB, ...
DEFAULT_SIZE_ID = 66
DEFAULT_NODE_NAME="node"


@task
def images():
    """Showing existing images """

    print "Showing images ..."
    d = get(API_DO_IMAGES)
    for image in d.get("images"):
        print "{0}, id={1}".format(image.get("name"), image.get("id"))
    return d

@task
def regions():
    """Showing existing regions """

    print "Showing regions ..."
    d = get(API_DO_REGIONS)
    for image in d.get("regions"):
        print "{0}, id={1}".format(image.get("name"), image.get("id"))
    return d

@task
def sizes():
    """Showing existing sizes """

    print "Showing sizes ..."
    d = get(API_DO_SIZES)
    for image in d.get("sizes"):
        print "{0}, id={1}".format(image.get("name"), image.get("id"))
    return d

@task
def droplets(name=None):
    """ List existing droplets matching given name """

    print "Getting droplets ..."
    response = get(API_DO_DROPLETS)
    droplets = response.get("droplets")

    # filtering by name
    if name :
        droplets_filtered = [d for d in droplets if name in d.get("name")]
        droplets = droplets_filtered

    for d in droplets:
        print "{0}->{1},{2},{3}".format(d.get("name"), d.get("ip_address"), d.get("id"),d.get("status"))

    print "Total droplets found {0}".format(len(droplets))
    return droplets

@task
def action(action,name=DEFAULT_NODE_NAME):
    """ Do action on droplet : ex. reboot| power_off| power_on| shutdown| destroy
        Note : default name is 'node'
    """
    if action not in "reboot,power_off,power_on,shutdown":
        print "Action is unknown : ", action
        return

    ds = droplets(name)

    for d in ds:
        print action+"-ing item :{0}, id={1}".format(d.get("name"), d.get("id"))
        call = API_DO_DROPLET_ACTION.format(d.get("id"), action)
        print "Calling", call
        r = requests.get(call)
        print 'Call status : ', r.status_code, r.text

@task
def spinup(name=DEFAULT_NODE_NAME,n=5,region=DEFAULT_REGION_ID,size=DEFAULT_SIZE_ID):
    """spinup(name,n): spin ups N nodes using snapshot with given name
       Defaults : default name is 'node', number of instances 5, region  - Amsterdam 2, size - 500Mb instance
    """
    d = get(API_DO_IMAGES)
    for image in d.get("images"):
        if (name== image.get("name")):
            print "Found image {0},id={1}".format(image.get("name"), image.get("id"))
            image_id=image.get("id")
            for i in xrange(int(n)):
                call = API_DO_DROPLET_NEW.format(name + "{0}".format(i), size, image_id, region)
                print "Calling", call
                r = requests.get(call)
                print 'Call status : ', r.status_code, r.text

@task
def destroy(name=DEFAULT_NODE_NAME,n=0,region=DEFAULT_REGION_ID,size=DEFAULT_SIZE_ID):
    """destroy(name,n): destroys n nodes matching name
       Defaults : default name is 'node', region  - Amsterdam 2, size - 500Mb instance
    """
    ds = droplets(name)
    ds = ds[0:int(n)]
    for d in ds:
        print "destroying item :name={0},id={1}".format(d.get("name"), d.get("id"))
        call = API_DO_DROPLET_DESTROY.format(d.get("id"))
        print "Calling", call
        r = requests.get(call)
        print 'Call status : ', r.status_code, r.text

def get(url):
    """ Execute GET on given url """

    r = requests.get(url)
    print 'Call status : ', r.status_code
    # print r.text
    d = json.loads(r.text)
    return d
