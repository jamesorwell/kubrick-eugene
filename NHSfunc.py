import json
import requests
import xmlschema
from pprint import pprint
my_username = "roryholmes"
my_password = "Buster769"


#creates the root community
def create_community(community_name, community_description, username, password):
    url = r'https://kubrick-group-training.collibra.com/rest/2.0/communities'
    my_data = {
      "name": community_name,
      "description": community_description}
    r = requests.post(url, json=my_data, auth=(username,password))
    print('status code is ', r.status_code)


def getId(organisation, search_term=None, *, username, password):
    url = r'https://kubrick-group-training.collibra.com/rest/2.0/' + organisation
    my_params = {'limit' : 10, 'name': search_term}
    http_response = requests.get(url, params=my_params, auth=(username, password))
    unpacked_objects = json.loads(http_response.text)
    output = []
    for community in unpacked_objects['results']:
        new_dict = {'id':community['id'], 'name': community['name']}
        output.append(new_dict)
    return output

def populate_lists():
    communities = []
    names = ['Business Metadata', 'Patient Metadata', 'Clinical Metadata', 'Consultant Metadata']
    parentIds = [getId('communities', 'EugeneNHS', username=my_username, password=my_password)[0]['id']] * len(names)
    descriptions = ['Community for all data regarding the running of the Hospitals', 'Community for all patient related Metadata', 'Community for all clinical Metadata', 'Community for all Metadata for Consultants']
    for x in range(len(names)):
        communities.append({'parentId' : parentIds[x], 'name' : names[x], 'description' : descriptions[x]})
    return communities

def child_communities(communities, username, password):
    url = r'https://kubrick-group-training.collibra.com/rest/2.0/communities/bulk'
    my_data = communities
    r = requests.post(url, json=my_data, auth=(username,password))
    print('status code is ', r.status_code)

def populate_domain_lists():
    domains = []
    names = ['ICD Reference Data', 'Consultant Codes', 'Diseases', 'Data Types', 'Code Sets']
    communityIds = []
    communityIds.append(getId('communities', 'Clinical Metadata', username=my_username, password=my_password)[0]['id'])
    communityIds.append(getId('communities','Consultant Metadata', username=my_username, password=my_password)[0]['id'])
    communityIds.append(getId('communities','Consultant Metadata', username=my_username, password=my_password)[0]['id'])
    communityIds.append(getId('communities','EugeneNHS', username=my_username, password=my_password)[0]['id'])
    communityIds.append(getId('communities', 'EugeneNHS', username=my_username, password=my_password)[0]['id'])
    typeIds = ['00000000-0000-0000-0000-000000020001', '00000000-0000-0000-0000-000000020001', '00000000-0000-0000-0000-000000010001', '00000000-0000-0000-0000-000000030001', '00000000-0000-0000-0000-000000020001']
    descriptions = ['Codelist containing reference codes for the ICD10', 'Codes referring to NHS Consultants', 'Glossary explaining the meanings for disease names', 'Glossary explaining meanings for all quidditch terms', 'Data Dictionary for all Students', 'Domain for all policies', 'Domain containing all code sets and values']
    for x in range(len(names)):
        domains.append({'name' : names[x], 'communityId' : communityIds[x], 'typeId' : typeIds[x], 'description' : descriptions[x]})
    return domains

#bulk imports domains
def create_domains(username, password):
    url = r'https://kubrick-group-training.collibra.com/rest/2.0/domains/bulk'
    my_data = populate_domain_lists()
    r = requests.post(url, json=my_data, auth=(username,password))
    print('status code is ', r.status_code)

def addNHSassets(assetchoice, username, password):

    url = r"https://kubrick-group-training.collibra.com/rest/2.0/assets/bulk"
    my_data = assetchoice
    r = requests.post(url, json=my_data, auth=(username,password))
    print("status code is ", r.status_code)

def addassets(filename, domain_name):
    file = open(filename, 'r')
    fileopend = json.load(file)
    domainId = getId('domains', domain_name, username=my_username, password=my_password)[0]["id"]
    for i in fileopend:
        i.update({"domainId" : domainId})
    addNHSassets(fileopend, username = my_username, password=my_password)

