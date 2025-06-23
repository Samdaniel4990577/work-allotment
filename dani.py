    
# ADD_USER
# @app.route('/add_user', methods=['GET', 'POST'])
# def add_user():
#     if 'loggedin' in session and session.get('role') == 1:  # Only admins can access
#         if request.method == 'POST':
#             user_name = request.form['user_name']
#             email = request.form['email']
#             password = request.form['password']
#             role = request.form['role']  # 1 for admin, 0 for user
#             city = request.form['city']
#             contact = request.form['contact']

#             # Handle photo upload if provided
            

#             # Hash the password for security
#             hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

#             cursor = mysql.connection.cursor()
#             cursor.execute(
#                 'INSERT INTO abi (user_name, email, password, role, city, contact, photo) VALUES (%s, %s, %s, %s, %s, %s, %s)',
#                 (user_name, email, hashed_password, role, city, contact, photo)
#             )
#             mysql.connection.commit()
#             cursor.close()

#             flash('User added successfully!', 'success')
#             return redirect(url_for('admin_dashboard'))

#         return render_template('add_user.html')  # Display form
#     else:
#         flash('Access denied. Admins only.')
#         return redirect(url_for('login'))

# @app.route('/add_user', methods=['GET', 'POST'])
# def add_user():
#     if 'loggedin' in session and session.get('role') == 1:  # Only admins can access
#         if request.method == 'POST':
#             user_name = request.form['user_name']
#             email = request.form['email']
#             password = request.form['password']
#             role = request.form['role']  # 1 for admin, 0 for user
#             city = request.form['city']
#             contact = request.form['contact']

#             # Handle photo upload if provided
#             photo = request.files['photo']  # Get the file from the request
#             photo_filename = None
#             if photo:
#                 photo_filename = photo.filename
#                 photo.save(os.path.join('static/uploads', photo_filename))  # Save the photo

#             # Hash the password for security
#             hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

#             cursor = mysql.connection.cursor()

#             # Check if email already exists
#             cursor.execute('SELECT * FROM abi WHERE email = %s', (email,))
#             existing_user = cursor.fetchone()

#             if existing_user:
#                 flash('Email already exists. Please choose another email.', 'danger')
#                 cursor.close()
#                 return redirect(url_for('add_user'))

#             cursor.execute(
#                 'INSERT INTO abi (user_name, email, password, role, city, contact, photo) VALUES (%s, %s, %s, %s, %s, %s, %s)',
#                 (user_name, email, hashed_password, role, city, contact, photo_filename)
#             )
#             mysql.connection.commit()
#             cursor.close()

#             flash('User added successfully!', 'success')
#             return redirect(url_for('admin_dashboard'))

#         return render_template('add_user.html')  # Display form
#     else:
#         flash('Access denied. Admins only.')
#         return redirect(url_for('login'))


# ADDMIN_DASHBORAD
# @app.route('/admin_dashboard')
# def admin_dashboard():
#     if 'loggedin' in session and session.get('role') == 1:
#         try:
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cursor.execute('SELECT user_id, user_name, email, time, photo, contact, city FROM abi')
#             users = cursor.fetchall()
#             cursor.close()
#         except Exception as e:
#             print(f"Database error: {e}")
#             users = []
        
#         # Debug: Print user data
#         for user in users:
#             print(f"User ID: {user.get('user_id')}, Name: {user.get('user_name')}, Photo: {user.get('photo')}")

#         return render_template('admin_dashboard.html', users=users)
#     else:
#         flash('Access denied. Admins only.')
#         return redirect(url_for('login'))


# @app.route('/admin_dashboard')
# def admin_dashboard():
#     if 'loggedin' in session and session.get('role') == 1:  # Check if admin
#         try:
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             # Fetch the user_id along with other details
#             cursor.execute('SELECT user_id, user_name, email, time, photo, contact, city FROM abi')
#             users = cursor.fetchall()
#             cursor.close()
#         except Exception as e:
#             print(f"Database error: {e}")
#             users = []
        
#         # Debug: Print user data
#         for user in users:
#             print(f"User ID: {user['user_id']}, Name: {user['user_name']}, Photo: {user['photo']}")

#         return render_template('admin_dashboard.html', users=users)
#     else:
#         flash('Access denied. Admins only.')
#         return redirect(url_for('login'))


# user_dashborad
# @app.route('/user_dashboard')
# def user_dashboard():
#     if 'loggedin' in session and session.get('role') == 0:
#         user_id = session.get('id')  # Ensure you use the correct key

#         try:
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cursor.execute('''
#                 SELECT task_id, task_name, due_date, status
#                 FROM tasks
#                 WHERE user_id = %s
#             ''', (user_id,))
#             tasks = cursor.fetchall()
#             cursor.close()
#         except Exception as e:
#             print(f"Database error: {e}")
#             tasks = []
#             print("Fetched tasks:", tasks)

#         return render_template('user_dashboard.html', tasks=tasks)
#     else:
#         flash('Access denied. User privileges required.')
#         return redirect(url_for('login'))


# @app.route('/index', methods=['POST', 'GET'])
# def index():
#     if 'loggedin' in session:
#         return render_template('main.html')
#     else:    
#         return redirect(url_for('login'))




# from flask import Flask, render_template, request, redirect, url_for, session, flash,send_from_directory
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# from flask_mysqldb import MySQL
# # import re
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.utils import secure_filename
# from flask import Response
# from werkzeug.security import generate_password_hash
# from PIL import Image
# import os, io
# import MySQLdb
# import base64
# from flask import send_file
# # import secrets
# import base64
# from flask_mail import Mail, Message
# from flask import Flask, render_template, request, redirect, url_for, session, flash
# import MySQLdb.cursors
# from werkzeug.security import check_password_hash
# import re
# import os

