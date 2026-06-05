import argparse
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser(description='Scroll message list to top to trigger loading older messages; returns whether new messages were loaded')
    args = parser.parse_args()

    js = """
    (async () => {
      try {
        const list = document.querySelector('[data-testid="dm-message-list-container"]') || document.querySelector('[data-testid="dm-message-list"]');
        if (!list) return JSON.stringify({ error: true, message: 'message list container not found' });

        const beforeCount = document.querySelectorAll('[data-testid^="message-"]:not([data-testid^="message-text-"])').length;
        list.scrollTop = 0;

        // Wait up to 5s for new messages to load
        let afterCount = beforeCount;
        for (let i = 0; i < 50; i++) {
          await new Promise(r => setTimeout(r, 100));
          afterCount = document.querySelectorAll('[data-testid^="message-"]:not([data-testid^="message-text-"])').length;
          if (afterCount > beforeCount) break;
        }

        return JSON.stringify({
          before_count: beforeCount,
          after_count: afterCount,
          loaded_more: afterCount > beforeCount,
          reached_top: afterCount === beforeCount  // No new messages loaded → likely at top
        });
      } catch(e) {
        return JSON.stringify({ error: true, message: e.message });
      }
    })()
    """
    print(js)

if __name__ == '__main__':
    main()
