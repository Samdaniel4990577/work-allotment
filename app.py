
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from PIL import Image
import os,io
from flask import send_file
from flask import render_template, request, redirect, url_for, session
from MySQLdb import cursors
import os
from werkzeug.utils import secure_filename

import base64
from flask_mail import Message






app = Flask(__name__)
app.secret_key = 'amose'  # Change this to a random secret key
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sam_project'

app.config['SECRET_KEY'] = 'nnnc vrva lknn jlew'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use Gmail's SMTP server
app.config['MAIL_PORT'] = 587  # Port for TLS
app.config['MAIL_USE_TLS'] = True  # Use TLS for security
app.config['MAIL_USE_SSL'] = False  # Disable SSL, use TLS
app.config['MAIL_USERNAME'] = 'sam499057@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'nnnc vrva lknn jlew'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'  # Default sender email
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

mail = Mail(app)


# Initialize MySQL
mysql = MySQL(app)

@app.route('/photo/<int:user_id>')
def photo(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT photo FROM abi WHERE user_id = %s', (user_id,))
    user = cursor.fetchone()

    if user and user['photo']:
        return send_file(
            io.BytesIO(user['photo']),
            mimetype='image/jpeg',
            as_attachment=False,
            download_name='profile.jpg'
        )
    return 'No image found', 404

4




@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        # Getting user input
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # Hash the password using the correct method
        if username and password and email:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            # Insert into database (example)
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO abi (user_name, email, password, role) VALUES (%s, %s, %s, %s)', 
                           (username, email, hashed_password, 0))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('login'))
        else:
            msg = 'Please fill out all fields.'

    return render_template('register.html', msg=msg)


@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(f"Attempting login with email: {email}")  # Debug statement

        if email and password:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM abi WHERE email = %s', (email,))
            account = cursor.fetchone()

            print(f"Fetched account: {account}")  # Debug statement

            if account and check_password_hash(account['password'], password):
                # Setting session variables
                session['loggedin'] = True
                session['id'] = account['user_id']  # Make sure 'id' is set correctly
                session['email'] = account['email']
                session['user_name'] = account['user_name']
                session['role'] = account['role']

                print(f"Session data set: {session}")  # Debug statement

                # Redirect based on role
                if session['role'] == 1:
                    return redirect(url_for('admin_dashboard'))  # Admin
                elif session['role'] == 0:
                    return redirect(url_for('user_dashboard'))  # User
            else:
                msg = 'Incorrect email or password!'
        else:
            msg = 'Please fill out both fields.'

    return render_template('login.html', msg=msg)






@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    return redirect(url_for('login'))



@app.route('/logout')
def user_logout():
    session.clear()  # Clear session data
    return redirect(url_for('login'))


@app.route('/user', methods=['POST', 'GET'])
def user():
    if 'loggedin' in session:
        user_role = session.get('role')
        
        # Ensure only admins can access this page
        if user_role != 1:  # Assuming role 1 is admin
            flash('Access denied. Admins only.')
            return redirect(url_for('index'))  # Redirect to 'index' instead of 'home'

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        query = '''
        SELECT abi.user_id, abi.user_name, abi.email, abi.role, abi.status, 
               tasks.task_id, tasks.task_name, tasks.due_date, tasks.status AS task_status
        FROM abi
        LEFT JOIN tasks ON abi.user_id = tasks.user_id
        '''
        cursor.execute(query)
        tasks = cursor.fetchall()
        cursor.close()
        
        task = {}
        for entry in tasks:
            user_id = entry['user_id']
            if user_id not in task:
                task[user_id] = {
                    'user_name': entry['user_name'],
                    'email': entry['email'],
                    'role': entry['role'],
                    'status': entry['status'],
                    'tasks': []
                }
            if entry['task_id']:
                task[user_id]['tasks'].append({
                    'task_id': entry['task_id'],
                    'task_name': entry['task_name'],
                    'due_date': entry['due_date'],
                    'task_status': entry['task_status']
                })
        
        return render_template('user.html', task=task)
    else:
        return redirect(url_for('login'))
    
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'loggedin' in session and session.get('role') == 1:
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT user_id, user_name, email, time, photo, contact, city FROM abi')
            users = cursor.fetchall()
            cursor.close()

            print(f"Fetched Users: {users}")  # Debug: Check fetched users
        except Exception as e:
            print(f"Database error: {e}")
            users = []

        # Construct full URL for photo
        for user in users:
            if user['photo']:
                user['photo'] = url_for('static', filename=f'uploads/{user["photo"]}')  # Create URL for photo
                print(f"User ID: {user['user_id']}, Photo URL: {user['photo']}")  # Debug: Print photo URL
            else:
                user['photo'] = None

        return render_template('admin_dashboard.html', users=users)
    else:
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))





