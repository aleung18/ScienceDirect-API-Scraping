# ScienceDirect-API-Scraping
Use Elsevier API search and retrieve articles by keyword on ScienceDirect
- Program first makes call to Elsevier's [ScienceDirect_Search_V2 API](https://dev.elsevier.com/search.html) to collect article PII
- Program then makes call to Elsevier's [Article Retrieval API](https://dev.elsevier.com/retrieval.html), with PII as a header

In order to use program, users must generate their own API on ScienceDirect, as well as email Elsevier and request for an Instituional Token.

As of November 2023, program does take a little long to run (approximately 5 minutes for 500 articles)
