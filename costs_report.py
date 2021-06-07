
import csv
import json
import requests
import glob
import os
import dateutil.parser

# users teams lists
first_user_list = [ 
"user1", 
"user2", 
"user3",
"user4",
"user5"]

second_user_list = [
"user6",
"user7",
"user8",
"user9",
"user10"]

# open JSON file
f = open('/full/path/kubecost_data.json',)
# returns JSON object as 
json_data = json.load(f)

# create classes from vars
class Namespace():
    def __init__(self, owner_name, total_cost, namespace_start_time, namespace_end_time, namespace_delta_time, team):
        self.owner_name = owner_name
        self.total_cost = total_cost
        self.namespace_start_time = namespace_start_time
        self.namespace_end_time = namespace_end_time
        self.namespace_delta_time = namespace_delta_time
        self.team = team

class Person():
    def __init__(self, owner_name, total_cost_amount, namespaces_amount, total_namespace_delta_time):
        self.owner_name = owner_name
        self.total_cost_amount = total_cost_amount
        self.namespaces_amount = namespaces_amount
        self.total_namespace_delta_time = total_namespace_delta_time


first_namespaces_array = []
second_namespaces_array = []
persons_1st = []
persons_2nd = []
    

# get data as vars
if 'data' in json_data:
    for item in json_data['data']:
        for key in item:
            deepest_value = item.get(key)
            owner_name = (deepest_value.get('name')).replace("owner=", "")
            total_cost = deepest_value.get('totalCost')
            # get namespace start date string value and convert it to date
            namespace_start_time = dateutil.parser.parse(deepest_value.get('start'))
            # get namespace end date string value and convert it to date
            namespace_end_time = dateutil.parser.parse(deepest_value.get('end'))
            namespace_delta_time = namespace_end_time - namespace_start_time
            if owner_name in first_user_list:
                team = "1st_team"
                # creare object of class Namespace
                namespace_object = Namespace(owner_name, total_cost, namespace_start_time, namespace_end_time, namespace_delta_time, team)
                # append object to array
                first_namespaces_array.append(namespace_object)
            elif owner_name in second_user_list:
                team = "2nd_team"
                # creare object of class Namespace
                namespace_object = Namespace(owner_name, total_cost, namespace_start_time, namespace_end_time, namespace_delta_time, team)
                # append object to array
                second_namespaces_array.append(namespace_object)
            else:
                pass

print("1st TEAM")
print("Total amount of users are " + str(len(first_user_list)))
print("Total amount of namespaces are " + str(len(first_namespaces_array)))
print("The average amount of running namespaces are " + str(len(first_namespaces_array)/len(first_user_list)))

# count total costs for value wtream
sum = 0 
for namespaces in first_namespaces_array:
    sum = sum + namespaces.total_cost
print("Total costs for team is " + str(sum))

# count by owner costs and namespaces
for namespace in first_namespaces_array:
    already_exists = False
    for person in persons_1st:
        if namespace.owner_name == person.owner_name:
            person.total_cost_amount = person.total_cost_amount + namespace.total_cost
            person.namespaces_amount = person.namespaces_amount + 1
            person.total_namespace_delta_time = person.total_namespace_delta_time + namespace.namespace_delta_time
            already_exists = True
    if already_exists == False: 
        person_object = Person(namespace.owner_name, namespace.total_cost, 1, namespace.namespace_delta_time)
        persons_1st.append(person_object)

print("Amount of users that run namespaces: " + str(len(persons_1st)))
# sort array by total_cost_amount
newlist = sorted(persons_1st, key=lambda x: x.total_cost_amount, reverse=True)

for person in newlist:
    print("User: " + str(person.owner_name) + ", Total cost: " + str(person.total_cost_amount) 
    + ", Total namespaces running time: " + str(person.total_namespace_delta_time) + ", Namespaces amount: " + str(person.namespaces_amount))

print("")
print("2nd TEAM")
print("Total amount of users are " + str(len(second_user_list)))
print("Total amount of namespaces are " + str(len(second_namespaces_array)))
print("The average amount of running namespaces are " + str(len(second_namespaces_array)/len(second_user_list)))

# count total costs for value wtream
sum = 0 
for namespaces in second_namespaces_array:
    sum = sum + namespaces.total_cost
print("Total costs for team is " + str(sum))

# count by owner costs and namespaces
for namespace in second_namespaces_array:
    already_exists = False
    for person in persons_2nd:
        if namespace.owner_name == person.owner_name:
            person.total_cost_amount = person.total_cost_amount + namespace.total_cost
            person.namespaces_amount = person.namespaces_amount + 1
            person.total_namespace_delta_time = person.total_namespace_delta_time + namespace.namespace_delta_time
            already_exists = True
    if already_exists == False: 
        person_object = Person(namespace.owner_name, namespace.total_cost, 1, namespace.namespace_delta_time)
        persons_2nd.append(person_object)

print("Amount of users that run namespaces: " + str(len(persons_2nd)))
# sort array by total_cost_amount
newlist = sorted(persons_2nd, key=lambda x: x.total_cost_amount, reverse=True)

for person in newlist:
    print("User: " + str(person.owner_name) + ", Total cost: " + str(person.total_cost_amount) 
    + ", Total namespaces running time: " + str(person.total_namespace_delta_time) +  ", Namespaces amount: " + str(person.namespaces_amount))


"""
# old way with request to API each time.
result = {}

ploads = {'window':'30d','aggregate':'label:owner','shareIdle':'false'}
response = requests.get('http://IP:PORT/model/allocation',params=ploads)

json_data = response.json() if response and response.status_code == 200 else None

if 'data' in json_data:
    for item in json_data['data']:
        #print(item)
        for key in item:
            deepest_value = item.get(key)
            owner_name = (deepest_value.get('name')).replace("owner=", "")
            total_cost = deepest_value.get('totalCost')
            if owner_name in first_user_list:
                result.update({total_cost:owner_name})
                #print(owner_name)
                #print(total_cost)

print(dict(sorted(result.items(), reverse = True)))
"""
