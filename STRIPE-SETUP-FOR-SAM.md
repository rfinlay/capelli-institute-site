# Setting up Stripe for book sales: a guide for Sam

The site sells each edition through a Stripe Payment Link. Stripe is the checkout; the money goes straight into your own Stripe account and then to your bank. RGF never holds your money and never sees your card data. Stripe's fee on a card sale in the US is 2.9% plus 30 cents (about $1.17 on a $30 book). There is no monthly fee.

## Part 1: open your Stripe account (about 20 minutes)

1. Go to stripe.com and click Start now. Sign up with your email. Use an email you check, because order notifications arrive there.
2. Stripe asks for business details: your legal business name (The Capelli Institute, or whichever entity sells the books), the EIN or your SSN if you sell as an individual, the business address, a phone number, and a short description such as "Books and printed lectures by the author."
3. Add the bank account that should receive the money. Payouts arrive on a rolling schedule, normally two business days after a sale once the account is established.
4. Finish the identity check Stripe asks for. Until this is done the account can take test payments only.
5. In Settings, under Branding, you can upload the Institute crest and set the gold and navy colors so the checkout page matches the site. The brand colors are navy 000C1E and gold FCB367.

## Part 2: create one Payment Link per edition

Each edition for sale (paperback, hardback, collector's, each printed lecture) gets its own link. That is what makes the Buy button on the matching page sell the matching thing.

1. In the Stripe dashboard, open Product catalog and click Add product.
2. Name it exactly as it appears on the site, for example "The Capelli Doctrine, Hardback Edition." Add the price. Choose One time. Save.
3. Open Payment Links and click New. Choose the product you just made.
4. Under Options, turn on Collect customers' addresses, and choose Shipping addresses. Add the countries you will ship to (United States at least). This is how you learn where to send the book.
5. If you charge for shipping, add a shipping rate here. If you collect Texas sales tax, Stripe Tax can calculate it for you; it costs a little extra per transaction, so decide with your accountant whether to turn it on.
6. Under After payment, you can leave Stripe's confirmation page or send buyers back to the book's page on the site. The book page addresses are:
   https://rfinlay.github.io/capelli-institute-site/books/ (then the title), for example
   https://rfinlay.github.io/capelli-institute-site/books/the-capelli-doctrine.html
   These change to thecapelliinstitute.com addresses once the domain is pointed at the site.
7. Click Create link. Copy the link. It looks like https://buy.stripe.com/ followed by letters and numbers.
8. Repeat for every edition. Keep a simple list: edition name, price, link.

## Part 3: put the links on the site

Open Pages CMS (see SAM-EDITOR-GUIDE), open the edition, paste the link into Buy link (Stripe Payment Link), and save. The Buy button goes live within a couple of minutes. Or send the list from Part 2 to Rick and we paste them for you.

## Part 4: when an order comes in

Stripe emails you for every sale. The Payments page in your dashboard shows the buyer's name, email, shipping address, and what they bought. You pack and ship the book, then mark it however you like (Stripe has a note field on each payment). Refunds are one click on the same page.

## What to send us

- The Payment Link for each edition, with the edition name (or just paste them in Pages CMS yourself).
- The price for each edition, so the page can show it next to the button.
- The ISBN for each edition that has one.
- Amazon page addresses for any edition that is also sold on Amazon.
- Your GitHub username, or the email address to invite, for the editor.

## What never to send us

Your Stripe password, bank details, or any card numbers. We never need them, and Stripe will never ask you to share them with anyone.
