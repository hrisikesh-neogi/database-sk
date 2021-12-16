from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import timedelta
from flask_cors import CORS, cross_origin
from sending_Class import mongo_operation
from data_pre import df_preprocessing, writer_dst
from member_detail import member_data_insertion, member_department_assign
import pandas as pd

# from flask_mail import Mail, Message
import data_prep2
from utils import get_config
from plotly_Dashboard.index import plotly_Dashboard
from department import department
from department import department_graph

client_ = get_config('config.ini')
# print(client_)

# client_ = {
#         "client_url": "mongodb+srv://shohurekotha:shohurekotha20@cluster0.vxe4d.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
#         "collection_name": "member_test",
#         "database": "SHOHUREKOTHA",
#         "path": "H:\\sohure kotha\\database@sk\\dataset\skmembers.csv",
    
#         }

app = Flask(__name__)
app.secret_key = "shohorekotha20"
# login_manager.init_app(app)
app.permanent_session_lifetime = timedelta(days=30)


import logging as lg


lg.basicConfig(filename='sending_Class.log', level=lg.INFO, format='%(asctime)s %(message)s')



department_graph (app)


@app.route('/')
@cross_origin()
def home():
    return render_template('home.html')

@app.route('/home/about')
@cross_origin()
def about():

    return render_template('about.html')

@app.route('/home/departments')
@cross_origin()
def departments():
    
        return render_template('departments.html')




@app.route('/home/team')
@cross_origin()

def team():
        
    return render_template('team.html')


@app.route('/policy')
@cross_origin()
def policy():
    return render_template('privacy_policy.html')


"""normal user signup

for users who are not members of shohure kotha"""

@app.route('/signup')
@cross_origin()
def signup():

    msg = request.args.get('msg')
    if msg is None:
        msg = "Hi! Please fill the form below to sign up."
    return render_template('signup.html', msg=msg)


# @app.route('/signup_test', methods=['POST'])
# @cross_origin()
# def signup_test():
#     if request.method == 'POST':
#         name = request.form['username']
#         email = request.form['email']
#         phone = request.form['phone']
#         password = request.form['password']
#         confirm_password = request.form['comfirm_password']
#         print(name, email, password, phone, confirm_password, phone)
#         return render_template('home.html')



#storing name and passwords 
@app.route('/signup/store', methods=['POST'])
@cross_origin()
def signup_store():
    try:

    
        if request.method == 'POST':
            name = request.form['username']
            email = request.form['email']
            phone = request.form['phone']
            department = request.form['department']
            password = request.form['password']
            confirm_password = request.form['comfirm_password']
            print(name, email, phone, password,  confirm_password, department)
            
        if confirm_password == password:
            
            data =  ({'username': name, 'email': email, 'password': password, 'department': department, 'phone': phone})
            db = mongo_operation(client_['client_url'], client_['database'])
            db.insert_oneData('Sk_normal_User', data)
           

            msg = "Successfully registered. Please login to continue."
            return redirect(url_for('signup', msg=msg))
        else:
            msg = "Password and confirm password does not match"
            return render_template('signup.html', msg = msg)

    except Exception as e:
        print(e)
        msg =  "Something went wront. Please check your credentials and try again."
        return render_template('signup.html', msg = msg)

        

"""new shohure kotha member registration"""

@app.route('/new_shohure_kotha_member_registration', methods = ['GET', 'POST'])
@cross_origin()
def new_member_registration():
    if request.method == 'POST':
        data = request.form.items()
        data = dict(data)
        data.pop('register')
        
        print(data)
        if data['password'] == data['confirm_password']:
            db = mongo_operation(client_['client_url'], client_['database'])
            email = db.find(collection_name = client_['collection_name'], query = {'email': data['email']})
            if len(email) > 0:
                print(email)
                msg = "Email already exists. Please try another email."
                return render_template('member_signup.html', msg = msg)
            else:
                data.pop('confirm_password')
                member_data_insertion(collection_name = "original_member_data", data = data)
                department = member_department_assign(data['department'])
                department_2 = member_department_assign(data['department_2'])
                data.update({'department': department})
                data.update({'department_2': department_2})
                print(data)
                member_data_insertion(data = data, collection_name = client_['collection_name'])
                return redirect(url_for('login', msg = "Successfully registered. Please login to continue."))
        else:
            return render_template('member_signup.html', msg = "Password and Confirm Password does not match.")
    else:
        return render_template('member_signup.html')