# from werkzeug.utils import secure_filename
# from PIL import Image
# from werkzeug.security import generate_password_hash
# from werkzeug.security import generate_password_hash

# # Hash the password using the correct method
# hashed_password = generate_password_hash(password, method='pbkdf2:sha256')




# @app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
# def edit_task(task_id):
#     if 'loggedin' in session:
#         if request.method == 'POST':
#             task_name = request.form['task_name']
#             due_date = request.form['due_date']
#             status = request.form['status']

#             cursor = mysql.connection.cursor()
#             cursor.execute('UPDATE tasks SET task_name = %s, due_date = %s, status = %s WHERE task_id = %s',
#                            (task_name, due_date, status, task_id))
#             mysql.connection.commit()
#             cursor.close()

#             return redirect(url_for('dashboard'))

#         else:
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cursor.execute('SELECT * FROM tasks WHERE task_id = %s', (task_id,))
#             task = cursor.fetchone()
#             cursor.close()

#             return render_template('edit_task.html', task=task)

#     else:
#         return redirect(url_for('login'))

# @app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
# def edit_task(task_id):
#     if 'loggedin' in session:
#         if request.method == 'POST':
#             task_name = request.form['task_name']
#             due_date = request.form['due_date']
#             status = request.form['status']

#             # Update the task in the database
#             cursor = mysql.connection.cursor()
#             cursor.execute('UPDATE tasks SET task_name = %s, due_date = %s, status = %s WHERE task_id = %s',
#                            (task_name, due_date, status, task_id))
#             mysql.connection.commit()
#             cursor.close()

#             # Get the logged-in user's email
#             user_email = session.get('email')

#             # Send email notification to the user
#             msg = Message('Task Edited Successfully',
#                           sender='your-email@gmail.com',  # Replace with your email
#                           recipients=[user_email])  # Send email to the logged-in user's email
#             msg.body = f'The task with ID {task_id} has been edited successfully.\n\n' \
#                        f'New Task Name: {task_name}\n' \
#                        f'New Due Date: {due_date}\n' \
#                        f'New Status: {"Completed" if status == "1" else "Pending"}'
#             mail.send(msg)

#             # Send email to admin if the task is completed
#             if status == "1":  # Status 1 means Completed
#                 admin_email = 'admin-email@gmail.com'  # Replace with the admin's email
#                 admin_msg = Message('Task Completed Notification',
#                                     sender='your-email@gmail.com',  # Replace with your email
#                                     recipients=[admin_email])  # Send to admin
#                 admin_msg.body = f'Task ID: {task_id}\nTask Name: {task_name}\nDue Date: {due_date}\n' \
#                                  f'was marked as Completed by the user {user_email}.'
#                 mail.send(admin_msg)

#             return redirect(url_for('dashboard'))

#         else:
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cursor.execute('SELECT * FROM tasks WHERE task_id = %s', (task_id,))
#             task = cursor.fetchone()
#             cursor.close()

#             return render_template('edit_task.html', task=task)

#     else:
#         return redirect(url_for('login'))


# @app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
# def edit_task(task_id):
#     if 'loggedin' in session:
#         if request.method == 'POST':
#             task_name = request.form['task_name']
#             due_date = request.form['due_date']
#             status = request.form['status']

#             # Check if an image file was uploaded
#             file = request.files['task_image']
#             if file and file.filename != '':
#                 filename = secure_filename(file.filename)
#                 file.save(os.path.join('static/uploads', filename))

#                 # Update the task including the image filename
#                 cursor = mysql.connection.cursor()
#                 cursor.execute('UPDATE tasks SET task_name = %s, due_date = %s, status = %s, image = %s WHERE task_id = %s',
#                                (task_name, due_date, status, filename, task_id))
#             else:
#                 # Update the task without changing the image
#                 cursor = mysql.connection.cursor()
#                 cursor.execute('UPDATE tasks SET task_name = %s, due_date = %s, status = %s WHERE task_id = %s',
#                                (task_name, due_date, status, task_id))

#             mysql.connection.commit()
#             cursor.close()

#             # Get the logged-in user's email
#             user_email = session.get('email')

#             # Send email notification to the user
#             msg = Message('Task Edited Successfully',
#                           sender='your-email@gmail.com',  # Replace with your email
#                           recipients=[user_email])
#             msg.body = f'The task with ID {task_id} has been edited successfully.\n\n' \
#                        f'New Task Name: {task_name}\n' \
#                        f'New Due Date: {due_date}\n' \
#                        f'New Status: {"Completed" if status == "1" else "Pending"}'
#             mail.send(msg)

#             # Send email to admin if the task is completed
#             if status == "1":  # Status 1 means Completed
#                 admin_email = 'admin-email@gmail.com'  # Replace with the admin's email
#                 admin_msg = Message('Task Completed Notification',
#                                     sender='your-email@gmail.com',  # Replace with your email
#                                     recipients=[admin_email])
#                 admin_msg.body = f'Task ID: {task_id}\nTask Name: {task_name}\nDue Date: {due_date}\n' \
#                                  f'was marked as Completed by the user {user_email}.'
#                 mail.send(admin_msg)

#             return redirect(url_for('dashboard'))

#         else:
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cursor.execute('SELECT * FROM tasks WHERE task_id = %s', (task_id,))
#             task = cursor.fetchone()
#             cursor.close()

#             return render_template('edit_task.html', task=task)

#     else:
#         return redirect(url_for('login'))