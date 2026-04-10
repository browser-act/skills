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
TEMPLATE_ID = "82163578680973165"
API_BASE_URL = "https://api.browseract.com/v2/workflow"

def run_youtube_video_task(api_key, channel_url, video_type="Popular"):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "workflow_template_id": TEMPLATE_ID,
        "input_parameters": [
            {"name": "YouTube_channel_url", "value": channel_url},
            {"name": "Video_type", "value": video_type}
        ]
    }

    # 1. Start Task
    print(f"Start Task", flush=True)
    try:
        res = requests.post(f"{API_BASE_URL}/run-task-by-template", json=payload, headers=headers, timeout=30).json()
    except Exception as e:
        print(f"Error: Connection to API failed - {e}", flush=True)
        return None

    if "id" not in res:
        print(f"Error: Could not start task. Response: {res}", flush=True)
        return None
    
    task_id = res["id"]
    print(f"Task started. ID: {task_id}", flush=True)
    
    # 2. Poll for Completion
    max_poll_time = 300
    poll_start = time.time()
    while time.time() - poll_start < max_poll_time:
        try:
            status_res = requests.get(f"{API_BASE_URL}/get-task-status?task_id={task_id}", headers=headers, timeout=30).json()
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
    else:
        print(f"Error: Task polling timed out after {max_poll_time} seconds.", flush=True)
        return None
    
    # 3. Get Results
    try:
        task_info = requests.get(f"{API_BASE_URL}/get-task?task_id={task_id}", headers=headers, timeout=30).json()
        
        # Extract data from output["string"] as requested
        # Usually task_info['output']['string'] contains the result
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
    # Prioritize command line API key, then environment variable
    api_key = os.getenv("BROWSERACT_API_KEY")
    
    if len(sys.argv) < 2:
        print("Usage: python youtube_video_api.py <channel_url> [video_type]", flush=True)
        sys.exit(1)
        
    if not api_key:
        print("\n[!] ERROR: BrowserAct API Key is missing.", flush=True)
        print("Please follow these steps:", flush=True)
        print("1. Go to: https://www.browseract.com/reception/integrations", flush=True)
        print("2. Copy your API Key.", flush=True)
        print("3. Provide it to me or set it as an environment variable (BROWSERACT_API_KEY).", flush=True)
        sys.exit(1)
        
    channel_url = sys.argv[1]
    video_type = sys.argv[2] if len(sys.argv) > 2 else "Popular"
    
    result = run_youtube_video_task(api_key, channel_url, video_type)
    if result:
        print(result, flush=True)