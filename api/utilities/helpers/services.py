from datetime import datetime

from api.models import User


def convert_date_to_date_time(date_string):
	# CONVERT DATE STRING TO DATE TIME OBJECT
	format_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
	return format_date


def assign_user(user_list):
	users = []
	if user_list and len(user_list) > 0:
		for user_id in user_list:
			user = User.find_by_id(user_id)
			if not user:
				continue
			else:
				users.append(user)
		return users


def check_assignee(task_assignees, project_assignee):
	project_user_ids = []
	assignee_list = []
	for user in project_assignee:
		project_user_ids.append(user.id)
	if project_user_ids and len(project_user_ids) > 0:
		for assignee in task_assignees:
			if assignee not in project_user_ids:
				task_assignees.remove(assignee)
			else:
				assignee_list.append(assignee)
		return assignee_list
	else:
		return []


def check_date_difference(task_due_date, project_due_date):
	duration = project_due_date - task_due_date
	duration_in_seconds = duration.total_seconds()
	value = True if duration_in_seconds > 0 else False
	return value
