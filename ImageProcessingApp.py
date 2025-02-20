import streamlit as st
import numpy as np
import cv2 
from rembg import remove
import os
def main():
    st.title("Image Processing App")
    st.write("This is a simple image processing app that removes the background of an image.")
    st.sidebar.subheader("Options")
    transformation=st.sidebar.selectbox("Choose a transformation",["Remove Background","Add Background","zoom","zoom smaller","rotate","flip","crop","resize","change brightness"])
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg","png","jpeg"])
    if uploaded_file is not None:
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        transformed_image=apply_transformation(image, transformation)
        st.image(transformed_image, caption="Processed Image", use_column_width=True)
        save_path="result.png"
        save_image(transformation,transformed_image,save_path)
        
        with open(save_path, "rb") as file:
            btn=st.download_button(label="Download Image", data=file, file_name="result.png", mime="image/png")
def apply_transformation(image, transformation):
        if transformation=="Remove Background":
            st.write("Removing Background...")
            st.write("This may take a while...")
            output = remove(image)
            st.image(output, caption="Processed Image", use_column_width=True)
        elif transformation=="zoom":
            st.write("zooming...")
            fxy=st.slider("zoom factor", 1.0, 1.5, 2.0,3.0)
            output=cv2.resize(image, None, fx=fxy, fy=fxy,interpolation=cv2.INTER_LINEAR)
        elif transformation=="zoom smaller":
            st.write("zooming...")
            fxy=st.slider("zoom factor", 0.25, 0.5, 0.75,0.2)
            output=cv2.resize(image, None, fx=fxy, fy=fxy,interpolation=cv2.INTER_LINEAR)
        elif transformation=="rotate":
            st.write("rotating...")
            output=cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif transformation=="flip":    
            st.write("flipping...")
            output=cv2.flip(image, 1)
        elif transformation=="change brightness":
            st.write("changing brightness...")
            output=cv2.convertScaleAbs(image, alpha=1.5, beta=0)
        else:
            st.write("No transformation selected")
            output=image
        return output
def save_image(transformation,image,save_path):
    if transformation=="Remove Background":
        cv2.imwrite(save_path, cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA))
    else:
        cv2.imwrite(save_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    st.write("Image saved at", save_path)
if __name__ == "__main__":
    main()