from config import *


pages = st.navigation(
    [
        st.Page(r"pages\main.py", title="Главная", default=True),
        st.Page(r"pages\upload_files.py", title="Добавление данных"),
        st.Page(r"pages\exit.py", title="Выход", icon="🔒"),
    ],
    position="top",
)

pages.run()