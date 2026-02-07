import os
import time
import requests
import json
import sys
import datetime
import io

# Force UTF-8 encoding for standard output and error streams to ensure compatibility with Windows PowerShell
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# API Configuration
# TEMPLATE_ID extracted from official BrowserAct Google News API documentation
TEMPLATE_ID = "77638424152140851"
API_BASE_URL = "https://api.browseract.com/v2/workflow"

def run_google_news_task(api_key, keywords, date_range="past week", limit=30):
    """
    Executes a Google News scraping task via BrowserAct API.
    
    Args:
        api_key (str): BrowserAct API Key
        keywords (str): Search keywords
        date_range (str): Time range filter (any time, past hours, past 24 hours, past week, past year)
        limit (int): Maximum number of items to extract
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "workflow_template_id": TEMPLATE_ID,
        "input_parameters": [
            {"name": "Search_Keywords", "value": keywords},
            {"name": "Publish_date", "value": date_range},
            {"name": "Datelimit", "value": str(limit)}
        ]
    }

    # 1. Start Task
    print(f"Starting task via BrowserAct API...", flush=True)
    try:
        response = requests.post(f"{API_BASE_URL}/run-task-by-template", json=payload, headers=headers)
        res = response.json()
    except Exception as e:
        print(f"Error: Connection to API failed - {e}", flush=True)
        return None

    if response.status_code == 401 or (isinstance(res, dict) and "Invalid authorization" in str(res)):
        print(f"Error: Invalid authorization. Please check your BrowserAct API Key.", flush=True)
        return None

    if "id" not in res:
        print(f"Error: Could not start task. Response: {res}", flush=True)
        return None
    
    task_id = res["id"]
    print(f"Task started successfully. Task ID: {task_id}", flush=True)
    
    # 2. Poll for Completion
    print(f"Waiting for task completion...", flush=True)
    while True:
        try:
            status_response = requests.get(f"{API_BASE_URL}/get-task-status?task_id={task_id}", headers=headers)
            status_res = status_response.json()
            status = status_res.get("status")
            
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Task Status: {status}", flush=True)
            
            if status == "finished":
                print(f"[{timestamp}] Task finished successfully.", flush=True)
                break
            elif status in ["failed", "canceled"]:
                print(f"Error: Task {status}. Please check your BrowserAct dashboard.", flush=True)
                return None
        except Exception as e:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Polling error: {e}. Retrying in 10s...", flush=True)
            
        time.sleep(10)
    
    # 3. Get Results
    print(f"Retrieving results...", flush=True)
    try:
        task_info_response = requests.get(f"{API_BASE_URL}/get-task?task_id={task_id}", headers=headers)
        task_info = task_info_response.json()
        
        # Extract structured data from API response
        output = task_info.get("output", {})
        result_string = output.get("string")
        
        if result_string:
            return result_string
        else:
            return json.dumps(task_info, ensure_ascii=False)
    except Exception as e:
        print(f"Error: Failed to retrieve results - {e}", flush=True)
        return None

if __name__ == "__main__":
    # Get API Key from environment variable
    api_key = os.getenv("BROWSERACT_API_KEY")
    
    if len(sys.argv) < 2:
        print("Usage: python google_news_api.py <keywords> [date_range] [limit]", flush=True)
        print("Example: python google_news_api.py \"AI technology\" \"past 24 hours\" 10", flush=True)
        sys.exit(1)
        
    if not api_key:
        print("\n[!] ERROR: BrowserAct API Key is missing.", flush=True)
        print("Please follow these steps:", flush=True)
        print("1. Go to: https://www.browseract.com/reception/integrations", flush=True)
        print("2. Copy your API Key.", flush=True)
        print("3. Set it as an environment variable (BROWSERACT_API_KEY) or provide it in the chat.", flush=True)
        sys.exit(1)
        
    keywords = sys.argv[1]
    date_range = sys.argv[2] if len(sys.argv) > 2 else "past week"
    limit = sys.argv[3] if len(sys.argv) > 3 else 30
    
    result = run_google_news_task(api_key, keywords, date_range, limit)
    if result:
        # Final output for the Agent to process
        print(result, flush=True)
