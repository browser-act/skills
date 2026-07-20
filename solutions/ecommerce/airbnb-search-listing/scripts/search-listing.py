import argparse
import sys


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-results', type=int, default=18)  # max items to return from current page
    args = parser.parse_args()

    js = f"""
(function() {{
  try {{
    const sc = Array.from(document.querySelectorAll('script')).find(
      s => s.textContent.includes('niobeClientData') && s.textContent.includes('StaysSearch')
    );
    if (!sc) return JSON.stringify({{error: true, message: 'niobeClientData not found - ensure page is an Airbnb search results page'}});

    const data = JSON.parse(sc.textContent);
    const staysEntry = data.niobeClientData.find(([key]) => key.startsWith('StaysSearch'));
    if (!staysEntry) return JSON.stringify({{error: true, message: 'StaysSearch entry not found in niobeClientData'}});

    const results = staysEntry[1].data.presentation.staysSearch.results;
    const searchResults = results.searchResults || [];
    const pageCursors = results.paginationInfo?.pageCursors || [];

    const maxResults = {args.max_results};
    const items = searchResults.slice(0, maxResults).map(r => {{
      const listing = r.demandStayListing;
      const numericId = listing ? atob(listing.id).split(':')[1] : null;
      return {{
        id: numericId,
        url: numericId ? 'https://www.airbnb.com/rooms/' + numericId : null,
        name: listing?.description?.name?.localizedStringWithTranslationPreference,
        lat: listing?.location?.coordinate?.latitude,
        lng: listing?.location?.coordinate?.longitude,
        rating: r.avgRatingLocalized,
        title: r.title,
        price_total: r.structuredDisplayPrice?.primaryLine?.price,
        price_qualifier: r.structuredDisplayPrice?.primaryLine?.qualifier,
        photos: (r.contextualPictures || []).map(p => p.picture),
        badges: (r.badges || []).map(b => b.text)
      }};
    }});

    return JSON.stringify({{
      items: items,
      count: items.length,
      total_pages: pageCursors.length,
      cursors: pageCursors
    }});
  }} catch(e) {{
    return JSON.stringify({{error: true, message: e.message}});
  }}
}})()
"""
    print(js)


if __name__ == '__main__':
    main()
