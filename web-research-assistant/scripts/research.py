#!/usr/bin/env python3
"""
Web Research Assistant - BrowserAct Skill

This script performs web research and searches the internet for information
when primary web access is restricted or blocked.

Template ID: TEMPLATE_ID_HERE
"""

import os
import json
import argparse
import requests
from typing import Optional, Dict, List


BROWSERACT_API_KEY = os.environ.get("BROWSERACT_API_KEY")
BROWSERACT_MCP_TOKEN = os.environ.get("BROWSERACT_MCP_TOKEN")
MCP_SERVER_URL = "https://mcp.browseract.com/"


def execute_web_search(query: str, search_engine: str = "google", max_results: int = 10, 
                       content_type: str = "all", time_range: str = "past_month") -> Dict:
    """
    Execute a web search using BrowserAct MCP.
    
    Args:
        query: Search query string
        search_engine: Search engine to use (google, bing, duckduckgo)
        max_results: Maximum number of results
        content_type: Type of content (all, news, articles, reports, data)
        time_range: Time filter (anytime, past_day, past_week, past_month, past_year)
    
    Returns:
        Dictionary containing search results
    """
    payload = {
        "action": "search",
        "query": query,
        "engine": search_engine,
        "max_results": max_results,
        "content_type": content_type,
        "time_range": time_range,
        "options": {
            "extract_data": True,
            "include_snippets": True,
            "follow_redirects": True
        }
    }
    
    response = requests.post(
        MCP_SERVER_URL,
        headers={
            "Authorization": f"Bearer {BROWSERACT_MCP_TOKEN}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=60000
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Search failed: {response.status_code} - {response.text}")


def extract_key_information(results: Dict) -> Dict:
    """
    Extract key information from search results.
    
    Args:
        results: Search results dictionary
    
    Returns:
        Dictionary with extracted key information
    """
    extracted = {
        "total_results": 0,
        "key_facts": [],
        "statistics": [],
        "sources": [],
        "summary": ""
    }
    
    if "results" in results:
        extracted["total_results"] = len(results["results"])
        
        for result in results["results"][:10]:
            if "title" in result:
                extracted["sources"].append({
                    "title": result["title"],
                    "url": result.get("url", ""),
                    "snippet": result.get("snippet", "")
                })
            
            # Extract potential statistics (numbers with context)
            if "snippet" in result:
                snippet = result["snippet"]
                # Simple heuristic for extracting statistics
                if any(char.isdigit() for char in snippet):
                    extracted["statistics"].append(snippet[:200])
    
    # Generate summary
    if extracted["sources"]:
        extracted["summary"] = f"Found {extracted['total_results']} relevant sources"
    
    return extracted


def format_research_report(results: Dict, extracted: Dict, query: str) -> str:
    """
    Format research report as markdown.
    
    Args:
        results: Raw search results
        extracted: Extracted key information
        query: Original search query
    
    Returns:
        Formatted markdown report
    """
    report = f"# Web Research Report\n\n"
    report += f"**Query**: {query}\n\n"
    report += f"**Date**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    report += "## Executive Summary\n\n"
    report += f"{extracted['summary']}\n\n"
    
    report += "## Key Findings\n\n"
    for i, fact in enumerate(extracted["key_facts"][:5], 1):
        report += f"{i}. {fact}\n"
    
    if not extracted["key_facts"]:
        report += "_No specific key facts extracted from search results._\n"
    
    report += "\n## Statistics & Data\n\n"
    for stat in extracted["statistics"][:5]:
        report += f"- {stat}\n"
    
    if not extracted["statistics"]:
        report += "_No statistics found in search results._\n"
    
    report += "\n## Data Sources\n\n"
    for i, source in enumerate(extracted["sources"][:10], 1):
        report += f"### {i}. {source['title']}\n"
        report += f"**URL**: {source['url']}\n"
        report += f"**Snippet**: {source['snippet'][:300]}...\n\n"
    
    report += "\n## Recommendations\n\n"
    report += "- Verify key findings with additional sources\n"
    report += "- Cross-reference statistics with official data\n"
    report += "- Check publication dates for currency\n"
    report += "- Consider multiple perspectives on the topic\n"
    
    return report


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Web Research Assistant - Supplement restricted web access with internet search"
    )
    parser.add_argument("query", help="Research topic or question to search for")
    parser.add_argument("--engine", "-e", default="google", 
                       choices=["google", "bing", "duckduckgo"],
                       help="Search engine to use")
    parser.add_argument("--max-results", "-m", type=int, default=10,
                       help="Maximum number of results (1-50)")
    parser.add_argument("--content-type", "-c", default="all",
                       choices=["all", "news", "articles", "reports", "data"],
                       help="Type of content to search for")
    parser.add_argument("--time-range", "-t", default="past_month",
                       choices=["anytime", "past_day", "past_week", "past_month", "past_year"],
                       help="Time filter for results")
    parser.add_argument("--output", "-o", help="Output file path for report")
    parser.add_argument("--format", "-f", default="markdown",
                       choices=["markdown", "json"],
                       help="Output format")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if not BROWSERACT_MCP_TOKEN:
        print("Error: BROWSERACT_MCP_TOKEN environment variable not set")
        print("Get your token from: https://www.browseract.com/reception/integrations")
        return 1
    
    try:
        if args.verbose:
            print(f"Researching: {args.query}")
            print(f"Using engine: {args.engine}")
            print(f"Content type: {args.content_type}")
            print(f"Time range: {args.time_range}")
        
        # Execute search
        results = execute_web_search(
            args.query,
            args.engine,
            args.max_results,
            args.content_type,
            args.time_range
        )
        
        # Extract key information
        extracted = extract_key_information(results)
        
        # Generate report
        if args.format == "markdown":
            report = format_research_report(results, extracted, args.query)
        else:
            report = json.dumps({
                "query": args.query,
                "results": results,
                "extracted": extracted
            }, indent=2, ensure_ascii=False)
        
        # Output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            if args.verbose:
                print(f"Report saved to: {args.output}")
        else:
            print(report)
        
        if args.verbose:
            print(f"\nTotal sources found: {extracted['total_results']}")
            print(f"Sources used in report: {len(extracted['sources'])}")
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