def addattributes(jsondata, username, password):
    url = r"https://kubrick-group-training.collibra.com/rest/2.0/attributes/bulk"
    my_data = jsondata
    r = requests.post(url, json=my_data, auth=(username, password))
    print('status code is ', r.status_code)

def populateattributes(file):
    atr = open(file, 'r')
    jsond = json.load(atr)
    for x in jsond:
        a = getId('assets', x['name'], username = my_username, password=my_password)[0]['id']
        x.update({'assetId' : a})
    for all in jsond:
        all.pop('name')
    addattributes(jsond, username = my_username, password = my_password)
    atr.close()

def initialgetassets():
    schema = xmlschema.XMLSchema('CDS-XML_Standard_Data_Elements-V6-2-2.xsd')
    data_elements = schema.to_dict('CDS-XML_Standard_Data_Elements-V6-2-2.xsd')
    schema = xmlschema.XMLSchema('CDS-XML_Standard_Data_Structures-V6-2-2.xsd')
    data_structures = schema.to_dict('CDS-XML_Standard_Data_Structures-V6-2-2.xsd')
    elements = []
    codeSets = []
    codeSetNames = []
    codeValues = []
    for this_type in data_elements['xs:simpleType']:
        elements.append(this_type['@name'])
        try:
            codeSets.append(this_type['xs:restriction']['xs:enumeration'])
            codeSetNames.append(this_type['@name'].replace('_Type',' Code Set'))
            for value in this_type['xs:restriction']['xs:enumeration']:
                if value['@value'] not in codeValues:
                    codeValues.append(value['@value'])
        except:
            continue
    return elements, codeSets, codeSetNames, codeValues

def create_assets(names,domain_ids,type_ids,*,username,password):

    #check if names is list of names or single name for bulk/non bulk posting
    if isinstance(names, str):
        url = r'https://kubrick-group-training.collibra.com/rest/2.0/assets'

        #construct dict for single upload
        my_data = {"name":names,
                    "domainId":domain_ids,
                    "typeId":type_ids}

    else:
        url = r'https://kubrick-group-training.collibra.com/rest/2.0/assets/bulk'

        #condition checks to take both single and list of domains and types
        if isinstance(domain_ids, str):
            domain_ids = [domain_ids]*len(names)
        if isinstance(type_ids, str):
            type_ids = [type_ids]*len(names)

        #construct list of dicts for bulk upload
        indices = range(len(names))
        my_data = [{"name":names[k],
                    "domainId":domain_ids[k],
                    "typeId":type_ids[k]}
                        for k in indices]

    r = requests.post(url, json=my_data, auth=(username,password))
    print('status code is ', r.status_code)

def get_assets(domainId, search_term=None, *, username, password):

    url = r'https://kubrick-group-training.collibra.com/rest/2.0/assets'

    my_params = {'domainId' : domainId, 'limit' : 5, 'name': search_term}
    http_response = requests.get(url, params=my_params, auth=(username, password))

    unpacked_objects = json.loads(http_response.text)

    names_ids = []
    for result in unpacked_objects['results']:
        desired = ['name','id']
        names_ids.append({x:result[x] for x in desired})

    return names_ids

def get_codeValueAssets(domain_id, *, username, password):

    url = r'https://kubrick-group-training.collibra.com/rest/2.0/assets'

    my_params = {'domainId' : domain_id, 'limit' : None}
    http_response = requests.get(url, params=my_params, auth=(username, password))

    unpacked_objects = json.loads(http_response.text)

    names_ids = []
    for result in unpacked_objects['results']:
        desired = ['name','id']
        names_ids.append({x:result[x] for x in desired})

    return names_ids

