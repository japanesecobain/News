"""Build the claim adjudication ledger, corrected registers, permission gates, Amazon lifecycle scope,
source additions and verification queue. Data only; no network access.

pass_type vocabulary:
  first_pass_independent   - a researcher's original run, before shared feedback
  feedback_derived         - a correction made after reviewer feedback (not independent corroboration)
  reviewer_finding         - the reviewer's own check (a lead to test, not authority)
  cla_consolidation_check  - CLA's check in this pass (search extract or local computation)
disposition vocabulary:
  retained_constraint | retained_rescoped | rejected_inference | unresolved_dependency | excluded_from_decision | superseded_within_scope
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
T1 = "2026-10-04 (UTC) first pass"
T2 = "2026-10-04T21:45-22:00Z (=2026-10-05 06:45-07:00 JST) consolidation"

LEDGER_HEADER = ["adj_id", "topic", "researcher_ids", "pass_type", "original_assertion", "adjudicated_proposition", "disposition",
                 "publisher", "url", "page_section", "source_family", "publication_date", "event_or_effective_date", "data_period",
                 "cla_access_mode", "cla_access_at", "country_product_scope", "evidence_origin", "claim_status",
                 "support_or_counter", "inference_allowed", "inference_rejected", "decision_implication", "unresolved_boundary", "verification_queue_id"]

# Rows: tuples in LEDGER_HEADER order
L = [
    # ---------------- Permission / operating path ----------------
    ("ADJ-01", "Amazon delegated on-behalf ordering", "GRO-C034 (v2); reviewer retrieval; CLA-C003/C004 (first pass)", "feedback_derived + reviewer_finding",
     "CLA v1: Amazon blocks/litigates unauthorised agents (US). GRO v2: co.jp policies URL returned English Program Policies (updated 2026-04-14), Participation Requirements 6(k) prohibits orders on behalf of another person.",
     "Retrieved English text prohibits Associates from placing orders on behalf of others if that text is operative for Amazon.co.jp; the Japanese operating agreement has not been read by any researcher. Treat delegated Amazon execution as excluded from the current investment case.",
     "retained_constraint", "Amazon", "https://affiliate.amazon.co.jp/help/operating/policies/", "Participation Requirements 6(k) (per GRO and reviewer)", "Amazon Associates policy",
     "2026-04-14 (as returned)", "", "", "not accessed (egress 403); relies on GRO/reviewer retrieval of the same page", T2, "Amazon Associates; locale unreconciled",
     "official/first-party", "directly observed text by GRO; locale/applicability unresolved", "counter to delegated execution revenue",
     "Exclude delegated Amazon execution revenue now", "Japan-wide prohibition of all agents; prohibition of user-placed purchases via links; measured zero opportunity",
     "Do not book or test on-behalf Amazon execution", "Japanese operative terms; applicability to user-placed purchases", "VQ-01"),
    ("ADJ-02", "Amazon user-placed purchase via link on a personal-assistant surface", "CLA v1 model (C03 coverage assumed eligible)", "cla_consolidation_check",
     "CLA v1 C03 model assumed Amazon referrals were eligible across the assistant interface (coverage 0.75).",
     "Eligibility of Amazon affiliate links shown inside a private/one-to-one assistant surface is unresolved: Japanese agreement and surface rules unread. Exclude from investment case; keep as conditional revenue only.",
     "rejected_inference", "Amazon", "https://affiliate.amazon.co.jp/help/operating/policies/", "not read", "Amazon Associates policy", "", "", "",
     "not accessed", T2, "Amazon.co.jp Associates", "official/first-party (unread)", "unknown", "n/a",
     "Model C03 Amazon revenue only as 'if approved'", "That merchant-hosted checkout makes the referral eligible", "C03 booked revenue = rule zero under current gates", "Surface rules; Creators API threshold", "VQ-01"),
    ("ADJ-03", "Rakuten affiliate distribution via closed / one-to-one tools", "Reviewer finding; CLA search extract; GRO-C035 (other clauses)", "reviewer_finding + cla_consolidation_check",
     "Not in CLA v1 (CLA v1 treated affiliate links as available).",
     "Rakuten's guideline (updated 2025-06-26) prohibits sharing affiliate links via email, LINE, SNS DMs and other tools viewable only by specific people (incl. LINE official accounts, Open Chat, Discord, Chatwork), except for Rakuten-approved corporate partners, and prohibits automated distribution of links to such channels.",
     "retained_constraint", "Rakuten Group", "https://affiliate.rakuten.co.jp/guideline/rule/ ; https://affiliate.faq.rakuten.net/detail/000015637", "guideline sections on closed tools (search extract)", "Rakuten Affiliate guideline",
     "2025-06-26 (update)", "", "", "search extract only (page fetch 403)", T2, "Rakuten Affiliate, Japan", "official/first-party", "publisher-reported (extract)", "counter to C03 revenue on a personal-assistant surface",
     "A personal assistant cannot book Rakuten affiliate revenue without corporate-partner approval", "That all comparison products are barred; that a non-affiliate link is restricted",
     "C03 booked revenue excluded; approval route is a named dependency", "Exact wording; whether an in-app logged-in UI counts as a closed tool; partner criteria", "VQ-02;VQ-03"),
    ("ADJ-04", "Rakuten window, caps, competing-service clause", "GRO-C035 (v2, directly observed); CLA-C090 (v1, secondary)", "feedback_derived",
     "CLA v1: 24h cart + 89-day purchase; rates 2-4% (secondary). GRO v1 treated window as secondary-only.",
     "Guideline states 24h cart and 89-day completion; ordinary caps JPY 1,000 per item and JPY 3,000 per 'user-month' (basis unresolved) with a rate-up exception; prohibits using the programme to provide a competing or potentially competing service; prohibits results without a click.",
     "retained_constraint", "Rakuten Group", "https://affiliate.rakuten.co.jp/guideline/rule/", "rules (per GRO)", "Rakuten Affiliate guideline", "2025-06-26", "", "",
     "not accessed; GRO observation + CLA search extract on caps", T2, "Rakuten Affiliate, Japan", "official/first-party", "directly observed by GRO", "counter (caps, competing-service risk)",
     "Apply per-item cap once in C03 maths", "That the competing-service clause bans comparison generally", "Competing-service clause may be decisive for a comparison product", "JPY 3,000 basis; clause scope", "VQ-02"),
    ("ADJ-05", "Consumer order-history APIs at Amazon/Rakuten/Yahoo", "CLA-C007, CLA-C008 (first pass)", "first_pass_independent",
     "CLA v1: no consumer-authorised order API found; merchant APIs are seller-scoped.",
     "No consumer-authorised order-history API was found within CLA's search. This is 'no path found', not a clause prohibiting access.",
     "retained_rescoped", "Rakuten; LY Corp", "https://webservice.rakuten.co.jp ; https://developer.yahoo.co.jp/webapi/shopping/", "API catalogues (search summaries)", "Platform developer docs",
     "", "", "", "search summary", T1, "Rakuten Ichiba, Yahoo! Shopping", "official/first-party", "inference (negative finding)", "counter to API-based ingestion",
     "Use user-supplied records for discovery", "That no partner path could ever exist", "Do not plan API ingestion", "Partner programmes not explored", ""),
    ("ADJ-06", "Execution 'no permitted path in Japan'", "CLA v1 report section 3.2 conclusion", "cla_consolidation_check",
     "CLA v1: execution, payment, order APIs and delivery changes have no permitted third-party path.",
     "Rescoped: no CONNECTED permitted execution path was established for the intended cross-merchant task among the researched surfaces. Standalone merchants and wallets were not researched; merchant-hosted checkout handoff exists.",
     "rejected_inference", "", "", "", "", "", "", "", "self-audit", T2, "Japan; researched surfaces only", "inference", "inference", "n/a",
     "Execution remains unapproved until one connected path is documented", "'No path anywhere in Japan'", "Permitted-path memo is the only checkout follow-on", "Standalone merchants, wallets, Shopify JP", "VQ-04;VQ-05"),
    ("ADJ-07", "Carrier delivery-change authority", "CLA-C017, C019, C020 (first pass)", "first_pass_independent",
     "Carriers tie delivery changes to their own identity (Kuroneko Members/LINE, Smart Club, ゆうID); shipper APIs are B2B.",
     "Retained: changes are performed by the consignee on carrier channels; no third-party delegation path found. Not a prohibition finding (member terms unread).",
     "retained_rescoped", "Yamato; Sagawa; Japan Post", "kuronekoyamato.co.jp; sagawa-exp.co.jp; post.japanpost.jp", "help/LINE pages (search summaries)", "Carrier first-party", "", "", "",
     "search summary", T1, "JP carriers", "official/first-party", "company-reported", "counter to C01 change features", "Handoff to carrier channel", "Third parties can never be authorised", "Coordination value must come without change authority", "Member terms", "VQ-16"),
    ("ADJ-08", "3-D Secure vs scraping/permission", "CLA-C023 (first pass); GEM correction (as described by reviewer); reviewer (EMVCo)", "first_pass_independent + feedback_derived + reviewer_finding",
     "CLA v1: EMV 3DS required in principle at EC merchants (guideline). GEM: '3DS 2.0 blocks headless scraping'.",
     "3DS is issuer-side payment authentication (frictionless or challenge). It does not govern catalogue scraping or grant merchant permission. Chain: data access -> merchant/platform permission -> transaction preparation -> customer approval -> payment authentication -> merchant acceptance.",
     "retained_rescoped", "EMVCo; JP Credit Card Security Council (via secondary)", "https://www.emvco.com/knowledge-hub/optimising-online-payment-authentication-with-emv-3-d-secure/ ; https://www.businesslawyers.jp/articles/1447", "", "Payment authentication standard", "", "2025-03-31 (JP guideline target)", "",
     "not accessed (EMVCo: reviewer); JP guideline: search summary", T1, "Card payments, Japan", "official + secondary", "publisher-reported", "neutral",
     "Authentication must be handled within a permitted integration", "'3DS blocks headless scraping'; 'authentication proves universal infeasibility'", "Remove 3DS as an infeasibility argument", "", "")
    ,
    ("ADJ-09", "Japan agent-payment readiness", "CLA-C024/C025 (first pass); CLA consolidation search", "first_pass_independent + cla_consolidation_check",
     "CLA v1: Mastercard first JP production agentic transaction 2026-05-20 (pilot); Visa JP timing unknown; re-open checkout when 'any two' announcements fire.",
     "Visa 'Agentic Ready' (release 2026-04-30) is an issuer-readiness programme in 10 APAC markets with five named Japanese issuers (SB Payment Service, Credit Saison, Sumitomo Mitsui Card, MUFG NICOS, Rakuten Card); Visa Intelligent Commerce APAC pilots were announced for early 2026 (release 2025-11-17). These are controlled programmes: not merchant coverage, not startup eligibility, not scaled transactions.",
     "retained_rescoped", "Visa Worldwide Japan; Mastercard Japan", "https://www.visa.co.jp/about-visa/newsroom/press-releases/nr-jp-260430-2.html ; https://www.visa.co.jp/about-visa/newsroom/press-releases/nr-jp-251117.html ; mastercard.com/jp 2026/may", "release text (search extracts)", "Card networks", "2026-04-30; 2025-11-17; 2026-05-20", "", "",
     "search extract only", T2, "Japan issuers; agent payments", "official/first-party", "company-reported", "weak support for future feasibility",
     "Issuer readiness is emerging", "That a startup can execute payments today; that merchants accept agent tokens", "Replace 'any two announcements' with one connected permitted path for the intended task", "Startup eligibility; merchant acceptance; transaction volumes", "VQ-07"),
    ("ADJ-10", "UCP vs Universal Cart; Japan availability", "CLA-C026 (first pass); GEM correction; reviewer", "first_pass_independent + feedback_derived + reviewer_finding",
     "CLA v1: UCP checkout US live May 2026; JP not provided as of Jul 2026 (Japanese secondary).",
     "UCP (protocol) announced 2026-01-11; Universal Cart (consumer product) May 2026, US-first with supported checkout and merchant handoff. Japan availability not established - a bounded availability finding, not a durable local advantage.",
     "retained_rescoped", "Google", "https://developers.googleblog.com/under-the-hood-universal-commerce-protocol-ucp/", "", "Google UCP", "2026-01-11 (UCP); 2026-05 (Universal Cart)", "", "",
     "not accessed (403); dates per reviewer + CLA search summaries", T2, "US-first; JP not established", "official/first-party", "company-reported", "neutral",
     "Treat as availability fact", "That the gap is an asset or will persist", "No acceleration rationale", "Japan timing", "VQ-19"),
    ("ADJ-11", "OpenAI checkout change", "CLA-C027 (first pass); GRO-C036 (v2); GEM (4% fee); reviewer", "first_pass_independent + feedback_derived + reviewer_finding",
     "CLA v1: Instant Checkout retired early Mar 2026 after ~a dozen Shopify merchants. GEM: 4% launch fee.",
     "OpenAI's 2026-03-24 product-discovery page (extract) says initial Instant Checkout lacked desired flexibility; merchants may use their own checkout; Walmart builds an in-ChatGPT experience with account linking. This narrows generic in-chat checkout; it does not show chat interfaces are impossible or consumers reject them.",
     "retained_rescoped", "OpenAI", "https://openai.com/index/powering-product-discovery-in-chatgpt/ ; https://openai.com/index/buy-it-in-chatgpt/", "", "OpenAI commerce", "2025-09-29; 2026-03-24", "", "",
     "not accessed; GRO search extract", T2, "US; not Japan", "official/first-party", "company-reported (extract)", "narrow counter to generic in-chat checkout",
     "Deprioritising generic in-chat checkout is a decision", "~dozen-merchant count (third-party); exact 4% historical fee; universal demand rejection", "No generic in-chat checkout build", "Japan; retention", "VQ-13"),
    ("ADJ-12", "Shopify ChatGPT channel fees and scope", "Reviewer finding", "reviewer_finding",
     "Not in CLA v1 (CLA v1 noted Agentic Storefronts are US-buyer-focused).",
     "Shopify's ChatGPT channel routes buyers to merchant-hosted checkout with no additional selling fee beyond payment processing; eligibility is U.S.-customer-facing.",
     "retained_rescoped", "Shopify", "https://help.shopify.com/en/manual/online-sales-channels/agentic-storefronts/chatgpt", "", "Shopify help", "", "", "",
     "not accessed (403)", T2, "US customers; Shopify", "official/first-party", "reviewer-observed", "neutral",
     "A specific documented channel exists", "Generalising to all integrations, geographies or history", "Not a Japan path", "", "VQ-12"),
    ("ADJ-13", "Gmail restricted scopes and CASA cost", "CLA-C010/C011/C013 (first pass); GEM ($540, viable); reviewer (Google FAQ)", "first_pass_independent + feedback_derived + reviewer_finding",
     "CLA v1: restricted scopes; 'package delivery tracking' is a permitted app type; TAC list USD 540-720/yr (search summary). GEM: ~$540 so inbox parsing is viable.",
     "Assessment requirement is tied to restricted scopes with server-side storage/transmission; Google does not charge the fee; assessor pricing and tier depend on architecture. The USD 540-720 figure is one assessor's list price at search-summary level (likely the same source family as GEM's). A quote is not a compliance budget and does not establish viability.",
     "retained_rescoped", "Google; TAC Security", "https://developers.google.com/workspace/gmail/api/auth/scopes ; https://tacsecurity.com/esof/", "", "Google API policy; assessor pricing", "", "", "",
     "search summary (Google pages 403)", T1, "Global", "official/first-party + vendor", "publisher-reported (extract)", "neutral",
     "OAuth ingestion is permissible in principle for tracking", "'Cheap and viable'; 'expensive and impossible'", "No OAuth in discovery; cost ingestion per architecture later", "Engineering/remediation and recurring cost", "VQ-11"),
    ("ADJ-14", "Gmail Limited Use", "CLA-C012 (first pass)", "first_pass_independent",
     "Limited Use bars ad/sale use and transfer of restricted-scope data and derived data.",
     "Retained for any Gmail-API design; does not apply to user-forwarded mail (other obligations apply).", "retained_rescoped", "Google",
     "https://developers.google.com/terms/api-services-user-data-policy", "", "Google API policy", "", "", "", "search summary", T1, "Gmail API", "official/first-party", "publisher-reported", "counter to data monetisation",
     "Data resale is not a business model for Gmail-sourced data", "", "", "", "VQ-11"),
    ("ADJ-15", "A8 participant role", "GEM correction; reviewer", "feedback_derived + reviewer_finding",
     "GEM v1 applied advertiser fixed costs to a publisher startup (per reviewer).",
     "A8 distinguishes advertisers from free media members; advertiser costs do not apply to a startup earning publisher commissions. CLA v1 model contained no A8 advertiser cost. Bank-transfer fee details are immaterial and not inherited.",
     "retained_constraint", "FAN Communications (A8.net)", "https://www.a8.net/", "", "ASP", "", "", "", "not accessed", T2, "A8 publisher role", "official/first-party", "reviewer-observed", "neutral",
     "Remove advertiser fees from publisher models", "Fee trivia", "None for CLA model", "Surface rules for private distribution", "VQ-05"),
    # ---------------- Demand / substitutes ----------------
    ("ADJ-16", "Visa Japan delegation survey", "CLA-C078 (first pass); CLA consolidation search; reviewer flag", "first_pass_independent + cla_consolidation_check",
     "CLA v1 evidence plan: falsifier 'majority refusal to delegate'; marked spending authority 'falsified' on 27% refusal; cited '~1% auto-purchase' headline unverified.",
     "Sample: 4,120 people aged 20s-60s who use cashless payment, have no resistance to generative AI and use it at least monthly (Macromill, June 2026; Visa release 2026-08-17). If accuracy concerns were resolved: ~27% would not entrust AI with any purchasing step; ~5% would let AI add to cart with their own confirmation; ~1% would allow purchase without confirmation. Whether all shares use the full 4,120 base, and the wording of the other options, were not verified. 27% is not a majority, so CLA's own falsifier was NOT met.",
     "retained_rescoped", "Visa Worldwide Japan (via secondary)", "https://news.mynavi.jp/article/20260817-4830173/ ; https://www.commercepick.com/archives/100589 ; https://paymentnavi.com/paymentnews/180587.html", "chart values per secondary extracts", "Visa survey (one family)", "2026-08-17", "", "2026-06 fieldwork",
     "search extracts", T2, "Japan; AI-friendly cashless users (not population)", "company-sponsored survey", "company-reported", "adverse signal for execution delegation; not refusal majority",
     "Execution-level delegation is rare in an AI-friendly sample", "Majority refusal; treating the ~67% non-refusers as adopters of any product", "H03b -> UNRESOLVED (adverse signal)", "Base per chart; option wording; population generalisation", "VQ-06"),
    ("ADJ-17", "Criteo awareness survey", "CLA-C079 (first pass)", "first_pass_independent",
     "Japan lowest awareness of agentic shopping assistants among 7 countries (Oct-Dec 2025).", "Retained as low-weight context (sponsor, awareness not demand).", "excluded_from_decision",
     "Criteo (via travelvoice)", "https://www.travelvoice.jp/20260420-159495", "", "Criteo survey", "2026-04-20", "", "2025-10..12", "search summary", T1, "7 countries", "company-sponsored survey", "company-reported", "weak counter", "", "Awareness = demand", "", "", ""),
    ("ADJ-18", "Parcel as a Japanese tracking substitute", "GRO-C033 (v2, directly observed listing)", "feedback_derived",
     "Not in CLA v1.", "The Japan App Store lists Parcel with Japanese, Japan Post/Yamato/Sagawa named, developer-claimed Amazon ingestion once shipped (on-device credentials), premium listed at JPY 800/year, 4.7 from 323 ratings (as fetched by GRO).",
     "retained_constraint", "Ivan Pavlov Pty Ltd (Apple App Store)", "https://apps.apple.com/jp/app/parcel/id375589283", "listing", "App Store listing", "", "", "", "not accessed (403); GRO observation", T2, "JP App Store", "official/first-party (developer claims)", "directly observed by GRO", "counter to empty-market claim",
     "A Japanese-capable tracker exists; benchmark against it", "Listed price = willingness to pay or a price ceiling; ratings = active users; claims = tested capability", "Delivery follow-on must benchmark Parcel/Gmail/carrier tools", "Tested capability on Japanese orders", "VQ-15"),
    ("ADJ-19", "Gmail Purchases / package tracking", "CLA-C046 (first pass)", "first_pass_independent",
     "Purchases view rolled out to personal accounts globally; carrier tracking for participating US carriers; JP carriers reported unsupported.", "Retained, scoped: aggregation exists; Japanese carrier status tracking not established.", "retained_rescoped", "Google",
     "https://blog.google/products-and-platforms/products/gmail/one-stop-purchase-tracking-in-gmail/", "", "Gmail", "2025", "", "", "search summary", T1, "Global view; US carriers", "official/first-party", "company-reported", "partial substitute", "Include in benchmark", "Gmail solves Japanese tracking", "", "Japanese merchant parsing quality", ""),
    ("ADJ-20", "Yahoo! Shopping agent usage disclosure", "CLA-C040 (v1: 'no usage metrics found'); GRO-C038 (v2)", "first_pass_independent + feedback_derived",
     "CLA v1: no usage metric disclosed for the Yahoo agent.",
     "LY reported AI-agent-mediated merchandise value at about 20% in July 2026 (story 2026-08-20; repeated in release 020777) and planned an AI delivery forecast for end-September 2026. Company-reported; definition of 'AI-via' unverified; in-mall only; not incremental volume. CLA's single corroboration search did not surface it.",
     "superseded_within_scope", "LY Corporation", "lycorp story 20260820; release 020777", "", "LY Corp releases", "2026-08-20; 2026-09-02", "", "2026-07",
     "not accessed; GRO observation", T2, "Yahoo! Shopping (in-mall)", "official/first-party", "company-reported", "supports incumbent strength in-mall",
     "Incumbent agents are used inside their own malls", "Cross-merchant demand; that the forecast shipped", "Strengthens substitutes for in-mall jobs; does not restrict research to exceptions", "Metric definition", "VQ-14"),
    ("ADJ-21", "Carrier LINE notification flows", "CLA-C019-C021 (first pass)", "first_pass_independent",
     "Yamato phone-matched LINE notices without friend registration; Sagawa LINE; Japan Post LINE/ゆうID.", "Retained as strongest free delivery-notification substitute.", "retained_constraint", "Carriers", "see CLA-S085, S086, S088", "", "Carrier first-party", "", "", "",
     "search summary", T1, "JP carriers", "official/first-party", "company-reported", "counter to C01 empty-market", "Benchmark against them", "That they make any coordination product worthless", "", "Coverage of non-LINE users", ""),
    ("ADJ-22", "Redelivery trend", "CLA-C073/C074 (first pass)", "first_pass_independent",
     "Redelivery ~7.6% (Apr 2026, MLIT); diverse receipt target 50% by FY2030; 置き配 standardisation planned.", "Retained, scoped to delivery-miss pain only.", "retained_rescoped", "MLIT (via secondary)", "https://ecnomikata.com/ecnews/51084/", "", "MLIT redelivery survey", "2026-07-10", "", "2026-04",
     "search summary", T1, "Major carriers, Japan", "official statistic (via secondary)", "publisher-reported", "counter to redelivery wedge", "Redelivery is not a growth wedge", "Delivery coordination has no value", "", "", "VQ-20"),
    ("ADJ-23", "Incumbent metrics and registrations", "CLA-C043, C052, C053, C060, C061 (first pass)", "first_pass_independent",
     "Rakuten AI -41% time/+17% AOV; Rakuten Rebates 10M registered; Kakaku 54M (2017); Kuroneko 50M registrations; Money Forward ME 17.3M users.",
     "Excluded from decision-carrying role: company-reported registrations/active claims with undisclosed definitions.", "excluded_from_decision", "various", "see CLA-S035, S074, S076, S084, S096", "", "Company disclosures", "", "", "",
     "search summary", T1, "Japan", "company-reported", "company-reported", "n/a", "Existence of incumbents only", "Scale or adoption inferences", "", "", ""),
    # ---------------- Amazon lifecycle data ----------------
    ("ADJ-24", "Amazon order emails without item names", "CLA-C005/C006 (first pass); reviewer flag", "first_pass_independent",
     "CLA v1: from ~2026-07-08 Amazon confirmation emails list categories only (US documented); JP unverified; framed as cutting email-based ingestion for the largest merchant.",
     "Rescoped: account-level firsthand reports (US) concern the INITIAL order-confirmation message type; Amazon's statement (via secondary) says several order-related emails were simplified. No evidence here about shipment, delivery or refund emails, tracking numbers, or amazon.co.jp rollout. Missing product names are not missing all parcel data.",
     "retained_rescoped", "Developer report; Daring Fireball; Shopifreaks", "https://github.com/evanpurkhiser/email-to-lunchmoney/issues/7 ; https://daringfireball.net/linked/2026/08/12/amazon-spite", "issue text / commentary", "Amazon email change (one family)", "2026-08", "2026-07-08 (observed)", "",
     "search summary", T1, "US accounts; initial confirmation emails", "anecdotal + secondary", "firsthand account-level observation", "partial counter to email ingestion",
     "Item identity may be missing from initial confirmations", "JP rollout; loss of shipment/refund data; loss of tracking numbers", "Founder checks own amazon.co.jp messages by type (E001)", "All lifecycle message types; JP", "VQ-10"),
    # ---------------- Market / macro ----------------
    ("ADJ-25", "McKinsey 'biggest and fastest-growing'", "CLA-C120 (first pass); GRO-C037 (v2)", "first_pass_independent + feedback_derived",
     "Founder narrative: e-commerce is the biggest and fastest-growing category.",
     "MGI 'The next big arenas of competition' (Oct 2024) ranks e-commerce first by projected 2040 revenue (~USD 4T base -> 14-20T); not fastest growth; not Japan; not startup revenue. Two researchers' search extracts of one source family.",
     "retained_rescoped", "McKinsey Global Institute", "https://www.mckinsey.com/mgi/our-research/the-next-big-arenas-of-competition", "executive summary (extracts)", "MGI arenas", "2024-10", "", "2022 actual; 2040 forecast",
     "search summary", T1, "Global", "consultancy research", "third-party estimate", "ranking only", "Largest projected arena", "Consumer > B2B; fastest growth; startup revenue", "Close the macro thread", "Founder's exact original source", ""),
    ("ADJ-26", "Household denominator", "CLA v1 sizing; reviewer flag; CLA consolidation search", "cla_consolidation_check",
     "CLA v1: 55.7M households x 56.9% x heavy share.",
     "56.9% is the 2025 net-shopping usage rate of TWO-OR-MORE-person households (MIC). It cannot be applied to all households (incl. single-person) without adjustment. Spending covers goods AND services (food 21.6%, travel 20.9%, clothing 9.8%, appliances/furniture 7.0% of net-shopping spend). 55.7M total households was not re-verified. CLA v1 upside/base revenue figures are illustrative only.",
     "rejected_inference", "MIC Statistics Bureau (via secondary)", "https://www.stat.go.jp/data/joukyou/2025ar/gaikyou/pdf/gk01.pdf ; https://netshop.impress.co.jp/n/2026/02/09/15565", "summary (extract)", "MIC household survey", "2026-02", "", "2025",
     "search extract (PDF 403)", T2, "Japan, 2+ person households", "official statistic", "publisher-reported (extract)", "n/a",
     "Size only with household-type adjustment", "All-household application; physical-goods-only use of total spend; 'not venture-scale' as a universal cutoff", "Withdraw CLA v1 market-size outputs from decision use", "Single-person rate; household counts", "VQ-08;VQ-09"),
    # ---------------- Precedents ----------------
    ("ADJ-27", "Predecessors and allegations", "CLA-C054-C058 (first pass); GEM (Fast)", "first_pass_independent + feedback_derived",
     "CLA v1 cited Uketoru (ended), Two Tap, Spring, Unroll.me, Honey lawsuit; GEM cited Fast's collapse as consumer unwillingness to pay.",
     "Bounded historical examples only. Exclude closure-cause speculation (Uketoru), lawsuit details (Honey), and the universal demand inference from Fast (customer, payer, scope and causal mechanism not established).",
     "excluded_from_decision", "various", "see CLA-S078-S083, S032", "", "Historical", "", "", "", "search summary", T1, "US/JP", "secondary/anecdotal", "mixed", "weak counter",
     "Universal-checkout and receipt-mining predecessors were absorbed or ended", "Any causal demand conclusion", "None decision-carrying", "", ""),
    ("ADJ-28", "Amazon US agent conflicts (Perplexity, Muse, seller Agent Policy)", "CLA-C001-C004 (first pass)", "first_pass_independent",
     "CLA v1 used US litigation and blocking to argue browser execution on Amazon is contested.",
     "Retained scoped: Amazon.com contests unauthorised agents in the US; US CFAA rulings and Amazon.com blocking are not Japanese law or co.jp terms. Litigation details beyond the dated events are not decision-carrying.",
     "retained_rescoped", "Courts/press (US)", "see CLA-S043-S046", "", "US litigation/press", "2026-03..09", "", "", "search summary", T1, "US Amazon.com", "secondary", "publisher-reported", "counter to browser execution on Amazon",
     "Do not plan unauthorised browser execution", "Japan-wide legal conclusions", "", "", ""),
    # ---------------- Economics / QA ----------------
    ("ADJ-29", "Grok v2 precision defect", "Reviewer finding; CLA reproduction (QA_grok_v2.txt)", "reviewer_finding + cla_consolidation_check",
     "GRO v2 CSV stores C02/v1_base attributable_orders = 0.01 with revenue 0.96.",
     "Reproduced from the supplied CSV and reviewer-stated v1 inputs: exact 0.012; 2-dp display 0.01 saved as data; 0.01 x 80 = 0.80 != 0.96. Headline -29.04 correct in memory. Interchange/QA defect, not new economics. Repaired in GRO-D01.",
     "retained_constraint", "Grok (supplied file)", "00_inputs_supplied/GRO_v2/GRO_04_economics_model_v2.csv", "row C02/v1_base/attributable_orders", "GRO model", "", "", "", "local file inspection", T2, "Model export", "calculation", "calculation", "n/a",
     "Preserve exact values; round display only", "That economics changed", "Use GRO-D01 for any merge", "Reviewer's 29-check script not supplied", "VQ-17"),
    ("ADJ-30", "Grok v2 cohort definition", "Reviewer finding; CLA reproduction", "reviewer_finding + cla_consolidation_check",
     "GRO v2: retained_fraction_by_month = share of ACQUIRED cohort; formula multiplies by activation again.",
     "Reproduced from CSV text. Repaired: r_t = P(active at t | activated) with a applied once (or q_t without a). Inputs remain blank.", "retained_constraint", "Grok (supplied file)", "00_inputs_supplied/GRO_v2/GRO_04_economics_model_v2.csv", "C02/cohort rows", "GRO model", "", "", "",
     "local file inspection", T2, "Model", "calculation", "calculation", "n/a", "Activation once", "", "Bridge uses a x r_t x c_t with a guard test", "", "VQ-17"),
    ("ADJ-31", "CLA v1 export precision (self-audit)", "CLA consolidation QA", "cla_consolidation_check",
     "CLA v1 reported 141/141 workbook-Python matches.",
     "Re-run 2026-10-04T21:51Z: workbook vs Python 141/141 (implementation consistency only). But the CLA 04 CSV saved rounded values: 81/288 numeric cells differ from exact; 31/138 outputs do not reconcile from saved values within their displayed precision; no sign flips. Same defect class as Grok's. The original console result was not retained as a file.",
     "retained_constraint", "CLA (this researcher)", "01_original_CLA_export/ (ebd8cdf)", "04_economics_model.csv", "CLA model", "", "", "", "local", T2, "Model export", "calculation", "calculation", "n/a",
     "Original headline values stand in memory", "That 141/141 validated the economic design or the saved table", "Bridge exports exact + display columns", "", ""),
    ("ADJ-32", "CLA v1 'base case negative' framing", "CLA-C096-C099 (first pass); reviewer", "cla_consolidation_check",
     "CLA v1: base-case contributions negative; frontiers 36% handoff, 17% paid; 'not venture-scale'.",
     "These are scenario-conditional calculations on assumed inputs, not measured failure. In the bridge, every behavioural input is UNKNOWN in the observed scenario and dependent outputs are blank. The illustrative scenarios remain useful as frontiers only.",
     "rejected_inference", "CLA", "03_derivatives/bridge/bridge_outputs.csv", "", "CLA model", "", "", "", "local", T2, "Model", "calculation", "assumption/scenario", "n/a",
     "Frontiers show which inputs must be measured", "Base case = central estimate; upside = company", "Discovery must measure the inputs, not argue scenarios", "All behavioural inputs", ""),
    ("ADJ-33", "C04 human resolution vs partner fee", "CLA v1 memo (JPY 32/MAU partner break-even; C04 recommended); reviewer stress", "cla_consolidation_check",
     "CLA v1 recommended C04 exception service with partner payer; partner break-even ~JPY 32-40/MAU for tracking.",
     "Reproduced: 0.40 x 1 x 15 min x JPY 50 = JPY 300/household-month if all affected submit and all cases are human-handled. With a JPY 40 fee and JPY 31.6 illustrative tracking core, affordable submission x human-share x minutes = 0.42 (e.g. <=2.8% submission at 15 fully human minutes). A JPY 32-40 partner fee cannot fund a full-resolution promise; low-cost reminder economics must not be used to fund it.",
     "rejected_inference", "CLA", "03_derivatives/bridge/c04_stress_grid.csv", "", "CLA model", "", "", "", "local", T2, "Model", "calculation", "calculation (conditional)", "counter to CLA v1 C04 recommendation",
     "Drafting (C04a) and human resolution (C04b) are different products", "That C04 is the default next step", "Withdraw CLA v1 C04-first recommendation", "Incidence, submission, minutes, payer", ""),
    ("ADJ-34", "Founder hours double count", "CLA v1 model (team_fixed incl. ops lead + variable labour)", "cla_consolidation_check",
     "CLA v1 'actives to cover fixed team' included an ops/support lead while support minutes were also costed variably.",
     "Potential double count. Bridge prices every human minute once (labor_jpy_per_min) and carries no fixed team line.", "rejected_inference", "CLA", "", "", "CLA model", "", "", "", "local", T2, "Model", "calculation", "calculation", "n/a", "", "CLA v1 F10/F11 scale outputs", "Do not use F10/F11", "", ""),
    ("ADJ-35", "State and provenance in operating traces", "CLA v1 report Trace A/B; reviewer flag", "cla_consolidation_check",
     "CLA v1 traces: DMARC-gated ingestion of forwarded mail; idempotent mandates; merchant+order ID keys; JAN-confirmed matches; refund 'confirmed'.",
     "Corrected in CLA-D05: forwarded/redacted mail is user-supplied evidence, not authenticated merchant mail; refund requested != merchant-reported issuance != funds received; missing confirmation is not a payment state; order != package; a local mandate is not a merchant-enforced spend cap or idempotency; identifiers are scoped per user/tenant; missing/ambiguous JAN never asserts a confirmed match.",
     "rejected_inference", "CLA", "03_derivatives/CLA-D05_trace_state_corrections.md", "", "CLA traces", "", "", "", "local", T2, "Design", "design", "design", "n/a", "", "Authentication or payment states inferred from forwarded mail", "Use corrected state model in any prototype", "", ""),
    ("ADJ-36", "H02 status scope (CLA and GRO)", "GRO v2 H02; CLA v1 H02/H02a/H02b; reviewer", "feedback_derived + reviewer_finding",
     "GRO v2 marked the adequacy hypothesis H02 'contradicted' on the empty-market claim; CLA v1 marked H02a delivery visibility 'contradicted'.",
     "Split: H02a 'no relevant alternative exists' CONTRADICTED (Parcel, Gmail, carriers, in-mall agents); H02b 'alternatives adequately solve the chosen segment's job' UNRESOLVED per job.", "retained_rescoped", "", "", "", "", "", "", "", "local", T2, "Register", "inference", "inference", "n/a",
     "", "Adequacy settled by existence", "Status fields carry the qualification", "", ""),
    ("ADJ-37", "Test design: value without changed outcome", "GRO v2 E005R/E006 (not supplied; described by reviewer); CLA v1 E006", "reviewer_finding + cla_consolidation_check",
     "GRO tests required a changed offer or outcome; CLA v1 E006 required >=36% handoff.",
     "Value can be the same correct choice or resolution with materially less effort, uncertainty or error. Measure incremental benefit vs the strongest alternative AND full provider cost, including the loss tail; majority-positive cases are insufficient.",
     "retained_constraint", "", "", "", "", "", "", "", "reviewer description (GRO 06 not supplied)", T2, "Test design", "design", "design", "n/a",
     "", "Changed choice/outcome as a necessary condition", "Applied in the discovery kit", "", "VQ-17"),
    ("ADJ-38", "Gemini surviving universal verdict", "GEM correction (not supplied to CLA)", "feedback_derived",
     "GEM preserved a universal adverse verdict after corrections (per reviewer); 'Primary Source Inspected' cells empty as supplied.",
     "No independent evidentiary vote. Only independently supported corrections are used (A8 role; authentication vs scraping separation; protocol/product date separation).", "excluded_from_decision", "Gemini", "", "", "", "", "", "", "not supplied to CLA", T2, "", "", "unknown", "n/a",
     "", "Gemini verdict as corroboration", "", "Gemini table itself", "VQ-18"),
]

# ---------------- Corrected hypothesis register (CLA-D01) ----------------
HYP_HEADER = ["hypothesis_id", "hypothesis", "cla_v1_status", "gro_v2_status", "consolidated_status", "closed_scope", "unresolved_remainder", "decision_treatment", "key_adjudications", "next_evidence"]
HYP = [
    ("H01", "A definable Japanese customer segment has frequent, material cross-merchant purchase or delivery friction.", "UNRESOLVED", "unresolved", "UNRESOLVED",
     "Redelivery is falling and largely inside carrier tools (ADJ-22).", "Residual burden per job in an activity-selected cohort; mechanism depth in a separately labelled incident cohort.", "investigate in discovery", "ADJ-21;ADJ-22", "Discovery round"),
    ("H02", "Current merchant apps, carrier notifications, email, wallets, and aggregators do not already solve it adequately.", "UNRESOLVED (split)", "contradicted_by_identified_evidence", "UNRESOLVED (see H02a/H02b)",
     "Only the empty-market sub-claim is closed (H02a).", "Adequacy per job and segment (H02b).", "investigate in discovery", "ADJ-36", "Discovery round"),
    ("H02a", "SUB: No relevant alternative exists for tracking/notification.", "(CLA v1 H02a was 'delivery visibility not adequately solved' - different)", "(implicit in H02)", "CONTRADICTED",
     "Parcel, Gmail, carrier LINE flows, in-mall agents exist (ADJ-18..21).", "", "do not claim an empty market", "ADJ-18;ADJ-19;ADJ-20;ADJ-21", ""),
    ("H02b", "SUB: Existing alternatives do not adequately solve the chosen segment's job (per job: offer selection, checkout, delivery coordination, exceptions).", "UNRESOLVED (exceptions only)", "unresolved remainder", "UNRESOLVED (all four jobs)",
     "", "Burden after the strongest alternative the person already uses.", "investigate in discovery", "ADJ-36", "Discovery round; at most one follow-on"),
    ("H03", "Enough users will grant the data access and transaction authority required.", "CONTRADICTED (authority); UNRESOLVED (data)", "unresolved", "UNRESOLVED (see H03a/H03b)", "", "", "no execution test", "ADJ-16", ""),
    ("H03a", "SUB: Users will share minimum purchase records (shown, forwarded or redacted).", "UNRESOLVED", "unresolved", "UNRESOLVED",
     "", "Actual voluntary sharing behaviour by capture method; refusals respected and not generalised.", "observe in discovery (voluntary)", "", "Discovery record-sharing log"),
    ("H03b", "SUB: Users will authorise preparation or execution of purchases.", "CONTRADICTED", "unresolved", "UNRESOLVED (adverse signal for execution)",
     "In an AI-friendly sample ~5% would allow cart preparation with self-confirmation and ~1% unchecked purchase; 27% none (ADJ-16). Not majority refusal.", "Japanese population; specific bounded designs.", "no execution test", "ADJ-16", ""),
    ("H04", "A startup can obtain sufficient permitted, durable merchant, carrier, and payment access.", "CONTRADICTED (execution)", "unresolved", "UNRESOLVED (see H04a-f)", "", "", "permitted-path memo before any execution", "ADJ-01..ADJ-14", ""),
    ("H04a", "SUB: A consumer-authorised order-history API exists at top marketplaces.", "CONTRADICTED", "", "NO PATH FOUND (within search; not a prohibition)", "", "Partner programmes", "use user-supplied records", "ADJ-05", ""),
    ("H04b", "SUB: Delegated execution on Amazon is permitted for an Associates-monetised startup.", "CONTRADICTED", "prohibited if 6(k) operative", "UNRESOLVED (adverse clause; JP unreconciled) - underwriting exclusion", "", "Japanese operative terms", "exclude from investment case", "ADJ-01", "VQ-01"),
    ("H04c", "SUB: A third party can change delivery instructions for consignees.", "CONTRADICTED", "", "NO PATH FOUND", "", "Member terms", "handoff only", "ADJ-07", "VQ-16"),
    ("H04d", "SUB: Read-only order ingestion is permissible.", "SUPPORTED (conditional)", "", "SUPPORTED (conditional; architecture-specific cost unresolved)", "Gmail permitted app type for package tracking (ADJ-13)", "Cost; provenance limits of forwarding", "no OAuth in discovery", "ADJ-13;ADJ-14", "VQ-11"),
    ("H04e", "SUB: Referral (affiliate) links can be distributed on a personal-assistant surface.", "(not assessed)", "unresolved", "RESTRICTED for Rakuten except approved corporate partners (extract); UNRESOLVED for Amazon, Yahoo, ASPs", "", "Programme x surface approvals", "exclude booked referral revenue", "ADJ-02;ADJ-03;ADJ-04", "VQ-01..VQ-05"),
    ("H04f", "SUB: One connected permitted path exists for the intended cross-merchant execution task.", "CONTRADICTED", "", "NOT ESTABLISHED", "", "Standalone merchants, wallets, Shopify JP, issuer programmes", "execution not approved", "ADJ-06;ADJ-09", "Permitted-path memo"),
    ("H05", "Agentic checkout produces meaningful incremental benefit over existing checkout.", "UNRESOLVED", "unresolved", "UNRESOLVED", "Generic in-chat checkout narrowed by OpenAI's own account (ADJ-11).", "Checkout time/errors vs saved details in Japan.", "measure in discovery; no execution", "ADJ-11", ""),
    ("H06", "Tracking and checkout reinforce each other commercially.", "UNRESOLVED", "unresolved", "UNRESOLVED", "", "Co-occurrence and causation.", "note co-occurrence only", "", ""),
    ("H07", "Japan-specific requirements create an advantage worth more than the associated complexity.", "CONTRADICTED", "unresolved", "UNRESOLVED (no advantage established)", "Localisation is not a moat; incumbents localised.", "Whether a cross-ecosystem comparison reduces effort/uncertainty materially.", "park unless offer selection is selected", "", ""),
    ("H08", "Customers can be acquired and retained through a realistic channel.", "UNRESOLVED", "unresolved", "UNRESOLVED", "", "Quoted acquisition cost for one defined offer.", "no acquisition test now", "", ""),
    ("H09", "Contribution economics remain attractive after failures, support, incentives, and acquisition costs.", "CONTRADICTED (base case)", "unresolved", "UNRESOLVED (no bookable positive case established)", "Base cases are assumed, not measured (ADJ-32).", "All behavioural inputs; eligibility.", "no build", "ADJ-32;ADJ-33", "Per-job costs inside the one follow-on"),
    ("H10", "The company can defend value against incumbents, fast followers, and disintermediation.", "CONTRADICTED", "unresolved", "UNRESOLVED (no defensible position established; bundling risk supported)", "", "A narrow leftover job.", "no build", "ADJ-18;ADJ-20", ""),
    ("H11", "A specific recent change improves feasibility or demand.", "UNRESOLVED (mixed)", "unresolved", "UNRESOLVED", "", "A mechanism that helps a startup rather than incumbents.", "no new why-now research", "ADJ-09;ADJ-10;ADJ-11", ""),
    ("H12", "The result can be a durable independent company rather than a feature, low-margin service, or inaccessible platform dependency.", "CONTRADICTED (venture-scale)", "unresolved", "UNRESOLVED (no positive company case established)", "", "Value + permission + economics + acquisition overlap for one job.", "park theme if discovery finds no job", "ADJ-26", ""),
]

# ---------------- Jobs / concepts (CLA-D02) ----------------
JOB_HEADER = ["job_or_concept", "maps_to", "value_status", "permission_status", "economics_status", "strongest_alternative_to_beat", "discovery_treatment", "eligible_follow_on", "what_a_prototype_needs_first", "cla_v1_status_superseded"]
JOBS = [
    ("J1 Offer selection / comparison", "C03 (C05 replenishment folded in as deprioritised)", "UNRESOLVED", "Comparison itself: no barrier found. Referral revenue on a personal-assistant surface: RESTRICTED (Rakuten) / UNRESOLVED (others)", "No bookable revenue under current gates; conditional only",
     "Google AI Mode conversational shopping, in-mall AI (Yahoo, Rakuten, Rufus), Kakaku.com, point sites/Rebates", "include", "No-purchase offer-comparison task", "Net effort/uncertainty reduction vs strongest alternative; a permitted monetisation surface or a non-affiliate payer", "UNRESOLVED; economics fragile"),
    ("J2 Checkout preparation and user-approved execution", "C02", "UNRESOLVED", "NOT ESTABLISHED (no connected permitted path); Amazon delegated execution excluded", "Not computed (gated)",
     "Saved addresses/payment, one-click, Amazon Pay/Rakuten Pay/PayPay", "include (measure current checkout effort only)", "Permitted-path memo (no execution)", "One documented connected path for the intended task; issuer/merchant acceptance", "CONTRADICTED for now (watch)"),
    ("J3 Delivery coordination", "C01 (C01a forwarding)", "UNRESOLVED (empty-market claim contradicted)", "Read-only views permitted; changes via carrier channels only", "No sourced revenue; subscription WTP unmeasured; passive affiliate = rule zero",
     "Carrier LINE/member flows, Parcel, Gmail Purchases, merchant apps/agents", "include", "Parcel/Gmail/current-workflow benchmark", "Material residual burden after these tools for an activity-selected group", "CONTRADICTED as standalone"),
    ("J4a Exception assistance (drafting/reminders)", "C04a", "UNRESOLVED", "Read-only + user acts; no account access", "Low provider cost per draft; payer unknown; user still spends time",
     "Merchant/carrier support, own memory, in-mall post-purchase chat", "include", "Timed case assistance (drafting arm)", "Observed incidence, user minutes saved, payer", "UNRESOLVED - recommended first (withdrawn)"),
    ("J4b Human case resolution", "C04b", "UNRESOLVED", "Acts only via user; merchant controls outcome", "JPY 32-40 partner fee cannot fund full resolution (ADJ-33)",
     "Merchant/carrier support", "include as mechanism probe only", "Timed case assistance (human arm) with full cost distribution incl. failures", "Cost tail and payer evidence", "(bundled in C04)"),
    ("C06 Cross-border", "C06", "NOT RESEARCHED", "", "", "", "exclude", "none", "", "NOT RESEARCHED"),
    ("C07 Partner distribution", "C07", "UNRESOLVED", "Partner-authorised data", "Startup side positive only before unknown integration/sales costs; partner benefit unmeasured",
     "Partners' own tools; merchant SaaS", "not in this round", "none now (not a default rescue)", "Buyer evidence with stated fee and transferred-cost accounting", "UNRESOLVED (pivot candidate) - withdrawn as default"),
    ("C08 B2B infrastructure", "C08", "NOT RESEARCHED beyond existence of merchant-paid post-purchase SaaS", "", "", "Recustomer, AfterShip, OMS/WMS", "not in this round", "none now", "Separate buyer and operating evidence", "UNRESOLVED (partially researched)"),
    ("T01-T03 adjacent themes", "B2B logistics interoperability; SKU data infrastructure; physical-AI support", "NOT RESEARCHED", "", "", "", "not scored", "none", "", "NOT RESEARCHED"),
]

# ---------------- Permission gates (CLA-D03) ----------------
GATE_HEADER = ["gate_id", "program_or_counterparty", "data_source", "interface_surface", "user_action", "startup_action", "approval_required", "attributable_revenue",
               "permission_status", "applicability_status", "underwriting_treatment", "commercial_amount", "evidence", "validation_status"]
GATES = [
    ("G01", "Amazon Associates (Creators API)", "Amazon catalogue", "any", "-", "Fetch product/price data", "Approved account + >=10 qualifying sales in 30 days", "n/a", "gated", "applies to new entrants", "plan without Amazon data until threshold met", "n/a", "CLA-S033;CLA-S038", "search summary"),
    ("G02", "Amazon Associates", "-", "personal assistant (in-app/chat/LINE)", "User clicks and buys herself", "Show affiliate link", "Unknown (JP agreement unread)", "conditional", "unresolved", "Japanese terms unread", "exclude from investment case", "unknown", "ADJ-02", "unverified"),
    ("G03", "Amazon Associates", "-", "any", "User consents", "Place order on the user's behalf", "Prohibited in retrieved English text 6(k)", "none", "adverse clause (English text)", "JP operating agreement unreconciled", "exclude; do not test", "unknown (not an observed universal zero)", "GRO-C034;ADJ-01", "GRO direct observation; CLA unverified"),
    ("G04", "Rakuten Affiliate", "Rakuten item search API", "personal assistant / LINE / email / DM / closed tools", "User clicks", "Send affiliate link one-to-one", "Rakuten-approved corporate partner", "conditional on approval", "restricted except approved corporate partners", "applies to closed/one-to-one tools (in-app UI classification unconfirmed)", "exclude unless approval obtained", "unknown", "CLA-S124;CLA-S125;ADJ-03", "search extract"),
    ("G05", "Rakuten Affiliate", "Rakuten item search API", "any closed channel via automation", "-", "Auto-post affiliate links to email/LINE/DMs", "-", "none", "prohibited (extract)", "applies", "do not build", "n/a", "CLA-S124", "search extract"),
    ("G06", "Rakuten Affiliate", "Rakuten item search API", "public web comparison page", "User clicks", "Publish comparison with affiliate links", "Programme membership; competing-service clause", "conditional", "permitted subject to guideline", "competing-service clause unresolved", "conditional; not in current case", "unknown", "GRO-C035;ADJ-04", "GRO direct observation"),
    ("G07", "Yahoo! Shopping affiliate (ValueCommerce)", "Yahoo item search API v3", "personal assistant", "User clicks", "Show affiliate link", "Unknown", "conditional", "unresolved", "terms unread", "exclude", "unknown", "CLA-S094", "unverified"),
    ("G08", "ASP (A8 etc., media member)", "-", "personal assistant", "User clicks", "Show affiliate link", "Per-advertiser programme approval", "conditional", "unresolved", "publisher role confirmed; surface rules unread", "exclude", "unknown", "ADJ-15", "reviewer-observed role"),
    ("G09", "Merchant (no affiliate)", "-", "any", "User clicks", "Ordinary merchant link", "None", "none", "permitted ordinary link", "applies", "allowed; revenue rule zero", "0 by design", "-", "n/a"),
    ("G10", "Affiliate programmes", "User's historical receipts", "any", "-", "Read past orders", "-", "none", "n/a", "no qualifying click", "not commissionable", "0 by programme rule", "GRO-S039;CLA-S030", "programme rule"),
    ("G11", "Google (Gmail API)", "User mailbox", "server-side app", "User grants OAuth", "Read/store order emails", "Restricted-scope verification; annual assessment if stored/transmitted server-side", "n/a", "permitted app type (package tracking)", "architecture-specific", "not in this assignment", "cost unknown (quote != budget)", "ADJ-13", "search summary"),
    ("G12", "User (forwarding)", "User-forwarded or shown records", "local review", "User shows/forwards voluntarily", "Inspect locally; retain only with consent", "Participant consent; counsel on APPI/telecom before any service", "n/a", "research use with consent", "provenance = user-supplied, not authenticated merchant mail", "discovery only", "n/a", "ADJ-35", "design"),
    ("G13", "Carriers (Yamato/Sagawa/Japan Post)", "Tracking numbers", "carrier web/LINE", "Consignee changes delivery", "Change delivery for the user", "Carrier identity; none found for third parties", "none", "no path found", "member terms unread", "handoff only", "n/a", "ADJ-07", "search summary"),
    ("G14", "Card networks / issuers", "Payment credentials", "agent-initiated payment", "User approves", "Initiate payment", "Network agent-token programme + issuer + merchant acceptance", "n/a", "controlled programmes (Visa Agentic Ready issuers; Mastercard pilot)", "startup eligibility unknown", "not established", "unknown", "ADJ-09", "search extract"),
    ("G15", "Shopify (ChatGPT channel)", "Shopify catalogue", "ChatGPT", "User checks out on merchant", "(not the startup)", "-", "n/a", "documented US-customer channel; no extra selling fee", "not Japan", "n/a for JP", "n/a", "ADJ-12", "reviewer-observed"),
    ("G16", "Google (UCP / Universal Cart)", "Merchant UCP feeds", "Google surfaces", "User checks out", "(not the startup)", "Merchant UCP adoption; Google approval", "n/a", "US-first", "Japan not established", "n/a for JP", "n/a", "ADJ-10", "search summary"),
]

# ---------------- Amazon lifecycle scope (CLA-D04) ----------------
LIFE_HEADER = ["job", "required_field", "candidate_lifecycle_source", "what_is_observed", "scope_of_observation", "untested_dependency", "test"]
LIFE = [
    ("Delivery coordination", "Order identity (order number)", "Initial order-confirmation email", "Reported to remain present (order total and link)", "US accounts, initial confirmation, from ~2026-07-08", "Present in amazon.co.jp confirmations?", "CLA-E001 (founder's own messages, local review)"),
    ("Delivery coordination", "Item identity (name/quantity/price)", "Initial order-confirmation email", "Reported replaced by categories ('1 Home item')", "US accounts, initial confirmation", "Whether amazon.co.jp changed; whether later messages carry items", "CLA-E001"),
    ("Delivery coordination", "Shipment/package identity and carrier tracking number", "Shipment-confirmation email", "NOT OBSERVED by any researcher", "-", "Present in JP shipment emails? Amazon-delivered parcels have no external carrier number", "CLA-E001"),
    ("Delivery coordination", "Delivery status/ETA", "Carrier notices (LINE/email) for carrier-delivered parcels; Amazon app for own delivery", "Carrier flows documented (CLA-S085/S086/S088)", "JP carriers", "Share of Amazon parcels on own delivery (not found)", "Discovery: record which channel informed the user"),
    ("Exception assistance", "Return window / return status", "Return emails; Amazon order page (user only)", "NOT OBSERVED", "-", "Content of JP return emails", "CLA-E001 + discovery records"),
    ("Exception assistance", "Refund requested vs issued vs funds received", "Refund email (issuance as reported by merchant); card/bank statement (receipt)", "NOT OBSERVED", "-", "Whether refund emails state amount/date; receipt requires user's statement", "Discovery records (voluntary)"),
    ("Offer selection", "Product, price, availability", "Creators API (gated); product page (user view)", "API threshold reported", "Associates programme", "Threshold for a new entrant", "n/a in discovery"),
    ("Checkout execution", "-", "-", "Excluded (ADJ-01)", "-", "-", "Permitted-path memo only"),
]

# ---------------- Source additions (CLA-D06) ----------------
SRC_HEADER = ["source_id", "title", "publisher", "canonical_url", "language", "publication_date", "accessed_at", "access_status", "limitations"]
SRC = [
    ("CLA-S124", "楽天アフィリエイトガイドライン (closed-tool / automated distribution rules)", "Rakuten Group", "https://affiliate.rakuten.co.jp/guideline/rule/", "ja", "2025-06-26 (update)", T2, "search extract only; WebFetch EGRESS_BLOCKED", "Exact wording, partner criteria and in-app classification unverified"),
    ("CLA-S125", "メールやLINEでの紹介は規約違反となりますか？ (FAQ 000015637)", "Rakuten Affiliate FAQ", "https://affiliate.faq.rakuten.net/detail/000015637", "ja", "", T2, "search result title only", "Answer text not read"),
    ("CLA-S126", "Visa: オンライン購買におけるAIエージェントの受容性調査 (secondary reports)", "マイナビニュース / コマースピック / ペイメントナビ", "https://news.mynavi.jp/article/20260817-4830173/", "ja", "2026-08-17", T2, "search extracts", "Chart base and option wording unverified"),
    ("CLA-S127", "Visa、「Agentic Ready」プログラムを日本を含むアジア太平洋地域の50社超のパートナーとともに始動", "Visa Worldwide Japan", "https://www.visa.co.jp/about-visa/newsroom/press-releases/nr-jp-260430-2.html", "ja", "2026-04-30", T2, "search extract; page 403", "Programme scope/eligibility unverified"),
    ("CLA-S128", "Visa Intelligent Commerceをアジア太平洋地域に拡大、2026年初頭のAIコマース試験導入に向け準備", "Visa Worldwide Japan", "https://www.visa.co.jp/about-visa/newsroom/press-releases/nr-jp-251117.html", "ja", "2025-11-17", T2, "search result title", ""),
    ("CLA-S129", "家計消費状況調査 2025年 ネットショッピング支出内訳 (secondary)", "ネットショップ担当者フォーラム (reporting MIC)", "https://netshop.impress.co.jp/n/2026/02/09/15565", "ja", "2026-02-09", T2, "search extract", "2+ person households only; single-person data not found"),
]

# ---------------- Verification queue ----------------
VQ_HEADER = ["vq_id", "item", "exact_page_or_artifact", "why_decision_critical", "blocks", "who_can_do_it"]
VQ = [
    ("VQ-01", "Amazon.co.jp Associates Japanese operating agreement and programme policies", "https://affiliate.amazon.co.jp/help/operating/agreement ; .../policies/", "Decides delegated execution and assistant-surface referral eligibility", "J1 monetisation; J2", "Founder (public page read) or counsel"),
    ("VQ-02", "Rakuten affiliate guideline full text: closed tools, corporate partners, competing service, JPY 3,000 basis", "https://affiliate.rakuten.co.jp/guideline/rule/", "Decides whether any personal-assistant referral can earn Rakuten revenue", "J1 monetisation", "Founder"),
    ("VQ-03", "Rakuten FAQ on email/LINE referrals", "https://affiliate.faq.rakuten.net/detail/000015637", "Confirms reading of VQ-02", "J1", "Founder"),
    ("VQ-04", "Standalone merchant and wallet terms (pick only merchants named in discovery)", "Merchant ToS/affiliate pages; Amazon Pay/Rakuten Pay/PayPay merchant/consumer terms", "Needed before any 'no path' statement and before a permitted-path memo", "J2", "Founder after discovery"),
    ("VQ-05", "ValueCommerce/A8 terms on private/app distribution", "valuecommerce.ne.jp; a8.net terms", "Referral eligibility on assistant surfaces", "J1", "Founder"),
    ("VQ-06", "Visa 2026-08-17 release and chart", "visa.co.jp newsroom release; chart image", "Base (entire 4,120 or subgroup) and option wording for 27%/5%/1%", "H03b wording only", "Founder"),
    ("VQ-07", "Visa Agentic Ready release", "https://www.visa.co.jp/about-visa/newsroom/press-releases/nr-jp-260430-2.html", "Programme scope; any merchant/agent eligibility", "J2 permitted-path memo", "Founder"),
    ("VQ-08", "MIC 家計消費状況調査 2025 (gk01.pdf; household-type tables)", "https://www.stat.go.jp/data/joukyou/2025ar/gaikyou/pdf/gk01.pdf", "Household-type scope; single-person usage", "Any future sizing", "Founder (not needed for discovery)"),
    ("VQ-09", "Latest household counts by type", "Census / Statistics Bureau", "Denominator", "Any future sizing", "Founder (not needed for discovery)"),
    ("VQ-10", "Founder's own amazon.co.jp messages by type (confirmation, shipment, delivery, return, refund)", "Founder mailbox, local review, redacted notes only", "Whether item names and tracking numbers survive in JP", "J3, J4", "Founder"),
    ("VQ-11", "Google restricted-scope/CASA FAQ and an assessor quote for a specific architecture", "developers.google.com OAuth verification FAQ", "Only if an OAuth design is ever chosen", "Later", "Founder/engineer"),
    ("VQ-12", "Shopify ChatGPT channel help page", "https://help.shopify.com/en/manual/online-sales-channels/agentic-storefronts/chatgpt", "Scope check only", "None", "Optional"),
    ("VQ-13", "OpenAI 2026-03-24 and 2025-09-29 pages", "openai.com", "Scope check only", "None", "Optional"),
    ("VQ-14", "LY 2026-08-20 story / release 020777 definition of AI-via merchandise value", "lycorp.co.jp", "Interpreting incumbent strength", "None", "Optional"),
    ("VQ-15", "Parcel listing and tested capability on Japanese orders", "apps.apple.com/jp/app/parcel/id375589283", "Benchmark baseline if J3 is selected", "J3 follow-on", "Founder in follow-on"),
    ("VQ-16", "Carrier member terms on third-party/automated access and delegated changes", "Kuroneko Members, Smart Club, ゆうID terms", "Only if coordination product needs carrier actions", "J3", "Later"),
    ("VQ-17", "Grok v1 CSVs, calculate_r003_v2.py, reviewer audit JSON, R003_v2_addendum, GRO 06/07 v2", "Reviewer handoff zip (not supplied to CLA)", "Reproduce the 29 checks; finish GRO row adjudication", "Ledger completeness", "Reviewer to supply"),
    ("VQ-18", "Gemini correction table", "Reviewer handoff zip (not supplied to CLA)", "Confirm GEM proposition wording", "Ledger completeness", "Reviewer to supply"),
    ("VQ-19", "Google UCP announcement date and Universal Cart scope", "https://developers.googleblog.com/under-the-hood-universal-commerce-protocol-ucp/", "Date hygiene only", "None", "Optional"),
    ("VQ-20", "MLIT April 2026 redelivery release", "mlit.go.jp", "Context for J3", "None", "Optional"),
]


def write(name, header, rows, folder=HERE):
    with open(os.path.join(folder, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            assert len(r) == len(header), (name, r[0], len(r), len(header))
            w.writerow(r)
    print(f"{name}: {len(rows)} rows")


if __name__ == "__main__":
    vq_ids = {v[0] for v in VQ}
    for r in L:
        for q in filter(None, r[-1].split(";")):
            assert q in vq_ids, (r[0], q)
    adj_ids = {r[0] for r in L}
    write("02_claim_adjudication_ledger.csv", LEDGER_HEADER, L, folder=ROOT)
    write("CLA-D01_hypothesis_register_corrected.csv", HYP_HEADER, HYP)
    write("CLA-D02_job_and_concept_status.csv", JOB_HEADER, JOBS)
    write("CLA-D03_permission_gates.csv", GATE_HEADER, GATES)
    write("CLA-D04_amazon_lifecycle_data_scope.csv", LIFE_HEADER, LIFE)
    write("CLA-D06_source_additions.csv", SRC_HEADER, SRC)
    write("06_verification_queue.csv", VQ_HEADER, VQ, folder=ROOT)
