# The Hidden Chapter

One GitHub Pages catalog, organized by niche, with individual book recommendations and explicit Amazon buttons.

- Live site: https://4d1t-codezz.github.io/thehiddenchapter/
- `catalog.json`: six starter books, descriptions, sources, draft posts. Add a verified `amazon_link` per book to use an exact product link. Otherwise the button opens a title-and-author Amazon search with the existing public tracking ID.
- `build_site.py`: generates the home page, 16 shelves, six book pages, About, disclosure, and social-posts.md. Run `python build_site.py`.
- `social-posts.md`: six draft Facebook posts for motivation, Christian, and climate Pages. Review before posting.
- `sync_github.py publish`: commits an allowlisted set of public site files through GitHub's API and updates main without a force push. Requires your existing GitHub CLI authentication. Preserves other repository paths.

Confirm `SITE_TAG` in build_site.py belongs to the Associates account whose owner registers this website and the relevant Facebook Page URLs. No API key is required to build or use this website. No auto-redirects, checkout, price claims, or invented personal reviews.

Future auto-poster drafts can link through the site when website_routing is enabled in the auto-poster configuration. Generated book pages must be published before posts are scheduled. Empty shelves remain explicitly empty until books are added.
