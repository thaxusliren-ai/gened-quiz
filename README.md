# GenEd Board Exam Reviewer — by Nendran Duke

A **150-item General Education board exam practice test** built for **Education Generalists**
(the GenEd portion of the Philippine Licensure Examination for Teachers / LET).

Made and branded by **Nendran Duke**.

## Live site

The site is a **single, self-contained `index.html`** — no build step, no server, no dependencies.
Open `index.html` in any browser and it just works.

## Features

- **150 board exam items** across 5 subject areas:

  | Subject | Items |
  |---|---|
  | English | 30 |
  | Filipino | 25 |
  | Mathematics | 25 |
  | Science | 35 |
  | Social Science | 35 |

- Answer every question, then press **Submit**.
- **Score is revealed after submitting**: total correct, wrong, unanswered, time taken,
  a percentage and a rating band, plus a per-subject breakdown.
- **Review mode** shows each item with your pick vs. the correct answer and a short explanation.
  Filter by All / Correct / Wrong / Unanswered.
- **Question palette** to jump around; progress bar and a running timer.
- **Retake** option, and a **Print / Save as PDF** button.
- Fully **responsive** (works on phone, tablet, and desktop).

## Project files

| File | Purpose |
|---|---|
| `index.html` | **The deployed website.** Everything is embedded — CSS, JS, and all 150 questions. |
| `questions.py` | The question bank (source data), grouped by subject. |
| `build_site.py` | Generates `index.html` from `questions.py`. |

**Editing questions?** Change anything in `questions.py`, then re-run:
```bash
python3 build_site.py
```

## How to publish on GitHub (pages) 📦

The site is static, so hosting it free on GitHub Pages takes about a minute.

### Option A — GitHub Pages (recommended, free)

1. Create a new repository on GitHub (e.g. `gened-quiz`), and set it to *Public*.
2. Push these files to the repository (the `index.html` must be at the **repository root**):
   ```bash
   cd /path/to/gened-quiz
   git init
   git add .
   git commit -m "Add GenEd board exam reviewer"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/gened-quiz.git
   git push -u origin main
   ```
3. In your repository go to **Settings → Pages**.
4. Under **Build and deployment → Source**, choose **Deploy from a branch**, and pick
   the **main** branch with the **/ (root)** folder. Click **Save**.
5. Wait a minute or two — your site will be live at:
   `https://YOUR_USERNAME.github.io/gened-quiz/`

### Option B — Automatic deploy with GitHub Actions

A ready-made workflow is included at `.github/workflows/deploy.yml`. Just push to `main`;
GitHub Actions will build and publish the site to GitHub Pages automatically.
*(You'll still want to confirm the Pages source is set to "GitHub Actions" in Settings → Pages.)*

### Option C — Any static host

Because it's one file, you can also drop `index.html` onto Netlify, Vercel, Firebase,
Cloudflare Pages, or a server of your own — just serve the root folder.

## License

This question set is original practice content authored for review purposes. Feel free to
use, remix, and share it for study. Attribute **Nendran Duke**.
