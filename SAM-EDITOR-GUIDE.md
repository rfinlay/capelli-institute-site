# Editing your website: a one-page guide for Sam

Your site is built from two small files: one holds the books and lectures (titles, editions, prices, buy links, ISBNs, synopses), the other holds the main page text. You edit both through a simple form-style editor called Pages CMS. You never touch code. A few minutes after you save, the live site updates on its own.

## One-time setup

1. Create a free GitHub account at github.com if you do not have one, and send us the username. We add you to the site repository. (If you would rather not have a GitHub account, tell us; Pages CMS can also invite you by email, with a smaller set of permissions.)
2. Go to app.pagescms.org and click Sign in with GitHub.
3. When it asks, install the Pages CMS app and allow it to see the repository called capelli-institute-site.
4. Open capelli-institute-site. You will see two sections on the left: Books and lectures, and Site copy.

## Editing a price

1. Open Books and lectures.
2. Under Books, click the title. Under Editions, click the edition you want (Paperback, Hardback, Collector's, and so on).
3. In Price, type the number only, for example 29.95. No dollar sign.
4. Click Save at the top right. The page says Saved. Within about two minutes the live site shows the new price.

## Adding a buy button (your Stripe Payment Link)

1. In your Stripe dashboard, copy the Payment Link for that edition. It starts with https://buy.stripe.com/ (the separate guide, STRIPE-SETUP-FOR-SAM, walks through creating them).
2. In Pages CMS, open the same edition and paste the link into Buy link (Stripe Payment Link).
3. Save. The book page now shows a gold Buy this edition button that opens your Stripe checkout. Until a link is pasted, the button reads Available soon and cannot be clicked, so nothing on the site ever points at a dead checkout.
4. If the edition is also sold on Amazon, paste that page's address into Amazon link. A second button, Also on Amazon, appears under the buy button.

## Other things you can change the same way

- ISBN, binding, tagline, and availability for each edition.
- The synopsis, pull quote, keywords, and subtitle for each book.
- Each lecture's introduction, excerpt, and YouTube link.
- Site copy: the phone number and address in the footer, the line under the title on the home page, and the opening lines of the CEU, Workshops and Launch pages.

Fields marked read-only (page addresses, SKUs, cover art paths) are set by us. Send us new art or a new title and we place it; your edits keep working around it.

## Publishing

Saving is publishing. Each save makes a small record in the site's history with your name and the time, so any change can be undone. If a save is refused with a red message, the message says which field and why (for example, a buy link that does not start with https://). Fix it and save again.

If the site does not update after five minutes, or something looks wrong, text or email Rick. We can see every save and can put any page back the way it was.
