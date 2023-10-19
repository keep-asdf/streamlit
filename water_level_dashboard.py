
import streamlit as st

def main():
    st.title("Hello Streamlit!")

    user_input = st.text_input("Type something here:")
    st.write(f"You typed: {user_input}")

    number = st.slider("Choose a number:", 1, 100, 50)
    st.write(f"You selected {number}")

    options = ['Option 1', 'Option 2', 'Option 3']
    choice = st.selectbox("Choose an option:", options)
    st.write(f"You selected {choice}")

if __name__ == "__main__":
    main()
