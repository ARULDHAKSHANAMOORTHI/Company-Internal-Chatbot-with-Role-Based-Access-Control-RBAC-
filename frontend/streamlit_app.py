
# # import streamlit as st
# # import requests

# # API = "http://localhost:8000"

# # st.set_page_config(page_title="Internal Chatbot", page_icon="🤖")
# # st.title("🏢 Company Internal Chatbot")

# # if "token" not in st.session_state:
# #     st.subheader("Login")

# #     username = st.text_input("Username")
# #     password = st.text_input("Password", type="password")

# #     if st.button("Login"):
# #         res = requests.post(
# #             f"{API}/login",
# #             params={"username": username, "password": password}
# #         )

# #         if res.status_code == 200:
# #             st.session_state.token = res.json()["token"]
# #             st.session_state.chat = []
# #             st.success("Login successful")
# #             st.rerun()
# #         else:
# #             st.error("Invalid credentials")

# # else:
# #     st.subheader("Chat")

# #     for msg in st.session_state.chat:
# #         st.markdown(f"**You:** {msg['q']}")
# #         st.markdown(f"**Bot:** {msg['a']}")

# #     query = st.text_input("Type your message")

# #     if st.button("Send") and query:
# #         res = requests.post(
# #             f"{API}/chat",
# #             params={"query": query, "token": st.session_state.token}
# #         ).json()

# #         st.session_state.chat.append({
# #             "q": query,
# #             "a": res["answer"]
# #         })

# #         st.rerun()


# import streamlit as st
# import requests

# API = "http://localhost:8000"

# st.title("🏢 Infosys Internal Chatbot")

# if "token" not in st.session_state:
#     user = st.text_input("Username")
#     pwd = st.text_input("Password", type="password")

#     if st.button("Login"):
#         r = requests.post(f"{API}/login", params={
#             "username": user,
#             "password": pwd
#         })
#         st.session_state.token = r.json()["token"]
#         st.success("Logged in")

# else:
#     query = st.text_input("Ask your question")
#     if st.button("Ask"):
#         r = requests.post(
#             f"{API}/chat",
#             params={"query": query, "token": st.session_state.token}
#         ).json()

#         st.markdown("### 💬 Answer")
#         st.write(r["answer"])

#         st.markdown(f"**Confidence:** {r['confidence']}")

#         if r["sources"]:
#             st.markdown("### 📄 Sources")
#             for s in r["sources"]:
#                 st.write("-", s)


import streamlit as st
import requests
import jwt

API = "http://localhost:8000"
SECRET = "secret123"

st.set_page_config(layout="wide")

# SESSION STATE
if "token" not in st.session_state:
    st.session_state.token = None

# ---------------- LOGIN / SIGNUP PAGE ----------------
if not st.session_state.token:
    st.title("🔐 Infosys Internal Chatbot")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            r = requests.post(f"{API}/login", params={
                "username": user,
                "password": pwd
            })

            if r.status_code == 200:
                st.session_state.token = r.json()["token"]
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username")
        new_pwd = st.text_input("New Password", type="password")
        role = st.selectbox(
            "Select Role",
            ["employees", "finance", "marketing", "hr", "engineering", "c_level"]
        )

        if st.button("Signup"):
            r = requests.post(f"{API}/signup", params={
                "username": new_user,
                "password": new_pwd,
                "role": role
            })
            if r.status_code == 200:
                st.success("Account created. Please login.")
            else:
                st.error("User already exists")

# ---------------- CHAT PAGE ----------------
else:
    decoded = jwt.decode(
        st.session_state.token,
        SECRET,
        algorithms=["HS256"]
    )
    username = decoded["sub"]

    st.sidebar.title("🕘 Chat History")
    h = requests.get(f"{API}/history", params={"username": username}).json()

    for q, a in h:
        with st.sidebar.expander(q[:30]):
            st.write(a)

    st.title("💬 Infosys Internal Chatbot")

    query = st.text_input("Ask your question")
    if st.button("Send"):
        r = requests.post(
            f"{API}/chat",
            params={"query": query, "token": st.session_state.token}
        ).json()

        st.markdown("### Answer")
        st.write(r["answer"])
        st.markdown(f"**Confidence:** {r['confidence']}")

        if r["sources"]:
            st.markdown("### Sources")
            for s in r["sources"]:
                st.write("-", s)

    if st.button("Logout"):
        st.session_state.token = None
        st.experimental_rerun()
