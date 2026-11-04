import os
import time
import requests
import json
import sys
import datetime
import argparse
import re
from urllib.parse import urlparse

# Force UTF-8 encoding for standard output and error streams
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# API Configuration
TEMPLATE_ID = "84396171023358338"
API_BASE_URL = "https://api.browseract.com/v2/workflow"

def build_payload(keywords, limit, publication_date="-"):
    if not isinstance(keywords, str) or not keywords.strip():
        raise ValueError("A non-empty keyword is required")
    if isinstance(limit, bool) or int(limit) != limit or int(limit) < 1:
        raise ValueError("A positive integer limit is required")
    date = str(publication_date or "").strip()
    if not date or date.casefold() in {"不限", "all", "any", "unrestricted"}:
        date = "-"
    return {"workflow_template_id": TEMPLATE_ID, "input_parameters": [
        {"name": "keywords", "value": keywords.strip()},
        {"name": "Date_limit", "value": str(int(limit))},
        {"name": "publication_date", "value": date},
    ]}


def run_wechat_article_search_task(api_key, keywords, limit=10, publication_date="-", task_id=None, max_poll_time=1800):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = build_payload(keywords, limit, publication_date)

    # Start once, or observe an already-created task without another POST.
    if task_id is None:
        print("Start Task", file=sys.stderr, flush=True)
        try:
            response = requests.post(f"{API_BASE_URL}/run-task-by-template", json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            res = response.json()
        except (requests.RequestException, ValueError) as exc:
            print(f"Error: Task creation is unconfirmed ({type(exc).__name__}). Do not automatically resubmit.", file=sys.stderr, flush=True)
            return None
        task_id = res.get("id")
        if not task_id:
            print("Error: No task ID returned. Do not automatically resubmit.", file=sys.stderr, flush=True)
            return None
        print(f"Task started. ID: {task_id}", file=sys.stderr, flush=True)
    else:
        print(f"Observing existing task. ID: {task_id}", file=sys.stderr, flush=True)

    # 2. Poll for Completion
    poll_start = time.monotonic()
    while time.monotonic() - poll_start < max_poll_time:
        try:
            response = requests.get(f"{API_BASE_URL}/get-task-status", params={"task_id": task_id}, headers=headers, timeout=30)
            response.raise_for_status()
            status_res = response.json()
            if status_res.get("code") not in (None, 0, "0", 200, "200"):
                print(f"Error: Status API business code {status_res.get('code')}", file=sys.stderr, flush=True)
                return None
            status = status_res.get("status")

            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Task Status: {status}", file=sys.stderr, flush=True)

            if status == "finished":
                print(f"[{timestamp}] Task finished; validating article output.", file=sys.stderr, flush=True)
                break
            elif status in ["failed", "canceled", "paused"]:
                print(f"Error: Task {status}. Please check your BrowserAct dashboard.", file=sys.stderr, flush=True)
                return None
        except Exception as e:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Polling error: {e}. Retrying...", file=sys.stderr, flush=True)

        time.sleep(min(10, max(0, max_poll_time - (time.monotonic() - poll_start))))
    else:
        print(f"Error: Client wait expired; task {task_id} may still run. Resume with --task-id {task_id}; do not start a duplicate.", file=sys.stderr, flush=True)
        return None

    # 3. Get Results
    try:
        response = requests.get(f"{API_BASE_URL}/get-task", params={"task_id": task_id}, headers=headers, timeout=30)
        response.raise_for_status()
        task_info = response.json()
        if task_info.get("status") != "finished":
            raise ValueError("Task detail does not confirm finished")

        # Extract data from output["string"] as requested
        # Usually task_info['output']['string'] contains the result
        output = task_info.get("output", {})
        result_string = output.get("string")

        query = verify_search(task_info, keywords, publication_date)
        rows, summary = select_articles(result_string, int(limit), keywords)
        summary["actual_search_query"] = query
        print("Run summary: " + json.dumps(summary, ensure_ascii=False), file=sys.stderr, flush=True)
        return json.dumps(rows, ensure_ascii=False)
    except Exception as e:
        print(f"Error: Failed to retrieve results - {e}", file=sys.stderr, flush=True)
        return None

def verify_search(task_info, keywords, publication_date):
    normalize = lambda value: re.sub(r"\s+", "", str(value)).casefold()
    query = None
    for step in task_info.get("steps", []):
        goal = step.get("step_goal") or ""
        if "search box" in goal.casefold() or "search field" in goal.casefold():
            match = re.search(r'Input\s+"(.*?)"\s+into', goal, re.DOTALL)
            if match:
                query = match.group(1)
                break
    if query is None:
        raise ValueError("Actual search input is unavailable; cannot verify the requested query")
    expected_keyword = normalize(keywords)
    actual = normalize(query)
    if expected_keyword not in actual:
        raise ValueError("The task searched a different keyword")
    date = build_payload(keywords, 1, publication_date)["input_parameters"][2]["value"]
    if date == "-":
        if actual not in {expected_keyword, expected_keyword + "发布日期-"}:
            raise ValueError("The task did not apply unrestricted publication dates")
    elif normalize(date) not in actual:
        raise ValueError("The task did not apply the requested publication date")
    return query


def select_articles(result_string, limit, keywords=None):
    rows = json.loads(result_string) if isinstance(result_string, str) else result_string
    if not isinstance(rows, list):
        raise ValueError("Expected an article array")
    valid = []
    seen_urls = set()
    seen_articles = set()
    rejected = []
    for rank, source_row in enumerate(rows, 1):
        if not isinstance(source_row, dict):
            rejected.append({"row": rank, "reason": "not_an_object"})
            continue
        row = dict(source_row)
        title = row.get("title", row.get("Title"))
        body = row.get("body_content", row.get("Body Content"))
        raw_url = row.get("url_link", row.get("URL Link"))
        if not all(isinstance(v, str) and v.strip() for v in (title, body, raw_url)):
            rejected.append({"row": rank, "reason": "missing_title_body_or_url"})
            continue
        if keywords and any(term.casefold() not in (title + " " + body).casefold() for term in keywords.split()):
            rejected.append({"row": rank, "reason": "missing_keyword_term"})
            continue
        raw_url = raw_url.strip()
        url = raw_url[1:-1] if raw_url.startswith("{https://") and raw_url.endswith("}") else raw_url
        try:
            parsed = urlparse(url)
            good_url = parsed.scheme == "https" and parsed.hostname in {"mp.weixin.qq.com", "weixin.sogou.com"}
        except ValueError:
            good_url = False
        if not good_url:
            rejected.append({"row": rank, "reason": "invalid_or_placeholder_url"})
            continue
        author = row.get("author", row.get("Author"))
        date = row.get("publication_date", row.get("Publication Date"))
        identity = (title.strip().casefold(), str(author or "").strip(), str(date or "").strip())
        if url in seen_urls or ((author or date) and identity in seen_articles):
            rejected.append({"row": rank, "reason": "duplicate_article"})
            continue
        seen_urls.add(url)
        seen_articles.add(identity)
        row["url_link" if "url_link" in row else "URL Link"] = url
        valid.append(row)
    if len(valid) < limit:
        raise ValueError(f"Requested {limit} articles; only {len(valid)} usable records from {len(rows)} server rows")
    summary = {"server_rows": len(rows), "usable_rows": len(valid), "selected_rows": limit,
               "additional_usable_rows": len(valid) - limit, "rejected": rejected}
    return valid[:limit], summary


def validate_articles(result_string, limit):
    return select_articles(result_string, limit)[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search WeChat articles or observe an existing task")
    parser.add_argument("keywords")
    parser.add_argument("limit", nargs="?", default=10, type=int)
    parser.add_argument("publication_date", nargs="?", default="-", help="Use - for no date restriction; all API fields remain required")
    parser.add_argument("--task-id", help="Observe an existing task without submitting a new one")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()
    api_key = os.getenv("BROWSERACT_API_KEY", "").strip()
    if not api_key:
        parser.error("BROWSERACT_API_KEY is not configured; load the existing local key securely")
    if args.limit < 1 or args.timeout < 1:
        parser.error("limit and timeout must be positive")
    try:
        result = run_wechat_article_search_task(api_key, args.keywords, args.limit, args.publication_date, args.task_id, args.timeout)
    except Exception as exc:
        print("Error: " + str(exc).replace(api_key, "[REDACTED]"), file=sys.stderr, flush=True)
        sys.exit(1)
    if result is None:
        sys.exit(1)
    print(result, flush=True)