def getcodeIds():
    schema = xmlschema.XMLSchema('CDS-XML_Standard_Data_Elements-V6-2-2.xsd')
    data_elements = schema.to_dict('CDS-XML_Standard_Data_Elements-V6-2-2.xsd')
    create_code_relations = True
    if create_code_relations:
        #domainId = '6dd30de6-e911-4a64-afb8-0587ce93ef3c' #Code values domain
        codeValues = get_codeValueAssets(getId('domains', 'Code Sets', username=my_username, password=my_password)[0]['id'],username=my_username,password=my_password)
        #pprint(data_elements)
        codeSetIds = []
        codeValueIds = []
        for data_el in data_elements['xs:simpleType']:
            try:
                data_el['xs:restriction']['xs:enumeration']
                existsList = True
            except:
                existsList = False
            if existsList:
                #pprint(data_el['xs:restriction']['xs:enumeration'])
                for value in data_el['xs:restriction']['xs:enumeration']:
                    if isinstance(value,dict):
                        codeSets = get_assets(getId('domains', 'Code Sets', username=my_username, password=my_password)[0]['id'],data_el['@name'].replace('_Type',' Code Set'),username=my_username,password=my_password)
                        codeSetIds.append(codeSets[0]['id'])
                        codeValueIds.append([k['id'] for k in codeValues if k['name']==value['@value']][0])
    return codeValueIds, codeSetIds

def getname(organisation, domainId, username, password):
    url = r'https://kubrick-group-training.collibra.com/rest/2.0/' + organisation
    my_params = {'name' : '',
                'domainId' : domainId}
    http_response = requests.get(url, params=my_params, auth=(username, password))
    unpacked_objects = json.loads(http_response.text)
    output = []
    for community in unpacked_objects['results']:
        new_dict = community['name']
        output.append(new_dict)
    return output


def create_relations(sourceId, targetId, typeId,*, username, password):

    url = r'https://kubrick-group-training.collibra.com/rest/2.0/relations/bulk'
    indices = range(len(sourceId))
    my_data = [{
      "sourceId": sourceId[k],
      "targetId": targetId[k],
      "typeId": typeId}
      for k in indices]
    r = requests.post(url, json=my_data, auth=(username,password))
    print('status code is ', r.status_code)

def set_up_lists():
    codeset_list = initialgetassets()[2]
    element_list = getname('assets', getId('domains', 'Data Types', username=my_username, password=my_password)[0]['id'], username=my_username, password=my_password)
    codeset_list_sliced = []
    for i in codeset_list:
        codeset_list_sliced.append(i[:-9])
    listattempt = []
    for num in codeset_list_sliced:
        if num in element_list:
            id = getId('assets', num, username=my_username, password=my_password)
            listattempt.append(id)
    newlist = []
    for all in listattempt:
        newlist.append(all[:2])
    for i in newlist:
        for j in i:
            j.pop('name')
    for i in newlist:
            i[0]['sourceId'] = i[0].pop('id')
            i[1]['targetId'] = i[1].pop('id')
    for i in newlist:
        (i[0].update({'typeId' : '00000000-0000-0000-0000-000000007039'}))
    for y in newlist:
        y[0].update(y[1])
    finale = []
    for a in newlist:
        finale.append(a[0])
    return finale

def create_next_relations(listdata, username, password):
    url = r'https://kubrick-group-training.collibra.com/rest/2.0/relations'
    my_data = listdata
    r = requests.post(url, json=my_data, auth=(username,password))
    print('status code is ', r.status_code)

def set_relation():
    data = set_up_lists()
    for i in data:
        create_next_relations(i, username=my_username, password=my_password)


#master function
def master():
    create_community('EugeneNHS', 'Team Eugenes NHS metadata', username=my_username, password=my_password)
    child_communities(populate_lists(), username=my_username, password=my_password)
    create_domains(username=my_username, password=my_password)
    addassets('NHSDataTypes.json', 'Data Types')
    populateattributes('NHSattributes.json')
    create_assets((initialgetassets()[3]),getId('domains', 'Code Sets', username=my_username, password=my_password)[0]['id'],'00000000-0000-0000-0000-000000021001' ,username=my_username,password=my_password)
    create_assets((initialgetassets()[2]),getId('domains', 'Code Sets', username=my_username, password=my_password)[0]['id'],'00000000-0000-0000-0000-000000021002' ,username=my_username,password=my_password)
    create_relations(getcodeIds()[0],getcodeIds()[1],'00000000-0000-0000-0000-000000007041', username=my_username, password=my_password)
    set_relation()


#master()
