import argparse
import sys


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    js = r"""
    (function() {
      try {
        const sv = document.getElementById('scrollview');
        if (!sv) return JSON.stringify({error: true, message: '#scrollview not found — ensure user profile page is loaded'});
        const before = sv.scrollTop;
        const target = sv.scrollHeight;
        sv.scrollTo(0, target);
        return JSON.stringify({scrolled: true, from: Math.round(before), to: target, client_height: sv.clientHeight});
      } catch(e) {
        return JSON.stringify({error: true, message: e.message});
      }
    })()
    """
    print(js)


if __name__ == '__main__':
    main()
