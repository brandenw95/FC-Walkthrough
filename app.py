import streamlit as st
import base64

st.set_page_config(page_title="Cleaning Walkthrough", layout="centered")

walkthrough_type = st.sidebar.radio(

    "Walkthrough Type",
    ["Residential", "Commercial", "Move In/Out", "Custom"],
)

st.title(f"{walkthrough_type} Cleaning Walkthrough")
estimate_date = st.date_input("Date Estimate Sent")
estimate_numbers = st.text_input("Estimate #'s & Time")
completed_by = st.text_input("Completed By")
client_name = st.text_input("Client Name(s)")
billed_to = st.text_input("Billed to")
phone = st.text_input("Phone")
email = st.text_input("Email")
location = st.text_input("Location")
start_date = st.date_input("Preferred Start Date")

frequency_options = ["One-time", "Weekly", "Biweekly", "Every 4 Weeks"]
frequency = st.multiselect("Frequency", frequency_options)
frequency_other = st.text_input("Other Frequency")

referral_source = st.text_input("Referral Source")

service_options = [
    "Little Bit Clean",
    "Classic",
    "Diamond",
    "Heavy Focus",
    "Custom",
    "Move In/Out",
    "Commercial",
    "Pet Add-on",
    "Family Add-on",
]
service_type = st.multiselect("Service Type Requested", service_options)

floors_options = ["Windows", "Carpets"]
floors = st.multiselect("Floors", floors_options)
floors_other = st.text_input("Other Floors")

cleaning_level = st.slider("Level of Cleaning (1–10)", 1, 10, 5)
entry_instructions = st.text_area("Entry/Arrival Instructions")
supply_notes = st.text_area("Supply or Equipment Notes")
safety_instructions = st.text_area(
    "Safety Instructions", placeholder="Cats: Inside/Outside. Dogs: Inside/Outside. Names, other..."
)
special_requests = st.text_area("Special Requests/Instructions")
areas_excluded = st.text_area("Areas Not to Be Done")

closed_doors = st.radio(
    "Closed Doors?", ["Yes", "No", "Only if on task list"], horizontal=True
)
photo_consent = st.radio("Photo Consent?", ["Yes", "No"], horizontal=True)

walkthrough_photos = st.file_uploader(
    "Take Photos or Upload Images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True,
)

submitted = st.button("Submit Walkthrough")


if submitted:
    data = {
        "Walkthrough Type": walkthrough_type,
        "Date Estimate Sent": str(estimate_date),
        "Estimate #'s & Time": estimate_numbers,
        "Completed By": completed_by,
        "Client Name(s)": client_name,
        "Billed to": billed_to,
        "Phone": phone,
        "Email": email,
        "Location": location,
        "Preferred Start Date": str(start_date),
        "Frequency": ", ".join(frequency + ([frequency_other] if frequency_other else [])),
        "Referral Source": referral_source,
        "Service Type Requested": ", ".join(service_type),
        "Floors": ", ".join(floors + ([floors_other] if floors_other else [])),
        "Level of Cleaning": str(cleaning_level),
        "Entry/Arrival Instructions": entry_instructions,
        "Supply or Equipment Notes": supply_notes,
        "Safety Instructions": safety_instructions,
        "Special Requests/Instructions": special_requests,
        "Areas Not to Be Done": areas_excluded,
        "Closed Doors?": closed_doors,
        "Photo Consent?": photo_consent,
    }


    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"{walkthrough_type} Cleaning Walkthrough", ln=True, align="C")
    pdf.ln(4)
    pdf.set_font("Arial", size=12)
    for key, value in data.items():
        pdf.multi_cell(0, 8, f"{key}: {value}")
        pdf.ln(1)

    for img in walkthrough_photos or []:
        image = Image.open(img)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        image.save(tmp.name)
        pdf.add_page()
        pdf.image(tmp.name, w=180)
        tmp.close()

    pdf_bytes = pdf.output(dest="S").encode("latin1")
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" target="_blank">Open PDF</a>'

