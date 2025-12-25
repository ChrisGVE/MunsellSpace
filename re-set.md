We are working on expanding Centore's paper "Beige, aqua, fuchsia, etc.: Definitions for some non-basic colour names", lots of things have been done, and we went back and forth. While we have worked on a data pipeline, we had to revert to basics because you had skipped an important step.

Our first objective was to introduce Centore's paper into our `MunsellSpace` crate to add color overlays that were not defined in the original dataset. This has been done.

We then contemplated the idea of expanding on Centore's paper by using other color sources, some of them much larger than Centore's dataset. We worked on multiple steps in our data pipeline. Now we need to find our steps back and organize our whole setup logically. There are a lots of documents, dataset, scripts that were used until now, and tasks completed or not; overlay-preprocessing contains some of that but there are likely more files scattered around. I want you to make a plan to achieve this objective, organize this plan around agents of various expertise, and create a PRD, including the below folder structure for the cleaned up version, with high priority tasks and subtasks. Then deploy the agents with the necessary expertise to execute the tasks.


The target state must be, a single folder "more_non-basic_surface_colour_names", with the following structure
- archives/: all existing .md files that inform this analysis, but that will be replaced by clean rewritten files (especially the analysis results that will have to be re-run), for documents that are not date stamped, prefix them with the date/time when they were created
- inventory.md: a file that contains the list of all subfolders and their content
- archives/scripts/: all existing scripts, related to the topic, no rename no modification - but we'll take their content to recreate the scripts we'll have to use
- literature/: the article from Centore (jaic_v25_03.pdf)
- datasets/: our datasets (should be under assets)
- datasets/centore/: There are two data set PolyhedronFiles/ and PolyhedronFilesJustNames/ there are the reference data that support Centore's paper
- scripts/: we should have all Python scripts, based on an `uv` environment and it must be the only environment used, such that all scripts run, if more libraries are needed, they should be added to that environment
- writeups/: only a root 
- writeups/methodology/: should contain pipeline.md that details the end to end pipeline, and documents that details algorithms
- writeups/research_notes/: .md files that represent findings made along the way they should be dated as per the usual convention YYYYMMDD_HHMM_{name}.md (for notes that are in the archives and worth taking over, base the data/time to the creation stamp of the existing file)
- writeups/references/: it should contain a "reference_collection.md" with all references collected during the search, and "active_reference.md" the references that are actively being used. Think about it like references of an academic paper, reference of data sources, articles, web searches, etc. All references must be added to the collection, while in the active reference will be only the reference that are being used (i.e. we eliminate the fool's errants).
- writeups/results/: a folder that contains the detailed and summarized results of each experiment, analysis, conducted.
- writeups/drafts/: a folder where we'll collect the draft of an academic paper we'll write about our project and its results
- memory/: a folder dedicated to you to ensure that, BEFORE EVERY CONTEXT COMPACTING you'll store the relevant context information such that you minimize the loss of information from the compaction

You may also add folders to this structure, as long as the overall logical structure is conserved.
