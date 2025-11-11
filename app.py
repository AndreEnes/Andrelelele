import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import matplotlib.pyplot as plt

import dsp

st.set_page_config(page_title="Drawable Canvas Points", layout="wide")
st.title("Andrelelele 🎸")

col1, col2 = st.columns([2, 1])

with col1:
    st.caption("Draw something and listen to your doodle 🦐")
    
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="black",
        background_color="white",
        update_streamlit=True,
        height=400,
        width=600,
        drawing_mode="freedraw",
        key="canvas",
    )

with col2:
    st.subheader("🎶")

    debug_mode = st.toggle("Debug Mode")
    sample_duration = st.slider("Sample duration (s)", min_value=1, max_value=10)
    sample_frequency = st.number_input("Sample frequency (Hz)", value=440)
    scaler = st.selectbox("Scaler", ("MinMax", "Robust"))
    
    player = dsp.Player(
        sample_duration=sample_duration,
        sample_frequency=sample_frequency,
        debug_mode=debug_mode,
        scaler=scaler
    )

    if canvas_result.json_data is not None:
        objects = canvas_result.json_data.get("objects", [])
        all_points = []

        for obj in objects:
            if obj["type"] == "path":
                for segment in obj["path"]:
                    coords = segment[1:]
                    if len(coords) >= 2:
                        for i in range(0, len(coords), 2):
                            x, y = coords[i], coords[i + 1]
                            all_points.append((x, y))

        if all_points:
            df_points = pd.DataFrame(all_points, columns=["x", "y"])
            
            audio_data = player.generate_waveform(df_points)
            
            st.divider()
            st.subheader("Doodle sound")
            st.audio(audio_data, sample_rate=player.sample_rate)

            if player.debug_mode:
                st.subheader("Debug Section")
                debug_x, samples_per_wave = player.debug_waveform()

                fig, ax = plt.subplots()
                if len(audio_data) > 0:
                    plot_length = int(samples_per_wave)
                    ax.plot(debug_x[:plot_length], audio_data[:plot_length], 'o-')
                    ax.axhline(y=0, color='black')
                    ax.set_title("Generated Waveform")
                    ax.set_xlabel("Sample")
                    ax.set_ylabel("Amplitude")
                else:
                    ax.text(0.5, 0.5, "No data to plot", ha='center', va='center')
                    ax.set_title("Generated Waveform")
                st.pyplot(fig)
                st.caption("Generated waveform")
            
        else:
            st.info("Draw something!")
