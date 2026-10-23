"""Build the GitHub Pages catalog and Facebook drafts without API calls or secrets."""
import json, re
from pathlib import Path
from html import escape as esc
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parent
BASE="https://4d1t-codezz.github.io/thehiddenchapter"
SITE_TAG="thehiddenchap-20"  # Existing public tracking ID. Confirm ownership before promoting.
NICHES={
 "motivation":("Motivation","Small steps, clearer focus, and ideas for moving forward."),
 "christian":("Christian living","Faith, reflection, and thoughtful questions."),
 "climate":("Climate action","Understand the challenge. Explore the possibilities."),
 "depression":("Gentle reads","Thoughtful reading for difficult days."),
 "school":("School","Study skills and ideas beyond the classroom."),
 "careers":("Work & careers","New perspectives on work and what comes next."),
 "college":("College","Reading for the next chapter of student life."),
 "cooking":("Cooking","Recipes, technique, and stories from the kitchen."),
 "ai":("Artificial intelligence","Understand the ideas behind the technology."),
 "science":("Science & innovation","For curious minds and bigger questions."),
 "tech":("Technology","The people and systems shaping the digital world."),
 "finance":("Personal finance","Books about money, explained plainly."),
 "feminism":("Feminism","Perspectives on equality, history, and society."),
 "retirement":("Retirement","Make room for a new season of life."),
 "gardening":("Gardening","Grow your knowledge, indoors and out."),
 "philosophy":("Philosophy","Big questions. A little room to think.")}
BOOKS=json.loads((ROOT/"catalog.json").read_text(encoding="utf-8"))["books"]
def write(path,content):
 p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding="utf-8")
def layout(title,body,path="index.html",depth=0,description="Thoughtful book recommendations for your next chapter.",extra=""):
 pre="../"*depth
 canonical=BASE+"/"+path
 matched=next((b for b in BOOKS if path=="books/"+b["slug"]+".html"),None)
 if matched:
  image_url=BASE+"/"+matched["cover"]
  extra += f'<meta property="og:image" content="{image_url}"><meta property="og:image:alt" content="{esc(matched["title"],quote=True)} book cover"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{image_url}">'

 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | The Hidden Chapter</title><meta name="description" content="{esc(description,quote=True)}"><meta property="og:title" content="{esc(title,quote=True)}"><meta property="og:description" content="{esc(description,quote=True)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><link rel="canonical" href="{canonical}"><link rel="stylesheet" href="{pre}style.css">{extra}</head><body><a class="skip" href="#main">Skip to content</a><header><div class="wrap bar"><a class="brand" href="{pre}index.html"><span class="mark" aria-hidden="true">H<span>C</span></span>The Hidden Chapter</a><nav aria-label="Main navigation"><a href="{pre}index.html#browse">Browse the shelves</a><a href="{pre}about.html">Our approach</a></nav></div></header><main id="main">{body}</main><footer><div class="wrap"><div class="footer-top"><a class="brand" href="{pre}index.html">The Hidden Chapter<span class="dot">.</span></a><span>A little curiosity goes a long way.</span></div><p>As an Amazon Associate I earn from qualifying purchases. Amazon links may earn us a commission.</p><div class="footer-bottom"><span>AI-assisted book guides. No invented personal reviews.</span><a href="{pre}disclosure.html">Affiliate disclosure & privacy</a><span>© 2026 The Hidden Chapter</span></div></div></footer></body></html>'''
def cover(b,cls="",pre=""):
 return f'''<div class="book-art real-cover {cls}"><img src="{pre}{esc(b['cover'],quote=True)}" alt="{esc(b['title'],quote=True)} — {esc(b['author'],quote=True)}, {b['format'].lower()} cover" decoding="async" width="300" height="450"></div>'''
