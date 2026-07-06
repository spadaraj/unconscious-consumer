# TUC Substack Pipeline — Setup

Automates two things:

1. **Daily Notes page** — a page in your repo (`notes/today.html`) refreshes each morning with 3 candidate Substack Notes generated from articles.json. You bookmark it.
2. **Weekly restack digest page** — every Sunday evening, `notes/digest.html` refreshes with the top 5 recent posts from your subscriptions plus a POV angle for each.

Both run on GitHub Actions, commit the generated HTML back to your repo, and Vercel auto-deploys. You'll access them at:

- **https://theunconsciousconsumer.com/notes/today.html**
- **https://theunconsciousconsumer.com/notes/digest.html**

Both pages have "Copy" buttons — click, paste into Substack.

`notes/` is excluded from robots.txt and every generated page has `noindex, nofollow`, so search engines skip them. The URLs are guessable but not indexed. If someone genuinely wants your drafts they can guess the path; if that matters more, we can add password protection via Vercel.

---

## What you need to do (once)

### 1. Add your Anthropic API key as a repo secret

1. Go to **https://github.com/spadaraj/unconscious-consumer/settings/secrets/actions**
2. Click **New repository secret**. Name: `ANTHROPIC_API_KEY`. Value: paste your Anthropic key (starts with `sk-ant-`). Click **Add secret**.

That's the only secret needed. The daily job doesn't need it (it just reads the pre-built notes bank).

### 2. Commit and push these new files to GitHub

From your terminal, in the site folder:

```sh
cd /Users/adamspadaro/Documents/unconscious-consumer/unconscious-consumer
git add pipeline/ .github/workflows/ notes/ robots.txt
git commit -m "Add Substack Notes pipeline (daily + weekly HTML pages)"
git push
```

### 3. Run the Notes backfill once

This generates 5 Notes for each of your 57 articles and saves them to `pipeline/data/notes-bank.json`. Runs on your Mac, uses your Anthropic key. Should take ~10 minutes and cost a couple of dollars at most.

```sh
cd /Users/adamspadaro/Documents/unconscious-consumer/unconscious-consumer
pip3 install -r pipeline/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # paste your key here
python3 pipeline/generate_notes_bank.py
```

When it finishes, commit the bank so the GitHub Action can read it:

```sh
git add pipeline/data/notes-bank.json
git commit -m "Add initial Notes bank (~285 notes across 57 articles)"
git push
```

### 4. Test both builders locally

```sh
python3 pipeline/build_daily_notes.py
open notes/today.html
```

Should open a nicely-styled page in your browser with 3 notes and copy buttons.

For the digest:

```sh
python3 pipeline/build_restack_digest.py
open notes/digest.html
```

This calls Claude, so it uses your API key. Costs a few pennies.

### 5. Trigger the workflows once from GitHub

Go to **https://github.com/spadaraj/unconscious-consumer/actions**. You should see two workflows: "Daily Notes Page" and "Weekly Restack Digest Page". For each, click into it, then click **Run workflow** (top right). This fires the build once and confirms the commit-back works.

Wait ~30 seconds after each finishes, then visit:

- https://theunconsciousconsumer.com/notes/today.html
- https://theunconsciousconsumer.com/notes/digest.html

### 6. Bookmark both URLs on your phone and laptop

- Add to your browser bookmarks bar
- On iOS: Share → Add to Home Screen for a one-tap icon
- Optional: set a repeating iOS/macOS reminder — "Check notes/today at 9am daily" and "Check notes/digest Sunday evening"

---

## How to use it, day to day

**Every morning:** open `notes/today.html` on your phone or laptop. Skim the 3 candidates. Tap Copy on the one that reads best. Paste into Substack Notes. Optionally tweak. Post.

**Every Sunday evening:** open `notes/digest.html`. Skim the 5 picks. For any that look good: click the post title → open the post → hit restack in Substack → paste the copied angle as your caption → tweak → post.

That's it. No email checking, no other manual work.

---

## When you publish a new article

Add it to `articles.json` as you already do, then regenerate Notes for the new article:

```sh
python3 pipeline/generate_notes_bank.py   # skips articles already in bank
git add pipeline/data/notes-bank.json && git commit -m "Notes for new article" && git push
```

The generator is idempotent — it only processes articles it hasn't seen before.

---

## Customising

- **Change refresh times.** Edit the `cron:` line in `.github/workflows/daily-notes.yml` and `weekly-digest.yml`. Cron format: `minute hour day month weekday` (all in UTC). Current: 12:00 UTC daily (08:00 EDT), 22:00 UTC Sunday (18:00 EDT).
- **Change how many Notes per day** or **Substacks watched.** Edit `pipeline/config.json` or `pipeline/substacks.json`.
- **Fix a broken Substack feed URL.** Some URLs in `substacks.json` were my best guesses. If the weekly digest page shows fetch errors in the "Feed fetch errors" section at the bottom, open the publication's Substack in your browser and copy the actual base URL (without `/feed`) into `substacks.json`. Then commit and push.
- **Change the Notes voice.** Edit `SYSTEM_PROMPT` at the top of `pipeline/generate_notes_bank.py`. Then to test on a single article: temporarily delete a slug from `pipeline/data/notes-bank.json` under `generated_slugs`, delete its notes from the `notes` array, and re-run the generator. If the new voice reads better, add `--force` to regenerate everything: `python3 pipeline/generate_notes_bank.py --force`.
- **Change the page styling.** Edit the `<style>` block in `build_daily_notes.py` or `build_restack_digest.py`.

---

## What to check if something breaks

- **Page didn't update.** Go to **https://github.com/spadaraj/unconscious-consumer/actions**. Click the most recent run of the failing workflow. Check the logs for the failed step.
- **"ANTHROPIC_API_KEY not set" in the logs.** You didn't add the secret in step 1, or the name is misspelled. Names are case-sensitive.
- **Workflow failed at "Commit and push".** The `permissions: contents: write` line at the top of the workflow file needs to be present. Also check under repo Settings → Actions → General → "Workflow permissions" — it should be set to "Read and write permissions".
- **Weekly digest shows many feed errors at the bottom.** The URLs in `substacks.json` are best guesses for some publications. Fix as needed (see Customising above).
- **Copy buttons don't work on old browsers.** The Clipboard API needs a modern browser served over HTTPS. Your site is on HTTPS so this should be fine; on very old browsers the button will show an alert asking you to select the text manually.
- **The Notes voice is off.** Adjust `SYSTEM_PROMPT` in `generate_notes_bank.py` and regenerate.

---

## Cost, roughly

At current Claude Opus pricing:
- Backfill (once): ~$1–3 total for all 57 articles
- Weekly digest: ~$0.01–0.05 per run (52 runs/year = $0.50–2.50/year)
- Daily notes builder: $0 (no Claude call, just reads the bank)
- Regenerating notes for new articles: ~$0.03 per article

Under $5/year running cost after the initial backfill. To cut cost further, change `"claude_model"` in `config.json` to `"claude-sonnet-5"` — quality drops slightly, cost drops ~5x.
