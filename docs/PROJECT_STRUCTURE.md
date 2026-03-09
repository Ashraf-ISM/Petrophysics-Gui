# Project Structure

## Top Level

- `src/petroanalysis/`: installable application package
- `scripts/`: executable launch scripts
- `tools/`: standalone maintenance utilities
- `data/samples/`: bundled sample LAS and DLIS files
- `docs/`: project notes and diagrams
- `notebooks/`: exploratory notebooks
- `archive/experimental/`: legacy prototypes kept out of the runtime path

## Runtime Package Layout

- `src/petroanalysis/app/`: Qt application bootstrap and main window
- `src/petroanalysis/features/petro_analysis.py`: main workspace implementation
- `src/petroanalysis/features/plotting/`: plotting widgets and helpers
- `src/petroanalysis/ui/generated/`: generated Python UI classes
- `src/petroanalysis/widgets/`: reusable custom widgets
- `src/petroanalysis/resources/images/`: packaged runtime images
- `src/petroanalysis/resources/ui/`: original Qt Designer `.ui` source files
- `src/petroanalysis/utils/paths.py`: resource path helpers

## Notes

- The active application code now lives entirely under `src/petroanalysis`.
- Experimental files remain available under `archive/experimental/`, but are intentionally separated from the supported app path.
- Runtime images are resolved from packaged resources instead of the current working directory.
