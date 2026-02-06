"""
Amazon Competitor Analyzer Skill
================================
Scrapes Amazon product data from ASINs using BrowserAct API
and performs surgical competitive analysis.

Author: OpenCode
Version: 1.0.0
"""

import os
import sys
import json
import time
import csv
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any


# Configuration
BROWSERACT_API_KEY = os.getenv("BROWSERACT_API_KEY", "")
WORKFLOW_TEMPLATE_ID = "77814333389670716"
API_BASE_URL = "https://api.browseract.com/v2/workflow"


class AmazonCompetitorAnalyzer:
    """Main class for Amazon competitive analysis"""
    
    def __init__(self, api_key: str = None, workflow_template_id: str = None):
        """Initialize the analyzer with API credentials"""
        self.api_key = api_key or BROWSERACT_API_KEY
        self.workflow_template_id = workflow_template_id or WORKFLOW_TEMPLATE_ID
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def validate_asin(self, asin: str) -> bool:
        """Validate ASIN format"""
        return len(asin) == 10 and asin.isalnum()
    
    def extract_asins_from_text(self, text: str) -> List[str]:
        """Extract ASINs from user input text"""
        import re
        # Match 10-character alphanumeric strings starting with B0 or similar
        asin_pattern = r'\b[B0][A-Z0-9]{9}\b'
        asins = re.findall(asin_pattern, text.upper())
        return list(set(asins))  # Remove duplicates
    
    def submit_task(self, asin: str) -> Optional[str]:
        """Submit scraping task for a single ASIN"""
        if not self.validate_asin(asin):
            print(f"Invalid ASIN: {asin}")
            return None
        
        data = {
            "workflow_template_id": self.workflow_template_id,
            "input_parameters": [{"name": "ASIN", "value": asin}]
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/run-task-by-template",
                json=data,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                task_id = result.get("id")
                return task_id
            else:
                print(f"Failed to submit task for {asin}: {response.json().get('msg', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"Error submitting task for {asin}: {e}")
            return None
    
    def wait_for_task(self, task_id: str, timeout: int = 300) -> bool:
        """Wait for task completion"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(
                    f"{API_BASE_URL}/get-task-status?task_id={task_id}",
                    headers=self.headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    status = response.json().get("status")
                    
                    if status == "finished":
                        return True
                    elif status in ["failed", "canceled"]:
                        return False
                
                time.sleep(3)
                
            except Exception:
                time.sleep(5)
        
        return False
    
    def get_results(self, task_id: str) -> Optional[Dict]:
        """Get task results"""
        try:
            response = requests.get(
                f"{API_BASE_URL}/get-task?task_id={task_id}",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error getting results: {e}")
        
        return None
    
    def scrape_product(self, asin: str, wait_timeout: int = 300) -> Optional[Dict]:
        """Scrape a single product"""
        # Submit task
        task_id = self.submit_task(asin)
        if not task_id:
            return None
        
        # Wait for completion
        if not self.wait_for_task(task_id, wait_timeout):
            return None
        
        # Get results
        results = self.get_results(task_id)
        return results
    
    def scrape_multiple_products(self, asins: List[str], delay: int = 5) -> Dict[str, Any]:
        """Scrape multiple products"""
        results = {}
        
        for asin in asins:
            print(f"Processing: {asin}")
            
            data = self.scrape_product(asin)
            results[asin] = data
            
            if delay > 0 and asin != asins[-1]:
                time.sleep(delay)
        
        return results
    
    def analyze_competitive_position(self, products: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitive positioning"""
        analysis = {
            "price_analysis": {},
            "rating_analysis": {},
            "market_leaders": {},
            "opportunities": []
        }
        
        prices = []
        ratings = []
        
        for asin, data in products.items():
            if data:
                try:
                    product = data.get('results', {}).get('products', [{}])[0]
                    price = product.get('pricing', {}).get('current_price', 0)
                    rating = product.get('reviews', {}).get('average_rating', 0)
                    reviews = product.get('reviews', {}).get('total_count', 0)
                    brand = product.get('product_info', {}).get('brand', asin)
                    
                    prices.append((asin, price, brand))
                    ratings.append((asin, rating, reviews, brand))
                    
                except Exception:
                    pass
        
        # Sort by price
        prices.sort(key=lambda x: x[1])
        if prices:
            analysis["price_analysis"]["lowest"] = prices[0]
            analysis["price_analysis"]["highest"] = prices[-1]
            analysis["price_analysis"]["range"] = prices[-1][1] - prices[0][1]
        
        # Sort by rating
        ratings.sort(key=lambda x: x[1], reverse=True)
        if ratings:
            analysis["rating_analysis"]["top_rated"] = ratings[0]
            analysis["rating_analysis"]["by_volume"] = sorted(ratings, key=lambda x: x[2], reverse=True)
        
        return analysis
    
    def generate_csv_report(self, products: Dict[str, Any], output_path: str):
        """Generate CSV report"""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'ASIN', 'Product Title', 'Brand', 'Price ($)', 'Original Price ($)',
                'Discount (%)', 'Rating', 'Reviews Count', 'Weight', 'Features'
            ])
            
            for asin, data in products.items():
                if data:
                    try:
                        product = data.get('results', {}).get('products', [{}])[0]
                        writer.writerow([
                            asin,
                            product.get('product_info', {}).get('title', 'N/A')[:100],
                            product.get('product_info', {}).get('brand', 'N/A'),
                            product.get('pricing', {}).get('current_price', 'N/A'),
                            product.get('pricing', {}).get('original_price', 'N/A'),
                            product.get('pricing', {}).get('discount_percent', 'N/A'),
                            product.get('reviews', {}).get('average_rating', 'N/A'),
                            product.get('reviews', {}).get('total_count', 'N/A'),
                            product.get('specifications', {}).get('weight', 'N/A'),
                            ', '.join(product.get('specifications', {}).get('features', [])[:5])
                        ])
                    except:
                        writer.writerow([asin, 'Error', '', '', '', '', '', '', '', ''])
                else:
                    writer.writerow([asin, 'Failed', '', '', '', '', '', '', '', ''])
        
        print(f"CSV report saved: {output_path}")
    
    def generate_markdown_report(self, products: Dict[str, Any], output_path: str):
        """Generate comprehensive markdown report"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Amazon Competitive Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Products Analyzed:** {len(products)}\n\n")
            
            # Summary table
            f.write("## Data Summary\n\n")
            f.write("| ASIN | Brand | Price | Rating | Reviews |\n")
            f.write("|------|-------|-------|--------|---------|\n")
            
            for asin, data in products.items():
                if data:
                    try:
                        product = data.get('results', {}).get('products', [{}])[0]
                        info = product.get('product_info', {})
                        pricing = product.get('pricing', {})
                        reviews = product.get('reviews', {})
                        
                        f.write(f"| {asin} | {info.get('brand', 'N/A')} | "
                               f"${pricing.get('current_price', 'N/A')} | "
                               f"{reviews.get('average_rating', 'N/A')}/5 | "
                               f"{reviews.get('total_count', 'N/A'):,} |\n")
                    except:
                        f.write(f"| {asin} | Error | - | - | - |\n")
                else:
                    f.write(f"| {asin} | Failed | - | - | - |\n")
            
            # Detailed analysis
            f.write("\n## Detailed Analysis\n\n")
            
            competitive_analysis = self.analyze_competitive_position(products)
            
            f.write("### Price Positioning\n")
            if competitive_analysis.get("price_analysis"):
                pa = competitive_analysis["price_analysis"]
                if "lowest" in pa:
                    f.write(f"- Lowest Price: {pa['lowest'][2]} at ${pa['lowest'][1]}\n")
                if "highest" in pa:
                    f.write(f"- Highest Price: {pa['highest'][2]} at ${pa['highest'][1]}\n")
            
            f.write("\n### Rating Leaders\n")
            if competitive_analysis.get("rating_analysis"):
                ra = competitive_analysis["rating_analysis"]
                if "top_rated" in ra:
                    f.write(f"- Highest Rated: {ra['top_rated'][3]} at {ra['top_rated'][1]}/5\n")
            
            f.write("\n---\n")
            f.write(f"*Generated by Amazon Competitor Analyzer*\n")
        
        print(f"Markdown report saved: {output_path}")
    
    def generate_json_report(self, products: Dict[str, Any], output_path: str):
        """Generate JSON report"""
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "products_analyzed": len(products),
            "products": products,
            "analysis": self.analyze_competitive_position(products)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"JSON report saved: {output_path}")


def analyze_asins(asins: List[str], output_dir: str = None) -> Dict[str, Any]:
    """Main function to analyze multiple ASINs"""
    analyzer = AmazonCompetitorAnalyzer()
    
    print(f"Analyzing {len(asins)} ASINs...")
    
    # Scrape products
    products = analyzer.scrape_multiple_products(asins)
    
    # Generate reports if output directory specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
        base_path = os.path.join(output_dir, "amazon_analysis")
        analyzer.generate_csv_report(products, f"{base_path}.csv")
        analyzer.generate_markdown_report(products, f"{base_path}.md")
        analyzer.generate_json_report(products, f"{base_path}.json")
    
    return products


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Amazon Competitor Analyzer")
    parser.add_argument("asins", nargs="+", help="ASINs to analyze")
    parser.add_argument("-o", "--output", default=".", help="Output directory")
    parser.add_argument("-k", "--api-key", help="BrowserAct API key")
    
    args = parser.parse_args()
    
    # Initialize with custom API key if provided
    if args.api_key:
        global BROWSERACT_API_KEY
        BROWSERACT_API_KEY = args.api_key
    
    # Run analysis
    products = analyze_asins(args.asins, args.output)
    
    print(f"\nAnalysis complete! Analyzed {len(products)} products.")


if __name__ == "__main__":
    main()
