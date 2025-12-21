import streamlit as st
import os
from dashboard import (
    side_bar_file_operations,
)

# Side bar for file operations
side_bar_file_operations()

st.subheader("Evolution of Portfolio Value Over Time")
