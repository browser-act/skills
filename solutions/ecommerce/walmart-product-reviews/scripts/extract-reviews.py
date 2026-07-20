import argparse
import sys


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    js = r"""
(function() {
  try {
    var data = window.__NEXT_DATA__ && window.__NEXT_DATA__.props && window.__NEXT_DATA__.props.pageProps && window.__NEXT_DATA__.props.pageProps.initialData && window.__NEXT_DATA__.props.pageProps.initialData.data;
    if (!data || !data.reviews) return JSON.stringify({error: true, message: 'No reviews in __NEXT_DATA__. Ensure the page is a Walmart reviews page (walmart.com/reviews/product/...) or product detail page with reviews.'});

    var r = data.reviews;
    var reviews = [];
    var rawReviews = r.customerReviews || [];
    for (var i = 0; i < rawReviews.length; i++) {
      var rev = rawReviews[i];
      var badges = [];
      if (rev.badges) {
        for (var bi = 0; bi < rev.badges.length; bi++) {
          var b = rev.badges[bi];
          if (b.glassBadge && b.glassBadge.text) badges.push(b.glassBadge.text);
        }
      }
      var features = {};
      if (rev.features) {
        for (var fi = 0; fi < rev.features.length; fi++) {
          var f = rev.features[fi];
          if (f.name) features[f.name] = f.value;
        }
      }
      reviews.push({
        reviewId: rev.reviewId,
        rating: rev.rating,
        title: rev.reviewTitle || null,
        text: rev.reviewText || null,
        author: rev.userNickname || null,
        submittedDate: rev.reviewSubmissionTime || null,
        verifiedPurchase: badges.indexOf('Verified Purchase') >= 0,
        helpfulVotes: rev.positiveFeedback || 0,
        notHelpfulVotes: rev.negativeFeedback || 0,
        variantSelected: Object.keys(features).length > 0 ? features : null,
        badges: badges,
        fulfilledBy: rev.fulfilledBy || null,
        sellerName: rev.sellerName || null,
        media: rev.photos && rev.photos.length > 0 ? rev.photos : null
      });
    }

    return JSON.stringify({
      totalReviews: r.totalReviewCount || 0,
      averageRating: r.averageOverallRating || null,
      reviewsOnPage: reviews.length,
      ratingBreakdown: {
        5: r.ratingValueFiveCount || 0,
        4: r.ratingValueFourCount || 0,
        3: r.ratingValueThreeCount || 0,
        2: r.ratingValueTwoCount || 0,
        1: r.ratingValueOneCount || 0
      },
      lookupId: r.lookupId || null,
      reviews: reviews
    });
  } catch(e) {
    return JSON.stringify({error: true, message: e.message});
  }
})()
"""
    print(js)


if __name__ == '__main__':
    main()
