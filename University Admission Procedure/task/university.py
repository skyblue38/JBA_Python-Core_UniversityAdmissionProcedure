# JBA Python Core track
# Project: University Admission Procedure - https://hyperskill.org/projects/163
# Stage 7/7: Extensive Training
# Submitted by Chris Freeman, 31-Jan-2023


def avg_calc(dx: int, pr: list, ap: list) -> float:
    """ Department ranking is based on required subject average.
    This function returns the average of exam results expected by each department.
    'dx' is the Department code, 'pr' is list of exams for each department
    'ap' is the Applicant's details including their exam results. """
    subj_list = pr[dx][1]
    exam_total = 0.0
    for sx in subj_list:
        exam_total += ap[0][sx]
    exam_avg = exam_total / len(subj_list)
    entrance_exam = ap[0][4]
    if entrance_exam > exam_avg:
        return entrance_exam
    return exam_avg


dept_names = ['Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics']
dept_filename = ['biotech.txt', 'chemistry.txt', 'engineering.txt',
                 'mathematics.txt', 'physics.txt']
dept_places = [[], [], [], [], []]                      # selection lists for each dept
n_prefs = 3                                             # number of dept preferences
subjects = ['physics', 'chemistry', 'math', 'compsci']  # order of exam marks
pre_req = [(0, (0, 1)), (1, (1, )), (2, (2, 3)),        # subject exams for each dept
           (3, (2, )), (4, (0, 2))]
app_list = []                                           # list of applicants
n_places = int(input())                                 # available places in each dept
with open('applicants.txt', 'r', encoding='utf-8') as file:
    for line in file:                                   # read list of applicants
        first_name, last_name, physics, chemistry, math, compsci, entrance, \
            pref1, pref2, pref3 = line.strip().split()
        app_list.append([(float(physics), float(chemistry), float(math), float(compsci),
                          float(entrance)), first_name + ' ' + last_name, pref1, pref2, pref3])
for pref in range(n_prefs):                         # scan thru preferences requested
    for dept in range(len(dept_names)):             # for each department
        applied = []
        for ix, app in enumerate(app_list):         # scan the applicant list
            if app[pref+2] == dept_names[dept]:     # find preference for this department
                rex = avg_calc(dept, pre_req, app)  # required exam average
                applied.append((ix, app, rex))      # and transfer to applied list
        applied.sort(key=lambda x: (-x[2], x[1][1]))  # sort by exam in name
        selected = []
        for ix, app, rex in applied:
            if len(dept_places[dept]) < n_places:   # if places remain,
                selected.append(ix)                 # transfer applicant to department list
                dept_places[dept].append((app_list[ix], rex))
        if selected:
            for ix in sorted(selected, reverse=True):  # remove selected applicants from main list
                app_list.pop(ix)
for dept_no in range(len(dept_names)):              # scan thru department applicant lists
    print(dept_names[dept_no])
    f = open(dept_filename[dept_no], 'w', encoding='utf-8')
    for app in sorted(dept_places[dept_no], key=lambda x: (-x[1], x[0][1])):
        print(f'{app[0][1]} {round(app[1], 2)}')    # print approved applicant
        f.write(f'{app[0][1]} {round(app[1], 2)}\n')
    print()
    f.close()
