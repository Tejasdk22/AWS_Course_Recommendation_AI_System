import json
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urlencode, quote_plus

def scrape_indeed_jobs(job_title, location="Dallas, TX", num_pages=3):
    """Scrape job postings from Indeed"""
    jobs = []
    
    for page in range(num_pages):
        try:
            # Indeed search URL
            params = {
                'q': job_title,
                'l': location,
                'start': page * 10
            }
            url = f"https://www.indeed.com/jobs?{urlencode(params)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for card in job_cards:
                try:
                    title_elem = card.find('h2', class_='jobTitle')
                    company_elem = card.find('span', class_='companyName')
                    location_elem = card.find('div', class_='companyLocation')
                    salary_elem = card.find('div', class_='salary-snippet')
                    description_elem = card.find('div', class_='job-snippet')
                    
                    if title_elem and company_elem:
                        job = {
                            'title': title_elem.get_text(strip=True),
                            'company': company_elem.get_text(strip=True),
                            'location': location_elem.get_text(strip=True) if location_elem else location,
                            'salary': salary_elem.get_text(strip=True) if salary_elem else 'Not specified',
                            'description': description_elem.get_text(strip=True) if description_elem else '',
                            'source': 'Indeed'
                        }
                        jobs.append(job)
                except Exception as e:
                    continue
            
            time.sleep(random.uniform(1, 3))  # Be respectful
            
        except Exception as e:
            print(f"Error scraping Indeed page {page}: {e}")
            continue
    
    return jobs

def scrape_linkedin_jobs(job_title, location="Dallas, TX", num_pages=2):
    """Scrape job postings from LinkedIn"""
    jobs = []
    
    for page in range(num_pages):
        try:
            # LinkedIn search URL
            params = {
                'keywords': job_title,
                'location': location,
                'start': page * 25
            }
            url = f"https://www.linkedin.com/jobs/search?{urlencode(params)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='base-card')
            
            for card in job_cards:
                try:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    location_elem = card.find('span', class_='job-search-card__location')
                    salary_elem = card.find('span', class_='job-search-card__salary-info')
                    
                    if title_elem and company_elem:
                        job = {
                            'title': title_elem.get_text(strip=True),
                            'company': company_elem.get_text(strip=True),
                            'location': location_elem.get_text(strip=True) if location_elem else location,
                            'salary': salary_elem.get_text(strip=True) if salary_elem else 'Not specified',
                            'description': '',
                            'source': 'LinkedIn'
                        }
                        jobs.append(job)
                except Exception as e:
                    continue
            
            time.sleep(random.uniform(2, 4))  # Be respectful
            
        except Exception as e:
            print(f"Error scraping LinkedIn page {page}: {e}")
            continue
    
    return jobs

def extract_skills_from_jobs(jobs):
    """Extract common skills from job descriptions"""
    skills = {}
    
    # Common data science skills to look for
    skill_keywords = [
        'Python', 'R', 'SQL', 'Java', 'Scala', 'JavaScript',
        'Machine Learning', 'Deep Learning', 'AI', 'Artificial Intelligence',
        'Statistics', 'Mathematics', 'Linear Algebra', 'Calculus',
        'Data Analysis', 'Data Mining', 'Data Visualization',
        'Tableau', 'Power BI', 'Matplotlib', 'Seaborn', 'Plotly',
        'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch',
        'Apache Spark', 'Hadoop', 'Kafka', 'AWS', 'Azure', 'GCP',
        'Docker', 'Kubernetes', 'Git', 'Linux', 'Unix',
        'Business Intelligence', 'ETL', 'Data Warehousing',
        'A/B Testing', 'Hypothesis Testing', 'Regression Analysis',
        'Time Series', 'Natural Language Processing', 'NLP',
        'Computer Vision', 'Neural Networks', 'Random Forest',
        'XGBoost', 'LightGBM', 'Clustering', 'Classification'
    ]
    
    for job in jobs:
        description = job.get('description', '').lower()
        title = job.get('title', '').lower()
        combined_text = f"{title} {description}"
        
        for skill in skill_keywords:
            if skill.lower() in combined_text:
                skills[skill] = skills.get(skill, 0) + 1
    
    # Sort by frequency
    sorted_skills = sorted(skills.items(), key=lambda x: x[1], reverse=True)
    return sorted_skills

def analyze_job_market(job_title, location="Dallas, TX"):
    """Analyze job market for a specific role"""
    
    print(f"🔍 Scraping job market data for: {job_title}")
    
    # Scrape from multiple sources
    indeed_jobs = scrape_indeed_jobs(job_title, location)
    linkedin_jobs = scrape_linkedin_jobs(job_title, location)
    
    # Combine all jobs
    all_jobs = indeed_jobs + linkedin_jobs
    
    # Extract skills
    skills_analysis = extract_skills_from_jobs(all_jobs)
    
    # Analyze salary ranges
    salaries = []
    for job in all_jobs:
        salary = job.get('salary', '')
        if salary and salary != 'Not specified':
            # Extract numeric values from salary strings
            import re
            numbers = re.findall(r'\$?[\d,]+', salary)
            if numbers:
                try:
                    # Convert to integer (remove commas and $)
                    salary_num = int(numbers[0].replace(',', '').replace('$', ''))
                    salaries.append(salary_num)
                except:
                    continue
    
    # Calculate salary statistics
    salary_stats = {}
    if salaries:
        salary_stats = {
            'min_salary': min(salaries),
            'max_salary': max(salaries),
            'avg_salary': sum(salaries) / len(salaries),
            'median_salary': sorted(salaries)[len(salaries)//2]
        }
    
    # Market analysis
    market_analysis = {
        'job_title': job_title,
        'location': location,
        'total_jobs_found': len(all_jobs),
        'indeed_jobs': len(indeed_jobs),
        'linkedin_jobs': len(linkedin_jobs),
        'top_skills': skills_analysis[:15],  # Top 15 skills
        'salary_statistics': salary_stats,
        'job_postings': all_jobs[:10],  # First 10 job postings
        'scraping_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return market_analysis

def lambda_handler(event, context):
    """Lambda handler for job market scraping"""
    
    try:
        # Extract job title from event
        job_title = event.get('job_title', 'Data Scientist')
        location = event.get('location', 'Dallas, TX')
        
        # Analyze job market
        market_data = analyze_job_market(job_title, location)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'market_analysis': market_data,
                'message': f'Successfully analyzed job market for {job_title}'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'success': False,
                'error': str(e),
                'message': 'Failed to analyze job market'
            })
        }

if __name__ == "__main__":
    # Test the scraper
    test_event = {
        'job_title': 'Data Scientist',
        'location': 'Dallas, TX'
    }
    
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))
