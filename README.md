# Andrelelele

A new instrument.

## Summary

Draw freehand in the browser and convert the drawn path into a short, periodic audio waveform. The app uses `streamlit` with `streamlit-drawable-canvas` for input and a small DSP engine (`dsp.py`) to turn points into audio you can play with `st.audio`.

## Quick start

- Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Run the app:

```bash
streamlit run app.py
```

Open the URL shown by Streamlit (usually `http://localhost:8501`) and draw on the canvas.

## TODO

- `_remove_overlap()` in `dsp.Player` is a stub and should be implemented to handle self-overlapping doodles.
- `_calculate_cycles_for_duration()` may need tuning to precisely map cycles to audio samples.
- Degenerate drawings (very few points or zero ranges) are not specially handled.
