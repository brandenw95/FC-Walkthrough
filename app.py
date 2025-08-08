import streamlit as st
import base64
from pathlib import Path
from datetime import datetime

from string import Template


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
    frequency_display = ", ".join(
        frequency + ([frequency_other] if frequency_other else [])
    )
    service_type_display = ", ".join(service_type)
    floors_display = ", ".join(
        floors + ([floors_other] if floors_other else [])
    )

    image_tags = []
    for img in walkthrough_photos:
        b64_img = base64.b64encode(img.getvalue()).decode()
        src = f"data:{img.type};base64,{b64_img}"
        image_tags.append(
            f"<img src=\"{src}\" alt=\"Uploaded Photo\" onclick=\"openLightbox('{src}')\">"
        )

    images_html = ""
    if image_tags:
        images_html = f"""
    <div class=\"section\">
      <h2>Uploaded Photos</h2>
      <div class=\"image-gallery\">
        {'\n        '.join(image_tags)}
      </div>
    </div>
  """

    template = Template("""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <title>Walkthrough Summary</title>
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      padding: 2rem;
      background-color: #f9f9f9;
      color: #333;
    }
    h1, h2 {
      color: #5B9BA6;
    }
    .section {
      margin-bottom: 2rem;
      padding: 1rem;
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0,0,0,0.05);
    }
    label {
      font-weight: bold;
    }
    .image-gallery {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      margin-top: 1rem;
    }
    .image-gallery img {
      width: 150px;
      height: auto;
      border: 1px solid #ccc;
      border-radius: 4px;
      cursor: pointer;
      transition: transform 0.2s;
    }
    .image-gallery img:hover {
      transform: scale(1.05);
    }

    .lightbox {
      display: none;
      position: fixed;
      z-index: 9999;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.9);
      align-items: center;
      justify-content: center;
    }

    .lightbox.active {
      display: flex;
    }


    .lightbox img {
      max-width: 90vw;
      max-height: 90vh;
      border-radius: 6px;
      box-shadow: 0 0 10px black;
    }
  </style>
</head>
<body>
  <h1>Walkthrough Summary</h1>

  <div class=\"section\">
    <h2>Client & Job Info</h2>
    <p><label>Date Estimate Sent:</label> $estimate_date</p>
    <p><label>Estimate #'s & Time:</label> $estimate_numbers</p>
    <p><label>Completed By:</label> $completed_by</p>
    <p><label>Client Name:</label> $client_name</p>
    <p><label>Billed To:</label> $billed_to</p>
    <p><label>Phone:</label> $phone</p>
    <p><label>Email:</label> $email</p>
    <p><label>Location:</label> $location</p>
    <p><label>Preferred Start Date:</label> $start_date</p>
  </div>

  <div class=\"section\">
    <h2>Service Details</h2>
    <p><label>Frequency:</label> $frequency_display</p>
    <p><label>Referral Source:</label> $referral_source</p>
    <p><label>Service Types:</label> $service_type_display</p>
    <p><label>Floors:</label> $floors_display</p>
    <p><label>Cleaning Level (1-10):</label> $cleaning_level</p>
  </div>

  <div class=\"section\">
    <h2>Instructions & Notes</h2>
    <p><label>Entry/Arrival:</label> $entry_instructions</p>
    <p><label>Supplies:</label> $supply_notes</p>
    <p><label>Safety:</label> $safety_instructions</p>
    <p><label>Special Requests:</label> $special_requests</p>
    <p><label>Areas Not to Be Done:</label> $areas_excluded</p>
    <p><label>Closed Doors:</label> $closed_doors</p>
    <p><label>Photo Consent:</label> $photo_consent</p>
  </div>
  $images_html
  <div id=\"lightbox\" class=\"lightbox\" onclick=\"closeLightbox()\">
    <img id=\"lightbox-img\" src=\"\" alt=\"Full View\">
  </div>

<script>
  let lightbox = document.getElementById("lightbox");
  let lightboxImg = document.getElementById("lightbox-img");

  function openLightbox(src) {
    lightboxImg.src = src;
    lightbox.classList.add("active");
  }

  function closeLightbox() {
    lightbox.classList.remove("active");
  }

  let startX = 0;
  lightbox.addEventListener('touchstart', e => {
    startX = e.touches[0].clientX;
  });

  lightbox.addEventListener('touchend', e => {
    let endX = e.changedTouches[0].clientX;
    // Example: close lightbox on swipe left
    if (startX - endX > 50) {
      closeLightbox();
    }
  });
</script>
</body>
</html>
""")

    html_content = template.substitute(
        estimate_date=str(estimate_date),
        estimate_numbers=estimate_numbers,
        completed_by=completed_by,
        client_name=client_name,
        billed_to=billed_to,
        phone=phone,
        email=email,
        location=location,
        start_date=str(start_date),
        frequency_display=frequency_display,
        referral_source=referral_source,
        service_type_display=service_type_display,
        floors_display=floors_display,
        cleaning_level=cleaning_level,
        entry_instructions=entry_instructions,
        supply_notes=supply_notes,
        safety_instructions=safety_instructions,
        special_requests=special_requests,
        areas_excluded=areas_excluded,
        closed_doors=closed_doors,
        photo_consent=photo_consent,
        images_html=images_html,
    )


    filename = f"walkthrough_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    output_path = Path(__file__).parent / filename
    output_path.write_text(html_content, encoding="utf-8")

    st.markdown(
        f'<a href="{output_path.name}" target="_blank">Open Walkthrough</a>',
        unsafe_allow_html=True,
    )
