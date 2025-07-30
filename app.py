from config import *


pages = st.navigation(
    [
        st.Page(r"pages\main.py", title="Главная", default=True),
        st.Page(r"pages\upload_files.py", title="Добавление данных"),
		st.Page(r"pages\show_results.py", title="Просмотр результатов"),
		st.Page(r"pages\check_regex.py", title="Проверка выгрузки данных"),
        st.Page(r"pages\exit.py", title="Выход", icon="🔒"),
    ],
    position="top",
)

pages.run()