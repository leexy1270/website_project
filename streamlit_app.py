import streamlit as st


pages={
    "applications":[
        st.Page('main.py',title='Main Page',icon='🏠'),
        st.Page('page_1.py',title='Stock price',icon='📈'),
        st.Page('page_2.py',title='factor backtest',icon='📄'),
    ],
    "redo":[
        st.Page('paper.py')
    ]
}





pg=st.navigation(pages,position='sidebar')
st.set_page_config(page_title='Backtest Web',layout='wide')

pg.run()