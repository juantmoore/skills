---
source: grok-bot
name: in-person-client-session-setup
description: >-
  Use when a paid in-person (or hybrid) client workshop or 1:1 session is
  booked: set up the client's Drive folder, the invite with video conferencing
  for recording, the Know Before You Go guide, the pre-session readiness
  checklist and client email, and the post-session recording and notes delivery.
---
# In-person client session setup

Source of truth: the Customer Workshop Playbook Google Doc in the business Drive (client workshops folder), stages 4, 7, 8 and 9. When this process changes, update both the playbook and this skill, and add a row to the playbook's Lessons learned log.

Goal: every in-person session gets captured (screen, audio, transcript) and the client ends up with one organized folder, the same as a virtual engagement. All client email is drafted for the owner to review and send. Never send automatically.

## 0. Pre-session readiness checklist (review 2 to 3 days before and again the day before)
Track each item for the client and tell the owner which are still open.
1. Payment received and logged.
2. Logistics confirmed: date, time, venue or link, calendar invite, recording setup (sections 2 and 5).
3. Know Before You Go guide sent (section 3).
4. Defined outcome: what the client walks out with.
5. Known agents to build, agreed with the client.
6. Client knows which AI tool they'll use and has the right account or plan.
7. Access tested ahead of time: connectors, any admin approvals, and a test channel or sandbox. This is usually the biggest day-of risk.
8. Presentation built with light personalization (client logo).
9. Drive folder ready: Business Context, Agent Instructions, templates (section 1, plus the client-workshop-artifacts skill once the deck is final).
10. Owner's mental walkthrough of the session (the owner does this; just remind them).

## 1. Client folder (as soon as the engagement is confirmed)
- Standard layout in the business Drive: `client workshops` › `<Client>` › `<Client> (Shared)`.
- Inside `<Client> (Shared)`, create `Agent Instructions`, `Business Context`, and `Workshop Recordings & Notes`. They can start empty.
- Create only what's missing. If an older client uses a different layout, don't move anything; tell the owner.
- Don't share it with the client until the owner says so (usually within 24 hours after the session).

## 2. Calendar invite (business calendar)
- Create the event at the agreed date, time, and venue. Use the venue's real address, from the client's own invite or the email thread when possible.
- Add Google Meet. It's used for screen sharing and recording, even in person.
- Invite the client and send notifications only when the owner asks for the invite to go out.
- The description says: it's in person, the Meet link is for screen sharing and recording, the session will be recorded, and the client gets folder access within 24 hours. Link the Know Before You Go guide and add contact info.
- Don't edit or delete an invite the client sent; point out any duplicate instead.

## 3. Know Before You Go guide (send 2 to 3 days before)
- One page, easy to skim, short headings and checkbox bullets. Don't load it with requirements.
- Sections:
  - What to Expect: 2 to 3 bullets.
  - Hardware: laptop, charger, phone for sign-in codes. Optional: mouse, notebook, adapters.
  - Software: signed in to the AI platform account being used, and logins handy for the tools to connect, with a heads-up if admin approval is needed.
  - Come With (optional): 1 to 2 repetitive tasks and a non-sensitive sample.
  - Recording and Follow-Up: the session is recorded, with folder access within 24 hours.
  - Contact line.
- Store it in the client folder. Share it with the client as a viewer before the email that links it goes out.
- Draft the email for the owner to review and send.

## 4. Pre-session client email (about 1 day before)
Draft for the owner to review and send. Short and warm:
- Confirm payment was received.
- A brief note of excitement about the session.
- Ask what tools, beyond the ones we already know about, they use to manage or communicate about projects.
- Any timely security note, for example use a VPN on public Wi-Fi for a cafe session.

## 5. Day-of recording setup (checklist for the owner)
- Arrive 10 to 15 minutes early; find an outlet and test Wi-Fi. Bring a hotspot for cafes.
- Both people join the Meet from their laptops in the room. The client shares their screen while building.
- One audio path only. The wireless mic receiver goes into the owner's laptop as the Meet mic. The client's laptop has the mic muted and the speaker off so there's no feedback.
- Start the Meet recording and transcript at the very beginning. Mention the recording on the invite and again out loud at the start.
- Backups: turn on the mics' on-board recording, and optionally run a meeting notetaker or a local screen recording.
- Remind the client to keep sensitive personal data off their screen.

## 6. After the session (within 24 hours)
- Collect the Meet recording, the transcript, any backup audio, and the notetaker output.
- Write a summary that groups what was covered and decided by topic, and ends with next steps (owner and why for each).
- Put the recording, transcript, and summary in `Workshop Recordings & Notes/<Session N - date>`. Put the prompts and configs the client built in `Agent Instructions`, and client context in `Business Context`.
- When the owner approves, share the folder with the client and draft the delivery email for review.
- Suggest at least one row for the playbook's Lessons learned log.
