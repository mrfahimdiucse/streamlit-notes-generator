import streamlit as st
from api_calling import quiz_generator
from api_calling import note_generator, audio
from PIL import Image

st.header(":red[Note Summary and Quiz Generator]",anchor=False)
st.markdown("Upload upto 3 images to generate Note summary and Quiz")
st.divider()

with st.sidebar:
    st.header(":green[Controls]")
    images=st.file_uploader("Upload The Photos of your note",type=['jpg','jpeg','png'],accept_multiple_files=True)
    pil_images=[]
    for img in images:
        pil_img=Image.open(img)
        pil_images.append(pil_img)
    
    if images:
        if len(images)>3:
            st.error("Upload at max 3 images")
        else:
            st.subheader("Upload Images")
            col=st.columns(len(images))
            for i,img in enumerate(images):
                with col[i]:
                    st.image(img)
    selected=st.selectbox("Enter The Difficulty of Your Quiz",("Easy","Medium","Hard"),index=None)
    clicked=st.button("Click the button to initiate AI",type="primary")



#section creation
if clicked:
    if not images:
        st.error("Choose atleast 1 Image!")
    if not selected:
        st.error("Choose Difficulty Level!")
    if images and selected:
        #notes
        with st.container(border=True):
            st.subheader("Your Notes :")
            with st.spinner("AI is Writing notes for you"):
                generated_notes=note_generator(pil_images)
                st.markdown(generated_notes)
        #audio
        with st.container(border=True):
            st.subheader("Audio Voice:")
            with st.spinner("Audio is generating for you..."):
                #clearing markdown
                cleaned_notes = generated_notes.replace("#", "")
                cleaned_notes = generated_notes.replace("*", "")
                cleaned_notes = generated_notes.replace("_", "")
                cleaned_notes = generated_notes.replace("'", "")
                audio=audio(cleaned_notes)
                st.audio(audio)
        #quiz
        with st.container(border=True):
            st.subheader(f"Quiz ({selected}) Difficulty")
            with st.spinner("AI is Writing questions for you"):
                quiz=quiz_generator(pil_images,selected)
                st.markdown(quiz)


    

