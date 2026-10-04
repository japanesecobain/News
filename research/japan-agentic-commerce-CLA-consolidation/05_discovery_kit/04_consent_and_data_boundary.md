# Consent and data-handling boundary (discovery round)

**Applies to:** the job-comparison interviews in `01_interview_guide_ja.md`. It is not legal advice. Before any service handles other people's emails or records at scale, get counsel on APPI (including cross-border transfer under Art. 28) and on telecommunications-business notification (verification queue in `06_verification_queue.csv`).

## What the researcher will and will not do

| Will | Will not |
|---|---|
| Interview by voice, video or in person; take notes; record only with consent | Ask for passwords or one-time codes; log into any account; use inbox OAuth |
| View a record **on the participant's own screen** if they offer | Receive screenshots, files or forwarded emails in this round |
| Note which **fields** a record contained (item name present, delivery date present, tracking number present) | Transcribe order numbers, tracking numbers, links, addresses or names |
| Keep coded notes under a participant code | Upload any participant content to an AI service |
| Delete notes and recordings by a stated date, or earlier on request | Make purchases, contact merchants or carriers, or change deliveries for anyone |

## Three separate consents (record each Y/N)

1. **Recording and notes:** may the conversation be recorded or noted for this research?
2. **Retention:** may coded notes be kept until the deletion date? (Default: notes only; no record images.)
3. **AI upload:** may de-identified notes be processed by an AI service? (**Default: No.** This round does not need it.)

Consent to local viewing of a record is **not** consent to retention or AI upload.

## Identifiers

- Redaction is not anonymity. An order number, tracking number or order-page URL can identify a person. Do not write them down.
- Use participant codes (`P01`) and household codes (`H01`). Keep the code-to-contact mapping separate and delete it with the notes.

## Refusals

- Respect any refusal immediately and do not re-ask in the same session.
- Code the refusal as `record_shown = DECLINED`.
- A refusal is evidence about that capture method only. It is not evidence that the person has no need or would reject every interface.
- If an alternative capture method is studied later, run it as a separately labelled, pre-declared protocol with different participants or a fresh consent.

## Sensitive situations

- If a participant raises fraud, an unauthorised charge or a phishing email, do not investigate. Suggest they contact the merchant or card issuer through official channels, and record only that an exception of type `OTHER` occurred.
- Stop the session if the participant becomes uncomfortable.

## Incentives

- Pay a fixed, modest thank-you that does not depend on what the participant says or shows.
- Do not use incentives to obtain records.
