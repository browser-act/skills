import argparse
import sys


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser()
    parser.add_argument('keyword')              # search keyword or hashtag (e.g. "AI" or "#AI")
    parser.add_argument('--filter', default='top', choices=['top', 'recent'])  # sort order
    args = parser.parse_args()

    keyword = args.keyword.replace("'", "\\'")
    serp_filter = args.filter

    js = f"""
    (async function() {{
      try {{
        const html = document.documentElement.innerHTML;
        // Verify this is the correct search results page
        const urlCheck = location.href;
        const expectedKw = '{keyword}';
        const srIdx = html.indexOf('"searchResults":{{"inform_module"');
        if (srIdx < 0) {{
          return JSON.stringify({{error: true, message: 'searchResults not found in SSR HTML — navigate to the search page first: https://www.threads.com/search/?q=' + encodeURIComponent(expectedKw) + '&serp_type={serp_filter}'}});
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
        if (!edges.length) return JSON.stringify({{error: true, message: 'No search results found'}});
        const posts = [];
        for (const edge of edges) {{
          const thread = edge.node && edge.node.thread;
          if (!thread) continue;
          const items = thread.thread_items;
          if (!items || !items.length) continue;
          const post = items[0].post;
          if (!post) continue;
          const u = post.user || {{}};
          const info = post.text_post_app_info || {{}};
          posts.push({{
            id: post.pk || null,
            code: post.code || null,
            url: u.username && post.code ? 'https://www.threads.com/@' + u.username + '/post/' + post.code : null,
            text: (post.caption && post.caption.text) || null,
            taken_at: post.taken_at || null,
            like_count: post.like_count || 0,
            reply_count: info.direct_reply_count || 0,
            repost_count: info.repost_count || 0,
            quote_count: info.quote_count || 0,
            is_reply: info.is_reply || false,
            media_type: post.media_type || null,
            has_media: !!(
              (post.image_versions2 && post.image_versions2.candidates && post.image_versions2.candidates.length) ||
              (post.video_versions && post.video_versions.length) ||
              (post.carousel_media && post.carousel_media.length)
            ),
            user: {{
              pk: u.pk || null,
              username: u.username || null,
              full_name: u.full_name || null,
              is_verified: u.is_verified || false
            }}
          }});
        }}
        return JSON.stringify({{
          keyword: expectedKw,
          filter: '{serp_filter}',
          posts: posts,
          count: posts.length,
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
