import React from 'react';
import { Brain, Target, BookOpen, TrendingUp, Users, Award, CheckCircle, ArrowRight } from 'lucide-react';

const About = () => {
  const agents = [
    {
      name: 'Job Market Agent',
      description: 'Scrapes real-time job postings from LinkedIn, Indeed, and Glassdoor to analyze current market demands, salary trends, and required skills.',
      icon: TrendingUp,
      features: ['Real-time job market data', 'Salary analysis', 'Skill demand trends', 'Industry insights']
    },
    {
      name: 'Course Catalog Agent',
      description: 'Analyzes UTD course catalogs to extract skills, prerequisites, and career relevance for each course.',
      icon: BookOpen,
      features: ['Course skill mapping', 'Prerequisite analysis', 'Career relevance scoring', 'Curriculum optimization']
    },
    {
      name: 'Career Matching Agent',
      description: 'Matches your career goals with market demands and available courses to provide personalized recommendations.',
      icon: Target,
      features: ['Career path analysis', 'Skill gap identification', 'Personalized matching', 'Progression planning']
    },
    {
      name: 'Project Advisor Agent',
      description: 'Suggests hands-on projects from Kaggle, GitHub, and other platforms to build your portfolio and practical skills.',
      icon: Award,
      features: ['Portfolio projects', 'Skill building', 'Real-world experience', 'Career preparation']
    }
  ];

  const features = [
    {
      title: 'AI-Powered Analysis',
      description: 'Advanced AI agents work together to provide comprehensive career guidance',
      icon: Brain
    },
    {
      title: 'Real-Time Market Data',
      description: 'Access current job market trends, salary information, and skill demands',
      icon: TrendingUp
    },
    {
      title: 'Personalized Recommendations',
      description: 'Get course and career recommendations tailored to your major and goals',
      icon: Target
    },
    {
      title: 'Comprehensive Guidance',
      description: 'Complete career progression analysis from entry-level to senior positions',
      icon: Users
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              About UTD Course Recommendation AI
            </h1>
            <p className="text-xl md:text-2xl text-primary-100 max-w-3xl mx-auto">
              A comprehensive AI-powered course recommendation system designed specifically 
              for UTD students to make informed academic decisions.
            </p>
          </div>
        </div>
      </section>

      {/* System Overview */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How Our AI System Works
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our system uses multiple specialized AI agents that work together to provide 
              comprehensive career guidance tailored to your specific needs.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={index} className="text-center">
                  <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-8 h-8 text-primary-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
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

      {/* AI Agents Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Our AI Agents
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Four specialized AI agents work together to provide comprehensive career guidance
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {agents.map((agent, index) => {
              const Icon = agent.icon;
              return (
                <div key={index} className="card hover:shadow-lg transition-shadow duration-300">
                  <div className="flex items-start mb-4">
                    <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
                      <Icon className="w-6 h-6 text-primary-600" />
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">
                        {agent.name}
                      </h3>
                      <p className="text-gray-600 mb-4">
                        {agent.description}
                      </p>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Key Features:</h4>
                    <ul className="space-y-1">
                      {agent.features.map((feature, idx) => (
                        <li key={idx} className="flex items-center text-sm text-gray-600">
                          <CheckCircle className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Technology Stack
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built with cutting-edge AI and cloud technologies
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Brain className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">AI & Machine Learning</h3>
              <ul className="text-gray-600 space-y-1">
                <li>• AWS Bedrock AgentCore</li>
                <li>• Claude 3.5 Sonnet</li>
                <li>• Amazon Titan Models</li>
                <li>• Vector Databases</li>
              </ul>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Cloud Infrastructure</h3>
              <ul className="text-gray-600 space-y-1">
                <li>• AWS Lambda Functions</li>
                <li>• Amazon S3 Storage</li>
                <li>• DynamoDB Database</li>
                <li>• API Gateway</li>
              </ul>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <BookOpen className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Data Processing</h3>
              <ul className="text-gray-600 space-y-1">
                <li>• Web Scraping</li>
                <li>• Data Analysis</li>
                <li>• Real-time Processing</li>
                <li>• Knowledge Bases</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose Our System?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Get personalized, data-driven career guidance that adapts to your specific needs
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: 'Personalized Guidance',
                description: 'Get recommendations tailored to your major, student type, and career goals',
                icon: Target
              },
              {
                title: 'Real-Time Data',
                description: 'Access current job market trends and salary information',
                icon: TrendingUp
              },
              {
                title: 'Comprehensive Analysis',
                description: 'Complete career progression from entry-level to senior positions',
                icon: Users
              },
              {
                title: 'Course Optimization',
                description: 'Get the most relevant courses for your career path',
                icon: BookOpen
              },
              {
                title: 'Portfolio Building',
                description: 'Hands-on projects to build your skills and portfolio',
                icon: Award
              },
              {
                title: 'AI-Powered Insights',
                description: 'Advanced AI analysis of your career potential and opportunities',
                icon: Brain
              }
            ].map((benefit, index) => {
              const Icon = benefit.icon;
              return (
                <div key={index} className="card hover:shadow-lg transition-shadow duration-300">
                  <div className="flex items-center mb-4">
                    <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mr-4">
                      <Icon className="w-6 h-6 text-primary-600" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {benefit.title}
                    </h3>
                  </div>
                  <p className="text-gray-600">
                    {benefit.description}
                  </p>
                </div>
              );
            })}
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
          <a
            href="/career-guidance"
            className="inline-flex items-center px-8 py-4 bg-white text-primary-600 font-semibold rounded-lg hover:bg-primary-50 transition-colors duration-200 shadow-lg hover:shadow-xl"
          >
            Start Your Career Journey
            <ArrowRight className="ml-2 w-5 h-5" />
          </a>
        </div>
      </section>
    </div>
  );
};

export default About;