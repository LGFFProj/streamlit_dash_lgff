import streamlit as st

#Configurar Pagina
st.set_page_config(
    page_title="Atividade Avaliativa - N2", 
    page_icon=":rocket:", 
    layout="wide",
    initial_sidebar_state="auto", 
    menu_items=None
)



st.title(":money_with_wings: Tutorial de Como Perder Dinheiro :money_with_wings:")
st.subheader("Usando a Ferramenta")
st.write("Como a API da CoinBase limita a quantidade de Registros, essa aplicação só irá mostrar do Dia da Pesquisa Pra trás.")
st.write("1 - Preencher o Tipo de Ativo disponível na CoinBase, essa Lista é sempre atualizada na CoinBase, sugesta a aparecer novos itens")
st.image("Usando1.png")
st.write("2 - Escolher o Tempo das Velas, fica mais bonitos usar tempos acima de 5 Min.")
st.image("Usando2.png")
st.write("Depois só confirmar a selação e visualizar o Grafico, favor não usar essa informações pra gastar dinheiro. ")