def card(b,pre=""):
 return f'''<article class="book-card" data-title="{esc((b['title']+' '+b['author']).lower(),quote=True)}" data-niche="{b['niche']}"><a class="art-link" href="{pre}books/{b['slug']}.html" tabindex="-1" aria-hidden="true">{cover(b,pre=pre)}</a><div class="book-copy"><span class="label">{NICHES[b['niche']][0]}</span><h3><a href="{pre}books/{b['slug']}.html">{esc(b['title'])}</a></h3><p class="byline">{esc(b['author'])}</p><p>{esc(b['summary'])}</p><a class="text-link" href="{pre}books/{b['slug']}.html">Read the recommendation <span aria-hidden="true">↗</span></a></div></article>'''
def build():
 features=''.join(card(b) for b in BOOKS)
 shelves=''.join(f'<a class="shelf" href="niches/{key}.html"><span>{i:02}</span><strong>{esc(name)}</strong><span aria-hidden="true">↗</span></a>' for i,(key,(name,_)) in enumerate(NICHES.items(),1))
 options=''.join(f'<option value="{key}">{name}</option>' for key,(name,_) in NICHES.items())
 home=f'''<section class="hero wrap"><div><span class="eyebrow">A SHELF FOR EVERY SIDE OF YOU</span><h1>Find your<br>next <em>chapter.</em></h1><p class="hero-copy">Books for the things you care about. Explore ideas, discover a different perspective, and find a read that fits your life.</p><a class="btn" href="#browse">Explore the shelves <span aria-hidden="true">↗</span></a><p class="hero-note">Thoughtful recommendations. Room for your own opinion.</p></div><div class="hero-art" aria-label="Selections from the reading shelf">{cover(BOOKS[4],'hero-one')}{cover(BOOKS[0],'hero-two')}{cover(BOOKS[2],'hero-three')}<span class="art-caption">GOOD IDEAS LIVE BETWEEN THE COVERS.</span></div></section><div class="strip"><div class="wrap">Less endless scrolling. <em>More finding something worth reading.</em></div></div><section class="wrap section" id="browse"><div class="section-heading"><div><span class="eyebrow">THE READING ROOM</span><h2>A few good places to start.</h2></div><p>What it covers. Who it suits.<br>What to know before you choose.</p></div><form class="filters" role="search" onsubmit="return false"><label>Find a book<input type="search" id="search" placeholder="Search title or author…"></label><label>Your interest<select id="niche"><option value="all">All shelves</option>{options}</select></label><span id="count" role="status" aria-live="polite">6 recommendations</span></form><div class="book-grid" id="catalog">{features}</div><div id="empty" class="empty" hidden>No books match that search yet. Try another title or shelf.</div></section><section class="shelves-section"><div class="wrap section"><div class="section-heading"><div><span class="eyebrow">FOLLOW YOUR CURIOSITY</span><h2>One reading room.<br>Many different shelves.</h2></div><p>Start with motivation, faith, or climate.<br>More recommendations will join the shelves.</p></div><div class="shelves">{shelves}</div></div></section><section class="wrap editorial section"><span class="eyebrow">A NOTE FROM THE SHELF</span><h2>A recommendation,<br>not a promise.</h2><p>We explain what a book offers and where it may fall short. Our guides use AI assistance and published book information; they do not pretend to be personal reading experiences.</p><a class="text-link" href="about.html">How we put the shelves together ↗</a></section>'''
 write('index.html',layout('Find your next chapter',home,extra='<script defer src="catalog.js"></script>'))
 for key,(name,desc) in NICHES.items():
  picks=[b for b in BOOKS if b['niche']==key]
  contents=''.join(card(b,'../') for b in picks) if picks else '<div class="empty"><h2>This shelf is taking shape.</h2><p>There are no recommendations here yet. Explore the current reading room while we add more.</p><a class="btn" href="../index.html#browse">Explore available books ↗</a></div>'
  body=f'<section class="wrap section"><a class="breadcrumb" href="../index.html#browse">← All shelves</a><span class="eyebrow">THE {esc(name.upper())} SHELF</span><h1>{esc(name)}<span class="dot">.</span></h1><p class="lead">{esc(desc)}</p><div class="book-grid niche-grid">{contents}</div></section>'
  write(f'niches/{key}.html',layout(name,body,f'niches/{key}.html',1,desc))
 for b in BOOKS:
  query=urlencode({'k':b['title']+' '+b['author'],'i':'stripbooks','tag':SITE_TAG})
  link=b.get('amazon_link') or 'https://www.amazon.com/s?'+query
  from urllib.parse import urlparse
  u=urlparse(link)
  if u.scheme!='https' or not (u.hostname in ('amazon.com','www.amazon.com','amzn.to') or (u.hostname or '').endswith('.amazon.com')): raise ValueError('Expected an HTTPS Amazon link')
  related=''.join(card(other,'../') for other in BOOKS if other['niche']==b['niche'] and other!=b)
  body=f'''<section class="wrap section"><a class="breadcrumb" href="../niches/{b['niche']}.html">← {NICHES[b['niche']][0]}</a><div class="detail"><div class="detail-art">{cover(b,pre="../")}<p class="small">{b["format"]} · ISBN {b["isbn"]}<br><a href="{esc(b["cover_source"],quote=True)}">Publisher cover image</a></p></div><div><span class="eyebrow">{b['eyebrow']}</span><h1>{esc(b['title'])}</h1><p class="author">{esc(b['author'])}</p><p class="lead">{esc(b['summary'])}</p><div class="buy-box"><p class="small">Affiliate link · As an Amazon Associate I earn from qualifying purchases.</p><a class="btn" rel="sponsored noopener" href="{esc(link,quote=True)}">View this edition on Amazon ↗</a><p class="small">Links to the pictured edition. Confirm the selected format, availability, price, and seller on Amazon. Cover designs can vary between printings.</p></div></div></div><div class="review-body"><span class="eyebrow">BEFORE YOU CHOOSE</span><h2>What’s inside</h2><p>{esc(b['about'])}</p><div class="fit-grid"><div><h3>A good fit for</h3><p>{esc(b['suits'])}</p></div><div><h3>Worth knowing</h3><p>{esc(b['skip'])}</p></div></div><blockquote>{esc(b['takeaway'])}</blockquote><p class="small">AI-assisted overview based on published book information, not a firsthand review. <a href="{esc(b['source'],quote=True)}" rel="noopener">Source information ↗</a></p></div></section><section class="wrap section"><h2>On the same shelf</h2><div class="book-grid niche-grid">{related}</div></section>'''
  write(f"books/{b['slug']}.html",layout(b['title'],body,f"books/{b['slug']}.html",1,b['summary']))
 for name,title,content in [
 ('about','Our approach','<p>The Hidden Chapter is a reading room organized around interests: motivation, Christian living, climate action, and more. We publish short guides that explain what a book covers, who it may suit, and reasons to choose something else.</p><h2>How the guides are made</h2><p>Guides are drafted with AI assistance using published information about the books. Source links appear on individual book pages. These are informational overviews, not claims that someone on this site has personally read or tested every book.</p><h2>Choosing a book is personal</h2><p>We do not invent reader testimonials, star ratings, or personal transformation stories. Some shelves are still empty as the collection grows. Book images are real publisher covers identified by ISBN. Cover artwork belongs to its respective rights holders; designs may vary between printings.</p><h2>Where the links lead</h2><p>We do not sell books or take payments. Amazon handles availability, editions, prices, purchases, delivery, and returns. You choose whether to click through.</p>'),
 ('disclosure','Affiliate disclosure & privacy','<p><strong>As an Amazon Associate I earn from qualifying purchases.</strong></p><p>Links labeled as affiliate links may earn a commission when you make a qualifying purchase. This does not add an extra charge to your purchase. Affiliate relationships do not guarantee that a book will suit you.</p><h2>Amazon links</h2><p>Buttons take you to Amazon only when you click them. Current book buttons link to an edition identified by ISBN. Amazon may offer other formats on the same listing. Check the listing before buying; pricing and availability are controlled by Amazon. This site is independently operated and is not Amazon.</p><h2>Privacy</h2><p>This static website has no account system, contact form, advertising scripts, or analytics installed by us. Search and shelf filters run in your browser. The stylesheet requests fonts from Google Fonts, which may receive technical request information such as your IP address. The hosting provider, GitHub Pages, may process technical request information under its own privacy policy. After clicking an external link, that service’s privacy practices apply.</p><p><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub privacy statement</a> · <a href="https://www.amazon.com/gp/help/customer/display.html?nodeId=GX7NJQ4ZB8MHFRNJ">Amazon privacy notice</a></p>')]:
  write(name+'.html',layout(title,f'<section class="wrap section prose"><span class="eyebrow">THE HIDDEN CHAPTER</span><h1>{title}</h1>{content}</section>',name+'.html'))
 posts=['# Facebook post drafts','These six drafts are ready for your review and manual posting. They have not been published to Facebook. Each links to a specific recommendation page. Download the matching JPG from [the image library]('+BASE+'/post-images.html). Attach the image when composing the post.']
 for b in BOOKS:
  url=BASE+'/books/'+b['slug']+'.html'
  posts += ['## '+NICHES[b['niche']][0]+' — '+b['title'], '![Actual book cover]('+BASE+'/'+b['cover']+')\n\n[Download matching JPG]('+BASE+'/'+b['cover']+')',b['post']+'\n\n'+url+'\n\n#ad · The linked page contains Amazon affiliate links. As an Amazon Associate I earn from qualifying purchases.']
 write('social-posts.md','\n\n'.join(posts)+'\n')
 tiles=''.join(f'<article class="book-card"><div class="art-link">{cover(b)}</div><h2>{esc(b["title"])}</h2><p class="small">{b["format"]} · ISBN {b["isbn"]}</p><a class="btn" href="{b["cover"]}" download="{b["slug"]}.jpg">Download JPG ↓</a><p class="small"><a href="{esc(b["cover_source"],quote=True)}">Publisher image source</a></p></article>' for b in BOOKS)
 gallery='<section class="wrap section"><span class="eyebrow">FACEBOOK IMAGE LIBRARY</span><h1>The actual books.</h1><p class="lead">Use the matching publisher cover with each draft. These are the same images shown on the website.</p><p><a class="btn" href="facebook-images.zip" download>Download all six covers ↓</a></p><p class="small">Cover artwork belongs to its respective publishers and rights holders.</p><div class="book-grid niche-grid">'+tiles+'</div></section>'
 write('post-images.html',layout('Book images for posts',gallery,'post-images.html'))
 import zipfile
 with zipfile.ZipFile(ROOT/'facebook-images.zip','w',zipfile.ZIP_DEFLATED) as bundle:
  for b in BOOKS: bundle.write(ROOT/b['cover'],b['slug']+'.jpg')

 write('posts/atomic-habits.html',(ROOT/'books/atomic-habits.html').read_text(encoding='utf-8'))
 write('.nojekyll','')
 write('README.md',"""# The Hidden Chapter

One GitHub Pages catalog, organized by niche, with individual book recommendations and explicit Amazon buttons.

- Live site: https://4d1t-codezz.github.io/thehiddenchapter/
- `catalog.json`: six starter books, descriptions, sources, draft posts. Each book includes a publisher cover, ISBN, edition-specific Amazon link, and original image source.
- `build_site.py`: generates the home page, 16 shelves, six book pages, About, disclosure, and social-posts.md. Run `python build_site.py`.
- `social-posts.md`: six Facebook drafts with matching image links.
- `post-images.html`: downloadable cover library; `facebook-images.zip` contains all six original JPGs.
- `assets/covers/`: unmodified publisher cover images. Sources and ISBNs are recorded in catalog.json.
- `sync_github.py publish`: commits an allowlisted set of public site files through GitHub's API and updates main without a force push. Requires your existing GitHub CLI authentication. Preserves other repository paths.

Confirm `SITE_TAG` in build_site.py belongs to the Associates account whose owner registers this website and the relevant Facebook Page URLs. No API key is required to build or use this website. No auto-redirects, checkout, price claims, or invented personal reviews.

Future auto-poster drafts can link through the site when website_routing is enabled in the auto-poster configuration. Generated book pages must be published before posts are scheduled. Empty shelves remain explicitly empty until books are added.
""")
 print(f'Built {len(BOOKS)} book pages, {len(NICHES)} niche shelves, and six Facebook drafts.')
if __name__=='__main__': build()
