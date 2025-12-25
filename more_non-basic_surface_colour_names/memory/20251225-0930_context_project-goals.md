# Project Goals and Constraints

**Date**: 2024-12-25
**Context**: User clarification on project direction

---

## Primary Goals (Priority Order)

1. **Add new overlays**: Extend MunsellSpace library with color overlays not described in Centore's paper
2. **Firm up existing overlays**: Improve/validate the 30 overlays Centore described (if possible)
3. **Academic paper**: Side goal - write a paper about the work done (TBD)

---

## Key Decisions

### What Goes Into the Library
- **New/corrected Polyhedra** in the overlay category
- NOT the Fourier correction model (that's a research tool)

### Methodology Requirements
1. **Must replicate Centore's exact methodology first**
2. **Test reproduction**: Verify we can reproduce Centore's polyhedra using his data
3. **Then extend**: Apply the validated methodology to new data

### Research Tool vs Library
- Fourier 4 model: Research tool only (conclusions not confirmed)
- Pipeline scripts: Research tools
- Final polyhedra: Library integration

---

## Repository Rules

### Files That SHOULD Be in Repo
- Python scripts (consolidated under uv)
- Scraped datasets (with .md documenting source + date)
- Documentation (.md files)
- Created/processed data

### Files That Should NOT Be in Repo
- Literature PDFs (provide .md with citation + download URL)
- Downloaded datasets (provide .md with source URL + download date)
- Large result files (regenerable from scripts)

### File Operations
- Use `git mv` for tracked files
- Untracked files can be moved with regular mv

---

## Data Sources

### XKCD Data
- Location: `assets/xkcd/` (already in project)
- NOT to be duplicated in new structure

### Centore Data
- Polyhedron files: Keep in repo (small, essential)
- Source: Centore (2020) supplementary materials

### Scraped Vocabularies
- Include in repo with source documentation
- colorhexa, color-name.com, Wikipedia, Meodai

---

## Quality Standards

The workflow/pipeline must be:
1. **Independently replicable**: Anyone can reproduce results
2. **Easily maintained**: Clear structure, modular code
3. **Easily extended**: Add new color categories simply
4. **Nothing to guess**: All assumptions documented, all steps explicit

This is primordial for:
- MunsellSpace v1.2 documentation
- Potential academic paper

---

## Current Status

### Confirmed Conclusions
- None yet - previous analysis was haphazard
- Fourier 4 model: Jury still out
- All conclusions need rigorous validation

### What Previous Work Provides
- Cues and breadcrumbs for pipeline design
- Scripts that may be useful (need review)
- Data files that may be useful (need review)

---

## Next Steps

1. **Second cleanup pass**: Complete the reorganization
   - Empty `overlay-preprocessing/` completely
   - Consolidate scripts under single uv environment
   - Fix literature/datasets per repo rules

2. **Define pipeline**: Design rigorous workflow
   - Start with Centore replication
   - Validate methodology
   - Then extend to new colors

3. **Library integration**: Add validated polyhedra to MunsellSpace v1.2

---

**Stored by**: Claude Code
**For**: MunsellSpace Color Research Project
