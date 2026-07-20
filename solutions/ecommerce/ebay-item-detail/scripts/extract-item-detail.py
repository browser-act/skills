import argparse
import sys


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser(description='Extract full detail data from the currently open eBay item page')
    parser.parse_args()

    js = """
    (function() {
      try {
        const url = location.href;
        const itemMatch = url.match(/\\/itm\\/(\\d+)/);
        if (!itemMatch) {
          return JSON.stringify({ error: true, message: 'current URL does not look like an eBay item page (missing /itm/{id})', url });
        }
        const itemNumber = itemMatch[1];

        const titleEl = document.querySelector('h1.x-item-title__mainTitle .ux-textspans, h1.x-item-title__mainTitle, h1.x-item-title, h1[data-testid="x-item-title"]');
        if (!titleEl) {
          return JSON.stringify({ error: true, message: 'item title not found; page may not be a real item detail (redirected to search, sold-out page, or blocked)', url });
        }
        const title = titleEl.textContent.trim();

        const subTitleEl = document.querySelector('.x-item-title__subTitle .ux-textspans, .x-item-title__subTitle');
        const subTitle = subTitleEl ? subTitleEl.textContent.trim() : null;

        const categorySet = new Set();
        const categoryList = [];
        Array.from(document.querySelectorAll('.breadcrumbs a')).forEach(a => {
          const t = a.textContent.trim();
          if (t && !categorySet.has(t)) {
            categorySet.add(t);
            categoryList.push(t);
          }
        });
        const categories = categoryList;

        function parseNumber(str) {
          if (!str) return null;
          const cleaned = String(str).replace(/[^\\d.,\\-]/g, '');
          if (!cleaned) return null;
          const lastDot = cleaned.lastIndexOf('.');
          const lastComma = cleaned.lastIndexOf(',');
          let normalized;
          if (lastComma > lastDot) {
            normalized = cleaned.replace(/\\./g, '').replace(',', '.');
          } else {
            normalized = cleaned.replace(/,/g, '');
          }
          const n = parseFloat(normalized);
          return isNaN(n) ? null : n;
        }

        function parseCurrency(str) {
          if (!str) return null;
          const known = ['USD','EUR','GBP','JPY','AUD','CAD','CHF','HKD','SGD','NZD','SEK','NOK','DKK','MXN','BRL','INR','KRW','CNY'];
          for (const c of known) if (str.indexOf(c) >= 0) return c;
          const prefixPairs = [['US $','USD'], ['AU $','AUD'], ['NZ $','NZD'], ['HK $','HKD'], ['SG $','SGD'], ['S$','SGD'], ['C $','CAD'], ['CA $','CAD']];
          for (const [p, code] of prefixPairs) if (str.indexOf(p) >= 0) return code;
          if (str.indexOf('$') >= 0) return 'USD';
          if (str.indexOf('€') >= 0) return 'EUR';
          if (str.indexOf('£') >= 0) return 'GBP';
          if (str.indexOf('¥') >= 0) return 'JPY';
          return null;
        }

        const priceEl = document.querySelector('.x-price-primary .ux-textspans, .x-price-primary');
        let priceWithCurrency = priceEl ? priceEl.textContent.trim() : null;
        if (priceWithCurrency) {
          priceWithCurrency = priceWithCurrency
            .replace(/\\s*or\\s+Best\\s+Offer.*/i, '')
            .replace(/\\s*\\(approx\\.?[^)]*\\)/i, '')
            .replace(/\\s+to\\s+.*/i, '')
            .trim();
        }
        const price = parseNumber(priceWithCurrency);
        const currency = parseCurrency(priceWithCurrency);

        const specs = {};
        document.querySelectorAll('.ux-labels-values').forEach(row => {
          const labelEl = row.querySelector('.ux-labels-values__labels');
          const valueEl = row.querySelector('.ux-labels-values__values');
          if (!labelEl || !valueEl) return;
          const label = labelEl.textContent.replace(/:$/, '').trim();
          const value = valueEl.textContent.trim();
          if (label && value && !specs[label]) specs[label] = value;
        });

        const wasPriceWithCurrency = specs['Was'] || specs['UVP'] || specs['Prix conseillé'] || null;
        const wasPrice = parseNumber(wasPriceWithCurrency);

        let itemLocation = specs['Location'] || specs['Standort'] || null;
        if (!itemLocation) {
          const shippingBlock = specs['Shipping'] || specs['Versand'] || '';
          const locMatch = shippingBlock.match(/Located in:?\\s*([^\\.]+?)(?=$|Excludes|Delivery|Estimated|Ships)/i);
          if (locMatch) itemLocation = locMatch[1].trim();
        }

        const conditionRaw = specs['Condition'] || specs['Zustand'] || null;
        let condition = null;
        if (conditionRaw) {
          condition = conditionRaw
            .split(':')[0]
            .replace(/(?:An?\s+item|A\s+brand[-\s]?new|A\s+used|Un\s+item|Ein\s+Artikel|Un\s+articulo).*/i, '')
            .replace(/(?:Read\s+more|Read\s+less|about the condition|about the seller).*/i, '')
            .trim();
        }

        const brand = specs['Brand'] || specs['Marke'] || null;
        const type = specs['Type'] || specs['Model'] || specs['Modell'] || null;
        const mpn = specs['MPN'] || null;
        const upc = specs['UPC'] || null;
        const ean = specs['EAN'] || null;

        const sellerCardAvatar = document.querySelector('.x-sellercard-atf__avatar-info a');
        let seller = null;
        if (sellerCardAvatar) {
          try {
            const meta = sellerCardAvatar.getAttribute('data-clientpresentationmetadata');
            if (meta) {
              const parsed = JSON.parse(meta);
              if (parsed && parsed._ssn) seller = parsed._ssn;
            }
          } catch(e) {}
        }
        if (!seller) {
          const sellerNameEl = document.querySelector('.x-sellercard-atf__info .ux-textspans, .x-sellercard-atf__info a .ux-textspans');
          seller = sellerNameEl ? sellerNameEl.textContent.trim() : null;
        }

        const sellerLinkEl = document.querySelector('.x-sellercard-atf a[href*="/str/"], .x-sellercard-atf a[href*="/usr/"]');
        const sellerUrl = sellerLinkEl ? sellerLinkEl.href.split('?')[0] : null;

        const sellerInfoText = document.querySelector('.x-sellercard-atf__info')?.textContent?.trim() || '';
        let sellerFeedbackCount = null;
        let sellerPositiveRating = null;
        const fbMatch = sellerInfoText.match(/\\(([\\d,\\.]+K?)\\)/i);
        if (fbMatch) {
          let raw = fbMatch[1].replace(/,/g, '').replace(/\\./g, '');
          if (/K$/i.test(raw)) sellerFeedbackCount = Math.round(parseFloat(raw) * 1000);
          else sellerFeedbackCount = parseInt(raw, 10);
        }
        const posMatch = sellerInfoText.match(/(\\d+(?:\\.\\d+)?)%\\s*(?:positive|positiv|positivo|positif)/i);
        if (posMatch) sellerPositiveRating = parseFloat(posMatch[1]);

        const allTextNodes = Array.from(document.querySelectorAll('span, div')).filter(el => el.children.length < 2);
        let soldRaw = null;
        for (const el of allTextNodes) {
          const t = el.textContent.trim();
          if (/^[\\d,]+\\s+sold$/i.test(t) || /^Mehr als [\\d,]+ verkauft$/i.test(t) || /^[\\d,]+\\s+verkauft$/i.test(t)) {
            soldRaw = t;
            break;
          }
        }
        let sold = null;
        if (soldRaw) {
          const m = soldRaw.match(/[\\d,]+/);
          if (m) sold = parseInt(m[0].replace(/,/g, ''), 10);
        }

        let availableText = null;
        for (const el of allTextNodes) {
          const t = el.textContent.trim();
          if (/^(?:More than [\\d,]+ available|[\\d,]+ available|Last one|LAST ONE|More than [\\d,]+ left)$/i.test(t)) {
            availableText = t;
            break;
          }
        }
        let available = null;
        if (availableText) {
          if (/last one/i.test(availableText)) available = 1;
          else {
            const m = availableText.match(/[\\d,]+/);
            if (m) available = parseInt(m[0].replace(/,/g, ''), 10);
          }
        }

        const primaryImgEl = document.querySelector('.ux-image-carousel-item.image-treatment.active img, .ux-image-carousel-item.active img') ||
                             document.querySelector('.ux-image-carousel-item img') ||
                             document.querySelector('img[itemprop="image"]');
        let image = primaryImgEl ? primaryImgEl.src : null;
        if (image) image = image.replace(/\\/s-l\\d+\\./, '/s-l1600.').replace(/s-l\\d+\\.webp$/, 's-l1600.jpg');

        const imageSet = new Set();
        Array.from(document.querySelectorAll('.ux-image-carousel-item img, .ux-image-carousel img, .ux-image-magnify img')).forEach(i => {
          if (i.src) {
            const norm = i.src.replace(/\\/s-l\\d+\\./, '/s-l1600.').replace(/s-l\\d+\\.webp$/, 's-l1600.jpg');
            imageSet.add(norm);
          }
        });
        const images = Array.from(imageSet);

        const shipping = specs['Shipping'] || specs['Versand'] || null;
        const shippingCostMatch = shipping && shipping.match(/(?:US\\s*)?(?:\\$|€|£|C\\s*\\$|AU\\s*\\$)\\s*[\\d.,]+/);
        const shippingCost = shippingCostMatch ? shippingCostMatch[0].trim() : (shipping && /free/i.test(shipping) ? 'Free' : null);

        const whyToBuy = [];
        if (sold) whyToBuy.push(sold + ' sold');
        else if (soldRaw) whyToBuy.push(soldRaw);
        if (shippingCost === 'Free' || (shipping && /free/i.test(shipping))) whyToBuy.push('Free shipping');
        if (available === 1 || (availableText && /last one/i.test(availableText))) whyToBuy.push('Last one');
        if (wasPrice && price && wasPrice > price) {
          const pct = Math.round((1 - price / wasPrice) * 100);
          if (pct > 0) whyToBuy.push(pct + '% off');
        }
        if (sellerPositiveRating && sellerPositiveRating >= 99 && sellerFeedbackCount && sellerFeedbackCount >= 1000) {
          whyToBuy.push('Top-rated seller');
        }

        return JSON.stringify({
          url,
          itemNumber,
          title,
          subTitle,
          categories,
          price,
          priceWithCurrency,
          currency,
          wasPrice,
          wasPriceWithCurrency,
          available,
          availableText,
          sold,
          image,
          images,
          seller,
          sellerUrl,
          sellerFeedbackCount,
          sellerPositiveRating,
          itemLocation,
          brand,
          type,
          mpn,
          upc,
          ean,
          condition,
          shippingCost,
          shipping,
          whyToBuy,
          itemSpecifics: specs
        });
      } catch(e) {
        return JSON.stringify({ error: true, message: e.message, stack: (e.stack || '').slice(0, 300) });
      }
    })()
    """
    print(js)


if __name__ == '__main__':
    main()