@app.route('/user_dashboard')
def user_dashboard():
    if 'loggedin' in session and session.get('role') == 0:
        user_id = session.get('id')  # Ensure you use the correct key

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''
                SELECT task_id, task_name, due_date, status, image
                FROM tasks
                WHERE user_id = %s
            ''', (user_id,))
            tasks = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"Database error: {e}")
            tasks = []

        return render_template('user_dashboard.html', tasks=tasks)
    else:
        flash('Access denied. User privileges required.')
        return redirect(url_for('login'))


# General dashboard route to redirect based on role
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        user_role = session.get('role')

        if user_role == 1:  # Admin access
            return redirect(url_for('admin_dashboard'))
        elif user_role == 0:  # Regular user access
            return redirect(url_for('user_dashboard'))
        else:
            flash('Access denied!')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'loggedin' in session and session.get('role') == 1:  # Only admins can access
        if request.method == 'POST':
            user_name = request.form['user_name']
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']  # 1 for admin, 0 for user
            city = request.form['city']
            contact = request.form['contact']

            # Handle photo upload if provided
            photo = request.files['photo']  # Get the file from the request
            photo_filename = None
            if photo:
                photo_filename = photo.filename
                photo.save(os.path.join('static/uploads', photo_filename))  # Save the photo

            # Hash the password for security
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            cursor = mysql.connection.cursor()

            # Check if email already exists
            cursor.execute('SELECT * FROM abi WHERE email = %s', (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Email already exists. Please choose another email.', 'danger')
                cursor.close()
                return redirect(url_for('add_user'))

            cursor.execute(
                'INSERT INTO abi (user_name, email, password, role, city, contact, photo) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (user_name, email, hashed_password, role, city, contact, photo_filename)
            )
            mysql.connection.commit()
            cursor.close()

            # Send email notification to admin
            admin_email = 'sam499057@gmail.com'  # Change to your admin email
            admin_subject = 'New User Added'
            admin_body = f'A new user has been added:\n\nUser Name: {user_name}\nEmail: {email}'
            admin_msg = Message(admin_subject, recipients=[admin_email])
            admin_msg.body = admin_body
            mail.send(admin_msg)

            # Send welcome email to new user
            welcome_subject = 'Welcome to Our Platform!'
            welcome_body = f'Hi {user_name},\n\nWelcome to our platform! We are glad to have you here.\n\nBest regards,\nThe Team'
            welcome_msg = Message(welcome_subject, recipients=[email])
            welcome_msg.body = welcome_body
            mail.send(welcome_msg)

            flash('User added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

        return render_template('add_user.html')  # Display form
    else:
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))

# Display all tasks
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if 'loggedin' in session:  # Check if user is logged in
        user_id = session.get('user_id')

        # Fetch user details
        cursor = mysql.connection.cursor(cursors.DictCursor)
        cursor.execute('SELECT * FROM abi WHERE user_id = %s', (user_id,))
        user = cursor.fetchone()

        # Fetch tasks related to the user
        query = '''
        SELECT tasks.task_id, tasks.task_name, tasks.due_date, tasks.status, 
               abi.user_name
        FROM tasks
        LEFT JOIN abi ON tasks.user_id = abi.user_id
        WHERE tasks.user_id = %s OR tasks.user_id IS NULL
        '''
        cursor.execute(query, (user_id,))
        tasks = cursor.fetchall()
        cursor.close()

        return render_template('task/tasks.html', tasks=tasks, user=user)
    else:
        return redirect(url_for('login'))
 



@app.route('/assign_task', methods=['GET', 'POST'])
def assign_task():
    if 'loggedin' in session and session.get('role') == 1:  # Ensure only admins can access this
        if request.method == 'POST':
            task_name = request.form['task_name']
            due_date = request.form['due_date']
            user_id = request.form['user_id']
            
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO tasks (task_name, due_date, status, user_id) VALUES (%s, %s, %s, %s)', 
                           (task_name, due_date, 0, user_id))  # Default status 0 (incomplete)
            mysql.connection.commit()
            cursor.close()
            
            flash('Task assigned successfully!', 'success')
            return redirect(url_for('manage_tasks'))

        # Fetch all users for the assignment form
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT user_id, user_name FROM abi WHERE role = 0')  # Fetch users
        users = cursor.fetchall()
        cursor.close()

        return render_template('add_task.html', users=users)
    else:
        return redirect(url_for('login'))


# @app.route('/manage_tasks', methods=['GET', 'POST'])
# def manage_tasks():
#     if 'loggedin' in session and session.get('role') == 1:  # Admins only
#         if request.method == 'POST':
#             task_id = request.form['task_id']
#             user_id = request.form['user_id']
            
#             # Assign task to the user
#             cursor = mysql.connection.cursor()
#             cursor.execute('UPDATE tasks SET user_id = %s WHERE task_id = %s', (user_id, task_id))
#             mysql.connection.commit()
#             cursor.close()
            
#             flash('Task assigned successfully!', 'success')
#             return redirect(url_for('manage_tasks'))
        
#         cursor = mysql.connection.cursor()
        
#         # Fetch tasks
#         cursor.execute('''
#             SELECT t.task_id, t.task_name, t.due_date, t.status, a.user_name
#             FROM tasks t
#             LEFT JOIN abi a ON t.user_id = a.user_id
#         ''')
#         tasks = cursor.fetchall()

