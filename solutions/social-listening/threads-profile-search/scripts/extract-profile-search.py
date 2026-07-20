import argparse
import sys


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser()
    parser.add_argument('keyword')  # search keyword to find profiles
    args = parser.parse_args()

    keyword = args.keyword.replace("'", "\\'")

    js = f"""
    (function() {{
      try {{
        const html = document.documentElement.innerHTML;
        const srIdx = html.indexOf('"searchResults":{{"inform_module"');
        if (srIdx < 0) {{
          return JSON.stringify({{error: true, message: 'searchResults not found — navigate to profile search: https://www.threads.com/search/?q=' + encodeURIComponent('{keyword}') + '&type=profiles'}});
        }}
        let depth = 0;
        const start = html.indexOf('{{', srIdx + '"searchResults":'.length);
        if (start < 0) return JSON.stringify({{error: true, message: 'searchResults object start not found'}});
        let pos = start;
        while (pos < html.length) {{
          if (html[pos] === '{{') depth++;
          else if (html[pos] === '}}') {{ depth--; if (depth === 0) break; }}
          pos++;
        }}
        let sr;
        try {{
          sr = JSON.parse(html.slice(start, pos + 1));
        }} catch(pe) {{
          return JSON.stringify({{error: true, message: 'JSON parse failed: ' + pe.message}});
        }}
        const edges = sr.edges || [];
        if (!edges.length) return JSON.stringify({{error: true, message: 'No profiles found for keyword: {keyword}'}});
        // Deduplicate by username
        const seen = new Set();
        const profiles = [];
        for (const edge of edges) {{
          const thread = edge.node && edge.node.thread;
          if (!thread) continue;
          const items = thread.thread_items;
          if (!items || !items.length) continue;
          const post = items[0].post;
          if (!post || !post.user) continue;
          const u = post.user;
          if (!u.username || seen.has(u.username)) continue;
          seen.add(u.username);
          profiles.push({{
            pk: u.pk || null,
            username: u.username,
            full_name: u.full_name || null,
            is_verified: u.is_verified || false,
            is_private: u.text_post_app_is_private || false,
            profile_pic_url: u.profile_pic_url || null,
            profile_url: 'https://www.threads.com/@' + u.username
          }});
        }}
        return JSON.stringify({{
          keyword: '{keyword}',
          profiles: profiles,
          count: profiles.length,
          page_info: sr.page_info || null
        }});
      }} catch(e) {{
        return JSON.stringify({{error: true, message: e.message}});
      }}
    }})()
    """
    print(js)


if __name__ == '__main__':
    main()
