import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Sudoku Step Solver", layout="centered")
st.title("🧩 Sudoku Step Solver")

initial_puzzle = [
    [0, 1, 0, 6, 0, 0],
    [3, 4, 0, 1, 0, 0],
    [1, 0, 3, 0, 0, 0],
    [0, 0, 0, 2, 3, 0],
    [0, 0, 0, 0, 0, 0],
    [5, 3, 1, 0, 0, 0]
]

solution = [
    [2, 1, 5, 6, 4, 3],
    [3, 4, 6, 1, 5, 2],
    [1, 2, 3, 5, 6, 4],
    [6, 5, 4, 2, 3, 1],
    [4, 6, 2, 3, 1, 5],
    [5, 3, 1, 4, 2, 6]
]

step_plan = [
    {"digit": 1, "cells": [(3, 5), (4, 4)]},
    {"digit": 2, "cells": [(2, 1)]},
    {"digit": 3, "cells": [(0, 5), (4, 3)]},
    {"digit": 4, "cells": [(0, 4)]},
    {"digit": 5, "cells": [(4, 5), (1, 4), (2, 3), (0, 2), (3, 1)]},
    {"digit": 6, "cells": [(1, 2), (0, 3), (4, 1)]},
    {"digit": 2, "cells": [(0, 0), (1, 5), (5, 4), (4, 2)]},
    {"digit": 4, "cells": [(2, 5), (5, 3), (4, 0), (3, 2)]},
    {"digit": 6, "cells": [(2, 4), (5, 5)]}
]

if "step_index" not in st.session_state:
    st.session_state.step_index = 0

if st.session_state.step_index >= len(step_plan):
    st.success("🎉 Puzzle completed!")
    st.balloons()
    st.stop()

step = step_plan[st.session_state.step_index]
digit = step["digit"]
target_cells = step["cells"]

st.markdown(f"### Step {st.session_state.step_index + 1}: Fill all `{digit}`s in specific cells")

# Sudoku component
sudoku = components.declare_component("sudoku_step_solver", path="sudoku_component")
user_board = sudoku(initialPuzzle=initial_puzzle, allowedDigit=digit)

# Check button
if st.button("✅ Check"):
    correct = True
    for i, j in target_cells:
        if user_board[i][j] != digit:
            correct = False
            break

    # No extras
    for i in range(6):
        for j in range(6):
            if (i, j) not in target_cells and user_board[i][j] == digit and initial_puzzle[i][j] == 0:
                correct = False
                break

    if correct:
        st.success("✅ Correct!")
        st.session_state.step_index += 1
        st.rerun()
    else:
        st.error("❌ Incorrect. Make sure you filled the right cells with the correct number.")
