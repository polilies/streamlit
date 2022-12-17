import streamlit as st
import time

col1, col2, col3 = st.columns([1,2,1])

col1.markdown(" # Wellcome to my App")
col1.markdown("Here is some info for the App.")

uploaded_phote = col2.file_uploader("Upload a photo")
camera_photo = col2.camera_input("Take a photo")

progressbar = col2.progress(0)

for perc_completed in range(100):
    time.sleep(0.05)
    progressbar.progress(perc_completed + 1)

col2.success("Phoot uploaded succesfully")

col3.metric(label="Temperature", value="60 C", delta="-3 C")

with st.expander("Click to read more"):
    st.write("Hello, here are more details on this topic that you were interested in.")
