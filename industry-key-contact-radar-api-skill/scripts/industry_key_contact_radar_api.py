import os
import time
import requests
import json
import sys
import datetime
import io

# Force UTF-8 encoding for standard output and error streams
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# API Configuration
TEMPLATE_ID = "88313898888855812"
API_BASE_URL = "https://api.browseract.com/v2/workflow"

def run_industry_key_contact_radar_task(api_key, industry, date_limit=10, site="facebook.com", job_title="founder"):
    """
    Starts an Industry Key Contact Radar task and polls for completion.
    
    Args:
        api_key (str): BrowserAct API Key
        industry (str): The industry or field to search for contacts
        date_limit (int): Maximum number of records to extract
        site (str): The social platform or website to search on
        job_title (str): The specific role or job title of the target contact
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "workflow_template_id": TEMPLATE_ID,
        "input_parameters": [
            {"name": "industry", "value": str(industry)},
            {"name": "Datelimit", "value": str(date_limit)},
            {"name": "site", "value": str(site)},
            {"name": "Job_Title", "value": str(job_title)}
        ]
    }

    # 1. Start Task
    print(f"Starting task via BrowserAct API...", flush=True)
    try:
        response = requests.post(
            f"{API_BASE_URL}/run-task-by-template",
            json=payload, headers=headers, timeout=30
        )
        res = response.json()
    except Exception as e:
        print(f"Error: Connection to API failed - {e}", flush=True)
        return None

    if "id" not in res:
        res_str = str(res)
        if "Invalid authorization" in res_str:
            print("Error: Invalid authorization. Please check your BrowserAct API Key.", flush=True)
        elif "concurrent" in res_str.lower() or "too many running tasks" in res_str.lower():
            print("Error: Concurrent task limit reached. Please upgrade your plan at https://www.browseract.com/reception/recharge", flush=True)
        else:
            print(f"Error: Could not start task. Response: {res}", flush=True)
        return None
    
    task_id = res["id"]
    print(f"Task started successfully. Task ID: {task_id}", flush=True)
    
    # 2. Poll for Completion
    print(f"Waiting for task completion...", flush=True)
    max_poll_time = 900
    poll_start = time.time()
    finished = False
    
    while time.time() - poll_start < max_poll_time:
        try:
            status_res = requests.get(
                f"{API_BASE_URL}/get-task-status?task_id={task_id}",
                headers=headers, timeout=30
            ).json()
            status = status_res.get("status")

            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Task Status: {status}", flush=True)

            if status == "finished":
                print(f"[{timestamp}] Task finished successfully.", flush=True)
                finished = True
                break
            elif status in ["failed", "canceled"]:
                print(f"Error: Task {status}. Please check your BrowserAct dashboard.", flush=True)
                return None
        except Exception as e:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Polling error: {e}. Retrying...", flush=True)
            
        time.sleep(10)

    if not finished:
        print(f"Error: Task polling timed out after {max_poll_time} seconds.", flush=True)
        return None

    # 3. Get Results
    print(f"Retrieving results...", flush=True)
    try:
        task_info_response = requests.get(
            f"{API_BASE_URL}/get-task?task_id={task_id}",
            headers=headers, timeout=30
        )
        task_info = task_info_response.json()
        
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
        print("Usage: python industry_key_contact_radar_api.py <industry> [date_limit] [site] [job_title]", flush=True)
        print("Example: python industry_key_contact_radar_api.py \"Browser automation\" 10 \"facebook.com\" \"founder\"", flush=True)
        sys.exit(1)
        
    if not api_key:
        print("\n[!] ERROR: BrowserAct API Key is missing.", flush=True)
        print("Please follow these steps:", flush=True)
        print("1. Go to: https://www.browseract.com/reception/integrations", flush=True)
        print("2. Copy your API Key.", flush=True)
        print("3. Set it as an environment variable (BROWSERACT_API_KEY) or provide it in the chat.", flush=True)
        sys.exit(1)
        
    industry = sys.argv[1]
    date_limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    site = sys.argv[3] if len(sys.argv) > 3 else "facebook.com"
    job_title = sys.argv[4] if len(sys.argv) > 4 else "founder"
    
    result = run_industry_key_contact_radar_task(api_key, industry, date_limit, site, job_title)
    if result:
        print(result, flush=True)
