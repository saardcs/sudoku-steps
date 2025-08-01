import streamlit as st

# Steps with digit and coordinates to check
steps = [
    (1, [(3, 5), (4, 4)]),
    (2, [(2, 1)]),
    (3, [(0, 5), (4, 3)]),
    (4, [(0, 4)]),
    (5, [(4, 5), (1, 4), (2, 3), (0, 2), (3, 1)]),
    (6, [(1, 2), (0, 3), (4, 1)]),
    # 2nd iteration
    (2, [(0, 0), (1, 5), (5, 4), (4, 2)]),
    (4, [(2, 5), (5, 3), (4, 0), (3, 2)]),
    (6, [(2, 4), (5, 5)])
]

if "step_index" not in st.session_state:
    st.session_state.step_index = 0

def sanitize_board(raw_board):
    sanitized = []
    for row in raw_board:
        new_row = []
        for val in row:
            try:
                new_row.append(int(val))
            except (ValueError, TypeError):
                new_row.append(0)
        sanitized.append(new_row)
    return sanitized

# Assume `board` is coming from your existing sudoku component
# For example:
board = st.session_state.get("board")  # your sudoku component must store this in session_state

if board is None:
    st.write("Waiting for your Sudoku input...")
    st.stop()

user_board = sanitize_board(board)

digit, coords = steps[st.session_state.step_index]

# Check if all required cells have the digit
correct = True
for (i, j) in coords:
    if user_board[i][j] != digit:
        correct = False
        break

# Check that no extra cells have the digit (only those coords)
if correct:
    for i in range(6):
        for j in range(6):
            if user_board[i][j] == digit and (i, j) not in coords:
                correct = False
                break
        if not correct:
            break

if correct:
    st.success(f"Step {st.session_state.step_index+1}: Correct! You filled all {digit}s correctly.")
    st.session_state.step_index += 1
    if st.session_state.step_index >= len(steps):
        st.balloons()
        st.success("🎉 All steps completed! Well done!")
else:
    st.error(f"Step {st.session_state.step_index+1}: Incorrect. Please fill all {digit}s exactly as required.")

# Add a button to reset if needed
if st.button("Restart Steps"):
    st.session_state.step_index = 0
