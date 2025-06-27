import streamlit as st
from jinja2 import Environment, FileSystemLoader
from PIL import Image
from io import BytesIO
import base64

# === Hilfsfunktion: Bild zu base64 konvertieren ===
def convert_image_to_base64(uploaded_file):
    if uploaded_file is None:
        return ""
    image = Image.open(uploaded_file)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

# === Initialisiere dynamische Felder ===
for key in ["ausbildung", "erfahrung"]:
    if key not in st.session_state:
        st.session_state[key] = []

st.set_page_config(page_title="Lebenslauf Generator", layout="centered")
st.title("📄 Lebenslauf Generator (Cloud-Version)")

# === Persönliche Informationen ===
st.header("👤 Persönliche Informationen")
with st.form("form_info"):
    vorname = st.text_input("Vorname")
    nachname = st.text_input("Nachname")
    geburt = st.text_input("Geburtsdatum und -ort")
    adresse = st.text_input("Adresse")
    telefon = st.text_input("Telefon")
    email = st.text_input("E-Mail")
    ort_datum = st.text_input("Ort & aktuelles Datum")
    bild = st.file_uploader("Foto (PNG/JPG)", type=["png", "jpg", "jpeg"])
    sprachen = st.text_input("Sprachen")
    it = st.text_input("IT-Kenntnisse")
    interessen = st.text_input("Interessen / Hobbys")
    submitted = st.form_submit_button("✅ Speichern")

# === Ausbildung ===
st.header("🎓 Ausbildung")
with st.form("ausbildung_form"):
    z = st.text_input("Zeitraum", key="az")
    ort = st.text_input("Institution", key="ai")
    besch = st.text_area("Beschreibung", key="ab")
    if st.form_submit_button("➕ Hinzufügen"):
        st.session_state.ausbildung.append({"zeitraum": z, "institution": ort, "beschreibung": besch})

# === Berufserfahrung ===
st.header("💼 Berufserfahrung")
with st.form("erfahrung_form"):
    z = st.text_input("Zeitraum", key="ez")
    firma = st.text_input("Firma", key="ef")
    position = st.text_input("Position", key="ep")
    aufg = st.text_area("Aufgaben", key="ea")
    if st.form_submit_button("➕ Hinzufügen"):
        st.session_state.erfahrung.append({"zeitraum": z, "firma": firma, "position": position, "aufgaben": aufg})

# === HTML-Vorschau & Download ===
st.header("📄 Vorschau & Download")
if st.button("📤 HTML generieren & anzeigen"):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("cv_template.html")

    html = template.render(
        name=f"{vorname} {nachname}",
        birth_date=geburt,
        address=adresse,
        phone=telefon,
        email=email,
        date_location=ort_datum,
        signature_name=f"{vorname} {nachname}",
        ausbildung=st.session_state.ausbildung,
        erfahrung=st.session_state.erfahrung,
        skills={
            "sprachen": sprachen,
            "it": it,
            "interessen": interessen
        },
        image_base64=convert_image_to_base64(bild)
    )

    # Vorschau anzeigen
    st.markdown("### 📄 Lebenslauf-Vorschau")
    st.components.v1.html(html, height=1000, scrolling=True)

    # Download als HTML
    html_bytes = html.encode("utf-8")
    st.download_button("⬇️ HTML-Datei herunterladen", html_bytes, file_name="lebenslauf.html", mime="text/html")