@app.route('/login', methods = ['GET', 'POST'])
@cross_origin()
def login():
    if "user" in session:
        return redirect(url_for('user_login'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['pass']
            print(username, password)
            db = mongo_operation(client_['client_url'], client_['database'])
            data = db.find(collection_name = client_['collection_name'], query = {'name': username, 'password': password})
            if data.empty:
                normal_user = db.find(collection_name = "Sk_normal_User", query = {'username': username, 'password': password})
                if normal_user.empty:
                    msg = "Invalid username or password"
                    return render_template('login.html', msg=msg)
                else:
                    department = normal_user['department'][0]
                    email =  normal_user['email'][0]
                    phone = normal_user['phone'][0]
                    user = {'username': username,'password': password, 'department': department, 'email': email, 'phone': phone, 'type': 'normal_user'}
                    session.permanent = True
                    session['user'] = user
                    return redirect(url_for('shohor_out_home'))
            else:
                department = data['department'][0]
                pr = data['Pr'][0]
                email =  data['email'][0]
                phone = data['phone'][0]
                department_2 = data['department_2'][0]
                user = {'username': username,'password': password, 
                        'department': department, 'email': email, 'phone': phone,
                        'pr': pr, 'type': 'member', 'department_2':department_2}
                session.permanent = True
                session['user'] = user

                if len(data) != 0:
                    print(data)
                    print('got data')
                    print('successfully logged in')
                    print(user)
                    return redirect(url_for('user_login'))
                else:
                    msg = "Invalid credentials. Please try again."
                    return render_template('login.html', msg = msg)
        else:
            msg = request.args.get('msg')
            if msg is None:
                msg = "Hi!"
            return render_template('login.html', msg = msg)

@app.route('/logout')
@cross_origin()
def logout():
    if 'user' in session:
        session.pop('user', None)
        return redirect(url_for('home'))
    if 'admin_user' in session:
        session.pop('admin_user', None)
        return redirect(url_for('home'))
    if 'department_user' in session:
        session.pop('department_user', None)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/member/otherDepartments', methods = ['GET', 'POST'])
@cross_origin()
def member_other_departments():
    if 'user' in session:
        if session['user']['type'] == 'member':
    
            department_2 = session['user']['department_2']
            print(department_2)
            if department_2 == None or department_2 == 'no':
                return redirect(url_for('user_login'))
            else:
                
                if department_2 == 'writing':
                    return redirect(url_for('writing'))
                if department_2 == 'art' or department_2 == 'photography':
                    return redirect(url_for('art_photography'))

                if department_2 == 'music' or department_2 == 'vocal':
                    return redirect(url_for('vocal'))
                else:
                    return redirect(url_for('other_profiles'))

        if session['user']['type'] == 'normal_user':
            return redirect(url_for('shohor_out_home'))
    else:
        return redirect(url_for('login', msg = "Please login to continue."))

        
        





#checking the credentials
@app.route('/login/user_login/')
@cross_origin()
def user_login():
    username = session['user']['username']
    department = session['user']['department']
    email = session['user']['email']
    password = session['user']['password']
    
    if "user" in session:
        if session['user']['type'] == 'member':
            if department == 'writing':
                return redirect(url_for('writing'))
            if department == 'art' or department == 'photography':
                return redirect(url_for('art_photography'))

            if department == 'music' or department == 'vocal':
                return redirect(url_for('vocal'))
            else:
                return redirect(url_for('other_profiles'))
        if session['user']['type'] == 'normal_user':
            return redirect(url_for('shohor_out_home'))
    else:
        return redirect(url_for('login', msg = "Please login to continue"))







""" DEPARTMENT ROUTES """

"""VOCAL DEPARTMENT"""

@app.route('/login/user_login/vocal/home')
@cross_origin()
def vocal():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
                
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/vocal_profiles/vocal_index.html', 
        username =  username, department = department, email = email, pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))

@app.route('/login/user_login/vocal/vocal_department')
@cross_origin()
def vocal_department():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/vocal_profiles/vocal_department.html',
         username =  username, department = department, email = email, pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))

@app.route('/login/user_login/vocal/vocal_hod')
@cross_origin()
def vocal_hod():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/vocal_profiles/vocal_hod.html',
         username =  username, department = department, email = email, pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))
@app.route('/login/user_login/vocal/admins_details')
@cross_origin()
def admins_page_vocals():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/vocal_profiles/admin_detail_user.html',
         username =  username, department = department, email = email, pr = pr)
    else:
            return redirect(url_for('login', msg = "Please login to continue"))

