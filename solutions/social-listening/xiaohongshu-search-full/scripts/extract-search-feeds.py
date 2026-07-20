import argparse
import json
import sys


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser()
    parser.add_argument('--keyword', default='', help='Filter to notes whose title contains this keyword (case-insensitive). When provided, returns keyword_count alongside total_count.')
    args = parser.parse_args()

    keyword_js = json.dumps(args.keyword)  # safely escape for JS string literal

    js = f"""
(function() {{
  try {{
    var search = window.__INITIAL_STATE__ && window.__INITIAL_STATE__.search;
    if (!search) return JSON.stringify({{error: true, message: '__INITIAL_STATE__.search not found'}});

    var feedsRaw = search.feeds;
    var hasMoreRaw = search.hasMore;

    function unwrap(v) {{
      return (v && v._value !== undefined) ? v._value : v;
    }}
    function deepUnwrap(obj, depth) {{
      if (depth > 5 || obj === null || obj === undefined) return obj;
      obj = unwrap(obj);
      if (typeof obj !== 'object') return obj;
      if (Array.isArray(obj)) return obj.map(function(x) {{ return deepUnwrap(x, depth + 1); }});
      var r = {{}};
      Object.keys(obj).forEach(function(k) {{ r[k] = deepUnwrap(obj[k], depth + 1); }});
      return r;
    }}

    var feeds = deepUnwrap(feedsRaw, 0);
    var hasMore = deepUnwrap(hasMoreRaw, 0);

    if (!Array.isArray(feeds)) return JSON.stringify({{error: true, message: 'feeds is not an array', type: typeof feeds}});

    var allItems = [];
    for (var i = 0; i < feeds.length; i++) {{
      var item = feeds[i];
      if (!item || item.modelType !== 'note') continue;
      var card = item.noteCard || {{}};
      var user = card.user || {{}};
      var interact = card.interactInfo || {{}};
      var cover = card.cover || {{}};

      var pubDate = '';
      var tagInfo = card.cornerTagInfo;
      if (tagInfo) {{
        var arr = Array.isArray(tagInfo) ? tagInfo : Object.values(tagInfo);
        for (var j = 0; j < arr.length; j++) {{
          if (arr[j] && arr[j].type === 'publish_time') {{ pubDate = arr[j].text || ''; break; }}
        }}
      }}

      var coverUrl = cover.urlDefault || cover.url_default || '';
      if (!coverUrl) {{
        var imgList = card.imageList;
        if (imgList) {{
          var imgs = Array.isArray(imgList) ? imgList : Object.values(imgList);
          if (imgs.length > 0) {{
            var first = imgs[0];
            var infos = first.infoList || [];
            var dft = infos.filter(function(x) {{ return x.imageScene === 'WB_DFT'; }})[0] || infos[0];
            coverUrl = (dft && dft.url) || first.urlDefault || '';
          }}
        }}
      }}

      var noteId = item.id || item.trackId || '';
      var xsecToken = item.xsecToken || '';
      var noteUrl = noteId
        ? 'https://www.xiaohongshu.com/explore/' + noteId + '?xsec_token=' + encodeURIComponent(xsecToken) + '&xsec_source=pc_search'
        : '';

      allItems.push({{
        id: noteId,
        xsec_token: xsecToken,
        note_url: noteUrl,
        type: card.type || '',
        title: card.displayTitle || '',
        publish_date: pubDate,
        cover_url: coverUrl,
        liked_count: interact.likedCount || '0',
        collected_count: interact.collectedCount || '0',
        comment_count: interact.commentCount || '0',
        shared_count: interact.sharedCount || '0',
        author_nickname: user.nickname || user.nickName || '',
        author_id: user.userId || '',
        author_avatar: user.avatar || ''
      }});
    }}

    // Edit-distance based fuzzy matching.
    // Allows 1 edit per 5 chars of keyword length (min 1), checked against
    // every sliding window substring of each word in the text.
    function editDist(a, b) {{
      var m = a.length, n = b.length, i, j;
      var d = [];
      for (i = 0; i <= m; i++) {{ d[i] = [i]; for (j = 1; j <= n; j++) d[i][j] = 0; }}
      for (j = 0; j <= n; j++) d[0][j] = j;
      for (i = 1; i <= m; i++)
        for (j = 1; j <= n; j++)
          d[i][j] = a[i-1] === b[j-1] ? d[i-1][j-1] : 1 + Math.min(d[i-1][j], d[i][j-1], d[i-1][j-1]);
      return d[m][n];
    }}
    function fuzzyContains(kw, text) {{
      if (!kw || !text) return !kw;
      text = text.toLowerCase();
      kw = kw.toLowerCase();
      if (text.indexOf(kw) !== -1) return true;          // exact substring match
      var maxDist = Math.max(1, Math.floor(kw.length * 0.2));
      var words = text.split(/[\\s\\W]+/).filter(Boolean);
      for (var w = 0; w < words.length; w++) {{
        var word = words[w];
        // Slide a window of length [kw.length-maxDist, kw.length+maxDist] over the word
        for (var s = 0; s < word.length; s++) {{
          for (var l = Math.max(1, kw.length - maxDist); l <= kw.length + maxDist && s + l <= word.length; l++) {{
            if (editDist(kw, word.substr(s, l)) <= maxDist) return true;
          }}
        }}
      }}
      return false;
    }}

    var keyword = {keyword_js};
    var filteredItems;
    if (keyword) {{
      filteredItems = allItems.filter(function(x) {{ return fuzzyContains(keyword, x.title); }});
    }} else {{
      filteredItems = allItems;
    }}

    return JSON.stringify({{
      total_count: allItems.length,
      keyword_count: keyword ? filteredItems.length : null,
      has_more: !!hasMore,
      items: filteredItems
    }});
  }} catch(e) {{
    return JSON.stringify({{error: true, message: e.message}});
  }}
}})()
"""
    print(js)


if __name__ == '__main__':
    main()
