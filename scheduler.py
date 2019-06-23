import csv

# File addresses
STUDENT_MAJORS = "data/mock_student_majors.csv"
MAJOR_DEPARTMENTS = "data/mock_major_departments.csv"
DEPARTMENT_ADVISERS = "data/mock_major_advisers.csv"
SCHEDULE = "data/da_schedule.csv"

# Globaal variables
GROUP_SIZE = 3


class Student:
    '''
    The Student class represents complete information about a student.

    Attributes:
        name        -- string name of student
        major       -- string name of major
        department  -- string name of department
        adviser     -- string name of divisional adviser
        time_slot   -- time when student will meet with adivser
    '''

    def __init__(self, name='', major='', department='', adviser='', time_slot=None):
        self.name = name
        self.major = major
        self.department = department
        self.adviser = adviser
        self.time_slot = time_slot

    def __str__(self):
        return self.name
        # return '{}, {}, {}, {}, {}'.format(
        #     self.name, self.major, self.department, self.adviser, self.time_slot
        # )

    def __repr__(self):
        return '({})'.format(str(self))


class Group:
    '''
    The Group class represents a group of Students assigned to a single time_slot of an adviser from their department.

    Attributes:
        students        -- list of Student objects
        single_major    -- boolean indicating students all belong to the same major
        department      -- string indicating the department the students belong to
        time_slot       -- time slot that students will meet with adviser
    '''

    def __init__(self, students=[], single_major=True, department='', time_slot=None):
        self.students = students
        self.single_major = single_major
        self.department = department
        self.time_slot = time_slot

    def __str__(self):
        return str(self.students)
        # return '{}, {}, {}, {}'.format(
        #     self.students, self.single_major, self.department, self.time_slot
        # )

    def __repr__(self):
        return '({})'.format(str(self))

    def __len__(self):
        return len(self.students)

    def add(self, student):
        self.students.append(student)


def read_student_majors(csvfile):
    '''
    Reads csv of students, majors and returns list of Student objects
    with only the name and major fields populated.

    Args:
    csv --  string of csv file name containing students and majors

    Returns:
    students    -- list of Student objects with names and majors
    majors      -- dictionary mapping majors to list of students in that major
    '''
    students = []
    majors = {}
    with open(csvfile, 'r', encoding='utf-8-sig') as data:
        reader = csv.reader(data)

        for row in reader:
            if row[0] == '':
                return students, majors
            name, major = row[0], row[1]
            stud = Student(name=name, major=major)
            students.append(stud)
            if major in majors:
                majors[major].append(stud)
            else:
                majors[major] = [stud]
    return students, majors


def read_major_departments(csvfile):
    '''
    Reads csv of majors with their departments.

    Args:
    csv --  string of csv file name containing majors and departments

    Returns:
    major_dept -- dictionary mapping majors to departments
    dept_major -- dictionary mapping departments to list of majors in that department
    '''
    major_dept = {}
    dept_major = {}
    with open(csvfile, 'r', encoding='utf-8-sig') as data:
        reader = csv.reader(data)

        for row in reader:
            if row[0] == '':
                return major_dept, dept_major
            major, department = row[0], row[1]
            major_dept[major] = department
            if department in dept_major:
                dept_major[department].append(major)
            else:
                dept_major[department] = [major]
    return major_dept, dept_major


def read_dept_advisers(csvfile):
    '''
    Reads csv of department to adviser matching.

    Args:
    csv --  string of csv file name containing departments and advisers

    Returns:
    Dictionary mapping departments to advisers.
    '''
    dept_adviser = {}
    with open(csvfile, 'r', encoding='utf-8-sig') as data:
        reader = csv.reader(data)

        for row in reader:
            if row[0] == '':
                return dept_adviser
            department, adviser = row[1], row[0]
            dept_adviser[department] = adviser
    return dept_adviser


def populate_student_fields(students, major_dept, dept_adviser):
    '''
    Populates all fields of a Student object, except for time_slot.

    Args:
    students        -- list of Student objects
    major_dept      -- dictionary mapping majors to departments
    dept_adviser    -- dictionary mapping departments to advisers

    Returns:
    Nothing.
    '''
    for student in students:
        major = student.major
        department = major_dept[major]
        adviser = dept_adviser[department]

        student.department = department
        student.adviser = adviser
    return


def partition(total, group_size=GROUP_SIZE):
    '''
    Partitions total into groups of sizes group_size or group_size + 1.

    Args:
    total       -- integer containing the total number to partition
    group_size  -- target integer for the size of each group

    Returns:
    List of integer(s) where the nth integer represents the nth group size.
    '''
    if group_size == 3 and total < 6:
        return [total]

    partition = []

    groups = int(total / group_size)
    remainder = total % group_size

    for _ in range(groups):
        partition.append(group_size)

    # TODO: handle this case
    if groups < remainder:
        print('ERROR: IMPERFECT PARTITION')
        partition.append(remainder)
        return partition

    for i in range(remainder):
        partition[i] += 1

    return partition


def partition_majors(majors, major_dept, group_size=GROUP_SIZE):
    '''
    Groups students in each department of roughly group_size, where
    each group contains students who belong to the same major.

    Args:
    majors      -- dictionary mapping majors to list of students in that major
    major_dept  -- dictionary mapping majors to departments
    group_size  -- integer size of each group

    Returns:
    Dictionary mapping each department to a list of groups.
    '''
    groupings = {}
    for major in majors:
        department = major_dept[major]
        students = majors[major]
        distribution = partition(len(students), group_size)

        idx = 0
        for num in distribution:
            group = Group(students=[], single_major=True,
                          department=department)
            for _ in range(num):
                stud = students[idx]
                group.add(stud)
                idx += 1

            if department in groupings:
                groupings[department].append(group)
            else:
                groupings[department] = [group]

    return groupings


def assign_slots(groupings):
    '''
    Assign time slots to each group.

    Args:
    groupings   -- dictionary mapping each department to a list of groups of students

    Returns:
    Nothing.
    '''
    for department in groupings:
        groups = groupings[department]
        slot = 1
        for group in groups:
            group.time_slot = slot
            for student in group.students:
                student.time_slot = slot
            slot += 1
    return


def write_slots_csv(groupings, dept_adviser, destination=SCHEDULE):
    '''
    Writes the final schedule to a csv file.

    Args:
    groupings       -- dictionary mapping each department to a list of groups of students
    dept_adviser    -- dictionary mapping departments to advisers
    destination     -- string name of csv file to write to

    Rwweturns:
    Nothing. Writes adviser,time_slot,student,major to csv file. 
    '''
    with open(destination, 'w') as csvfile:
        for department in groupings:
            adviser = dept_adviser[department]
            groups = groupings[department]
            for group in groups:
                for student in group.students:
                    s = '{},{},{},{}\n'.format(
                        adviser, group.time_slot, student.name, student.major
                    )
                    csvfile.write(s)
    print('success!')


if __name__ == "__main__":
    # Read stuff
    students, majors = read_student_majors(STUDENT_MAJORS)
    major_dept, dept_major = read_major_departments(MAJOR_DEPARTMENTS)
    dept_advisers = read_dept_advisers(DEPARTMENT_ADVISERS)

    # Fill students info
    populate_student_fields(students, major_dept, dept_advisers)

    # Group students and assign to time slots
    groupings = partition_majors(majors, major_dept)
    assign_slots(groupings)

    # Output results
    write_slots_csv(groupings, dept_advisers, destination=SCHEDULE)
