import streamlit as st


pages={
    "applications":[
        st.Page('main.py',title='Main Page',icon='🏠'),
        st.Page('page_1.py',title='Backtest Web',icon='📈'),
        st.Page('page_2.py',title='Page 2',icon='📄'),
    ],
    "redo":[
        st.Page('paper.py')
    ]
}





pg=st.navigation(pages,position='sidebar')
st.set_page_config(page_title='Backtest Web',layout='wide')

pg.run()