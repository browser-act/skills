import os
import time
import requests
import json
import sys

# API Configuration
TEMPLATE_ID = "77805072070738748"
API_BASE_URL = "https://api.browseract.com/v2/workflow"

def run_google_maps_task(api_key, keywords, language="en", country="us", max_dates=100):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "workflow_template_id": TEMPLATE_ID,
        "input_parameters": [
            {"name": "KeyWords", "value": keywords},
            {"name": "language", "value": language},
            {"name": "country", "value": country},
            {"name": "TargetURL", "value": "https://www.google.com/maps"},
            {"name": "max_dates", "value": str(max_dates)}
        ]
    }
    
    # 1. Start Task
    try:
        res = requests.post(f"{API_BASE_URL}/run-task-by-template", json=payload, headers=headers).json()
    except Exception as e:
        print(f"Error: Connection to API failed - {e}")
        return None

    if "id" not in res:
        print(f"Error: Could not start task. Response: {res}")
        return None
    
    task_id = res["id"]
    
    # 2. Poll for Completion
    while True:
        try:
            status_res = requests.get(f"{API_BASE_URL}/get-task-status?task_id={task_id}", headers=headers).json()
            status = status_res.get("status")
            
            if status == "finished":
                break
            elif status in ["failed", "canceled"]:
                print(f"Error: Task {status}. Please check your BrowserAct dashboard.")
                return None
        except Exception as e:
            # Silent retry on minor connection issues
            pass
            
        time.sleep(3)
    
    # 3. Get Results
    try:
        task_info = requests.get(f"{API_BASE_URL}/get-task?task_id={task_id}", headers=headers).json()
        
        # Extract data from output["string"] as requested
        output = task_info.get("output", {})
        result_string = output.get("string")
        
        if result_string:
            return result_string
        else:
            return json.dumps(task_info, ensure_ascii=False)
    except Exception as e:
        print(f"Error: Failed to retrieve results - {e}")
        return None

if __name__ == "__main__":
    # Prioritize command line API key, then environment variable
    api_key = os.getenv("BROWSERACT_API_KEY")
    
    if len(sys.argv) < 2:
        print("Usage: python google_maps_search_api.py <keywords> [language] [country] [max_dates]")
        sys.exit(1)
        
    if not api_key:
        print("\n[!] ERROR: BrowserAct API Key is missing.")
        print("Please follow these steps:")
        print("1. Go to: https://www.browseract.com/reception/integrations")
        print("2. Copy your API Key.")
        print("3. Provide it to me or set it as an environment variable (BROWSERACT_API_KEY).")
        sys.exit(1)
        
    keywords = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "en"
    country = sys.argv[3] if len(sys.argv) > 3 else "us"
    max_dates = sys.argv[4] if len(sys.argv) > 4 else 100
    
    result = run_google_maps_task(api_key, keywords, language, country, max_dates)
    if result:
        print(result)
