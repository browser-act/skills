import argparse
import sys


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser()
    parser.add_argument('username')  # Threads/Instagram username (without @)
    args = parser.parse_args()

    username = args.username.lstrip('@').replace("'", "\\'")

    js = f"""
    (async function() {{
      try {{
        const username = '{username}';
        const res = await fetch(
          'https://www.threads.com/api/v1/users/web_profile_info/?username=' + encodeURIComponent(username),
          {{ headers: {{ 'X-IG-App-ID': '238260118697367' }} }}
        );
        if (!res.ok) {{
          return JSON.stringify({{error: true, message: 'Profile API returned ' + res.status + ' for @' + username}});
        }}
        const data = await res.json();
        const user = data && data.data && data.data.user;
        if (!user) {{
          return JSON.stringify({{error: true, message: 'User not found: @' + username}});
        }}
        return JSON.stringify({{
          pk: user.id || null,
          username: user.username || username,
          full_name: user.full_name || null,
          biography: user.biography || null,
          follower_count: (user.edge_followed_by && user.edge_followed_by.count) || null,
          following_count: (user.edge_follow && user.edge_follow.count) || null,
          is_verified: user.is_verified || false,
          is_private: user.is_private || false,
          profile_pic_url: user.profile_pic_url || null,
          profile_url: 'https://www.threads.com/@' + (user.username || username),
          external_url: user.external_url || null
        }});
      }} catch(e) {{
        return JSON.stringify({{error: true, message: e.message}});
      }}
    }})()
    """
    print(js)


if __name__ == '__main__':
    main()