"""Writing DEPARTMENT"""

@app.route('/login/user_login/writing/home')  ## home for writers
@cross_origin()
def writing():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/writers_profiles/writer_index.html', 
        username =  username, department = department, email = email ,
        pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))
@app.route('/login/user_login/writing/writing_department')
@cross_origin()
def writing_department():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/writers_profiles/writer_department.html', 
        username =  username, department = department, email = email,
        pr = pr)
        
    else:
        return redirect(url_for('login', msg = "Please login to continue"))
@app.route('/login/user_login/writing/writing_hod')
@cross_origin()
def writing_hod():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email'] 
        pr = session['user']['pr']
        return render_template('/writers_profiles/writer_hod.html', 
        username =  username, department = department, email = email,
        pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))
@app.route('/login/user_login/writing/admins_details')
@cross_origin()
def admins_page_writers():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/writers_profiles/admin_detail_user.html',
         username =  username, department = department, email = email,
         pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))




""" Art and Photography DEPARTMENT """

@app.route('/login/user_login/art_photography/home')
@cross_origin()
def art_photography():

    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/art&photo_profiles/art&photo_index.html', 
        username =  username, department = department, email = email,
        pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))
@app.route('/login/user_login/art_photography/art&photo_department')
@cross_origin()
def art_photo_department():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/art&photo_profiles/art&photo_department.html', 
        username =  username, department = department, email = email,
        pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))
@app.route('/login/user_login/art_photography/art&photo_hod')
@cross_origin()
def art_photo_hod():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/art&photo_profiles/art&photo_hod.html', 
        username =  username, department = department, email = email,
        pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))
@app.route('/login/user_login/art_photography/admins_details')
@cross_origin()
def art_photo_admins_page():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/art&photo_profiles/admin_detail_user.html', 
        username =  username, department = department, email = email,
        pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))






#FOR other members

@app.route('/login/user_login/other_members/home')
@cross_origin()
def other_profiles():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/other_profiles/other_index.html', 
        username =  username, department = department, email = email, pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))

@app.route('/login/user_login/other_members/department')
def other_department():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/other_profiles/other_department.html', 
        username =  username, department = department, email = email, pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))


@app.route('/login/user_login/other_members/hod')
def other_hod():
    if "user" in session:

        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/other_profiles/other_hod.html', username =  username,
         department = department, email = email, pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))


@app.route('/login/user_login/other_members/admins_details')
def other_admins_page():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        department_2 = session['user']['department_2']
        if department != department_2:
            if department_2 != None and department_2 != 'no':
                department = department+', '+department_2
            else:
                department = department
        email = session['user']['email']
        pr = session['user']['pr']
        return render_template('/other_profiles/admin_detail_user.html', username =  username, 
        department = department, email = email, pr = pr)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))



@app.route('/user/profile')
@cross_origin()
def profile():
    username = session['user']['username']
    email = session['user']['email']
    pr = session['user']['pr']
    db = mongo_operation(client_['client_url'], client_['database'])
    user_Details = db.find(collection_name = 'original_member_data', query = {'email': email})
    if user_Details.empty:
        
        return render_template('404.html')

    else:
        print(user_Details)
        department= member_department_assign(user_Details['department'][0]).capitalize()
        joined_as = str(user_Details['department'][0]).capitalize()
        joined_as2 = str(user_Details['department_2'][0]).capitalize()
        if joined_as2 != 'No':
            joined_as = joined_as + ' & ' + joined_as2
            department2 = ', '+member_department_assign(user_Details['department_2'][0]).capitalize()
        else:
            department2 = ''
        user_phone = user_Details['phone'][0]
        address = user_Details['address'][0]
        joiningDate = user_Details['joiningDate'][0]
        pr_Details = db.find('sk_pr', {'Name':pr})
        pr_phone_no = pr_Details['Phone Number'][0]
        dob = user_Details['DOB'][0]

        return render_template('profile.html',
        username =  username, department = department, email = email, 
        pr = pr, pr_phone_no = pr_phone_no,
        address = address, joiningDate = joiningDate,
        joined_as = joined_as, department2 = department2, phone = user_phone, dob = dob)
    



""" normal user pages ( for users who are not members of shohure kotha )"""


