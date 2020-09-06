# Import modules
import sys
from helper import *
from ruamel import yaml
import json
import xml.etree.ElementTree as ET

import xml.dom.minidom as MD

# Main function
if __name__ == "__main__":
    #########################################
    #              Procedure 1              #
    #########################################
    print ("Patataaaaaaa")


    #########################################
    #              Procedure 2              #
    #########################################
    print('##################')
    print('###### YAML ######')
    print('##################')

    # Open the user.yaml file as read only
    with open ('user.yaml','r') as file:
        # Load the stream using safe_load
        data = yaml.safe_load(file)
    # Print the object type
    print("Type of user_yaml variable:")
    print (type(data))
    print('----------------------')

    # Iterate over the keys of the user_yaml and print them
    print('Keys in user_yaml:')
    for details in data:
        print(details)
    print('----------------------')

    # Create a new instance of class User
    user = User()
    # Assign values from the user_yaml to the object user
    user.id = data['id']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.birth_date = data['birth_date']
    user.address = data['address']
    user.score = data['score']

    # Print the user object
    print('User object:')
    print(user)

    #########################################
    #              Procedure 3              #
    #########################################
    print('##################')
    print('###### JSON ######')
    print('##################')

    # Create JSON structure from the user object
    user_json = json.dumps(user, default = serializeUser, indent=4, sort_keys=True)

    # Print the created JSON structure
    print('Print user_json:')
    print (user_json)
    print('----------------------')

    # Create JSON structure with indents and sorted keys
    print('JSON with indents and sorted keys')
    

    #########################################
    #              Procedure 4              #
    #########################################
    print('######################')
    print('# XML - Element Tree #')
    print('######################')

    # Parse the user.xml file
    with open ('user.xml', 'r') as file:
        myTree = ET.parse(file)

    # Get the root element
    myRoot = myTree.getroot()
    
    # Print the tags
    print('Tags in the XML:')    
    for element in myRoot:
        print (element.tag)

    print('----------------------')

    # Print the value of id tag
    print('id tag value:'+str(myRoot.find('id').text))
    print('----------------------')

    # Find all elements with the tag address in root
    allAddresses = myRoot.findall('address')
        
    # Print the adresses in the xml
    print('Addresses:')
    for address in allAddresses:
        for i in address:
            print(i.tag + ':' + i.text)
    print('----------------------')
    
    # Print the elements in root with their tags and values
    print('Print the structure')    
    for e in myRoot.iter():   
        print(e.tag + ':' + e.text)
    
    # Parsing XML files with MiniDOM 
    print('######################')
    print('### XML - MiniDOM ####')
    print('######################')

    # Parse the user.xml file
    dom = MD.parse('user.xml')
    # Print the tags
    for node in dom.childNodes:
        printTags(node.childNodes)
    print('----------------------')    

    # Accessing element value
    print('Accessing element value')
    idElements = dom.getElementsByTagName('id')
    elementID = idElements.item(0)
    print(elementID.firstChild.data)
    print('----------------------')

    # Print elements from the DOM with tag name 'address'
    print('Addresses:')
    for node in dom.getElementsByTagName('address'):
        printNodes (node.childNodes)
    print('----------------------')

    # Print the entire structure with printNodes
    print('The structure:')
    for node in dom.childNodes:
        printNodes(node.childNodes)

    #########################################
    #              Procedure 5              #
    #########################################
    print('######################')
    print('#   Use Namespaces   #')
    print('######################')

    # Parse the user.xml file
    with open ('item.xml','r') as file:
        myTree = ET.parse(file)
    # Get the root element
    root = myTree.getroot()
    # Define namespaces 
    namespaces = {'a':'https://www.example.com/network', 'b':'https://www.example.com/furniture'}
    # Set table as the root element 
    elementsInNSa = root.findall('a:table', namespaces)
    elementsInNSb = root.findall('b:table', namespaces)
    
    # Elements in NS a
    print('Elements in NS a:')   
    for e in elementsInNSa:
        for i in e.iter():
            print (i.tag+':'+i.text)
    print('----------------------')

    # Elements in NS b
    print('Elements in NS b:')
    for e in elementsInNSb:
        for i in e.iter():
            print (i.tag+':'+i.text)