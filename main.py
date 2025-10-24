"""
Main application entry point for AWS Career Guidance AI System
"""

import asyncio
import sys
import os
from typing import Optional
import argparse
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from career_guidance_system import CareerGuidanceSystem, lambda_handler


async def interactive_mode():
    """Run the system in interactive mode for testing."""
    print("🤖 AWS Career Guidance AI System")
    print("=" * 50)
    print("Type 'quit' or 'exit' to stop the system")
    print("Type 'help' for available commands")
    print("=" * 50)
    
    system = CareerGuidanceSystem()
    
    while True:
        try:
            user_input = input("\n💬 Your career question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye! Good luck with your career journey!")
                break
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            if not user_input:
                print("❌ Please enter a question.")
                continue
            
            print("\n🔄 Processing your query...")
            response = await system.process_query(user_input)
            
            print(f"\n📊 Career Guidance Response:")
            print("=" * 50)
            print(response.unified_response)
            
            # Show additional details if requested
            show_details = input("\n❓ Show detailed breakdown? (y/n): ").strip().lower()
            if show_details in ['y', 'yes']:
                print_detailed_response(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Good luck with your career journey!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again or type 'help' for assistance.")


def print_help():
    """Print help information."""
    print("\n📚 Available Commands:")
    print("- Ask any career-related question")
    print("- 'help' - Show this help message")
    print("- 'quit', 'exit', 'q' - Exit the system")
    print("\n💡 Example Questions:")
    print("- 'I want to become a data scientist. What should I learn?'")
    print("- 'What are the most in-demand skills in tech right now?'")
    print("- 'I'm a beginner in programming. What projects should I start with?'")
    print("- 'What courses should I take to transition into machine learning?'")


def print_detailed_response(response):
    """Print detailed response breakdown."""
    print(f"\n📈 Detailed Analysis:")
    print("=" * 50)
    
    print(f"\n🏢 Job Market Insights:")
    print("-" * 30)
    print(response.job_market_insights)
    
    print(f"\n📚 Course Recommendations:")
    print("-" * 30)
    print(response.course_recommendations)
    
    print(f"\n🎯 Career Matching Analysis:")
    print("-" * 30)
    print(response.career_matching_analysis)
    
    print(f"\n🛠️ Project Suggestions:")
    print("-" * 30)
    print(response.project_suggestions)
    
    print(f"\n📝 Session Info:")
    print(f"Session ID: {response.session_id}")
    print(f"Timestamp: {response.timestamp}")


async def batch_mode(queries_file: str):
    """Run the system in batch mode with queries from a file."""
    try:
        with open(queries_file, 'r') as f:
            queries = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File {queries_file} not found")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in file {queries_file}")
        return
    
    if not isinstance(queries, list):
        print("❌ Error: Queries file should contain a list of questions")
        return
    
    print(f"🔄 Processing {len(queries)} queries in batch mode...")
    
    system = CareerGuidanceSystem()
    results = []
    
    for i, query in enumerate(queries, 1):
        print(f"\n📝 Processing query {i}/{len(queries)}: {query[:50]}...")
        
        try:
            response = await system.process_query(query)
            results.append({
                'query': query,
                'response': response.unified_response,
                'session_id': response.session_id,
                'timestamp': response.timestamp
            })
            print(f"✅ Query {i} completed")
        except Exception as e:
            print(f"❌ Query {i} failed: {e}")
            results.append({
                'query': query,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
    
    # Save results
    output_file = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Batch processing completed. Results saved to {output_file}")


def create_sample_queries_file():
    """Create a sample queries file for batch mode."""
    sample_queries = [
        "I want to become a data scientist. What should I learn?",
        "What are the most in-demand skills in tech right now?",
        "I'm a beginner in programming. What projects should I start with?",
        "What courses should I take to transition into machine learning?",
        "How can I build a strong portfolio for software engineering roles?",
        "What are the salary expectations for data analysts vs data scientists?",
        "I have a non-technical background. How can I break into tech?",
        "What are the best online platforms for learning programming?",
        "How important are certifications in the tech industry?",
        "What should I focus on to become a machine learning engineer?"
    ]
    
    with open('sample_queries.json', 'w') as f:
        json.dump(sample_queries, f, indent=2)
    
    print("✅ Sample queries file created: sample_queries.json")


async def test_mode():
    """Run the system in test mode with predefined queries."""
    print("🧪 Running Career Guidance System in Test Mode")
    print("=" * 50)
    
    system = CareerGuidanceSystem()
    
    test_queries = [
        "I want to become a data scientist. What should I learn?",
        "What are the most in-demand skills in tech right now?",
        "I'm a beginner in programming. What projects should I start with?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test Query {i}: {query}")
        print("-" * 50)
        
        try:
            response = await system.process_query(query)
            print(f"✅ Response generated successfully")
            print(f"Session ID: {response.session_id}")
            print(f"Response length: {len(response.unified_response)} characters")
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print(f"\n✅ Test mode completed")


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="AWS Career Guidance AI System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive mode
  python main.py --test             # Test mode
  python main.py --batch queries.json  # Batch mode
  python main.py --create-sample    # Create sample queries file
        """
    )
    
    parser.add_argument(
        '--mode', 
        choices=['interactive', 'test', 'batch'],
        default='interactive',
        help='Run mode (default: interactive)'
    )
    
    parser.add_argument(
        '--batch-file',
        type=str,
        help='JSON file with queries for batch mode'
    )
    
    parser.add_argument(
        '--create-sample',
        action='store_true',
        help='Create a sample queries file and exit'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run in test mode (same as --mode test)'
    )
    
    args = parser.parse_args()
    
    if args.create_sample:
        create_sample_queries_file()
        return
    
    if args.test or args.mode == 'test':
        asyncio.run(test_mode())
    elif args.mode == 'batch':
        if not args.batch_file:
            print("❌ Error: --batch-file is required for batch mode")
            return
        asyncio.run(batch_mode(args.batch_file))
    else:  # interactive mode
        asyncio.run(interactive_mode())


if __name__ == "__main__":
    main()
