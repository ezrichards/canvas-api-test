import os
from canvasapi import Canvas
from datetime import datetime
from dateutil.parser import isoparse
from dotenv import load_dotenv

def filter_courses(courses):
    """
    Filters out empty courses (if any). Canvas sometimes has empty courses.
    Credit to https://github.com/Person314159/cs221bot/ for finding this.
    """
    filteredCourses = []
    for course in courses:
        if hasattr(course, "name"):
            filteredCourses.append(course)
    return filteredCourses

def get_enrollments(user):
    """
    Gets the specified user's active course enrollments.
    """
    enrollments = []
    for enrollment in user.get_enrollments():        
        enrollments.append(canvas.get_course(enrollment.__getattribute__("course_id")).__getattribute__("name"))
    return enrollments

load_dotenv()

canvas = Canvas(os.getenv("API_URL"), os.getenv("API_KEY"))
user = canvas.get_user(26508)
# course = canvas.get_course('36822')

print("ALL COURSES:\n")
for course in filter_courses(user.get_courses()):
    print(course.__getattribute__("name"))

print("\nENROLLED COURSES:\n")
for enrollment in get_enrollments(user):
    print(enrollment)

print("\nGRADES:\n")
size = 0
for enrollment in user.get_enrollments():
    size += 1

for i in range(0, size):
    try:
        final_score = user.get_enrollments()[i].__getattribute__("grades")['final_score']
        if final_score != None and final_score != 0.0:
            print(user.get_enrollments()[i].__getattribute__("grades")['html_url'])
            print("Final Grade:", final_score)
    except:
        pass

print("\nASSIGNMENTS:\n")
for assignment in course.get_assignments():
    now = datetime(2021, 8, 26, 0, 0) # example date
    # now = datetime.now()

    due_at = assignment.__getattribute__("due_at")
    if due_at:
        diff = isoparse(due_at).replace(tzinfo=None) - now

        # if assignment is due in the next week, display
        if int(str(diff).split(" days")[0]) <= 7:
            due_at_str = isoparse(due_at).strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"NOW: {now}")
            print(f"DIFF: {diff}")
            print(f"DUE DATE: {due_at_str}")
    
            title = "Assignment: " + assignment.__getattribute__("name")
            url = assignment.__getattribute__("html_url")

            print(title)
            print(url)

            points = assignment.get_submission(user).__getattribute__("score")
            possible_points = assignment.__getattribute__("points_possible")
            
            if(points != None and possible_points > 0):
                print("Points: ", points)
                print("Possible Points: ", possible_points)
                percentage = (points / possible_points) * 100
                print("PERCENTAGE: ", percentage)

            print("")
