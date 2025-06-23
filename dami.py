@app.route('/update_task/<int:task_id>', methods=['POST', 'GET'])
# def update_task(task_id):
#     if 'loggedin' in session:
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         if request.method == 'POST':
#             task_name = request.form['task_name']
#             due_date = request.form['due_date']
#             status = request.form['status']
            
#             cursor.execute('UPDATE tasks SET task_name = %s, due_date = %s, status = %s WHERE task_id = %s',
#                            (task_name, due_date, status, task_id))
#             mysql.connection.commit()
#             cursor.close()
#             flash('Task updated successfully!', 'success')
#             return redirect(url_for('tasks'))
        
#         cursor.execute('SELECT * FROM tasks WHERE task_id = %s', (task_id,))
#         task = cursor.fetchone()
#         cursor.close()
#         return render_template('task/update_task.html', task=task)
#     else:
#         return redirect(url_for('login'))
    

# @app.route('/delete_task/<int:task_id>', methods=['POST'])
# def delete_task(task_id):
#     if 'loggedin' in session:
#         cursor = mysql.connection.cursor()
#         cursor.execute('DELETE FROM tasks WHERE task_id = %s', (task_id,))
#         mysql.connection.commit()
#         cursor.close()
#         flash('Task deleted successfully!', 'success')
#         return redirect(url_for('tasks'))
#     else:
#         return redirect(url_for('login'))