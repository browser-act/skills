import os
import time
import json
import requests
import argparse
import sys

# ============ Configuration Area ============
# Template ID for Amazon Product API
TEMPLATE_ID = "77670107419143475"

# API configuration
API_BASE_URL = "https://api.browseract.com/v2/workflow"
POLL_INTERVAL = 5  # seconds
MAX_WAIT_TIME = 1800  # 30 minutes
# ============================================

def get_api_key():
    api_key = os.getenv("BROWSERACT_API_KEY")
    if not api_key:
        print("Error: BROWSERACT_API_KEY environment variable not set.", flush=True)
        sys.exit(1)
    return api_key

def run_task_by_template(api_key, keywords, brand, pages, lang):
    """Start a task using template"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    input_parameters = [
        {"name": "KeyWords", "value": keywords},
        {"name": "Brand", "value": brand},
        {"name": "Maximum_number_of_page_turns", "value": str(pages)},
        {"name": "language", "value": lang}
    ]
    
    data = {
        "workflow_template_id": TEMPLATE_ID,
        "input_parameters": input_parameters,
    }
    
    api_url = f"{API_BASE_URL}/run-task-by-template"
    try:
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            task_id = result.get("id")
            print(f"Task started, Task ID: {task_id}", flush=True)
            return task_id
        elif response.status_code == 401:
            print(f"Error: Invalid authorization. Please check your BROWSERACT_API_KEY.", flush=True)
            sys.exit(1)
        else:
            print(f"Failed to start task: {response.text}", flush=True)
            return None
    except Exception as e:
        print(f"Exception occurred: {str(e)}", flush=True)
        return None

def get_task_status(api_key, task_id):
    """Get task status"""
    headers = {"Authorization": f"Bearer {api_key}"}
    api_url = f"{API_BASE_URL}/get-task-status?task_id={task_id}"
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json().get("status")
        return None
    except:
        return None

def get_task_results(api_key, task_id):
    """Get detailed task results"""
    headers = {"Authorization": f"Bearer {api_key}"}
    api_url = f"{API_BASE_URL}/get-task?task_id={task_id}"
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Warning: Error fetching results: {str(e)}", flush=True)
        return None

def main():
    parser = argparse.ArgumentParser(description="Amazon Product API Skill Script")
    parser.add_argument("--keywords", required=True, help="Search keywords")
    parser.add_argument("--brand", default="Apple", help="Filter by brand")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages")
    parser.add_argument("--lang", default="en", help="Language")
    
    args = parser.parse_args()
    
    api_key = get_api_key()
    
    print(f"Initializing Amazon Product search for: '{args.keywords}' (Brand: {args.brand})", flush=True)
    
    task_id = run_task_by_template(api_key, args.keywords, args.brand, args.pages, args.lang)
    if not task_id:
        sys.exit(1)
        
    start_time = time.time()
    print(f"Waiting for task to complete...", flush=True)
    
    while True:
        if time.time() - start_time > MAX_WAIT_TIME:
            print("Error: Timeout reached.", flush=True)
            sys.exit(1)
            
        status = get_task_status(api_key, task_id)
        if status == "finished":
            print("\nTask completed!", flush=True)
            break
        elif status == "failed":
            print("\nTask failed.", flush=True)
            sys.exit(1)
        elif status == "canceled":
            print("\nTask canceled.", flush=True)
            sys.exit(1)
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Task Status: {status or 'unknown'}", flush=True)
            
        time.sleep(POLL_INTERVAL)
        
    results = get_task_results(api_key, task_id)
    if results:
        # According to standard, results should be printed to console
        print(json.dumps(results, indent=2, ensure_ascii=False), flush=True)
    else:
        print("Warning: No results found.", flush=True)

if __name__ == "__main__":
    main()
