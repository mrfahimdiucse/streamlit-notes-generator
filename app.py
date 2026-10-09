import streamlit as st 
from api_calling import note_generator,audio_transcription,quiz_generator
from PIL import Image



#title
st.title("Note Summary and Quiz Generator")
st.markdown("Upload upto 3 images to generate Note summary and Quizzes")
st.divider()


with st.sidebar:
    st.header("Controls")

    #image
    images = st.file_uploader(
        "Upload the photos of your note",
        type=['jpg','jpeg','png'],
        accept_multiple_files=True
    )

    if images:
        if len(images)>3:
            st.error("Upload at max 3 images")
        else:
            pil_images = []
            for img in images:
                try:
                    pil_images.append(Image.open(img).convert("RGB"))
                except Exception:
                    st.error(f"Could not read {img.name}. Upload a valid JPG or PNG image.")
                    pil_images = []
                    break

            st.subheader("Uploaded images")
            if pil_images:
                col = st.columns(len(images))
                for i, img in enumerate(pil_images):
                    with col[i]:
                        st.image(img)

    #difficulty 
    selected_option = st.selectbox(
        "Enter the difficulty of your quiz",
        ("Easy","Medium","Hard"),
        index = None
    )

    pressed= st.button("Click the button to initiate AI",type="primary")


if pressed:
    if not images:
        st.error("You must upload 1 image")
    elif len(images) > 3:
        st.error("Upload at most 3 images")
    if not selected_option:
        st.error("You must select a difficulty")

    if images and len(images) <= 3 and selected_option:
        if not pil_images:
            st.stop()

        #note 

        with st.container(border=True):
            st.subheader("Your note")

            #the portion below will be replaced by API Call

            with st.spinner("AI is writing notes for you"):
                try:
                    generated_notes = note_generator(pil_images)
                except Exception as error:
                    st.error(f"Could not generate your notes: {error}")
                    st.stop()
                st.markdown(generated_notes)





        #Audio transcipt
        with st.container(border=True):
            st.subheader("Audio version")



            #the portion below will be replaced by API Call 
            with st.spinner("AI is generating audio transcript for you"):

                #clearing the markdown

                generated_notes = generated_notes.replace("#","")
                generated_notes = generated_notes.replace("*","")
                generated_notes = generated_notes.replace("-","")
                generated_notes = generated_notes.replace("`","")


                try:
                    audio_data = audio_transcription(generated_notes)
                except Exception as error:
                    st.error(f"Could not generate audio: {error}")
                    st.stop()
                st.audio(audio_data, format="audio/mp3")


        #quiz

        with st.container(border=True):
            st.subheader(f"Quiz ({selected_option}) Difficulty")

            #the portion below will be replaced by API Call 

            with st.spinner("AI is generating the quizzes"):
                try:
                    quizzes = quiz_generator(pil_images,selected_option)
                except Exception as error:
                    st.error(f"Could not generate your quiz: {error}")
                    st.stop()
                st.markdown(quizzes)
