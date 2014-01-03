# digitalocean-python-wrapper

super simple digitalocean.com API python wrapper
see https://developers.digitalocean.com for all APIs

# Prerequisites
- Install fabric (see http://docs.fabfile.org/en/1.8).
- COPY AND PASTE your API_KEY and CLIENT_ID (see https://cloud.digitalocean.com/api_access)

# Usage  
<code> fab --list</code> to see help

<code> fab droplets</code> to see existing droplets

<code> fab images</code> to see existing images

<code> fab sizes</code> to see existing sizes

<code> fab regions</code> to see existing regions

<code> fab spinup:N,name</code> spin ups N droplets using snapshot with given name
for example <code> fab spinup:	bitcoinminer,10</code> spinups 10 bitcoin servers using snapshot "bitcoinminer".
Defaults : default name is 'node', number of instances 5, region  - Amsterdam 2, size - 500Mb instance

<code> fab action:action_name,droplet_name</code> executes action_name on droplets matching droplet_name
for example <code> fab action:destroy,	bitcoinminer</code> destroys all droplets with names matching bitcoinminer. Defaults: default name : node

# Notes 
- To use some commands you need to have snapshot
- Some commands have default parameters for ex. when we spinup up the droplets we use the smallest droplet configuration by default.


