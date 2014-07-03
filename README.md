# Poseidon

Poseidon is simple command line tool to manage digital ocean droplets.
see https://developers.digitalocean.com for all APIs.

# Prerequisites
- Install fabric
- 
<code> pip install fabric </code>

(see http://docs.fabfile.org/en/1.8)

- replace API_KEY and CLIENT_ID with real values (see https://cloud.digitalocean.com/api_access)

# Usage  
<code> fab --list</code> to list all available commands

<code> fab droplets</code> to list all existing droplets

<code> fab images</code> to list all existing images

<code> fab sizes</code> to list all existing sizes

<code> fab regions</code> to list all existing regions

<code> fab spinup:N, name</code> spins up N droplets using snapshot with given name
Default name is node. 
for example <code> fab spinup:	bitcoinminer,10</code> spinups 10 bitcoin servers using snapshot "bitcoinminer".
Defaults : default name is 'node', number of instances 5, region  - Amsterdam 2, size - 500Mb instance

<code> fab destroy:N, name </code> destroys N droplets using name prefix
Default name is node. 
for example <code> fab spinup:	bitcoinminer,10</code> spinups 10 bitcoin servers using snapshot "bitcoinminer".
Defaults : default name is 'node', number of instances 5, region  - Amsterdam 2, size - 500Mb instance

<code> fab action:action_name,droplet_name</code> executes action_name on droplets matching droplet_name
Default name is node. 
for example <code> fab action:destroy,bitcoinminer</code> destroys all droplets with names matching bitcoinminer.

# Notes 
 - Some commands have default parameters for ex. when we spinup up the droplets we use the smallest droplet configuration by default.


