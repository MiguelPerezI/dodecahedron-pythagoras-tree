# The American Mathematical Monthly: submission package

Rebuild everything with `bash monthly/build.sh`. Upload the files in `monthly/upload/`.

## Files to upload in the Taylor & Francis Submission Portal

Required by the File Upload step (`upload/required/`):

| Portal file type | File |
|---|---|
| Manuscript - with author details | `upload/required/1_Manuscript_with_author_details.pdf` |
| Manuscript - anonymous | `upload/required/2_Manuscript_anonymous.pdf` |
| Cover Letter | `upload/required/3_Cover_Letter.pdf` |

Optional extras (`upload/optional/`). The portal accepts them, and the Instructions for Authors ask LaTeX authors for the source zip, so upload them too:

| Portal file type | File |
|---|---|
| LaTeX Source Files (single zip) | `upload/optional/LaTeX_source.zip` |
| Figure (one file each) | `upload/optional/figures/Figure_*.jpg` and `Figure_*.eps` |

## Form fields (copy and paste)

**Article type:** Research Article (18 pages in the review layout; the guideline is 6 to 20).

**Title:** A Pythagoras Tree Grown from a Dodecahedron

**Abstract** (223 words; the limit is 250): paste from the manuscript.

**Keywords** (5, the maximum): Pythagoras tree; dodecahedron; self-similar fractal; iterated function system; mathematical art

**MSC 2020** (up to 3): 28A80 (Fractals), 52B10 (Three-dimensional polytopes), 00A66 (Mathematics and visual arts)

**Author:** Miguel Esteban Pérez Ibarra, Escuela Superior de Física y Matemáticas, Instituto Politécnico Nacional, Mexico City, Mexico. Corresponding author, supersluky@gmail.com. Add your ORCID iD if you have one.

**Funding:** No funding was received for this work.

**Disclosure statement:** The author reports there are no competing interests to declare.

**Data availability:** https://github.com/MiguelPerezI/dodecahedron-pythagoras-tree

**Data set associated with the paper?** Yes. The portal asks for a DOI or hyperlink. A Zenodo DOI is preferred (see below); the GitHub link is accepted.

**Color in print:** No. Color online is free; print color costs £300 for the first figure. The cover letter says black-and-white print is acceptable.

## Decide before submitting

1. **Generative AI declaration.** Updated on 2026-10-24. It says English is not the author's native language and that Claude (Anthropic) was used only to help draft and edit parts of the text and to help produce the Blender renders, and for no other purpose. The cover letter mentions it too.
2. **Affiliation.** T&F asks for the affiliation where the research was done. If you are no longer at ESFM, either keep ESFM because the work grew from your studies there, or write "Independent researcher, Mexico City". The anonymous PDF is unaffected.
3. **Double-anonymous review.** The anonymous PDF has no name, email, acknowledgment, biography, or GitHub link, and the PDF metadata is empty. But the public GitHub repository and any arXiv posting can be found by title. T&F says this is allowed, but anonymity can then not be guaranteed. If the arXiv version is posted, mention it in the cover letter.
4. **Official style file.** The Monthly asks for `maa-monthly.sty` from `Monthly_Templates.zip`, linked from the journal's Instructions for Authors. The download sites block automated access, so download it yourself and put it in `monthly/source/`. The build picks it up automatically. Then rerun `bash monthly/build.sh` and check the page count.
5. **Zenodo DOI (recommended).** Connect the GitHub repository to Zenodo, publish a release, and use the DOI in the data availability statement.
6. **arXiv and the Monthly together.** T&F allows preprints. Upload the arXiv version first if you want the date on record.

## What changed from the arXiv version

* American spelling (generalized, remodeled, colored, center, neighboring, analog, Acknowledgments).
* Single quotation marks, as the T&F style guide requires.
* New abstract for a general reader, with almost no notation.
* Five keywords and the MSC codes.
* Added sections in the order the journal requires: Funding, Disclosure, Declaration of generative AI use, Data availability, Notes on contributor.
* References in the NLM style that T&F uses, with completed issue and page data.
* A list of figure captions at the end, and the figures as separate files, with line art as EPS.
* The mathematics is unchanged.
