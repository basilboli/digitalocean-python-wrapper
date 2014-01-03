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


# 2 - Amsterdam 1, 1 - New York 1, 3 - San Francisco 1, 4 -  New York 2, 5- Amsterdam 2
DEFAULT_REGION_ID = 5
# 62 - 2GB, 63 - 1GB, 66 - 500Mb, 64 - 4GB, ...
DEFAULT_SIZE_ID = 66



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
def show(command=None):
    """ Show information about created droplets"""

    print "Showing droplets ..."
    d = get(API_DO_DROPLETS)
    for droplet in d.get("droplets"):
        print "{0} ----> {1},{2},{3}".format(droplet.get("name"), droplet.get("ip_address"), droplet.get("id"),
                                             droplet.get("status"))
        if (command is not None):
            pass

@task
def action(action,name="node"):
    """ Do action on droplet : ex. reboot| power_off| power_on| shutdown| destroy
        Note : default name is 'node'
    """

    if action not in "reboot,power_off,power_on,shutdown,destroy":
        print "Action is unknown : ", action
        return

    print "Getting droplets ..."
    d = get(API_DO_DROPLETS)

    for droplet in d.get("droplets"):
        if (name in droplet.get("name")):
            print "{0}, id={1}".format(droplet.get("name"), droplet.get("id"))
            call = API_DO_DROPLET_ACTION.format(droplet.get("id"), action)
            print "Calling", call
            r = requests.get(call)
            print 'Call status : ', r.status_code, r.text

@task
def spinup(n=5,image_name="node",region=DEFAULT_REGION_ID,size=DEFAULT_SIZE_ID):
    """spinup(name,n): spin ups N nodes using snapshot with given name
    Defaults : default name is 'node', number of instances 5, region  - Amsterdam 2, size - 500Mb instance
    """
    d = get(API_DO_IMAGES)
    for image in d.get("images"):
        if (image_name== image.get("name")):
            print "Found image {0},id={1}".format(image.get("name"), image.get("id"))
            image_id=image.get("id")
            for i in xrange(int(n)):
                name = image_name + "{0}".format(i)
                call = API_DO_DROPLET_NEW.format(name, size, image_id, region)
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

