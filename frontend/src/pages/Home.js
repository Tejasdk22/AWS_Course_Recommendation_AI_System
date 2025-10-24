import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Brain, Target, BookOpen, TrendingUp, Users, Award } from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Analysis',
      description: 'Get personalized course recommendations powered by advanced AI agents'
    },
    {
      icon: Target,
      title: 'Academic Planning',
      description: 'Plan your academic path based on your major and career goals'
    },
    {
      icon: BookOpen,
      title: 'Course Recommendations',
      description: 'Get tailored course suggestions for your academic journey'
    },
    {
      icon: TrendingUp,
      title: 'Curriculum Insights',
      description: 'Access course data and academic requirements information'
    },
    {
      icon: Users,
      title: 'Academic Guidance',
      description: 'Benefit from comprehensive course progression analysis'
    },
    {
      icon: Award,
      title: 'Skill Building',
      description: 'Get course recommendations to build your academic skills'
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 text-white">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              UTD Course Recommendation
              <span className="block text-primary-200">AI System</span>
            </h1>
            <p className="text-xl md:text-2xl text-primary-100 mb-8 max-w-3xl mx-auto">
              Get personalized course recommendations, academic planning, and curriculum guidance 
              powered by advanced AI agents designed specifically for UTD students.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/course-recommendations"
                className="inline-flex items-center px-8 py-4 bg-white text-primary-600 font-semibold rounded-lg hover:bg-primary-50 transition-colors duration-200 shadow-lg hover:shadow-xl"
              >
                Get Course Recommendations
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
              <Link
                to="/about"
                className="inline-flex items-center px-8 py-4 border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-primary-600 transition-colors duration-200"
              >
                Learn More
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Powered by Advanced AI Agents
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our system uses multiple specialized AI agents working together to provide 
              comprehensive career guidance tailored to your specific needs.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  className="card hover:shadow-lg transition-shadow duration-300 group"
                >
                  <div className="flex items-center mb-4">
                    <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center group-hover:bg-primary-200 transition-colors duration-200">
                      <Icon className="w-6 h-6 text-primary-600" />
                    </div>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our AI agents work together to provide you with comprehensive career guidance
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              { step: '1', title: 'Tell Us About Yourself', description: 'Share your major, student type, and career goals' },
              { step: '2', title: 'AI Agents Analyze', description: 'Multiple AI agents analyze job market and course data' },
              { step: '3', title: 'Get Recommendations', description: 'Receive personalized course and career recommendations' },
              { step: '4', title: 'Plan Your Future', description: 'Build your career path with detailed progression plans' }
            ].map((item, index) => (
              <div key={index} className="text-center">
                <div className="w-16 h-16 bg-primary-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {item.title}
                </h3>
                <p className="text-gray-600">
                  {item.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-600 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Plan Your Career?
          </h2>
          <p className="text-xl text-primary-100 mb-8">
            Get started with personalized career guidance today
          </p>
          <Link
            to="/course-recommendations"
            className="inline-flex items-center px-8 py-4 bg-white text-primary-600 font-semibold rounded-lg hover:bg-primary-50 transition-colors duration-200 shadow-lg hover:shadow-xl"
          >
            Start Your Academic Journey
            <ArrowRight className="ml-2 w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;