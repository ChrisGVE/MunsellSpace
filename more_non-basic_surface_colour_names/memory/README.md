# Memory Folder - Context Preservation for Claude Code

## Purpose

This folder preserves critical context across Claude Code sessions. Before context compaction occurs, key information should be stored here to minimize information loss.

## Usage

When working on complex multi-session tasks:

1. **Before ending a session** or when context is becoming large, save important state to this folder
2. **At session start**, review recent context files to restore working knowledge
3. **During work**, update context files with significant decisions and findings

## File Naming Convention

Format: `YYYYMMDD-HHMM_context_{topic}.md`

Examples:
- `20251224-2240_context_project-state.md` - Current project state summary
- `20251224-1500_context_algorithm-design.md` - Algorithm design decisions
- `20251225-0930_context_debugging-session.md` - Debugging findings

## What to Store

### High Priority
- Current task state and progress
- Key decisions made with rationale
- Blocking issues and their resolution attempts
- Critical findings from investigation/research

### Medium Priority
- File locations of important resources
- API patterns and conventions discovered
- Test results and validation outcomes

### Low Priority (optional)
- Session timestamps for continuity
- Links to external resources consulted
- Notes for future sessions

## Retention Policy

- Keep recent context files (last 7 days active work)
- Archive older files if they contain permanently valuable decisions
- Delete files that are superseded by newer context

## Related Files

- `/Users/chris/dev/projects/libraries/MunsellSpace/.taskmaster/tasks/tasks.json` - Task state
- `/Users/chris/dev/projects/libraries/MunsellSpace/CLAUDE.md` - Project instructions
- `/Users/chris/dev/projects/libraries/MunsellSpace/.taskmaster/docs/` - PRD documents
