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
SINGLE_TEMPLATE_ID = "87197468034420377"
BATCH_TEMPLATE_ID = "87198942474882969"
API_BASE_URL = "https://api.browseract.com/v2/workflow"


def run_single_video_task(api_key, target_url):
    """
    Starts a single YouTube video transcript extraction task and polls for completion.
    Returns the transcript and metadata as a string, or None on failure.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "workflow_template_id": SINGLE_TEMPLATE_ID,
        "input_parameters": [
            {"name": "TargetURL", "value": target_url}
        ]
    }

    # 1. Start Task
    print(f"[Single Mode] Starting transcript extraction for: {target_url}", flush=True)
    try:
        res = requests.post(
            f"{API_BASE_URL}/run-task-by-template",
            json=payload, headers=headers, timeout=30
        ).json()
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
    print(f"Task started. ID: {task_id}", flush=True)

    # 2. Poll for Completion
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
    try:
        task_info = requests.get(
            f"{API_BASE_URL}/get-task?task_id={task_id}",
            headers=headers, timeout=30
        ).json()

        output = task_info.get("output", {})
        result_string = output.get("string")

        if result_string:
            return result_string
        else:
            return json.dumps(task_info, ensure_ascii=False)
    except Exception as e:
        print(f"Error: Failed to retrieve results - {e}", flush=True)
        return None


def run_batch_video_task(api_key, keywords, upload_date="This week", limit=3):
    """
    Starts a batch YouTube video transcript extraction task and polls for completion.
    Returns transcripts and metadata for multiple videos as a string, or None on failure.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "workflow_template_id": BATCH_TEMPLATE_ID,
        "input_parameters": [
            {"name": "KeyWords", "value": keywords},
            {"name": "Upload_date", "value": upload_date},
            {"name": "Datelimit", "value": str(limit)}
        ]
    }

    # 1. Start Task
    print(f"[Batch Mode] Searching for '{keywords}' | Upload date: {upload_date} | Limit: {limit}", flush=True)
    try:
        res = requests.post(
            f"{API_BASE_URL}/run-task-by-template",
            json=payload, headers=headers, timeout=30
        ).json()
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
    print(f"Task started. ID: {task_id}", flush=True)

    # 2. Poll for Completion
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
    try:
        task_info = requests.get(
            f"{API_BASE_URL}/get-task?task_id={task_id}",
            headers=headers, timeout=30
        ).json()

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
    if len(sys.argv) < 3:
        print("Usage:", flush=True)
        print("  Single video:  python youtube_transcript_analysis_api.py single \"<YouTube_URL>\"", flush=True)
        print("  Batch videos:  python youtube_transcript_analysis_api.py batch \"<keywords>\" [upload_date] [limit]", flush=True)
        sys.exit(1)

    api_key = os.getenv("BROWSERACT_API_KEY")
    if not api_key:
        print("\n[!] ERROR: BrowserAct API Key is missing.", flush=True)
        print("Please follow these steps:", flush=True)
        print("1. Go to: https://www.browseract.com/reception/integrations", flush=True)
        print("2. Copy your API Key.", flush=True)
        print("3. Provide it to me or set it as an environment variable (BROWSERACT_API_KEY).", flush=True)
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "single":
        target_url = sys.argv[2]
        result = run_single_video_task(api_key, target_url)
        if result:
            print("\n" + "=" * 60, flush=True)
            print("TRANSCRIPT EXTRACTION RESULT", flush=True)
            print("=" * 60, flush=True)
            print(result, flush=True)
            print("\n" + "=" * 60, flush=True)
            print("EXTRACTION COMPLETE — Agent should now perform a concise, bullet-point 8-dimension analysis on the transcript without outputting the full raw text.", flush=True)
            print("=" * 60, flush=True)

    elif mode == "batch":
        keywords = sys.argv[2]
        upload_date = sys.argv[3] if len(sys.argv) > 3 else "This week"
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 3
        result = run_batch_video_task(api_key, keywords, upload_date, limit)
        if result:
            print("\n" + "=" * 60, flush=True)
            print("BATCH TRANSCRIPT EXTRACTION RESULT", flush=True)
            print("=" * 60, flush=True)
            print(result, flush=True)
            print("\n" + "=" * 60, flush=True)
            print("EXTRACTION COMPLETE — Agent should now perform a concise, bullet-point 8-dimension analysis on each transcript without outputting the full raw text.", flush=True)
            print("=" * 60, flush=True)

    else:
        print(f"Error: Unknown mode '{mode}'. Use 'single' or 'batch'.", flush=True)
        sys.exit(1)
