def get_undergraduate_data_science_recommendations(major):
    """Get undergraduate data science course recommendations based on UTD catalog"""
    
    base_recommendations = {
        'career_path': f'Data Scientist ({major} Track) - Undergraduate',
        'key_skills_needed': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Visualization'],
        'student_type': 'Undergraduate',
        'degree_requirements': 'Based on UTD 2025-2026 Undergraduate Catalog - 40-50 courses over 8 semesters',
        'total_courses': '40-50 courses over 8 semesters',
        'core_courses': [],
        'elective_courses': [],
        'course_sequence': [],
        'prerequisites': [],
        'next_steps': []
    }
    
    if major == 'Business Analytics':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'R', 'SQL', 'Statistics', 'Business Intelligence', 'Tableau', 'Power BI'],
            'core_courses': [
                'BUAN 3341 - Business Analytics (Major Core)',
                'BUAN 4341 - Advanced Business Analytics (Major Core)',
                'BUAN 4342 - Data Mining and Machine Learning (Major Core)',
                'BUAN 4343 - Big Data Analytics (Major Core)',
                'BUAN 4344 - Business Intelligence (Major Core)',
                'BUAN 4345 - Business Intelligence and Analytics (Major Core)',
                'MATH 1325 - Business Calculus (Prerequisite)',
                'MATH 1326 - Business Calculus II (Prerequisite)',
                'STAT 3331 - Probability and Statistics (Prerequisite)',
                'MIS 3300 - Business Programming (Prerequisite)'
            ],
            'elective_courses': [
                'MKT 4330 - Marketing Analytics (Major Elective)',
                'MKT 4331 - Digital Marketing Analytics (Major Elective)',
                'MIS 4350 - Data Mining and Business Intelligence (Major Elective)',
                'MIS 4354 - Data Visualization (Major Elective)',
                'MIS 4356 - Database Systems (Major Elective)',
                'MIS 4357 - Cloud Computing (Major Elective)',
                'Plus 30+ general education and free electives'
            ],
            'course_sequence': [
                'Year 1: General education + MATH 1325, 1326, STAT 3331',
                'Year 2: MIS 3300, BUAN 3341, general education courses',
                'Year 3: BUAN 4341, 4342, 4344, major electives',
                'Year 4: BUAN 4343, 4345, remaining electives, capstone'
            ],
            'prerequisites': ['MATH 1325, 1326 for BUAN courses', 'STAT 3331 for advanced courses'],
            'graduation_plan': {
                'total_courses': '40-50 courses over 8 semesters',
                'major_courses': '12-15 courses',
                'general_education': '15-20 courses',
                'free_electives': '10-15 courses',
                'graduation_requirements': 'Complete all major requirements + general education'
            },
            'next_steps': [
                'Start with MATH 1325 and STAT 3331 for foundation',
                'Take BUAN 3341 in sophomore year',
                'Complete BUAN 4342 for machine learning skills',
                'Build portfolio with business analytics projects'
            ]
        })
    elif major == 'Information Technology Management':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'SQL', 'Machine Learning', 'Data Visualization', 'Cloud Computing'],
            'core_courses': [
                'MIS 4350 - Data Mining and Business Intelligence (Major Core)',
                'MIS 4351 - Advanced Data Mining (Major Core)',
                'MIS 4352 - Machine Learning for Business (Major Core)',
                'MIS 4353 - Big Data Analytics (Major Core)',
                'MIS 4354 - Data Visualization (Major Core)',
                'MIS 4356 - Database Systems (Major Core)',
                'MIS 3300 - Business Programming (Prerequisite)',
                'MIS 3310 - Database Systems I (Prerequisite)',
                'MATH 1325 - Business Calculus (Prerequisite)',
                'STAT 3331 - Probability and Statistics (Prerequisite)'
            ],
            'elective_courses': [
                'BUAN 3341 - Business Analytics (Major Elective)',
                'BUAN 4344 - Business Intelligence (Major Elective)',
                'MKT 4330 - Marketing Analytics (Major Elective)',
                'MKT 4331 - Digital Marketing Analytics (Major Elective)',
                'MIS 4355 - Software Engineering (Major Elective)',
                'MIS 4357 - Cloud Computing (Major Elective)',
                'Plus 30+ general education and free electives'
            ],
            'course_sequence': [
                'Year 1: General education + MATH 1325, STAT 3331',
                'Year 2: MIS 3300, 3310, general education courses',
                'Year 3: MIS 4350, 4351, 4352, major electives',
                'Year 4: MIS 4353, 4354, 4356, remaining electives, capstone'
            ],
            'prerequisites': ['MIS 3300, 3310 for MIS courses', 'MATH 1325, STAT 3331 for advanced courses'],
            'graduation_plan': {
                'total_courses': '40-50 courses over 8 semesters',
                'major_courses': '12-15 courses',
                'general_education': '15-20 courses',
                'free_electives': '10-15 courses',
                'graduation_requirements': 'Complete all major requirements + general education'
            },
            'next_steps': [
                'Start with MIS 3300 and MATH 1325 for foundation',
                'Take MIS 4350 in sophomore year',
                'Complete MIS 4352 for ML business applications',
                'Build projects combining IT and analytics'
            ]
        })
    elif major == 'Computer Science':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Visualization', 'Algorithms'],
            'core_courses': [
                'CS 1336 - Computer Science I (Major Core)',
                'CS 2336 - Computer Science II (Major Core)',
                'CS 3345 - Data Structures and Algorithm Analysis (Major Core)',
                'CS 4352 - Database Systems (Major Core)',
                'CS 4351 - Software Engineering (Major Core)',
                'CS 4353 - Computer Networks (Major Core)',
                'MATH 2418 - Linear Algebra (Prerequisite)',
                'MATH 2419 - Calculus II (Prerequisite)',
                'STAT 3331 - Probability and Statistics (Prerequisite)',
                'MATH 3330 - Probability and Statistics (Prerequisite)'
            ],
            'elective_courses': [
                'CS 6313 - Statistical Methods for Data Science (Major Elective)',
                'CS 6375 - Machine Learning (Major Elective)',
                'CS 6301 - Special Topics in Computer Science (Data Mining) (Major Elective)',
                'CS 6302 - Special Topics in Computer Science (Big Data) (Major Elective)',
                'CS 6303 - Special Topics in Computer Science (Deep Learning) (Major Elective)',
                'Plus 30+ general education and free electives'
            ],
            'course_sequence': [
                'Year 1: General education + CS 1336, MATH 2418, 2419',
                'Year 2: CS 2336, 3345, STAT 3331, general education',
                'Year 3: CS 4352, 4351, 4353, major electives',
                'Year 4: CS 6313, 6375, remaining electives, capstone'
            ],
            'prerequisites': ['CS 1336, 2336 for CS courses', 'MATH 2418, 2419 for advanced courses'],
            'graduation_plan': {
                'total_courses': '40-50 courses over 8 semesters',
                'major_courses': '12-15 courses',
                'general_education': '15-20 courses',
                'free_electives': '10-15 courses',
                'graduation_requirements': 'Complete all major requirements + general education'
            },
            'next_steps': [
                'Start with CS 1336 and MATH 2418 for foundation',
                'Take CS 2336 and 3345 in sophomore year',
                'Complete CS 4352 for database skills',
                'Build portfolio projects using Python and scikit-learn'
            ]
        })
    
    return base_recommendations