#         # Fetch users
#         cursor.execute('SELECT user_id, user_name FROM abi WHERE role = 0')  # role = 0 is for users
#         users = cursor.fetchall()
        
#         cursor.close()
        
#         # Debug: Print fetched data
#         print("Fetched tasks:", tasks)
#         print("Fetched users:", users)
        
#         return render_template('manage_tasks.html', tasks=tasks, users=users)
#     else:
#         return redirect(url_for('login'))

@app.route('/manage_tasks', methods=['GET', 'POST'])
def manage_tasks():
    if 'loggedin' in session and session.get('role') == 1:  # Admins only
        if request.method == 'POST':
            task_id = request.form['task_id']
            user_id = request.form['user_id']

            # Assign task to the user
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE tasks SET user_id = %s WHERE task_id = %s', (user_id, task_id))
            mysql.connection.commit()
            cursor.close()

            # Fetch the email of the assigned user
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT email FROM abi WHERE user_id = %s', (user_id,))
            user_email = cursor.fetchone()

            if user_email:
                # Fetch task details and image
                cursor.execute('SELECT task_name, due_date, image FROM tasks WHERE task_id = %s', (task_id,))
                task = cursor.fetchone()
                
                if task:
                    task_name, due_date, image_filename = task
                    user_subject = 'New Task Assigned'
                    user_body = f'Hi,\n\nA new task has been assigned to you:\n\nTask Name: {task_name}\nDue Date: {due_date}\n\nBest regards,\nThe Team'
                    user_msg = Message(user_subject, recipients=[user_email[0]])
                    user_msg.body = user_body

                    # Attach image if it exists
                    if image_filename:
                        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                        with open(image_path, 'rb') as img:
                            user_msg.attach(image_filename, 'image/png', img.read())

                    mail.send(user_msg)

            flash('Task assigned successfully, and email with image sent!', 'success')
            return redirect(url_for('manage_tasks'))

        cursor = mysql.connection.cursor()

        # Fetch tasks
        cursor.execute('''
            SELECT t.task_id, t.task_name, t.due_date, t.status, t.image, a.user_name
            FROM tasks t
            LEFT JOIN abi a ON t.user_id = a.user_id
        ''')
        tasks = cursor.fetchall()

        # Fetch users
        cursor.execute('SELECT user_id, user_name FROM abi WHERE role = 0')  # role = 0 is for users
        users = cursor.fetchall()

        cursor.close()

        return render_template('manage_tasks.html', tasks=tasks, users=users)
    else:
        return redirect(url_for('login'))



    

@app.route('/add_new_task', methods=['GET', 'POST'])
def add_new_task():
    if 'loggedin' in session and session.get('role') == 1:  # Admins only
        if request.method == 'POST':
            task_name = request.form['task_name']
            due_date = request.form['due_date']
            status = request.form['status']
            user_id = request.form['user_id'] if request.form['user_id'] else None
            
            # Handle file upload
            image_file = request.files.get('task_image')  # Get the uploaded file
            image_filename = None
            
            if image_file and allowed_file(image_file.filename):
                image_filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

            # Insert new task into the database
            cursor = mysql.connection.cursor()
            cursor.execute(''' 
                INSERT INTO tasks (task_name, due_date, status, user_id, image) 
                VALUES (%s, %s, %s, %s, %s)
            ''', (task_name, due_date, status, user_id, image_filename))
            mysql.connection.commit()

            # Fetch the email of the assigned user
            if user_id:
                cursor.execute('SELECT email FROM abi WHERE user_id = %s', (user_id,))
                user_email = cursor.fetchone()

                if user_email:
                    # Send email notification to the assigned user
                    user_subject = 'New Task Assigned'
                    user_body = f'Hi,\n\nA new task has been assigned to you:\n\nTask Name: {task_name}\nDue Date: {due_date}\nStatus: {status}\n\nBest regards,\nThe Team'
                    user_msg = Message(user_subject, recipients=[user_email[0]])  # user_email[0] contains the email address
                    user_msg.body = user_body
                    mail.send(user_msg)

            cursor.close()

            flash('Task added successfully!', 'success')
            return redirect(url_for('manage_tasks'))

        # Fetch users for the dropdown
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT user_id, user_name FROM abi WHERE role = 0')  # Fetch users who are not admins
        users = cursor.fetchall()
        cursor.close()

        print(users)  # Debugging statement to check fetched users

        return render_template('add_new_task.html', users=users)
    else:
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))




