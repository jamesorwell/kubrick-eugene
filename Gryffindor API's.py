import json
import requests
my_username = 'roryholmes'
my_password = 'Buster769'

#creates the root community
def create_community(community_name, community_description, username, password):
    url = r'https://kubrick-group-training.collibra.com/rest/2.0/communities'
    my_data = {
      "name": community_name,
      "description": community_description}
    r = requests.post(url, json=my_data, auth=(username,password))
    print('status code is ', r.status_code)

#allows ability to search for ID's
def get_gryffindorId(search_term=None, *, username, password):
    url = r'https://kubrick-group-training.collibra.com/rest/2.0/communities'
    my_params = {'limit' : 10, 'name': search_term}
    http_response = requests.get(url, params=my_params, auth=(username, password))
    unpacked_objects = json.loads(http_response.text)
    output = []
    for community in unpacked_objects['results']:
        new_dict = {'id':community['id'], 'name': community['name']}
        output.append(new_dict)
    return output

#input values here to set up bulk import communities
def populate_lists():
    communities = []
    names = ['Students2', 'Staff2', 'Quidditch2']
    parentIds = [get_gryffindorId( 'Gryffindor2', username=my_username, password=my_password)[0]['id']] * len(names)
    descriptions = ['Student Community', 'Staff Community', 'Go, go Gryffindor']
    for x in range(len(names)):
        communities.append({'parentId' : parentIds[x], 'name' : names[x], 'description' : descriptions[x]})
    return communities

#bulk imports communities
def child_communities(communities, username, password):
    url = r'https://kubrick-group-training.collibra.com/rest/2.0/communities/bulk'
    my_data = communities
    r = requests.post(url, json=my_data, auth=(username,password))
    print('status code is ', r.status_code)

#input values here to set up bulk import domains
def populate_domain_lists():
    domains = []
    names = ['Current Squad3', 'Fixtures3', 'Results3', 'Quidditch Glossary3', 'Student Data Dictionary3', 'Gryffindor Policy']
    communityIds = [[get_gryffindorId('Quidditch2', username=my_username, password=my_password)[0]['id']]*4][0]
    communityIds.append(get_gryffindorId('Students2', username=my_username, password=my_password)[0]['id'])
    communityIds.append(get_gryffindorId('Gryffindor2', username=my_username, password=my_password)[0]['id'])
    typeIds = ['00000000-0000-0000-0000-000000030011', '00000000-0000-0000-0000-000000030011', '00000000-0000-0000-0000-000000030011', '00000000-0000-0000-0000-000000010001', '00000000-0000-0000-0000-000000030011', '00000000-0000-0000-0000-000000030013']
    descriptions = ['Gryffindor Quidditch Playing Squad', 'Gryffindor quidditch team upcoming events', 'Gryffindor quidditch team results', 'Glossary explaining meanings for all quidditch terms', 'Data Dictionary for all Students', 'Domain for all policies']
    for x in range(len(names)):
        domains.append({'name' : names[x], 'communityId' : communityIds[x], 'typeId' : typeIds[x], 'description' : descriptions[x]})
    return domains

#bulk imports domains
def create_domains(username, password):
    url = r'https://kubrick-group-training.collibra.com/rest/2.0/domains/bulk'
    my_data = populate_domain_lists()
    r = requests.post(url, json=my_data, auth=(username,password))
    print('status code is ', r.status_code)
    print(r.reason)

#master function
def master():
    create_community('Gryffindor2', 'A community for the students and staff of Gryffindor House', username=my_username, password=my_password)
    child_communities(populate_lists(), username=my_username, password=my_password)
    create_domains(username=my_username, password=my_password)

master()
