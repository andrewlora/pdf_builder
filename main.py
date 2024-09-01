import streamlit as st
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        if hasattr(self, 'document_title'):
            self.set_font(family='Arial', style="B", size=12)
            self.cell(w=0, h=10, txt=self.document_title,border=0, ln=1, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font(family='Arial', style="I", size=8)
        self.cell(w=0, h=10, txt=f'Page {self.page_no()}', border=0, ln=0, align='C')

    def chapter_title(self, title, font='Arial', size=12):
        self.set_font(family=font, style="B", size=size)
        self.cell(w=0, h=10, txt=title, border=0, ln=1, align='L')
        self.ln(10)

    def chapter_body(self, body, font='Arial', size=12):
        self.set_font(family=font, style="", size=size)
        self.multi_cell(w=0, h=10,txt=body)
        self.ln()

def create_pdf(filename, document_title, author, chapters, image_path=None):
    pdf = PDF()
    pdf.document_title = document_title
    pdf.add_page()
    if author:
        pdf.set_author(author)

    if image_path:
        pdf.image(image_path, x=0, y=25, w=pdf.w -20)
        pdf.ln(120)

    for chapter in chapters:
        title, body, font, size = chapter
        pdf.chapter_title(title, font, size)
        pdf.chapter_body(body, font, size)

    pdf.output(filename)

def main():
    st.title("PDF Generator with Python")
    st.header("Document Configuration")
    document_title = st.text_input("Document Title", "Write here ....")
    author = st.text_input("Author", "")
    uploaded_image = st.file_uploader("Upload an Image Document(optional)", type=["jpg", "png"])
    st.header("Document Chapters")
    chapters = []
    chapter_count = st.number_input("Chapters number", min_value=1, max_value=10, value=1)

    for i in range(chapter_count):
        st.subheader(f"Chapter {i+1}")
        title = st.text_input(f"Chapter title {i + 1}", f"Chapter title {i + 1}")
        body = st.text_area(f"Chapter body {i + 1}", f"Chapter body {i + 1}")
        font = st.selectbox(f"Chapter Font {i + 1}", ['Arial', 'Courier', 'Times'])
        size = st.slider(f"Chapter Font Size {i + 1}", 8, 24, 12)
        chapters.append((title, body, font, size))

    if st.button("Generate PDF"):
        image_path = uploaded_image.name if uploaded_image else None
        if image_path:
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

        create_pdf(filename='history.pdf', document_title=document_title, author=author, chapters=chapters, image_path=image_path)
        with open("history.pdf", "rb") as pdf_file:
            pdf_byte = pdf_file.read()
        st.download_button(
            label="Download PDF",
            data=pdf_byte,
            file_name="history.pdf",
            mime='application/octet-stream'
        )
        st.success("PDF was generated successfully")


if __name__ == "__main__":
    main()
