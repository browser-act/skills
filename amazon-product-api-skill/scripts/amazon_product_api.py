import os
import time
import requests
import json
import sys
import datetime
import io

# Force UTF-8 encoding for standard output and error streams to handle multi-language content
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# API Configuration
# Amazon Product API Template ID
TEMPLATE_ID = "77670107419143475"
API_BASE_URL = "https://api.browseract.com/v2/workflow"

def run_amazon_product_task(api_key, keywords, brand="Apple", pages=1, language="en"):
    """
    Executes an Amazon Product search task via BrowserAct API.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "workflow_template_id": TEMPLATE_ID,
        "input_parameters": [
            {"name": "KeyWords", "value": keywords},
            {"name": "Brand", "value": brand},
            {"name": "Maximum_number_of_page_turns", "value": str(pages)},
            {"name": "language", "value": language}
        ]
    }

    # 1. Start Task
    print(f"Starting Amazon Product search task for keywords: {keywords}", flush=True)
    try:
        response = requests.post(f"{API_BASE_URL}/run-task-by-template", json=payload, headers=headers)
        res = response.json()
    except Exception as e:
        print(f"Error: Connection to API failed - {e}", flush=True)
        return None

    if "id" not in res:
        # Check for authorization error
        if "Invalid authorization" in str(res):
            print(f"Error: Invalid authorization. Please check your BrowserAct API Key.", flush=True)
        else:
            print(f"Error: Could not start task. Response: {res}", flush=True)
        return None
    
    task_id = res["id"]
    print(f"Task started. ID: {task_id}", flush=True)
    
    # 2. Poll for Completion
    while True:
        try:
            status_res = requests.get(f"{API_BASE_URL}/get-task-status?task_id={task_id}", headers=headers).json()
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
            print(f"[{timestamp}] Polling error: {e}. Retrying...", flush=True)
            
        time.sleep(10)
    
    # 3. Get Results
    try:
        task_info = requests.get(f"{API_BASE_URL}/get-task?task_id={task_id}", headers=headers).json()
        
        # Extract data from output["string"] or the whole result
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
    # Get API key from environment variable
    api_key = os.getenv("BROWSERACT_API_KEY")
    
    if len(sys.argv) < 2:
        print("Usage: python amazon_product_api.py <keywords> [brand] [pages] [language]", flush=True)
        sys.exit(1)
        
    if not api_key:
        print("\n[!] ERROR: BrowserAct API Key is missing.", flush=True)
        print("Please follow these steps:", flush=True)
        print("1. Go to: https://www.browseract.com/reception/integrations", flush=True)
        print("2. Copy your API Key.", flush=True)
        print("3. Set it as an environment variable (BROWSERACT_API_KEY) or provide it in the chat.", flush=True)
        sys.exit(1)
        
    keywords = sys.argv[1]
    brand = sys.argv[2] if len(sys.argv) > 2 else "Apple"
    pages = sys.argv[3] if len(sys.argv) > 3 else 1
    language = sys.argv[4] if len(sys.argv) > 4 else "en"
    
    result = run_amazon_product_task(api_key, keywords, brand, pages, language)
    if result:
        print(result, flush=True)
