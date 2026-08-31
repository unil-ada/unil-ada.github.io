*Practical advice, not rules. The binding rules are in the Requirements
document; nothing here changes them. If the two ever disagree, the
Requirements win.*

"Shipping" means handing over work that someone else can open, read and
run without asking you a single question. Most marks lost on this project
are lost here — not in the modelling.

---

## The test that matters

Before you submit, do this on a machine that is not the one you worked on:

1. Download your own submission, as a marker would.
2. Unzip it into an empty folder.
3. Follow your own README exactly as written, changing nothing.
4. See whether the results in your paper appear.

If step 4 fails, you have found what the marker would have found. Almost
every problem below is caught by this one test.

## What to hand over

```
lastname_firstname/
  paper.pdf              the research paper
  README.md              how to reproduce, in order
  code/                  the scripts and notebooks
  data/                  the data, or how to get it
  figures/               what the paper shows
  recording.mp4          or a link, if the file is large
```

Use lowercase names with no spaces and no accents. `data final (2).csv`
breaks on other people's machines; `prices_2020_2024.csv` does not.

## The README

Half a page is plenty. In this order:

- what the project does, in two sentences;
- what to install (`pip install -r requirements.txt` is the whole answer,
  if you write the requirements file);
- what to run, in the order to run it;
- how long it takes, and what it produces;
- where the data came from.

Write it as instructions to a stranger, because that is who reads it.

## Code

- **A script that runs top to bottom beats clever code that needs
  explaining.** You are graded on evidence that you can apply the
  methods, not on style.
- **Set the random seed.** If your numbers change every run, nobody can
  check anything in your paper.
- **No absolute paths.** `/Users/anna/Desktop/thesis/data.csv` exists on
  exactly one computer in the world. Use `data/prices.csv`.
- **Restart the notebook and run it once, in order, before submitting.**
  Notebooks that work only if cells are run out of order are the most
  common reproducibility failure there is.
- **Keep secrets out.** No API keys in the code. If your project needs
  one, say in the README which key is needed and where to put it.

## Data

- Small and shareable: include it.
- Large or licensed: include the download script and say plainly what the
  licence permits. Requirement 4.6 allows this.
- Say where every data set came from and what you did to clean it. "I
  dropped 412 rows with missing prices" is a sentence the marker wants
  to read; silence about it is not.

## The paper

- Use the SIAM template from the start. Reformatting at the end always
  costs more than it saves.
- Every figure needs axis labels, units, and a caption saying what to
  look at.
- Report what you actually ran. If a method failed, that belongs in the
  paper — Requirement 6.3 lets an honest negative result score full marks.

## The recording

- Fifteen minutes, screen plus voice. A Zoom recording of yourself is fine.
- A structure that fits the time: the question (2 min), the data (2 min),
  the method (4 min), the results (5 min), what you would do next (2 min).
- Watch the first minute back before submitting. Inaudible sound is the
  usual failure, and it cannot be fixed after the deadline.
- Say your name at the start.

## Declaring your tools

Requirement 5 asks which tools you used and what for. A few honest lines:

> ChatGPT: drafted the plotting code in `figures.py`; rewrote three
> paragraphs of the introduction for clarity. All statistical results are
> my own work and were checked by hand.

Nobody is penalised for using assistants — the course teaches you to. The
penalty is for not declaring them, and for being unable to explain what
you handed in.

## The week before the deadline

- Run the reproduction test above. Now, not on the last evening.
- Check the page count against Requirement 4.2.
- Check the eight required sections are present and in order.
- Submit a first version early. You can replace it; you cannot create it
  after the deadline.