@app.route('/user/profile/shohor_out/home')
@cross_origin()
def shohor_out_home():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        email = session['user']['email']
        return render_template('/normal_users/other_index.html', 
        username =  username, department = department, email = email)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))


@app.route('/user/profile/shohor_out/departments')
@cross_origin()
def shohor_out_department():
    if "user" in session:
        username = session['user']['username']
        department = session['user']['department']
        email = session['user']['email']
        return render_template('/normal_users/other_department.html', 
        username =  username, department = department, email = email)
    else:
        return redirect(url_for('login', msg = "Please login to continue"))


# admin pages


@app.route('/dashboard/admin/login',  methods = ['GET', 'POST'])
@cross_origin()
def admin_login():
    if request.method == 'POST':
        data = request.form.items()
        data =  dict(data)
        if data['email'] == 'shohurekotha20@gmail.com' and data["password"] == "admin@sk":
            session['admin_user'] = data
            
            return redirect(url_for('admin_home'))
        else:
            return render_template('/admin_dash/login.html', msg = "hey admin!")

    return render_template('/admin_dash/login.html', msg = "hey admin!")



@app.route('/dashboard/admin/home', methods = ['GET', 'POST'])
@cross_origin()
def admin_home():
    if "admin_user" in session:
        
        db = mongo_operation(client_['client_url'], client_['database'])
        data = db.find(collection_name = 'original_member_data', query = {})
        data.to_csv('dataset\data.csv')
        columns = data.columns
        values = [[data.loc[i, col] for col in data.columns ] for i in range(len(data)) ]
        
        return render_template('/admin_dash/admin_index.html', 
        titles = columns, rows =  values )
    else:
        return render_template('/admin_dash/login.html', msg = "hey admin! Please Login.")

@app.route('/dashboard/admin/tables')
@cross_origin()
def admin_tables():
    db = mongo_operation(client_['client_url'], client_['database'])
    data = db.find(collection_name = 'original_member_data', query = {})
    
    columns = data.columns
    values = [[data.loc[i, col] for col in data.columns ] for i in range(len(data)) ]
    
    return render_template('/admin_dash/tables.html', 
    titles = columns, rows =  values )


#showing the graph from plotlyd dash




"""department dashboards"""
@app.route('/department/register', methods=['POST', 'GET'])
@cross_origin()
def dept_register():
    if request.method == 'POST':
        data = request.form.items()
        data = dict(data)
        if data['password'] == data['confirm password']:
            db  = mongo_operation (client_['client_url'], client_['database'])
            db.insert_oneData(collection_name = "department_login", record = data)
            print(data)
            return redirect(url_for('department_login', msg = "successfully registered. Please login."))
        return render_template('/department_dash/register.html', msg  = "password not matched")
    else:
        return render_template('/department_dash/register.html', msg = "register")

@app.route('/department/dashboard/login',  methods = ['GET', 'POST'])
def department_login():
    if request.method == 'POST':
        data = request.form.items()
        data =  dict(data)
        db  = mongo_operation (client_['client_url'], client_['database'])
        
        find_Data = db.find('department_login', query={'department': data['department'], 'password': data['password']})
        if find_Data.empty:
            return redirect(url_for('department_login', msg = "Invalid Username or Password"))
        else:
            # department = find_Data['department'][0]
            # data['department'] = department
            session.permanent = True
            session['department_user'] = data
           
            return redirect(url_for('department_home'))
    else:
        msg = request.args.get('msg')
        if msg is None:
            msg = "Please Login to continue!"  
        
        return render_template('/department_dash/login.html', msg = msg )

@app.route('/department/dashboard/home', methods = ['GET', 'POST'])
@cross_origin()
def department_home():
    if "department_user" in session:
        dept = session['department_user']['department']
        dpt = department(dept)
        if dept == 'pr':
            columns, values = dpt.pr_data()
       
        else:

            columns, values = dpt.get_values_col()
        

    
        return render_template('/department_dash/dpt_index.html',
        titles = columns, rows =  values, department = dept )
    else:
        return redirect(url_for('department_login', msg = "please login to continue."))

@app.route('/department/dashboard/tables') 
@cross_origin()
def department_tables():
    if "department_user" in session:
        dept = session['department_user']['department']
        dpt = department(dept)
        if dept == 'pr':
            columns, values = dpt.pr_data()
       
        else:

            columns, values = dpt.get_values_col()

    
        return render_template('/department_dash/tables.html',
        titles = columns, rows =  values, department = dept )
    else:
        return redirect(url_for('department_login', msg = "please login to continue."))

