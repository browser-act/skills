import argparse
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser()
    parser.add_argument('page', type=int, help='Target page number (1-based)')
    args = parser.parse_args()

    js = f"""
    (function() {{
      try {{
        var targetPage = {args.page};
        var pages = document.querySelectorAll('[class*="search-pagination-page-box"]');
        if (pages.length === 0) {{
          return JSON.stringify({{ error: true, message: 'Pagination not found — results may be too few for multiple pages' }});
        }}
        for (var i = 0; i < pages.length; i++) {{
          if (parseInt(pages[i].textContent.trim()) === targetPage) {{
            pages[i].click();
            return JSON.stringify({{ ok: true, clicked_page: targetPage }});
          }}
        }}
        return JSON.stringify({{ error: true, message: 'Page ' + targetPage + ' not found in pagination. Available pages: ' + Array.from(pages).map(function(p) {{ return p.textContent.trim(); }}).join(', ') }});
      }} catch(e) {{
        return JSON.stringify({{ error: true, message: e.message }});
      }}
    }})()
    """
    print(js)

if __name__ == '__main__':
    main()
