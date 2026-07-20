import argparse
import sys


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser(description='Extract eBay item cards from the current search or category page')
    parser.add_argument('--max-items', type=int, default=0,
                        help='Maximum number of items to return from the current page (0 = all cards on page)')
    args = parser.parse_args()

    max_items = args.max_items

    js = f"""
    (function() {{
      try {{
        const cardSel = '.srp-results > li.s-card';
        const cards = Array.from(document.querySelectorAll(cardSel));
        if (cards.length === 0) {{
          return JSON.stringify({{ error: true, message: 'no item cards found (selector=' + cardSel + '); page may not be an eBay search/category result, or DOM changed' }});
        }}

        function cleanText(t) {{
          if (!t) return null;
          return t
            .replace(/Opens in a new window or tab.*/i, '')
            .replace(/Wird in neuem Fenster oder Tab geöffnet.*/i, '')
            .replace(/S['’]ouvre dans une nouvelle fenêtre.*/i, '')
            .replace(/Se abre en una ventana nueva.*/i, '')
            .replace(/Si apre in una nuova finestra.*/i, '')
            .replace(/Wordt geopend in een nieuw venster.*/i, '')
            .replace(/在新的窗口或标签页中打开.*/i, '')
            .replace(/新しいウィンドウまたはタブで開きます.*/i, '')
            .replace(/^\\s*(New Listing|Neues Angebot|Nueva publicación|Nouvelle annonce)\\s*/i, '')
            .trim();
        }}

        function parseNumber(str) {{
          if (!str) return null;
          const m = String(str).replace(/,/g, '').replace(/\\./g, function(match, offset, s) {{
            return (offset === s.lastIndexOf('.') && s.length - offset <= 3) ? '.' : '';
          }}).match(/-?\\d+(?:\\.\\d+)?/);
          return m ? parseFloat(m[0]) : null;
        }}

        function parseCurrency(str) {{
          if (!str) return null;
          const known = ['USD','EUR','GBP','JPY','AUD','CAD','CHF','HKD','SGD','NZD','SEK','NOK','DKK','MXN','BRL','INR','KRW','CNY'];
          for (const c of known) if (str.indexOf(c) >= 0) return c;
          const prefixPairs = [['US $','USD'], ['AU $','AUD'], ['NZ $','NZD'], ['HK $','HKD'], ['SG $','SGD'], ['S$','SGD'], ['C $','CAD'], ['CA $','CAD']];
          for (const p of prefixPairs) if (str.indexOf(p[0]) >= 0) return p[1];
          if (str.indexOf('$') >= 0) return 'USD';
          if (str.indexOf('€') >= 0) return 'EUR';
          if (str.indexOf('£') >= 0) return 'GBP';
          if (str.indexOf('¥') >= 0) return 'JPY';
          return null;
        }}

        const totalHeading = document.querySelector('.srp-controls__count-heading, h1.srp-controls__count-heading')?.textContent?.trim() || null;
        const totalMatch = totalHeading && totalHeading.match(/[\\d,]+/);
        const totalResultsApprox = totalMatch ? parseInt(totalMatch[0].replace(/,/g, ''), 10) : null;

        const nextLinkEl = document.querySelector('a.pagination__next, nav a[rel="next"]');
        const nextPageUrl = nextLinkEl && !nextLinkEl.getAttribute('aria-disabled') ? nextLinkEl.href : null;
        const currentPageMatch = location.href.match(/[?&]_pgn=(\\d+)/);
        const currentPage = currentPageMatch ? parseInt(currentPageMatch[1], 10) : 1;

        const maxItems = {max_items};
        const scanCards = maxItems > 0 ? cards.slice(0, maxItems) : cards;

        const items = scanCards.map(card => {{
          const link = card.querySelector('a.s-card__link');
          const rawHref = link?.href || '';
          const url = rawHref.split('?')[0] || null;
          const itemNumber = card.dataset.listingid || (url && (url.match(/\\/itm\\/(\\d+)/) || [])[1]) || null;

          const titleEl = card.querySelector('.s-card__title .su-styled-text.primary') || card.querySelector('.s-card__title');
          const title = cleanText(titleEl?.textContent);

          const subtitleEls = Array.from(card.querySelectorAll('.s-card__subtitle'));
          const subtitles = subtitleEls.map(e => e.textContent.trim()).filter(Boolean);
          const subtitle = subtitles[0] || null;

          const caption = card.querySelector('.s-card__caption')?.textContent?.trim() || null;

          const priceEl = card.querySelector('.s-card__attribute-row .su-styled-text.positive.bold, .s-card__attribute-row .su-styled-text.bold, .s-card__price');
          const priceWithCurrency = priceEl?.textContent?.trim() || null;
          const price = parseNumber(priceWithCurrency);
          const currency = parseCurrency(priceWithCurrency);

          const wasPriceEl = card.querySelector('.s-card__attribute-row .su-styled-text.strikethrough, .s-card__attribute-row .su-styled-text.negative.strikethrough, .su-styled-text.strikethrough');
          const wasPriceWithCurrency = wasPriceEl?.textContent?.trim() || null;
          const wasPrice = parseNumber(wasPriceWithCurrency);

          const attrRows = Array.from(card.querySelectorAll('.s-card__attribute-row')).map(e => e.textContent.trim());
          const bidsText = attrRows.find(t => /\\bbid|Gebot|encheres|puja|offerte/i.test(t)) || null;
          const bids = bidsText ? (parseNumber(bidsText) || null) : null;
          const shippingText = attrRows.find(t => /shipping|Versand|delivery|livraison|envío|spedizione|verzending|运输|配送/i.test(t)) || null;

          const sellerRawText = card.querySelector('.su-card-container__attributes__secondary')?.textContent?.trim() || null;
          const sellerNameEl = card.querySelector('.su-card-container__attributes__secondary .su-styled-text.primary');
          let seller = sellerNameEl?.textContent?.trim() || null;
          if (!seller && sellerRawText) {{
            const m = sellerRawText.match(/^(.+?)\\s+\\d+(?:\\.\\d+)?%\\s*(?:positive|positiv|positivo|positif)/i);
            if (m) seller = m[1].trim();
          }}
          let sellerFeedbackCount = null;
          let sellerPositiveRating = null;
          if (sellerRawText) {{
            const fbMatch = sellerRawText.match(/\\((\\d[\\d,\\.]*(?:K)?)\\)/i);
            if (fbMatch) {{
              let raw = fbMatch[1].replace(/,/g, '').replace(/\\./g, '');
              if (/K$/i.test(raw)) sellerFeedbackCount = Math.round(parseFloat(raw) * 1000);
              else sellerFeedbackCount = parseInt(raw, 10);
            }}
            const posMatch = sellerRawText.match(/(\\d+(?:\\.\\d+)?)%\\s*(?:positive|positiv|positivo|positif)/i);
            if (posMatch) sellerPositiveRating = parseFloat(posMatch[1]);
          }}

          const reviewsCountRaw = card.querySelector('.s-card__reviews-count')?.textContent?.trim() || null;
          const reviewsCountMatch = reviewsCountRaw && reviewsCountRaw.match(/^(\\d[\\d,]*)/);
          const reviewsCount = reviewsCountMatch ? parseInt(reviewsCountMatch[1].replace(/,/g, ''), 10) : null;
          const starRatingRaw = card.querySelector('.x-star-rating')?.textContent?.trim() || null;
          const starRatingMatch = starRatingRaw && starRatingRaw.match(/(\\d+(?:\\.\\d+)?)/);
          const starRating = starRatingMatch ? parseFloat(starRatingMatch[1]) : null;

          const imgEl = card.querySelector('img.s-card__image') || card.querySelector('img');
          let image = imgEl?.src || null;
          if (image) image = image.replace(/\\/s-l\\d+\\./, '/s-l1600.');

          return {{
            itemNumber,
            url,
            title,
            subtitle,
            caption,
            price,
            priceWithCurrency,
            currency,
            wasPrice,
            wasPriceWithCurrency,
            bids,
            shipping: shippingText,
            seller,
            sellerRawText,
            sellerFeedbackCount,
            sellerPositiveRating,
            reviewsCount,
            starRating,
            image
          }};
        }});

        return JSON.stringify({{
          currentUrl: location.href,
          hostname: location.hostname,
          currentPage,
          nextPageUrl,
          hasNextPage: !!nextPageUrl,
          totalResultsApprox,
          totalResultsRaw: totalHeading,
          itemsOnPage: cards.length,
          returnedCount: items.length,
          items
        }});
      }} catch(e) {{
        return JSON.stringify({{ error: true, message: e.message, stack: (e.stack || '').slice(0, 300) }});
      }}
    }})()
    """
    print(js)


if __name__ == '__main__':
    main()