@app.route('/admin')
@cross_origin()
def index():
    return render_template('admin_index.html')




@app.route('/mongo')
@cross_origin()
def mongo():
    return render_template('mongo_createCOL.html') 


@app.route('/mongo/bulk_up', methods = ['GET', 'POST'])
@cross_origin()
def bulk_up():
    try:
        if request.method == 'POST' :
            client_url = client_["client_url"]
            collection_name = str(request.form['collection_name'])
            database = client_["database"]
            path = str(request.form['path'])
            db = mongo_operation(client_url, database)
            db.bulk_insert("./static/data.csv", collection_name)
            print('data inserted ')
            lg.info('data inserted successfully')
            return render_template('results.html')

    except Exception as e:
        print('error occured:', str(e))
        # lg.info('error occured:'+' '+str(e))
        return jsonify('error occured:'+' '+str(e))


@app.route('/find', methods=['GET', 'POST'])
@cross_origin()
def find():
    return render_template('find.html')


@app.route('/find/columns', methods=['POST', 'GET'])
@cross_origin()
def columns_():
    columns = ['Email Address', 'Name', 'phoneNo_wp', 'callingNo', 'Date of joining Shohure Kotha', 'Date of Birth', 'Occupation', 
    'Hobbies / Interests', 'You are joining as a','agree with rules']
    return render_template('column.html', titles = columns)


@app.route('/find/sk_dataset', methods=['POST', 'GET'])
@cross_origin()
def sk_dataset():
    try:
        if request.method == 'POST' :
            client_url = client_["client_url"]
            collection_name = request.form['collection_name']
            dataset = request.form['dataset_names']
            database = client_["database"]
            query = {}
            print(collection_name,query)

            db = mongo_operation(client_url, database)
            if dataset == 'member':
                data = db.find(collection_name, query)
                final_data, values = data_prep2.members_data_pre(data)
                columns = final_data.columns
            else:
                final_data = db.find(collection_name, query)
                values, columns = data_prep2.writers_final(final_data)

                

            print('data = ', values)

            lg.info('data inserted successfully')
            return render_template('results.html', titles= columns, rows = values) 

    except Exception as e:
        print('error occured:', str(e))
        # lg.info('error occured:'+' '+str(e))
        return jsonify('error occured:'+' '+str(e))


@app.route('/find/find_Data', methods=['POST', 'GET'])
@cross_origin()
def find_Data():
    try:
        if request.method == 'POST':
            client_url = client_["client_url"]
            collection_name = request.form['collection_name']
            database = client_["database"]
            column = str(request.form['column_name'])
            value = request.form['value']
            file = column+'_'+value

            query = {}
            
            query[column] = value
            print( query,  client_url, database, collection_name, column, value)
            db = mongo_operation(client_url, database)
            data = db.find(collection_name, query)

            # data preprocessing, column renaming, and data to list conversion
            df_pre = df_preprocessing(data)
            final_data = df_pre.dropping_col()
            final_data.to_csv('static/data.csv')
            data_values = df_pre.df_to_list()
            print('data = ', data_values)

            print('got data ')
            lg.info('data GOT successfully')
            return render_template('results.html', titles= final_data.columns.values, rows = data_values, data = file)
        else:
            print ("problem occurs")
    except Exception as e:
        print('error occured:', str(e))
        # lg.info('error occured:'+' '+str(e))
        return jsonify('error occured:'+' '+str(e))


""" writer's data put """


@app.route('/writer', methods=['POST', 'GET'])
@cross_origin()
def writer():
    return render_template('writers_page.html')


@app.route('/writer/mongo/writers', methods=['POST', 'GET'])
@cross_origin()
def writer_mongo():
    try:
        if request.method == 'POST' :
            client_url = client_["client_url"]
            collection_name = str(request.form['collection_name'])
            database = client_["database"]
            path = str(request.form['path'])
            # preprocessing the writer's data
            data = data_prep2.writers_data_pre(path)

            db = mongo_operation(client_url, database)
            db.bulk_insert('./writers_Raw/writers_data.csv', collection_name)
            print('data inserted ')
            lg.info('data inserted successfully')
            return render_template('data_inserted_Succ.html', collection_name = collection_name)

    except Exception as e:
        print('error occured:', str(e))
        # lg.info('error occured:'+' '+str(e))
        return jsonify('error occured:'+' '+str(e))


if __name__ == '__main__':
    app.run(debug=True)
