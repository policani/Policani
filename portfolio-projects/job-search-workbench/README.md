# Job Search Workbench

Job Search Workbench is a local, single-file tool for job seekers who want to scan many employer career pages without opening each one manually.

It runs in your browser, pulls public job postings from supported employer job-board systems, filters them against your search criteria, and exports a review list to CSV. There is no account, no backend, no API key, and no hosted database.

## Who It Is For

- Job seekers tracking specific roles across many target companies.
- People who want a more precise alternative to generic job alerts.
- Career coaches or mentors helping someone review opportunities.
- Searchers who care about title fit, remote/hybrid/onsite fit, salary range, posting age, and evidence in the job description.

It is not an auto-apply tool, recruiting outreach tool, candidate database, or applicant tracking system.

## What Job Seekers Can Search

The workbench is most useful when your target employers publish jobs through common applicant tracking systems. These systems power many public careers pages, especially at technology companies, software companies, venture-backed startups, remote-first companies, SaaS businesses, and larger organizations with structured recruiting teams.

The app can fetch postings from public job-board endpoints for:

- Greenhouse
- Lever
- Ashby
- SmartRecruiters
- Recruitee
- Himalayas, when its public search endpoint is available

It also creates helper links for sources that should not be treated as direct fetch targets:

- Workday is link-only in this build.
- LinkedIn, Indeed, HiringCafe, and Google are search links only. The app does not scrape those sites.

The best use case is a curated target-company search: add companies you care about, run a scan, then review the ranked results and source-health diagnostics.

## What It Does

- Filters by posting age, work arrangement, country, metro area, salary floor, title keywords, body evidence, and exclusions.
- Routes jobs into Main Candidates, Review Queue, and screened-out diagnostics.
- Shows which sources worked, which were unavailable, and which are link-only.
- Exports Main and Review results to CSV.
- Saves settings only in your browser's local storage.

## How To Use

1. Open `job_search_workbench.html` in a modern desktop browser.
2. Add title keywords, evidence keywords, exclusions, and source lines.
3. Choose posting age, location, work arrangement, and salary floor.
4. Click **Run Search**.
5. Review Main Candidates and Review Queue.
6. Export CSV if you want to work the list elsewhere.

Source format examples:

```text
greenhouse|company-slug
ashby|company-slug
lever|company-slug
recruitee|company-slug
smartrecruiters|CompanySlug
workday|Company|host|tenant|site
himalayas|keyword-search
```

## Source Health and Errors

Some source issues are normal. Companies rename boards, close public endpoints, block browser-origin requests, rate-limit traffic, or use Workday pages that are better handled as links.

Those expected issues do not invalidate the roles fetched from working sources.

Raw run errors are different. They usually mean the app hit an unhandled response shape or bug. A public release should show zero raw run errors in a representative scan.

Current ship-readiness check: after fixing the Lever response parser, a full default-source parser check returned `437` working sources, `34` expected unavailable/link-only sources, and `0` raw run errors.

## Responsible Use

This project is intended for personal job-search triage against public job-posting data. It is closer to a public job-board API client than a traditional webpage scraper because it uses public or documented posting endpoints where available.

That does not make every use risk-free. Public access does not automatically grant unlimited rights to collect, republish, commercialize, or ignore platform terms.

Please keep usage in the lower-risk lane:

- Do not use credentials, cookies, private tokens, or logged-in sessions.
- Do not bypass CAPTCHAs, paywalls, anti-bot systems, rate limits, or access controls.
- Do not auto-apply to jobs.
- Do not use it for spam or recruiting outreach.
- Do not collect candidate personal data.
- Do not bulk republish full job descriptions as a competing job database.
- Keep source lists and run frequency reasonable.

Relevant public references:

- Greenhouse Job Board API: https://developers.greenhouse.io/job-board
- Lever Postings API: https://github.com/lever/postings-api
- Ashby public job posting API: https://developers.ashbyhq.com/docs/public-job-posting-api
- SmartRecruiters API overview: https://developers.smartrecruiters.com/docs/customer-overview

## Privacy

The app has no backend and no account system. Settings are saved in browser local storage on your machine. CSV exports are created locally by your browser.

Do not paste private resumes, credentials, application drafts, or personal candidate data into public source lists or GitHub issues.

## Limitations

- Public job-board APIs change over time.
- Browser CORS behavior can vary by platform and endpoint.
- Salary parsing is best-effort.
- Location classification is heuristic and should be checked before applying.
- Workday is intentionally link-only in this single-file build.

## Suggested GitHub Metadata

Repository description:

> Local-first job search workbench for filtering and ranking public employer job-board postings from Greenhouse, Lever, Ashby, SmartRecruiters, Recruitee, and more.

Suggested topics:

```text
job-search
job-board
ats
greenhouse
lever
ashby
smartrecruiters
recruitee
career-tools
local-first
single-file-app
csv-export
```
