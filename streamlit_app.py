import streamlit as st
import qrcode
import io
import streamlit.components.v1 as components

st.set_page_config(page_title="Sudoku Prep", layout="centered")
st.title("Sudoku Prep")

# Sidebar with QR code
st.sidebar.header("Scan This QR Code to View Menu Online")
qr_link = "https://sudoku-steps.streamlit.app"  # Replace with your actual URL
qr = qrcode.make(qr_link)
buf = io.BytesIO()
qr.save(buf)
buf.seek(0)
st.sidebar.image(buf, width=300, caption=qr_link)

# Step plan as per your instructions
step_plan = [
    {"digit": 1, "cells": [(3, 5), (4, 4)]},
    {"digit": 2, "cells": [(2, 1)]},
    {"digit": 3, "cells": [(0, 5), (4, 3)]},
    {"digit": 4, "cells": [(0, 4)]},
    {"digit": 5, "cells": [(4, 5), (1, 4), (2, 3), (0, 2), (3, 1)]},
    {"digit": 6, "cells": [(1, 2), (0, 3), (4, 1)]},

    # Second iteration:
    {"digit": 2, "cells": [(0, 0), (1, 5), (5, 4), (4, 2)]},
    {"digit": 4, "cells": [(2, 5), (5, 3), (4, 0), (3, 2)]},
    {"digit": 6, "cells": [(2, 4), (5, 5)]},
]

# Session state for tracking steps
if "step_index" not in st.session_state:
    st.session_state.step_index = 0

# Declare your sudoku component (assuming you have it locally as before)
sudoku = components.declare_component("sudoku", path="sudoku_component")  # Adjust if needed

# Show progress or completion
if st.session_state.step_index >= len(step_plan):
    st.balloons()
    st.success("🎉 Congratulations, you completed the Sudoku step-by-step!")

    nickname = st.text_input("Enter your nickname:")
    roll_number = st.text_input("Enter your roll number:")

    if st.button("Submit Score"):
        if nickname.strip() and roll_number.strip():
            import gspread
            from google.oauth2.service_account import Credentials
            import datetime

            scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            service_account_info = st.secrets["gcp_service_account"]
            creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
            client = gspread.authorize(creds)

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                sheet = client.open("Review").worksheet("Sudoku")
            except gspread.WorksheetNotFound:
                st.error("Worksheet not found. Please check your Google Sheet.")
            else:
                row = [roll_number.strip(), nickname.strip(), timestamp]
                sheet.append_row(row)
                st.success("✅ Score submitted!")
        else:
            st.warning("Please enter your nickname and roll number.")
    st.stop()

# Current step info
step = step_plan[st.session_state.step_index]
digit = step["digit"]
coords = step["cells"]

st.write(f"### Step {st.session_state.step_index + 1} - Fill all `{digit}`s in the puzzle")

# Render Sudoku board (6x6) component
board = sudoku()

if board is None:
    st.warning("Waiting for board input...")
    st.stop()

if st.button("Check Solution"):
    correct = True
    for (i, j) in coords:
        try:
            cell_val = int(board[i][j])
        except (ValueError, TypeError):
            cell_val = 0

        if cell_val != digit:
            correct = False
            break

    for i in range(6):
        for j in range(6):
            try:
                cell_val = int(board[i][j])
            except (ValueError, TypeError):
                cell_val = 0

            if cell_val == digit and (i, j) not in coords:
                correct = False
                break

    if correct:
        st.success("✅ Correct for this step! Moving to next step.")
        st.session_state.step_index += 1
        st.experimental_rerun()
    else:
        st.error("❌ Incorrect — please fill only the correct cells with the digit now.")
