import argparse
import sys


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser()
    parser.parse_args()

    js = r"""
    (function() {
      try {
        const result = {};

        // Strategy 1: JSON-LD Person/Organization/LocalBusiness/Store
        const lds = Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map(s => {
          try { return JSON.parse(s.textContent); } catch(e) { return null; }
        }).filter(Boolean);
        const flat = lds.flatMap(l => Array.isArray(l) ? l : [l]);
        const sellerLd = flat.find(l => ['Person', 'Organization', 'LocalBusiness', 'Store', 'OnlineStore'].includes(l['@type']));
        if (sellerLd) {
          result.name = sellerLd.name || null;
          result.description = sellerLd.description || null;
          result.url = sellerLd.url || null;
          result.image = Array.isArray(sellerLd.image) ? sellerLd.image[0] : (sellerLd.image || null);
          result.rating = sellerLd.aggregateRating?.ratingValue != null ? parseFloat(sellerLd.aggregateRating.ratingValue) : null;
          result.review_count = sellerLd.aggregateRating?.reviewCount != null ? parseInt(sellerLd.aggregateRating.reviewCount) : null;
          result._source = 'json-ld';
        }

        // Strategy 2: Amazon seller page
        if (window.location.hostname.includes('amazon.')) {
          // Try specific seller/storefront selectors before falling back to generic h1
          const sellerNameEl = document.querySelector('#sellerName, .a-profile-name.seller-name, #storeName, [class*="storeName"], .store-name-text, .s-store-name');
          // Also try: first h1 inside the main seller content container (not cart widgets)
          const contentH1 = document.querySelector('#dp-container h1, #storefront-header h1, .seller-profile-container h1, [data-cel-widget="merchant-info"] h1');
          const sellerName = (sellerNameEl || contentH1)?.textContent.trim();
          if (!result.name && sellerName) result.name = sellerName;
          const ratingText = document.querySelector('#seller-feedback-summary .feedback-count-text, .feedback-detail')?.textContent.trim();
          if (!result.rating && ratingText) {
            const m = ratingText.match(/(\d+\.?\d*)\s*out of\s*5/i);
            if (m) result.rating = parseFloat(m[1]);
          }
          const rcText = document.querySelector('#seller-feedback-summary .feedback-count, a[href*="feedback"]')?.textContent.trim();
          if (!result.review_count && rcText) result.review_count = parseInt(rcText.replace(/[^0-9]/g, '')) || null;
          result._platform = 'amazon';
        }

        // Strategy 3: eBay seller
        if (window.location.hostname.includes('ebay.')) {
          const ebayName = document.querySelector('.str-seller-card__seller-name a, .si-content h1, .str-title')?.textContent.trim();
          if (!result.name && ebayName) result.name = ebayName;
          const posFeedback = document.querySelector('.str-seller-card__positive-feedback, .positive-feedback-percentage')?.textContent.trim();
          if (posFeedback) result.positive_feedback_pct = posFeedback;
          const fbCount = document.querySelector('.str-seller-card__feedback-count, .feedback-number')?.textContent.trim();
          if (!result.review_count && fbCount) result.review_count = parseInt(fbCount.replace(/[^0-9]/g, '')) || null;
          result._platform = 'ebay';
        }

        // Strategy 4: Generic fallback
        if (!result.name) result.name = document.querySelector('h1, .seller-name, .store-name, [class*="seller-title"], [class*="merchant-name"]')?.textContent.trim() || null;
        if (!result.description) result.description = document.querySelector('.seller-description, .about-seller, [class*="seller-bio"], [class*="store-description"]')?.textContent.trim() || null;
        if (!result.rating) {
          const rEl = document.querySelector('[class*="rating"] [class*="value"], [class*="feedback-score"]');
          if (rEl) result.rating = parseFloat(rEl.textContent.replace(/[^0-9.]/g, '')) || null;
        }

        const joinedEl = document.querySelector('[class*="joined"], [class*="member-since"], [class*="since"]');
        if (joinedEl) result.joined = joinedEl.textContent.trim();

        const returnEl = document.querySelector('[class*="return-policy"] p, [class*="returns-policy"]');
        if (returnEl) result.return_policy = returnEl.textContent.trim().slice(0, 300);

        result.url = window.location.href;

        if (!result.name) {
          return JSON.stringify({ error: true, message: 'No seller data found. Ensure this is a seller or merchant profile page.' });
        }
        return JSON.stringify(result);
      } catch(e) {
        return JSON.stringify({ error: true, message: e.message });
      }
    })()
    """
    print(js)


if __name__ == '__main__':
    main()
