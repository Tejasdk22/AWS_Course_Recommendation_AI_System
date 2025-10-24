"""
AWS Lambda function for EmailSchedulerAgent
Manages email notification frequency and scheduling
"""

import json
import boto3
from typing import Dict, Any, List
from datetime import datetime, timedelta
import time

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for EmailSchedulerAgent
    Manages email notification scheduling and frequency
    """
    
    try:
        # Extract scheduling data from event
        user_email = event.get('user_email', '')
        user_name = event.get('user_name', 'Student')
        notification_type = event.get('notification_type', 'job_alerts')
        frequency = event.get('frequency', 'weekly')
        session_id = event.get('sessionId', '')
        
        print(f"EmailSchedulerAgent processing {notification_type} with {frequency} frequency for: {user_email}")
        
        # Initialize agent
        agent = EmailSchedulerAgent()
        
        # Process scheduling request
        result = agent.schedule_notifications(user_email, user_name, notification_type, frequency)
        
        return {
            'statusCode': 200,
            'body': {
                'agent': 'EmailSchedulerAgent',
                'notification_type': notification_type,
                'frequency': frequency,
                'scheduling_result': result,
                'sessionId': session_id,
                'timestamp': datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        print(f"Error in EmailSchedulerAgent: {e}")
        return {
            'statusCode': 500,
            'body': {
                'error': str(e),
                'agent': 'EmailSchedulerAgent'
            }
        }

class EmailSchedulerAgent:
    """Email Scheduler Agent that manages notification frequency and scheduling"""
    
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = 'utd-career-guidance-email-schedule'
        self.table = self.dynamodb.Table(self.table_name)
        
    def schedule_notifications(self, user_email: str, user_name: str, 
                             notification_type: str, frequency: str) -> Dict[str, Any]:
        """Schedule notifications based on user preferences"""
        
        # Define frequency settings
        frequency_settings = self._get_frequency_settings()
        
        # Calculate next notification time
        next_notification = self._calculate_next_notification(frequency, notification_type)
        
        # Store user preferences
        user_preferences = {
            'user_email': user_email,
            'user_name': user_name,
            'notification_type': notification_type,
            'frequency': frequency,
            'next_notification': next_notification.isoformat(),
            'preferences': {
                'job_alerts': frequency_settings['job_alerts'],
                'course_reminders': frequency_settings['course_reminders'],
                'project_deadlines': frequency_settings['project_deadlines'],
                'market_updates': frequency_settings['market_updates']
            },
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Store in DynamoDB
        try:
            self.table.put_item(Item=user_preferences)
            print(f"✅ User preferences stored for {user_email}")
        except Exception as e:
            print(f"⚠️  Error storing preferences: {e}")
        
        # Generate scheduling summary
        scheduling_summary = self._generate_scheduling_summary(user_preferences)
        
        return {
            'user_email': user_email,
            'notification_type': notification_type,
            'frequency': frequency,
            'next_notification': next_notification.isoformat(),
            'scheduling_summary': scheduling_summary,
            'preferences_stored': True
        }
    
    def _get_frequency_settings(self) -> Dict[str, Dict[str, Any]]:
        """Get default frequency settings for different notification types"""
        
        return {
            'job_alerts': {
                'frequency': 'daily',
                'time': '09:00',
                'description': 'Daily job alerts every day at 9:00 AM',
                'enabled': True,
                'reason': 'Job market changes rapidly, new opportunities appear daily'
            },
            'course_reminders': {
                'frequency': 'on-demand',
                'description': 'Course reminders only when user requests them',
                'enabled': True,
                'reason': 'Course information is static, only send when user asks'
            },
            'project_deadlines': {
                'frequency': 'weekly',
                'day_of_week': 'friday',
                'time': '14:00',
                'description': 'Weekly project deadline reminders every Friday at 2:00 PM',
                'enabled': True,
                'reason': 'Helps students stay on track with portfolio building'
            },
            'market_updates': {
                'frequency': 'monthly',
                'day_of_month': 1,
                'time': '08:00',
                'description': 'Monthly market updates on the 1st of each month at 8:00 AM',
                'enabled': True,
                'reason': 'Market trends change slowly, monthly updates are sufficient'
            },
            'personalized_recommendations': {
                'frequency': 'on-demand',
                'description': 'Personalized recommendations only when user requests them',
                'enabled': True,
                'reason': 'User-driven, only send when user interacts with system'
            }
        }
    
    def _calculate_next_notification(self, frequency: str, notification_type: str) -> datetime:
        """Calculate next notification time based on frequency"""
        
        now = datetime.now()
        
        if frequency == 'daily':
            return now + timedelta(days=1)
        elif frequency == 'weekly':
            # Next Monday
            days_ahead = 0 - now.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return now + timedelta(days=days_ahead)
        elif frequency == 'bi-weekly':
            # Every other Monday
            days_ahead = 0 - now.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 14
            else:
                days_ahead += 7
            return now + timedelta(days=days_ahead)
        elif frequency == 'monthly':
            # First day of next month
            if now.month == 12:
                next_month = now.replace(year=now.year + 1, month=1, day=1)
            else:
                next_month = now.replace(month=now.month + 1, day=1)
            return next_month
        else:
            # Default to weekly
            days_ahead = 0 - now.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return now + timedelta(days=days_ahead)
    
    def _generate_scheduling_summary(self, user_preferences: Dict[str, Any]) -> str:
        """Generate a summary of the scheduling configuration"""
        
        notification_type = user_preferences['notification_type']
        frequency = user_preferences['frequency']
        next_notification = user_preferences['next_notification']
        
        summary = f"""
        📧 Email Notification Schedule Summary
        
        User: {user_preferences['user_name']} ({user_preferences['user_email']})
        Notification Type: {notification_type.replace('_', ' ').title()}
        Frequency: {frequency.title()}
        Next Notification: {next_notification}
        
        📅 Schedule Details:
        """
        
        # Add specific schedule details based on notification type
        if notification_type == 'job_alerts':
            summary += """
        • Job Alerts: DAILY (every day at 9:00 AM)
        • Content: New job postings matching your career goals
        • Sources: Indeed, LinkedIn, Glassdoor
        • Reason: Job market changes rapidly, new opportunities appear daily
        • Frequency: You can change this to weekly or monthly if preferred
        """
        elif notification_type == 'course_reminders':
            summary += """
        • Course Reminders: ON-DEMAND (only when you request them)
        • Content: Course registration deadlines and recommendations
        • Includes: Prerequisites, course sequencing, registration dates
        • Reason: Course information is static, only send when you ask
        • Frequency: Always on-demand based on your requests
        """
        elif notification_type == 'project_deadlines':
            summary += """
        • Project Deadlines: Weekly (every Friday at 2:00 PM)
        • Content: Portfolio project reminders and new project suggestions
        • Includes: Project timelines, skill development goals
        • Reason: Helps you stay on track with portfolio building
        • Frequency: You can change this to bi-weekly or monthly
        """
        elif notification_type == 'market_updates':
            summary += """
        • Market Updates: Monthly (1st of each month at 8:00 AM)
        • Content: Job market trends and salary insights
        • Includes: Skill demand analysis, industry updates
        • Reason: Market trends change slowly, monthly updates are sufficient
        • Frequency: You can change this to weekly or bi-weekly
        """
        elif notification_type == 'personalized_recommendations':
            summary += """
        • Personalized Recommendations: ON-DEMAND (only when you request them)
        • Content: Tailored course and project recommendations
        • Includes: Career guidance, skill gap analysis, next steps
        • Reason: User-driven, only send when you interact with system
        • Frequency: Always on-demand based on your requests
        """
        
        summary += f"""
        
        🔧 Customization Options:
        • Change frequency: daily, weekly, bi-weekly, monthly
        • Pause notifications: Set frequency to 'disabled'
        • Update preferences: Contact career-guidance@utdallas.edu
        
        📱 To modify your preferences, reply to any email or visit the UTD Career Guidance portal.
        """
        
        return summary
    
    def get_user_schedule(self, user_email: str) -> Dict[str, Any]:
        """Get user's current email schedule"""
        
        try:
            response = self.table.get_item(Key={'user_email': user_email})
            if 'Item' in response:
                return response['Item']
            else:
                return {'error': 'User schedule not found'}
        except Exception as e:
            return {'error': str(e)}
    
    def update_user_schedule(self, user_email: str, new_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Update user's email schedule preferences"""
        
        try:
            # Get current preferences
            current = self.get_user_schedule(user_email)
            if 'error' in current:
                return current
            
            # Update preferences
            updated_preferences = current.copy()
            updated_preferences.update(new_preferences)
            updated_preferences['updated_at'] = datetime.now().isoformat()
            
            # Recalculate next notification
            next_notification = self._calculate_next_notification(
                updated_preferences['frequency'], 
                updated_preferences['notification_type']
            )
            updated_preferences['next_notification'] = next_notification.isoformat()
            
            # Store updated preferences
            self.table.put_item(Item=updated_preferences)
            
            return {
                'success': True,
                'updated_preferences': updated_preferences,
                'message': 'Schedule updated successfully'
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_due_notifications(self) -> List[Dict[str, Any]]:
        """Get all notifications that are due to be sent"""
        
        try:
            # Scan table for due notifications
            response = self.table.scan()
            due_notifications = []
            
            current_time = datetime.now()
            
            for item in response['Items']:
                next_notification = datetime.fromisoformat(item['next_notification'])
                
                if next_notification <= current_time:
                    due_notifications.append(item)
            
            return due_notifications
            
        except Exception as e:
            print(f"Error getting due notifications: {e}")
            return []

if __name__ == "__main__":
    # Test the agent
    test_event = {
        'user_email': 'test@utdallas.edu',
        'user_name': 'John Doe',
        'notification_type': 'job_alerts',
        'frequency': 'weekly',
        'sessionId': 'test123'
    }
    
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))
