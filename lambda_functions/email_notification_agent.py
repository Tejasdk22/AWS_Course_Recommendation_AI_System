"""
AWS Lambda function for EmailNotificationAgent
Sends personalized email notifications to users
"""

import json
import boto3
from typing import Dict, Any, List
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for EmailNotificationAgent
    Sends personalized email notifications to users
    """
    
    try:
        # Extract email data from event
        user_email = event.get('user_email', '')
        user_name = event.get('user_name', 'Student')
        recommendations = event.get('recommendations', {})
        email_type = event.get('email_type', 'recommendation_summary')
        session_id = event.get('sessionId', '')
        
        print(f"EmailNotificationAgent sending {email_type} to: {user_email}")
        
        # Initialize agent
        agent = EmailNotificationAgent()
        
        # Send email
        email_result = agent.send_notification_email(
            user_email, user_name, recommendations, email_type
        )
        
        return {
            'statusCode': 200,
            'body': {
                'agent': 'EmailNotificationAgent',
                'email_sent': email_result['success'],
                'email_type': email_type,
                'recipient': user_email,
                'sessionId': session_id,
                'timestamp': datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        print(f"Error in EmailNotificationAgent: {e}")
        return {
            'statusCode': 500,
            'body': {
                'error': str(e),
                'agent': 'EmailNotificationAgent'
            }
        }

class EmailNotificationAgent:
    """Email Notification Agent that sends personalized emails to users"""
    
    def __init__(self):
        self.ses_client = boto3.client('ses', region_name='us-east-1')
        self.sender_email = 'noreply@utd-career-guidance.com'
        
    def send_notification_email(self, user_email: str, user_name: str, 
                              recommendations: Dict[str, Any], email_type: str) -> Dict[str, Any]:
        """Send personalized notification email"""
        
        try:
            # Generate email content based on type
            email_content = self._generate_email_content(user_name, recommendations, email_type)
            
            # Send email using SES
            response = self.ses_client.send_email(
                Source=self.sender_email,
                Destination={'ToAddresses': [user_email]},
                Message={
                    'Subject': {'Data': email_content['subject']},
                    'Body': {
                        'Html': {'Data': email_content['html_body']},
                        'Text': {'Data': email_content['text_body']}
                    }
                }
            )
            
            return {
                'success': True,
                'message_id': response['MessageId'],
                'email_type': email_type
            }
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return {
                'success': False,
                'error': str(e),
                'email_type': email_type
            }
    
    def _generate_email_content(self, user_name: str, recommendations: Dict[str, Any], email_type: str) -> Dict[str, str]:
        """Generate email content based on type and recommendations"""
        
        if email_type == 'recommendation_summary':
            return self._generate_recommendation_summary_email(user_name, recommendations)
        elif email_type == 'course_reminder':
            return self._generate_course_reminder_email(user_name, recommendations)
        elif email_type == 'job_opportunity':
            return self._generate_job_opportunity_email(user_name, recommendations)
        elif email_type == 'project_deadline':
            return self._generate_project_deadline_email(user_name, recommendations)
        else:
            return self._generate_general_notification_email(user_name, recommendations)
    
    def _generate_recommendation_summary_email(self, user_name: str, recommendations: Dict[str, Any]) -> Dict[str, str]:
        """Generate recommendation summary email"""
        
        subject = f"🎓 Your Personalized Career Guidance Summary - {user_name}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">🎓 UTD Career Guidance - Your Personalized Summary</h2>
                
                <p>Dear {user_name},</p>
                
                <p>Thank you for using the UTD Career Guidance AI System! Here's your personalized career guidance summary:</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2c3e50;">📚 Course Recommendations</h3>
                    <ul>
                        <li><strong>Career Path:</strong> {recommendations.get('career_path', 'Data Scientist')}</li>
                        <li><strong>Total Courses:</strong> {recommendations.get('total_courses', '40-43 courses')}</li>
                        <li><strong>Key Skills Needed:</strong> {', '.join(recommendations.get('key_skills_needed', [])[:5])}</li>
                    </ul>
                </div>
                
                <div style="background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2c3e50;">🚀 Next Steps</h3>
                    <ul>
                        <li>Review your course recommendations</li>
                        <li>Register for recommended courses</li>
                        <li>Start working on suggested projects</li>
                        <li>Build your professional portfolio</li>
                    </ul>
                </div>
                
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2c3e50;">📅 Important Dates</h3>
                    <ul>
                        <li><strong>Course Registration:</strong> Check UTD course catalog for registration dates</li>
                        <li><strong>Project Deadlines:</strong> Set personal deadlines for portfolio projects</li>
                        <li><strong>Career Fair:</strong> UTD Career Fair - Check UTD events calendar</li>
                    </ul>
                </div>
                
                <p>Best regards,<br>
                UTD Career Guidance AI System</p>
                
                <hr style="margin: 30px 0;">
                <p style="font-size: 12px; color: #666;">
                    This email was generated by the UTD Career Guidance AI System. 
                    For questions, contact career-guidance@utdallas.edu
                </p>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        UTD Career Guidance - Your Personalized Summary
        
        Dear {user_name},
        
        Thank you for using the UTD Career Guidance AI System! Here's your personalized career guidance summary:
        
        Course Recommendations:
        - Career Path: {recommendations.get('career_path', 'Data Scientist')}
        - Total Courses: {recommendations.get('total_courses', '40-43 courses')}
        - Key Skills Needed: {', '.join(recommendations.get('key_skills_needed', [])[:5])}
        
        Next Steps:
        - Review your course recommendations
        - Register for recommended courses
        - Start working on suggested projects
        - Build your professional portfolio
        
        Best regards,
        UTD Career Guidance AI System
        """
        
        return {
            'subject': subject,
            'html_body': html_body,
            'text_body': text_body
        }
    
    def _generate_course_reminder_email(self, user_name: str, recommendations: Dict[str, Any]) -> Dict[str, str]:
        """Generate course registration reminder email"""
        
        subject = f"📚 Course Registration Reminder - {user_name}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">📚 Course Registration Reminder</h2>
                
                <p>Dear {user_name},</p>
                
                <p>Don't forget to register for your recommended courses! Here's a reminder of your personalized course plan:</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2c3e50;">🎯 Recommended Courses</h3>
                    <ul>
                        <li>Check UTD course catalog for availability</li>
                        <li>Register for courses that align with your career goals</li>
                        <li>Consider prerequisites and course sequencing</li>
                    </ul>
                </div>
                
                <div style="background-color: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2c3e50;">⏰ Registration Deadlines</h3>
                    <ul>
                        <li><strong>Priority Registration:</strong> Check your UTD account for your registration time</li>
                        <li><strong>Regular Registration:</strong> Open registration period</li>
                        <li><strong>Late Registration:</strong> Additional fees may apply</li>
                    </ul>
                </div>
                
                <p>Best regards,<br>
                UTD Career Guidance AI System</p>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        Course Registration Reminder
        
        Dear {user_name},
        
        Don't forget to register for your recommended courses! Here's a reminder of your personalized course plan.
        
        Recommended Courses:
        - Check UTD course catalog for availability
        - Register for courses that align with your career goals
        - Consider prerequisites and course sequencing
        
        Registration Deadlines:
        - Priority Registration: Check your UTD account for your registration time
        - Regular Registration: Open registration period
        - Late Registration: Additional fees may apply
        
        Best regards,
        UTD Career Guidance AI System
        """
        
        return {
            'subject': subject,
            'html_body': html_body,
            'text_body': text_body
        }
    
    def _generate_job_opportunity_email(self, user_name: str, recommendations: Dict[str, Any]) -> Dict[str, str]:
        """Generate job opportunity notification email"""
        
        subject = f"💼 New Job Opportunities - {user_name}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">💼 New Job Opportunities</h2>
                
                <p>Dear {user_name},</p>
                
                <p>We found new job opportunities that match your career goals! Here are some positions you might be interested in:</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2c3e50;">🎯 Matching Positions</h3>
                    <ul>
                        <li>Check Indeed, LinkedIn, and Glassdoor for current openings</li>
                        <li>Look for positions that match your skill set</li>
                        <li>Consider internships and entry-level positions</li>
                    </ul>
                </div>
                
                <div style="background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2c3e50;">📈 Market Trends</h3>
                    <ul>
                        <li>Data Science roles are in high demand</li>
                        <li>Python and SQL skills are most requested</li>
                        <li>Remote work opportunities are increasing</li>
                    </ul>
                </div>
                
                <p>Best regards,<br>
                UTD Career Guidance AI System</p>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        New Job Opportunities
        
        Dear {user_name},
        
        We found new job opportunities that match your career goals! Here are some positions you might be interested in.
        
        Matching Positions:
        - Check Indeed, LinkedIn, and Glassdoor for current openings
        - Look for positions that match your skill set
        - Consider internships and entry-level positions
        
        Market Trends:
        - Data Science roles are in high demand
        - Python and SQL skills are most requested
        - Remote work opportunities are increasing
        
        Best regards,
        UTD Career Guidance AI System
        """
        
        return {
            'subject': subject,
            'html_body': html_body,
            'text_body': text_body
        }
    
    def _generate_project_deadline_email(self, user_name: str, recommendations: Dict[str, Any]) -> Dict[str, str]:
        """Generate project deadline reminder email"""
        
        subject = f"🚀 Project Deadline Reminder - {user_name}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">🚀 Project Deadline Reminder</h2>
                
                <p>Dear {user_name},</p>
                
                <p>Don't forget about your portfolio projects! Here's a reminder of your recommended projects:</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2c3e50;">📋 Recommended Projects</h3>
                    <ul>
                        <li>Build a data analysis dashboard</li>
                        <li>Create a machine learning model</li>
                        <li>Develop a web application</li>
                        <li>Contribute to open source projects</li>
                    </ul>
                </div>
                
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2c3e50;">⏰ Project Timeline</h3>
                    <ul>
                        <li><strong>Week 1-2:</strong> Project planning and setup</li>
                        <li><strong>Week 3-4:</strong> Development and implementation</li>
                        <li><strong>Week 5-6:</strong> Testing and documentation</li>
                        <li><strong>Week 7-8:</strong> Portfolio presentation</li>
                    </ul>
                </div>
                
                <p>Best regards,<br>
                UTD Career Guidance AI System</p>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        Project Deadline Reminder
        
        Dear {user_name},
        
        Don't forget about your portfolio projects! Here's a reminder of your recommended projects.
        
        Recommended Projects:
        - Build a data analysis dashboard
        - Create a machine learning model
        - Develop a web application
        - Contribute to open source projects
        
        Project Timeline:
        - Week 1-2: Project planning and setup
        - Week 3-4: Development and implementation
        - Week 5-6: Testing and documentation
        - Week 7-8: Portfolio presentation
        
        Best regards,
        UTD Career Guidance AI System
        """
        
        return {
            'subject': subject,
            'html_body': html_body,
            'text_body': text_body
        }
    
    def _generate_general_notification_email(self, user_name: str, recommendations: Dict[str, Any]) -> Dict[str, str]:
        """Generate general notification email"""
        
        subject = f"📧 UTD Career Guidance Update - {user_name}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">📧 UTD Career Guidance Update</h2>
                
                <p>Dear {user_name},</p>
                
                <p>Here's an update from your UTD Career Guidance AI System:</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2c3e50;">📚 Latest Updates</h3>
                    <ul>
                        <li>New course recommendations available</li>
                        <li>Updated job market analysis</li>
                        <li>Fresh project ideas and resources</li>
                    </ul>
                </div>
                
                <p>Best regards,<br>
                UTD Career Guidance AI System</p>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        UTD Career Guidance Update
        
        Dear {user_name},
        
        Here's an update from your UTD Career Guidance AI System:
        
        Latest Updates:
        - New course recommendations available
        - Updated job market analysis
        - Fresh project ideas and resources
        
        Best regards,
        UTD Career Guidance AI System
        """
        
        return {
            'subject': subject,
            'html_body': html_body,
            'text_body': text_body
        }

if __name__ == "__main__":
    # Test the agent
    test_event = {
        'user_email': 'test@utdallas.edu',
        'user_name': 'John Doe',
        'recommendations': {
            'career_path': 'Data Scientist',
            'total_courses': '40-43 courses',
            'key_skills_needed': ['Python', 'Machine Learning', 'Statistics']
        },
        'email_type': 'recommendation_summary',
        'sessionId': 'test123'
    }
    
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))
