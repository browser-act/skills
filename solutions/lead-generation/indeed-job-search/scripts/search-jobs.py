import argparse
import sys
import json


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-items', type=int, default=0, help='Max items to return, 0 for all')
    args = parser.parse_args()

    max_items = args.max_items

    js = f"""
(async function() {{
  try {{
    const pd = window.mosaic && window.mosaic.providerData;
    if (!pd) return JSON.stringify({{error: true, message: "mosaic.providerData not found - page may not be a valid Indeed search results page"}});
    const jc = pd['mosaic-provider-jobcards'];
    if (!jc) return JSON.stringify({{error: true, message: "mosaic-provider-jobcards not found in providerData"}});
    const model = jc.metaData && jc.metaData.mosaicProviderJobCardsModel;
    if (!model) return JSON.stringify({{error: true, message: "mosaicProviderJobCardsModel not found"}});
    const results = model.results;
    if (!results || results.length === 0) return JSON.stringify({{error: true, message: "No job results found on this page"}});
    const maxItems = {max_items};
    const items = (maxItems > 0 ? results.slice(0, maxItems) : results).map(r => ({{
      id: r.jobkey,
      positionName: r.displayTitle || null,
      company: r.company || null,
      location: r.formattedLocation || null,
      postedAt: r.formattedRelativeTime || null,
      salary: r.salarySnippet ? r.salarySnippet.text : null,
      salaryMin: r.extractedSalary ? r.extractedSalary.min : null,
      salaryMax: r.extractedSalary ? r.extractedSalary.max : null,
      salaryCurrency: r.salarySnippet ? r.salarySnippet.currency : null,
      salaryType: r.extractedSalary ? r.extractedSalary.type : null,
      jobType: r.jobTypes && r.jobTypes.length > 0 ? r.jobTypes : null,
      rating: r.companyRating || null,
      reviewsCount: r.companyReviewCount || null,
      companyLogo: r.companyBrandingAttributes ? r.companyBrandingAttributes.logoUrl : null,
      snippet: r.snippet || null,
      sponsored: !!r.sponsored,
      expired: !!r.expired,
      newJob: !!r.newJob,
      url: r.jobkey ? "https://www.indeed.com/viewjob?jk=" + r.jobkey : null,
      externalApplyLink: r.thirdPartyApplyUrl || null
    }}));
    return JSON.stringify({{pageNumber: model.pageNumber, totalResults: items.length, results: items}});
  }} catch(e) {{
    return JSON.stringify({{error: true, message: e.message}});
  }}
}})()
"""
    print(js)


if __name__ == '__main__':
    main()
