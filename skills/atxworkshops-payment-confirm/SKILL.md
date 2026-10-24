---
source: grok-bot
name: atxworkshops-payment-confirm
description: >-
  Use when a Stripe successful payment arrives for an ATXWorkshops product (a
  cohort, a 1:1 or a client workshop), or when running the post-payment
  confirmation SOP. Drafts the confirmation and calendar holds for the owner to
  review and send.
---
# ATXWorkshops payment confirm

Source of truth: the Customer Workshop Playbook Google Doc in the business Drive (client workshops folder), stage 3. When this process changes, update both the playbook and this skill, and add a row to the playbook's Lessons learned log.

## When this applies
A customer just paid for an ATXWorkshops product. The trigger is a Stripe **successful payment** alert to the business inbox.

## Trigger (watch)
- Stripe team notifications are on for successful payments.
- `hello@getspiffy.ai` is a Stripe team member, so alerts land in the business Gmail.
- Goal: within **2 hours** of the alert, the confirmation draft and calendar holds are ready for the owner.

## Within 2 hours, do this

### 1. Capture payment facts
From the Stripe email or receipt: customer name, email, amount, product, receipt id, and any slot choices. If slots are missing, check the checkout notes, or ask in the confirmation email.

### 2. Draft the confirmation email
- From: `hello@getspiffy.ai`
- To: the buyer
- Tone: warm, clear, short
- Include: thanks, the product name, what they get, the session times, Meet links once calendar holds exist, a location line for in-person sessions ("address coming" until the venue is set), and a reply-friendly close.
- Cohort products only: one line with the refund rule (for example, a full refund if the minimum seats aren't met).

### 3. Draft the calendar holds
- One hold per session the buyer booked, matching their slots. Use the business calendar.
- In-person sessions: the venue (or "address coming") plus Google Meet for screen sharing and recording.
- Virtual sessions or office hours: Google Meet.
- Title clearly, for example `<Product>: <Name>: In person`.
- Add the buyer as a guest but don't send invites until the owner approves.

### 4. Ownership and send rules
- Draft only. Never send the confirmation or the invites on your own, at 2 hours or ever.
- Tell the owner the draft and holds are ready, with the payment facts.
- The owner reviews and sends. After the owner sends, check Sent and confirm the invites went out.
- If nothing has gone out 2 hours after the alert, remind the owner. Don't send.

## Next
Booking and setup (client folder, invite details, Know Before You Go guide) is in the in-person-client-session-setup skill and playbook stage 4.
