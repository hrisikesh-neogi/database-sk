from sending_Class import mongo_operation

client_ = {
        "client_url": "mongodb+srv://shohurekotha:shohurekotha20@cluster0.vxe4d.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
        "database": "SHOHUREKOTHA" }
pr = ['Sayani Maity', 'Shreya Lahiri', 'Susmita Chatterjee', 'Tanusri Majumder', 'Shrestha Barui']

db = mongo_operation(client_['client_url'],client_['database'])

def member_data_insertion(collection_name, data):
    
    """
    fuction for assigning the pr and singup data upload to mongo db.
    takes: 
        collection_name: collection name of the database
        data : dictionary of member registration data
    returns:
        None
        prints the message of success or failure
    pr = pr list
    db = mongo db connection
    """

    available_data =  db.find(collection_name, {})
    pr_data = db.find('sk_pr', {})
    available_pr = [name for name in pr_data['Name']]
    if len(available_data) > 0:
        id_num = len(available_data)+1
        pr_name = available_data['Pr'][len(available_data)-1]
        if pr_name in available_pr:
            if available_pr.index(pr_name) != (len(pr)-1):
                pr_assign = available_pr[available_pr.index(pr_name)+1]
            else:
                pr_assign = pr[0]
    else:
        pr_assign = pr[0]
        id_num = 1
    data['_id'] = id_num
    data['Pr'] = pr_assign
        
    db.insert_oneData(collection_name, data)
    print(f'data inserted into {collection_name}. \n data: \n {data}')
    
    
def member_department_assign(joining_as):

    """
    for assigning members to the department.
    takes:
        collection_name: collection name of the database
        joining_as: member joining as
    returns: department
    """
    if joining_as == 'writer':
        department = 'writing'
    if joining_as == "calligrapher":
        department = 'art'
    if joining_as == 'singer':
         department = 'music'
    if joining_as == 'artist':
        department = 'art'
    if joining_as == 'editor(text/video)':
        department = 'art'
    if joining_as == 'vocal artist':
        department = 'vocal'
    if joining_as == "photographer":
        department = 'photography'
    
    if joining_as == 'dancer':
        department = 'dance'
    if joining_as == "pr":
        department = 'pr'

    if joining_as == 'no':
        department = ''
    
    return department
    
