# Third-generation cephalosporin resistance among *Klebsiella pneumoniae* in Peru

Data and code for the systematic review and meta-analysis "Third-generation cephalosporin resistance among *Klebsiella pneumoniae* in Peru: a systematic review and meta-analysis".

- **Authors:** Diego Salas, Lourdes Judith Espinoza, Gabriel Ariel Vásquez, Leydy Carhuamaca, Antonio Marty Quispe
- **Protocol:** PROSPERO [CRD420251268259](https://www.crd.york.ac.uk/PROSPERO/view/CRD420251268259)
- **Archived copy:** Zenodo, https://doi.org/10.5281/zenodo.21608907
- **Version:** 2.0, October 2026. Eleven studies, twelve reports. It replaces version 1.0, which held ten studies.

Results are reported in the manuscript. This repository holds what is needed to check and rerun them.

## Contents

| Path | What it is |
|---|---|
| `data/main_dataset_v3.csv` | Analysis dataset. One row per report, with the blood and urine isolates of Rondon et al. in two rows |
| `data/full_text_decisions.csv` | Every report assessed in full text, with the decision and the reason for exclusion. Source of the PRISMA flow diagram and of Supplementary Table S5 |
| `data/extraction_audit.csv` | Extraction of the primary outcome verified against each article. Source of Supplementary Table S6 |
| `search/pubmed_2026-09-18.csv` | Records retrieved from PubMed on 18 September 2026 |
| `search/scopus_2026-09-19.csv` | Records retrieved from Scopus on 19 September 2026, bibliographic fields only |
| `search/title_abstract_screening.csv` | Title and abstract screening by two reviewers, with the consensus decision |
| `analysis/analysis.qmd` | The complete analysis in R and Quarto. It writes `results/` and `figures/` |
| `analysis/make_tables_1_2.py` | Builds Tables 1 and 2 as Word files from `results/` |
| `results/` | Tables written by the analysis: pooled estimates, sensitivity analyses, study-level results and JBI ratings |

Abstracts are not included in the search files because they belong to the publishers. Figures are not stored here because the analysis regenerates them.

## How to rerun the analysis

1. Install R 4.6 or later and Quarto.
2. Install the R packages: `dplyr`, `forcats`, `ggplot2`, `ggrepel`, `janitor`, `knitr`, `meta`, `metafor`, `ragg`, `readxl`, `scales`, `stringr`, `tibble`, `tidyr`, `writexl`.
3. From the repository root run `quarto render analysis/analysis.qmd`.
4. Optionally run `python analysis/make_tables_1_2.py`. It needs Python 3 and no extra packages.

The analysis was run with R 4.6.1, `meta` 8.5-0 and `metafor` 5.0-1. Pooled proportions use a random-effects model on logit-transformed proportions with REML.

## Reading the data

Column names and notes are in Spanish, the working language of the team. The main ones are listed here.

**`main_dataset_v3.csv`**

| Column | Meaning |
|---|---|
| `study_label_author`, `study_year_range`, `meta_year` | Study, isolate-collection period and its midpoint |
| `location`, `hospital`, `sample_type` | Setting and specimen |
| `n_tested`, `n_resistant`, `prevalence` | Isolates tested for the cephalosporin used, isolates resistant or non-susceptible, and their ratio |
| `agent_used` | Cephalosporin, or ESBL phenotype, behind the count |
| `measurement_tier` | 1, resistance to a named cephalosporin. 2, resistance to the class without naming the drug. 3, ESBL phenotype used as a surrogate |
| `primary_report` | `SI` when the row enters the primary analysis |
| `ctx`, `cro`, `caz`, `cip`, `tmp_smx`, `carbapenem_resistance`, `esbl` and similar | Proportion resistant to each antimicrobial, where reported |

**`full_text_decisions.csv`**

| Column | Meaning |
|---|---|
| `Decision` | `INCLUIDO` included, `EXCLUIDO` excluded, `NO RECUPERADO` full text not retrieved |
| `Codigo` | Reason for exclusion, see below |
| `Motivo_principal_EN` | Reason for exclusion in English, as printed in Supplementary Table S5 |
| `En_flujo_PRISMA` | `SI` when the report is counted in the PRISMA flow diagram |
| `Captado_PubMed_…`, `Captado_Scopus_…` | Whether the database search retrieved the report |

| Code | Reason for exclusion |
|---|---|
| E1 | *Klebsiella* reported at genus level only |
| E2 | No Peruvian data |
| E3 | Non-human isolates, animal or environmental |
| E4 | Case or outbreak report without prevalence estimate |
| E5 | Resistance-selected sampling, no population denominator |
| E6 | Not a primary observational study |
| E7 | No *K. pneumoniae*-specific third-generation cephalosporin data |
| E8 | Unpublished thesis |

**`title_abstract_screening.csv`**: `Revisora_1` and `Revisora_2` are the two reviewers' decisions and `Consenso` is the agreed decision. `EXCLUIR` means exclude and `INCLUIR` means assess in full text. Rows with a `Registro_ID` and no consensus had already been assessed in full text.

## License and citation

Data and code are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). To cite them, use the Zenodo record above. All data were extracted from published studies and are provided in aggregated, study-level form.

## Contact

Diego Salas, through the issues page of this repository.
