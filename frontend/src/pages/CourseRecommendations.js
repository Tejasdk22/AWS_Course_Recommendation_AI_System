import React, { useState } from 'react';
import { useCourse } from '../context/CourseContext';
import { GraduationCap, User, Target, Loader, CheckCircle, AlertCircle, BookOpen, TrendingUp, Briefcase, Award } from 'lucide-react';

const CourseRecommendations = () => {
  const { loading, results, error, submitCourseQuery, clearResults } = useCourse();
  const [formData, setFormData] = useState({
    major: '',
    studentType: '',
    careerGoal: ''
  });

  const majors = [
    'Business Analytics',
    'Computer Science', 
    'Information Technology Management',
    'Mathematics',
    'Statistics',
    'Engineering'
  ];

  const studentTypes = [
    'Graduate',
    'Undergraduate'
  ];

  const careerGoals = [
    'Data Scientist',
    'Data Engineer', 
    'Data Analyst',
    'Machine Learning Engineer',
    'Software Engineer',
    'Business Analyst',
    'Product Manager',
    'Consultant'
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.major && formData.studentType && formData.careerGoal) {
      submitCourseQuery(formData);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const CourseCard = ({ course, type }) => (
    <div className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow duration-200">
      <div className="flex items-start justify-between mb-2">
        <h4 className="font-semibold text-gray-900">{course.code} - {course.name}</h4>
        <span className="text-sm text-primary-600 bg-primary-50 px-2 py-1 rounded">
          {course.credits} credits
        </span>
      </div>
      <p className="text-gray-600 text-sm mb-3">{course.description}</p>
      <div className="space-y-2">
        <div>
          <span className="text-xs font-medium text-gray-500">Skills Taught:</span>
          <div className="flex flex-wrap gap-1 mt-1">
            {course.skills_taught?.map((skill, idx) => (
              <span key={idx} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                {skill}
              </span>
            ))}
          </div>
        </div>
        <div>
          <span className="text-xs font-medium text-gray-500">Career Relevance:</span>
          <p className="text-xs text-gray-600 mt-1">{course.career_relevance}</p>
        </div>
      </div>
    </div>
  );

  const CareerLevelCard = ({ level, data }) => (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-semibold text-gray-900">{data.title}</h4>
        <span className="text-sm font-medium text-primary-600">{data.salary_range}</span>
      </div>
      <p className="text-gray-600 text-sm mb-3">{data.description}</p>
      <div className="space-y-2">
        <div>
          <span className="text-xs font-medium text-gray-500">Skills Required:</span>
          <div className="flex flex-wrap gap-1 mt-1">
            {data.skills_required?.map((skill, idx) => (
              <span key={idx} className="text-xs bg-primary-100 text-primary-700 px-2 py-1 rounded">
                {skill}
              </span>
            ))}
          </div>
        </div>
        <div className="text-xs text-gray-500">
          Experience: {data.experience_needed}
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Course Recommendation AI
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Get personalized course recommendations, academic planning, and curriculum guidance 
            powered by advanced AI agents.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Form Section */}
          <div className="lg:col-span-1">
            <div className="card sticky top-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                <User className="w-5 h-5 mr-2 text-primary-600" />
                Plan Your Academic Path
              </h2>
              
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Major Selection */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <GraduationCap className="w-4 h-4 inline mr-1" />
                    Your Major
                  </label>
                  <select
                    value={formData.major}
                    onChange={(e) => handleInputChange('major', e.target.value)}
                    className="input-field"
                    required
                  >
                    <option value="">Select your major</option>
                    {majors.map(major => (
                      <option key={major} value={major}>{major}</option>
                    ))}
                  </select>
                </div>

                {/* Student Type */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <User className="w-4 h-4 inline mr-1" />
                    Student Type
                  </label>
                  <select
                    value={formData.studentType}
                    onChange={(e) => handleInputChange('studentType', e.target.value)}
                    className="input-field"
                    required
                  >
                    <option value="">Select student type</option>
                    {studentTypes.map(type => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                </div>

                {/* Career Goal */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Target className="w-4 h-4 inline mr-1" />
                    Career Goal
                  </label>
                  <select
                    value={formData.careerGoal}
                    onChange={(e) => handleInputChange('careerGoal', e.target.value)}
                    className="input-field"
                    required
                  >
                    <option value="">Select career goal</option>
                    {careerGoals.map(goal => (
                      <option key={goal} value={goal}>{goal}</option>
                    ))}
                  </select>
                </div>

                {/* Submit Button */}
                  <button
                    type="submit"
                    disabled={loading || !formData.major || !formData.studentType || !formData.careerGoal}
                    className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                  >
                    {loading ? (
                      <>
                        <Loader className="w-4 h-4 mr-2 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <BookOpen className="w-4 h-4 mr-2" />
                        Get Course Recommendations
                      </>
                    )}
                  </button>

                {results && (
                  <button
                    type="button"
                    onClick={clearResults}
                    className="w-full btn-secondary"
                  >
                    Start Over
                  </button>
                )}
              </form>
            </div>
          </div>

          {/* Results Section */}
          <div className="lg:col-span-2">
            {loading && (
              <div className="card text-center py-12">
                <div className="loading-dots mx-auto mb-4">
                  <div></div>
                  <div></div>
                  <div></div>
                  <div></div>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  AI Agents are analyzing your academic path...
                </h3>
                <p className="text-gray-600">
                  This may take a few moments while our agents gather course data and academic information.
                </p>
              </div>
            )}

            {error && (
              <div className="card border-red-200 bg-red-50">
                <div className="flex items-center mb-4">
                  <AlertCircle className="w-5 h-5 text-red-600 mr-2" />
                  <h3 className="text-lg font-semibold text-red-800">Error</h3>
                </div>
                <p className="text-red-700">{error}</p>
              </div>
            )}

            {results && (
              <div className="space-y-8">
                {/* Parsed Information */}
                {results.parsed_information && (
                  <div className="card">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                      <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
                      Analysis Summary
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="text-center p-4 bg-primary-50 rounded-lg">
                        <div className="text-sm text-primary-600 font-medium">Major</div>
                        <div className="text-lg font-semibold text-primary-800">{results.parsed_information.major}</div>
                      </div>
                      <div className="text-center p-4 bg-green-50 rounded-lg">
                        <div className="text-sm text-green-600 font-medium">Student Type</div>
                        <div className="text-lg font-semibold text-green-800">{results.parsed_information.student_type}</div>
                      </div>
                      <div className="text-center p-4 bg-purple-50 rounded-lg">
                        <div className="text-sm text-purple-600 font-medium">Career Goal</div>
                        <div className="text-lg font-semibold text-purple-800">{results.parsed_information.career_goal}</div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Career Analysis */}
                {results.specific_career_analysis && (
                  <div className="space-y-6">
                    {/* Career Description */}
                    <div className="card">
                      <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                        <Briefcase className="w-5 h-5 mr-2 text-primary-600" />
                        Career Overview
                      </h3>
                      <p className="text-gray-700 leading-relaxed">
                        {results.specific_career_analysis.career_description}
                      </p>
                    </div>

                    {/* Market Analysis */}
                    {results.specific_career_analysis.market_analysis && (
                      <div className="card">
                        <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                          <TrendingUp className="w-5 h-5 mr-2 text-primary-600" />
                          Market Analysis
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <div>
                            <h4 className="font-semibold text-gray-900 mb-2">Job Market Summary</h4>
                            <div className="space-y-2 text-sm">
                              <div><span className="font-medium">Opportunities:</span> {results.specific_career_analysis.market_analysis.job_market_summary?.total_opportunities}</div>
                              <div><span className="font-medium">Growth:</span> {results.specific_career_analysis.market_analysis.job_market_summary?.growth_prospect}</div>
                              <div><span className="font-medium">Salary:</span> {results.specific_career_analysis.market_analysis.job_market_summary?.average_salary}</div>
                            </div>
                          </div>
                          <div>
                            <h4 className="font-semibold text-gray-900 mb-2">Top Skills</h4>
                            <div className="flex flex-wrap gap-1">
                              {results.specific_career_analysis.market_analysis.job_market_summary?.top_skills_demanded?.map((skill, idx) => (
                                <span key={idx} className="text-xs bg-primary-100 text-primary-700 px-2 py-1 rounded">
                                  {skill}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Career Progression */}
                    {results.specific_career_analysis.career_progression && (
                      <div className="card">
                        <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                          <Award className="w-5 h-5 mr-2 text-primary-600" />
                          Career Progression
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          {Object.entries(results.specific_career_analysis.career_progression).map(([level, data]) => (
                            <CareerLevelCard key={level} level={level} data={data} />
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Course Recommendations */}
                    {results.specific_career_analysis.course_recommendations && (
                      <div className="card">
                        <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                          <BookOpen className="w-5 h-5 mr-2 text-primary-600" />
                          Course Recommendations
                        </h3>
                        
                        {/* Core Courses */}
                        {results.specific_career_analysis.course_recommendations.core_courses && (
                          <div className="mb-6">
                            <h4 className="text-lg font-semibold text-gray-900 mb-3">Core Courses (6 Required)</h4>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                              {results.specific_career_analysis.course_recommendations.core_courses.map((course, idx) => (
                                <CourseCard key={idx} course={course} type="core" />
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Elective Courses */}
                        {results.specific_career_analysis.course_recommendations.elective_courses && (
                          <div>
                            <h4 className="text-lg font-semibold text-gray-900 mb-3">Elective Courses (6 Chosen)</h4>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                              {results.specific_career_analysis.course_recommendations.elective_courses.map((course, idx) => (
                                <CourseCard key={idx} course={course} type="elective" />
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CourseRecommendations;