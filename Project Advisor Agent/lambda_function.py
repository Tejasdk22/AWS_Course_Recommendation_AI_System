import json
import boto3
import requests
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

# -------------------------------------
# CONFIGURATION
# -------------------------------------
BEDROCK_MODEL_ID = "arn:aws:bedrock:us-east-2:831981619381:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0"
bedrock = boto3.client("bedrock-runtime")

# -------------------------------------
# UTILITIES
# -------------------------------------

def search_duckduckgo(query, max_results=5):
    """Perform a DuckDuckGo search (free, no API key)."""
    try:
        url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json"
        r = requests.get(url, timeout=10)
        data = r.json()
        results = []
        for item in data.get("RelatedTopics", []):
            if isinstance(item, dict) and "Text" in item and "FirstURL" in item:
                results.append({"title": item["Text"], "url": item["FirstURL"]})
                if len(results) >= max_results:
                    break
        return results
    except Exception as e:
        print("DuckDuckGo error:", e)
        return []

def search_github_projects(role, max_results=5):
    """Fetch GitHub repositories for technical projects."""
    try:
        url = "https://api.github.com/search/repositories"
        params = {"q": f"{role} project", "sort": "stars", "order": "desc", "per_page": max_results}
        headers = {"Accept": "application/vnd.github.v3+json"}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        data = resp.json()
        return [
            {"title": i["name"], "url": i["html_url"], "description": i.get("description", "")}
            for i in data.get("items", [])
        ]
    except Exception as e:
        print("GitHub error:", e)
        return []

def search_forage_projects(role, max_results=5):
    """Scrape The Forage programs relevant to a role."""
    try:
        url = f"https://www.theforage.com/virtual-experience/search?query={quote(role)}"
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        results = []
        for line in resp.text.split("\n"):
            if "/virtual-experience/programs" in line and "href" in line:
                href = line.split('"')[1]
                if not href.startswith("http"):
                    href = "https://www.theforage.com" + href
                title = href.split("/")[-1].replace("-", " ").title()
                results.append({"title": title, "url": href})
                if len(results) >= max_results:
                    break
        return results
    except Exception as e:
        print("Forage error:", e)
        return []

# -------------------------------------
# ROLE CLASSIFIER
# -------------------------------------

def is_technical_role(role):
    tech_keywords = [
        "data", "engineer", "developer", "scientist", "analyst",
        "machine", "ai", "cloud", "software", "security", "devops",
        "it", "network", "database", "system"
    ]
    return any(k in role.lower() for k in tech_keywords)

# -------------------------------------
# PARALLEL CERTIFICATION SEARCH
# -------------------------------------

def get_live_certifications(role):
    """Parallel DuckDuckGo searches for certifications across tech and non-tech platforms."""
    base = [
        f"{role} certification site:coursera.org",
        f"{role} certification site:udemy.com",
        f"{role} certification site:linkedin.com/learning",
        f"{role} certification site:edx.org",
        f"{role} certification site:futurelearn.com",
        f"{role} certification site:harvard.edu",
    ]

    if is_technical_role(role):
        base += [
            f"{role} certification site:aws.amazon.com/certification",
            f"{role} certification site:learn.microsoft.com",
            f"{role} certification site:ibm.com/training",
            f"{role} certification site:databricks.com/learn",
            f"{role} certification site:snowflake.com/en/certifications",
            f"{role} certification site:education.oracle.com",
        ]
    else:
        base += [
            f"{role} certification site:hubspot.com/academy",
            f"{role} certification site:google.com/skillshop",
            f"{role} certification site:shrm.org",
            f"{role} certification site:pmi.org",
            f"{role} certification site:cfainstitute.org",
            f"{role} certification site:corporatefinanceinstitute.com",
        ]

    results = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(search_duckduckgo, q, 2) for q in base]
        for future in as_completed(futures):
            results += future.result()
    return results

# -------------------------------------
# PARALLEL PROJECT SEARCH
# -------------------------------------

def get_live_projects(role):
    """Parallel project sourcing for tech and non-tech roles."""
    tasks = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        if is_technical_role(role):
            tasks.append(executor.submit(search_github_projects, role, 3))
            tasks.append(executor.submit(search_duckduckgo, f"{role} project site:kaggle.com", 2))
            tasks.append(executor.submit(search_duckduckgo, f"{role} lab site:snowflake.com", 1))
            tasks.append(executor.submit(search_duckduckgo, f"{role} cloud lab site:oracle.com", 1))
        else:
            tasks.append(executor.submit(search_forage_projects, role, 4))
            tasks.append(executor.submit(search_duckduckgo, f"{role} case study site:slideshare.net", 2))
            tasks.append(executor.submit(search_duckduckgo, f"{role} project site:behance.net", 2))

        projects = []
        for f in as_completed(tasks):
            projects += f.result()
        return projects

# -------------------------------------
# PROMPT BUILDER
# -------------------------------------

def build_prompt(role, level, live_projects, live_certs):
    system = (
        "You are an AI career advisor that gives personalized project and certification recommendations "
        "based on real web data. Respond only in JSON format."
    )
    user = f"""
Role: {role}
Level: {level}

Live Projects:
{json.dumps(live_projects, indent=2)}

Live Certifications:
{json.dumps(live_certs, indent=2)}

Generate:
- 3 project ideas (title, objective, estimated_hours, key_skills)
- 3 certification suggestions (title, platform, focus_area)
Output strictly in JSON.
"""
    return {
        "anthropic_version": "bedrock-2023-05-31",
        "system": system,
        "messages": [{"role": "user", "content": [{"type": "text", "text": user}]}],
        "max_tokens": 1000,
        "temperature": 0.6,
    }

# -------------------------------------
# MAIN HANDLER
# -------------------------------------

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        role = body.get("role", "Business Analyst")
        level = body.get("student_level", "Undergraduate")

        # Fetch data in parallel
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_certs = executor.submit(get_live_certifications, role)
            future_projects = executor.submit(get_live_projects, role)
            live_certs = future_certs.result()
            live_projects = future_projects.result()

        # Call Bedrock
        payload = build_prompt(role, level, live_projects, live_certs)
        resp = bedrock.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(payload),
            accept="application/json",
            contentType="application/json",
        )

        raw = resp["body"].read().decode("utf-8")
        data = json.loads(raw)
        content = "".join([c["text"] for c in data.get("content", [])])
        ai_resp = json.loads(content)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "role": role,
                "level": level,
                "ai_summary": ai_resp,
                "live_certifications": live_certs,
                "live_projects": live_projects,
            }),
        }

    except Exception as e:
        print("Error:", e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