@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if 'loggedin' in session:
        if request.method == 'POST':
            task_name = request.form['task_name']
            due_date = request.form['due_date']
            status = request.form['status']

            # Fetch the current user info
            user_name = session.get('user_name')  # Get the username from session
            user_email = session.get('email')  # Get the user's email

            # Initialize variables
            filename = None
            image_base64 = None

            # Check if an image file was uploaded
            file = request.files['task_image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join('static/uploads', filename)
                file.save(file_path)

                # Convert the image to Base64
                with open(file_path, "rb") as image_file:
                    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

            # Update the task with or without image
            cursor = mysql.connection.cursor()
            if filename:
                cursor.execute('UPDATE tasks SET task_name = %s, due_date = %s, status = %s, image = %s WHERE task_id = %s',
                               (task_name, due_date, status, filename, task_id))
            else:
                cursor.execute('UPDATE tasks SET task_name = %s, due_date = %s, status = %s WHERE task_id = %s',
                               (task_name, due_date, status, task_id))

            mysql.connection.commit()
            cursor.close()

            # Prepare email content for the user
            user_msg = Message('Task Edited Successfully',
                               sender='your-email@gmail.com',  # Replace with your email
                               recipients=[user_email])

            img_tag = f'<p>Task Image:</p><img src="data:image/png;base64,{image_base64}" alt="Task Image" width="200">' if image_base64 else ''

            # Email body with task details for the user
            user_msg.html = f'''
                <p>Dear {user_name},</p>
                <p>The task with ID <strong>{task_id}</strong> has been edited successfully.</p>
                <ul>
                    <li><strong>New Task Name:</strong> {task_name}</li>
                    <li><strong>New Due Date:</strong> {due_date}</li>
                    <li><strong>Status:</strong> {"Completed" if status == "1" else "Pending"}</li>
                </ul>
                {img_tag}
                <p>Thank you!</p>
            '''
            mail.send(user_msg)

            # Prepare email content for the admin
            admin_email = 'admin-email@example.com'  # Replace with your admin email
            admin_msg = Message('Task Status Updated',
                                sender='your-email@gmail.com',  # Replace with your email
                                recipients=[admin_email])
            
            admin_img_tag = f'<p>Task Image:</p><img src="data:image/png;base64,{image_base64}" alt="Task Image" width="200">' if image_base64 else ''

            # Email body with task details for the admin
            admin_msg.html = f'''
                <p>The task with ID <strong>{task_id}</strong> has been updated.</p>
                <ul>
                    <li><strong>Assigned User:</strong> {user_name}</li>
                    <li><strong>Task Name:</strong> {task_name}</li>
                    <li><strong>Due Date:</strong> {due_date}</li>
                    <li><strong>Status:</strong> {"Completed" if status == "1" else "Pending"}</li>
                </ul>
                {admin_img_tag}
                <p>Thank you!</p>
            '''
            mail.send(admin_msg)

            return redirect(url_for('dashboard'))

        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM tasks WHERE task_id = %s', (task_id,))
            task = cursor.fetchone()
            cursor.close()

            return render_template('edit_task.html', task=task)

    else:
        return redirect(url_for('login'))



@app.route('/delete_task/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM tasks WHERE task_id = %s', (task_id,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('dashboard'))

    else:
        return redirect(url_for('login'))
    


# today
@app.route('/pending_tasks')
def pending_tasks():
    if 'loggedin' in session and session.get('role') == 1:  # Check if admin
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Join the tasks table with the abi table to get user details
            cursor.execute('''
                SELECT t.task_id, t.task_name, t.due_date, t.status, t.user_id, t.image, a.user_name, a.photo
                FROM tasks t
                LEFT JOIN abi a ON t.user_id = a.user_id
                WHERE t.status = 0
            ''')  # 0 for pending
            pending_tasks = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"Database error: {e}")
            pending_tasks = []

        return render_template('pending_tasks.html', tasks=pending_tasks)
    else:
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))


@app.route('/completed_tasks')
def completed_tasks():
    if 'loggedin' in session and session.get('role') == 1:  # Check if admin
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Join the tasks table with the abi table to get user details
            cursor.execute('''
                SELECT t.task_id, t.task_name, t.due_date, t.status, t.user_id, t.image, a.user_name, a.photo
                FROM tasks t
                LEFT JOIN abi a ON t.user_id = a.user_id
                WHERE t.status = 1  # Assuming 1 indicates completed tasks
            ''')
            completed_tasks = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"Database error: {e}")
            completed_tasks = []

        return render_template('completed_tasks.html', tasks=completed_tasks)
    else:
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
