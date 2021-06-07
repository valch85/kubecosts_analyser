# kubecosts_analyser
analyse Kubecost (https://www.kubecost.com/) API response between two teams

**Provide report by team and users:**
- total amount of users
- total amount of launched namespaces
- the average amount of running namespaces
- total costs for a team
- amount of users that run namespaces
- personified: tootal cost, total namespaces runing time, namespaces amount

**Preparations**

- save data to file for future analises by command: 
`curl http://IP_OF_KUBECOST:PORT/model/allocation \\n  -d window=30d \\n  -d aggregate=label:owner \\n  -d shareIdle=false -G |jq > kubecost_data.json`
- change path in the script (open JSON file section)
- change users teams lists

