import streamlit as st
from jinja2 import Environment, FileSystemLoader
import pdfkit import HTML
from PIL import Image
import base64
from io import BytesIO
import os

# === Hilfsfunktion: Bild zu base64 konvertieren ===
def convert_image_to_base64(uploaded_file):
    if uploaded_file is None:
        return ""
    image = Image.open(uploaded_file)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_image

# === Initialisiere SessionState für dynamische Listen ===
for key in ["ausbildung", "erfahrung"]:
    if key not in st.session_state:
        st.session_state[key] = []

st.set_page_config(page_title="Lebenslauf Generator", layout="centered")
st.title("📄 Lebenslauf Generator")

# === Persönliche Daten ===
st.header("👤 Persönliche Informationen")
with st.form("persoenliche_daten"):
    vorname = st.text_input("Vorname")
    nachname = st.text_input("Nachname")
    geburt = st.text_input("Geburtsdatum und -ort", placeholder="z.B. 15.03.1995 in Köln")
    adresse = st.text_input("Adresse")
    telefon = st.text_input("Telefonnummer")
    email = st.text_input("E-Mail")
    ort_datum = st.text_input("Ort & aktuelles Datum", placeholder="z.B. Berlin, den 27.06.2025")
    bild = st.file_uploader("📷 Foto hochladen", type=["jpg", "jpeg", "png"])
    sprachen = st.text_input("Sprachen", placeholder="Deutsch, Englisch, ...")
    it_kenntnisse = st.text_input("IT-Kenntnisse", placeholder="MS Office, Python, ...")
    interessen = st.text_input("Interessen / Hobbys", placeholder="Reisen, Musik, ...")
    submitted = st.form_submit_button("✅ Speichern")

# === Ausbildung hinzufügen ===
st.header("🎓 Ausbildung")
with st.form("ausbildung_form"):
    a_zeitraum = st.text_input("Zeitraum", key="zeitraum_a")
    a_institution = st.text_input("Institution", key="institution_a")
    a_beschreibung = st.text_area("Beschreibung", key="beschreibung_a")
    if st.form_submit_button("➕ Ausbildung hinzufügen"):
        st.session_state.ausbildung.append({
            "zeitraum": a_zeitraum,
            "institution": a_institution,
            "beschreibung": a_beschreibung
        })

# === Berufserfahrung hinzufügen ===
st.header("💼 Berufserfahrung")
with st.form("erfahrung_form"):
    e_zeitraum = st.text_input("Zeitraum", key="zeitraum_e")
    e_firma = st.text_input("Firma", key="firma_e")
    e_position = st.text_input("Position", key="position_e")
    e_aufgaben = st.text_area("Aufgaben / Tätigkeiten", key="aufgaben_e")
    if st.form_submit_button("➕ Erfahrung hinzufügen"):
        st.session_state.erfahrung.append({
            "zeitraum": e_zeitraum,
            "firma": e_firma,
            "position": e_position,
            "aufgaben": e_aufgaben
        })

# === PDF Generierung ===
st.header("📄 PDF-Erstellung")
if st.button("📥 Lebenslauf als PDF generieren"):
    full_name = f"{vorname} {nachname}"
    image_base64 = convert_image_to_base64(bild)

    daten = {
        "name": full_name,
        "birth_date": geburt,
        "address": adresse,
        "phone": telefon,
        "email": email,
        "date_location": ort_datum,
        "signature_name": full_name,
        "ausbildung": st.session_state.ausbildung,
        "erfahrung": st.session_state.erfahrung,
        "skills": {
            "sprachen": sprachen,
            "it": it_kenntnisse,
            "interessen": interessen
        },
        "image_base64": image_base64
    }

    # Lade HTML Template & rendere es
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("cv_template.html")
    html_content = template.render(**daten)

    # Generiere PDF
    pdf_file_path = "lebenslauf_output.pdf"
    pdfkit.from_string(html_content, "lebenslauf_output.pdf")


    # Download anzeigen
    with open(pdf_file_path, "rb") as f:
        st.download_button("⬇️ Lebenslauf herunterladen", f, file_name="lebenslauf.pdf", mime="application/pdf")
