import streamlit as st
import json
import os

# Caminho dos arquivos JSON
AMIGOS_FILE = 'Amigos.json'
LIVROS_FILE = 'Livros.json'
EMPRESTIMOS_FILE = 'Emprestimos.json'

# Função para carregar dados dos arquivos JSON
def carregar_arquivo(caminho_arquivo, padrao=[]):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return padrao

# Função para salvar dados nos arquivos JSON
def salvar_arquivo(caminho_arquivo, dados):
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Função para buscar livros com base em uma palavra-chave
def buscar_livros(palavra_chave, livros):
    livros_filtrados = []
    for livro in livros:
        if (palavra_chave.lower() in livro['titulo'].lower() or
            palavra_chave.lower() in livro['autor'].lower() or
            palavra_chave.lower() in livro['anotacoes'].lower() or
            palavra_chave.lower() in livro['citacoes'].lower()):
            livros_filtrados.append(livro)
    return livros_filtrados

# Carregar dados iniciais
amigos = carregar_arquivo(AMIGOS_FILE)
livros = carregar_arquivo(LIVROS_FILE)
emprestimos = carregar_arquivo(EMPRESTIMOS_FILE)

# Inicializar o estado do Streamlit
if 'dados_formulario' not in st.session_state:
    st.session_state.dados_formulario = {
        'titulo': '',
        'autor': '',
        'genero': '',
        'status': '',
        'avaliacao': 0,
        'anotacoes': '',
        'citacoes': ''
    }

if 'amigo_logado' not in st.session_state:
    st.session_state.amigo_logado = None

if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = "Cadastro ou Login"

pagina = ''

# Cadastro/Login
if st.session_state.amigo_logado is None:
    st.title('Bem-vindo a Nuvem dos Livros')
    st.image("13.jpg", use_container_width=True)
        
       # Mensagem de boas-vindas
    st.write("Cadastre-se ou faça login para continuar.")
    
    # Adicionando uma chave única para evitar duplicidade
    opcao = st.radio('Escolha uma opção:', ['Entrar', 'Cadastrar'], key="opcao_cadastro")
    
    if opcao == 'Cadastrar':
        # Código para cadastrar o usuário (se necessário)
        st.write("Você escolheu a opção de cadastro.")
    elif opcao == 'Entrar':
        # Código para login do usuário (se necessário)
        st.write("Você escolheu a opção de login.")

    if opcao == 'Entrar':
        nome_amigo = st.text_input('Nome de Usuário', key="nome_usuario_login")
        senha_amigo = st.text_input('Senha', type='password', key="senha_login")

        if st.button('Entrar'):
            if nome_amigo and senha_amigo:
                amigo_encontrado = next((amigo for amigo in amigos if amigo['nome'] == nome_amigo), None)
                if amigo_encontrado:
                    if amigo_encontrado['senha'] == senha_amigo:
                        st.session_state.amigo_logado = nome_amigo
                        st.session_state.pagina_atual = "Adicionar Livro"
                        st.success(f'Bem-vindo de volta, {nome_amigo}!')
                        st.rerun()
                    else:
                        st.warning("Senha incorreta. Tente novamente.")
                else:
                    st.error('Nome de usuário não encontrado.')
            else:
                st.error("Por favor, preencha todos os campos.")

    elif opcao == 'Cadastrar':
        nome_amigo = st.text_input('Nome de Usuário', key="nome_usuario_cadastro")
        telefone_amigo = st.text_input('Número de Telefone', key="telefone_cadastro")
        senha_amigo = st.text_input('Senha', type='password', key="senha_cadastro")
        confirmacao_senha = st.text_input('Confirme a Senha', type='password', key="confirmacao_senha_cadastro")

        if st.button('Cadastrar'):
            # Verificando se todos os campos obrigatórios foram preenchidos
            if nome_amigo and telefone_amigo and senha_amigo and confirmacao_senha:
                if senha_amigo == confirmacao_senha:
                    if nome_amigo not in [amigo['nome'] for amigo in amigos]:
                        amigos.append({
                            'nome': nome_amigo,
                            'telefone': telefone_amigo,
                            'senha': senha_amigo
                        })
                        salvar_arquivo(AMIGOS_FILE, amigos)
                        st.success(f'Cadastro realizado com sucesso! Bem-vindo, {nome_amigo}!')
                        st.session_state.amigo_logado = nome_amigo
                        st.session_state.pagina_atual = "Adicionar Livro"
                        st.rerun()
                    else:
                        st.warning(f'O nome de usuário "{nome_amigo}" já está cadastrado.')
                else:
                    st.error('As senhas não coincidem!')
            else:
                # Detalhando qual campo falta preencher
                if not nome_amigo:
                    st.error("O campo 'Nome de Usuário' é obrigatório.")
                if not telefone_amigo:
                    st.error("O campo 'Número de Telefone' é obrigatório.")
                if not senha_amigo:
                    st.error("O campo 'Senha' é obrigatório.")
                if not confirmacao_senha:
                    st.error("O campo 'Confirmar Senha' é obrigatório.")

else:
    amigo_logado = st.session_state.amigo_logado


    # Navegação do app
    st.sidebar.title("Navegação")
    
    pagina = st.sidebar.radio("Escolha uma página:", [
        "Adicionar Livro", "Livros Lidos", "Livros Lendo", "Quero Ler",
        "Livros Favoritos", "Editar Livro", "Encontrar um livro", "Gráficos de Gêneros", "Emprestar Livro",
        "Amigos"
    ])


# Página 1: "Adicionar Livro"
if pagina == "Adicionar Livro":
    st.title('Cadastro de Livro')

    # Formulário de Cadastro de Livro
    with st.form(key='formulario_livro'):
        st.session_state.dados_formulario['titulo'] = st.text_input('Título do Livro', st.session_state.dados_formulario['titulo'])
        st.session_state.dados_formulario['autor'] = st.text_input('Autor', st.session_state.dados_formulario['autor'])
        st.session_state.dados_formulario['genero'] = st.text_input('Gênero', st.session_state.dados_formulario['genero'])

        # Botão de submeter o formulário para cadastrar livro
        botao_cadastrar_livro = st.form_submit_button('Cadastrar Livro')

    # Se o livro foi cadastrado, exibe a escolha do status
    if botao_cadastrar_livro:
        if not st.session_state.dados_formulario['titulo'] or not st.session_state.dados_formulario['autor'] or not st.session_state.dados_formulario['genero']:
            st.error("Todos os campos (Título, Autor, Gênero) precisam ser preenchidos!")
        else:
            st.session_state.dados_formulario['status'] = None  # Reset status
            st.success('Livro cadastrado com sucesso! Agora, defina o status do livro.')
            # Direciona o usuário para a parte de escolher o status
            st.session_state.passos_atual = 'status'

# Etapa 2: Escolher o Status (após cadastro do livro)
if 'passos_atual' in st.session_state and st.session_state.passos_atual == 'status':
    st.subheader('Escolha o Status do Livro')

    status_lido = st.button('Lido')
    status_lendo = st.button('Lendo')
    status_quero_ler = st.button('Quero Ler')

    # Definir o status de acordo com o botão clicado
    if status_lido:
        st.session_state.dados_formulario['status'] = 'Lido'
        st.session_state.passos_atual = 'avaliacao'
        st.success("Status definido como 'Lido'. Agora, adicione sua avaliação.")
    elif status_lendo:
        st.session_state.dados_formulario['status'] = 'Lendo'
        st.session_state.passos_atual = 'anotacoes'
        st.success("Status definido como 'Lendo'. Agora, adicione suas anotações e citações.")
    elif status_quero_ler:
        st.session_state.dados_formulario['status'] = 'Quero Ler'
        st.session_state.passos_atual = 'concluir'
        st.success("Status definido como 'Quero Ler'. Até Breve!")

# Etapa 3: Adicionar Avaliação (após definir o status do livro)
if 'passos_atual' in st.session_state and st.session_state.passos_atual == 'avaliacao':
    st.subheader('Adicione uma Avaliação')

    # Campos para avaliação
    avaliacao = st.slider('Avaliação (de 1 a 10)', 0, 10)
    st.session_state.dados_formulario['avaliacao'] = avaliacao

    # Botão para salvar a avaliação e passar para a próxima etapa
    botao_avaliacao = st.button('Salvar Avaliação')

    if botao_avaliacao:
        st.session_state.passos_atual = 'anotacoes'
        st.success('Avaliação salva com sucesso! Agora, adicione suas anotações.')

# Etapa 4: Adicionar Anotações e Citações
if 'passos_atual' in st.session_state and st.session_state.passos_atual == 'anotacoes':
    st.subheader('Adicione suas Anotações sobre o Livro')

    # Campo para anotações
    anotacoes = st.text_area('Anotações', st.session_state.dados_formulario['anotacoes'])
    st.session_state.dados_formulario['anotacoes'] = anotacoes

    # Campo para citações
    citacoes = st.text_area('Citações', st.session_state.dados_formulario['citacoes'])
    st.session_state.dados_formulario['citacoes'] = citacoes

    # Botão único para salvar anotações, citações e avançar
    botao_salvar = st.button('Salvar Anotações e Citações')

        # Avançar para a próxima etapa ou concluir
    st.session_state.passos_atual = 'concluir'
    st.success('Anotações e Citações salvas com sucesso! Cadastro concluído.')
   
# Etapa 5: Adicionar Concluir (após definir o status Quero Ler)
if 'passos_atual' in st.session_state and st.session_state.passos_atual == 'concluir':
    st.subheader("Concluir Cadastro")

    # Exibe o botão "Salvar com sucesso!" para a etapa "Quero Ler" e outras
    botao_concluir = st.button('Salvar com sucesso!')

    if botao_concluir:
        # Salvar o livro no arquivo
        livro = st.session_state.dados_formulario.copy()
        livros.append(livro)  # Adicionar o livro à lista de livros
        salvar_arquivo(LIVROS_FILE, livros)  # Salvar a lista atualizada no arquivo

        # Resetar o formulário para o próximo livro
        st.session_state.dados_formulario = {
            'titulo': '',
            'autor': '',
            'genero': '',
            'status': '',
            'avaliacao': 0,
            'anotacoes': '',
            'citacoes': ''
        }

        # Resetar a etapa de fluxo do formulário
        st.session_state.passos_atual = None
        st.success('Livro cadastrado com sucesso!')

        # Redirecionar para a página inicial ou recarregar a aplicação
        st.rerun()

# Página 2: Livros Lidos
if pagina == "Livros Lidos":
    st.title('Livros Lidos')
    st.image("bibli3.jpg", caption="Biblioteca Nacional de Lisboa", use_container_width=True)
    
    # Filtrando livros marcados como 'Lido'
    livros_lidos = []
    for livro in livros:
        if livro['status'] == 'Lido':
            livros_lidos.append(livro)

    # Exibindo os livros lidos
    if livros_lidos:
        for index, livro in enumerate(livros_lidos):
            key_botao = f"botao_{livro['titulo'].replace(' ', '').replace('-', '').replace('.', '')}{index}"
            if st.button(f"{livro['titulo']}", key=key_botao):
                st.write(f"*Título:* {livro['titulo']}")
                st.write(f"*Autor:* {livro['autor']}")
                st.write(f"*Avaliação:* {livro['avaliacao']}")
                st.write(f"*Anotações:* {livro['anotacoes']}")
                st.write(f"*Citações:* {livro['citacoes']}")
    else:
        st.write("Nenhum livro marcado como 'Lido'.")


# Página 3: Livros Lendo
if pagina == "Livros Lendo":
    st.title('Livros Lendo')
    st.image("bibli6.webp", caption="Real Gabinete Português de Leitura, Rio de Janeiro", use_container_width=True)
    livros_lendo = []

    # Filtrando os livros com status 'Lendo' usando um if
    for livro in livros:
        if livro['status'] == 'Lendo':
            livros_lendo.append(livro)

    if livros_lendo:
        for index, livro in enumerate(livros_lendo):
            key_botao = f"botao_{livro['titulo'].replace(' ', '').replace('-', '').replace('.', '')}{index}"
            if st.button(f"{livro['titulo']}", key=key_botao):
                st.write(f"*Título:* {livro['titulo']}")
                st.write(f"*Autor:* {livro['autor']}")
                st.write(f"*Avaliação:* {livro['avaliacao']}")
                st.write(f"*Anotações:* {livro['anotacoes']}")
                st.write(f"*Citações:* {livro['citacoes']}")
    else:
        st.write("Nenhum livro marcado como 'Lendo'.")

# Página 4: Quero Ler
if pagina == "Quero Ler":
    st.title('Quero Ler')
    st.image("bibli7.jpg", caption="Biblioteca pública de Nova Iorque, EUA", use_container_width=True)
    livros_quero_ler = []

    # Filtrando os livros com status 'Quero Ler' usando um if
    for livro in livros:
        if livro['status'] == 'Quero Ler':
            livros_quero_ler.append(livro)

    if livros_quero_ler:
        for index, livro in enumerate(livros_quero_ler):
            key_botao = f"botao_{livro['titulo'].replace(' ', '').replace('-', '').replace('.', '')}{index}"
            if st.button(f"{livro['titulo']}", key=key_botao):
                st.write(f"*Título:* {livro['titulo']}")
                st.write(f"*Autor:* {livro['autor']}")
                st.write(f"*Avaliação:* {livro['avaliacao']}")
                st.write(f"*Anotações:* {livro['anotacoes']}")
                st.write(f"*Citações:* {livro['citacoes']}")
    else:
        st.write("Nenhum livro marcado como 'Quero Ler'.")

# Página 5: Livros Favoritos
if pagina == "Livros Favoritos":
    st.title('Livros Favoritos')
    st.image("3.jpg", use_container_width=True)
    livros_favoritos = []

    # Filtrando os livros com avaliação maior ou igual a 9 usando um if
    for livro in livros:
        if livro['avaliacao'] >= 9:
            livros_favoritos.append(livro)

    if livros_favoritos:
        for index, livro in enumerate(livros_favoritos):
            key_botao = f"botao_{livro['titulo'].replace(' ', '').replace('-', '').replace('.', '')}{index}"
            if st.button(f"{livro['titulo']}", key=key_botao):
                st.write(f"*Título:* {livro['titulo']}")
                st.write(f"*Autor:* {livro['autor']}")
                st.write(f"*Avaliação:* {livro['avaliacao']}")
                st.write(f"*Anotações:* {livro['anotacoes']}")
                st.write(f"*Citações:* {livro['citacoes']}")
    else:
        st.write("Nenhum livro com avaliação superior ou igual a 9.")


# Página 6: Página de Editar Livro
if pagina == "Editar Livro":
    st.title("Editar Livro")
    st.image("8.jpg", use_container_width=True)

    # Selecionar o livro a ser editado
    livro_selecionado = st.selectbox("Selecione o livro a ser editado", [""] + [livro['titulo'] for livro in livros])

    # Encontrar o livro na lista
    livro_para_editar = None
    for livro in livros:  # Alterado de 'Livros' para 'livros'
        if livro['titulo'] == livro_selecionado:
            livro_para_editar = livro
            break

    if livro_para_editar:
        # Organizando os botões de editar e excluir lado a lado
        col1, col2 = st.columns(2)

        # Botão de editar
        with col1:
            editar_livro = st.button(f"Editar {livro_para_editar['titulo']}", key=f"editar_{livro_para_editar['titulo']}")

        # Botão de excluir
        with col2:
            excluir_livro = st.button(f"Excluir {livro_para_editar['titulo']}", key=f"excluir_{livro_para_editar['titulo']}")

        # Lógica para editar o livro
        if editar_livro:
            # Formulário para editar o livro selecionado
            with st.form(key='formulario_editar_livro'):
                livro_para_editar['titulo'] = st.text_input('Título do Livro', livro_para_editar['titulo'], key="titulo_editar")
                livro_para_editar['autor'] = st.text_input('Autor', livro_para_editar['autor'], key="autor_editar")
                livro_para_editar['genero'] = st.text_input('Gênero', livro_para_editar['genero'], key="genero_editar")
                livro_para_editar['avaliacao'] = st.slider('Avaliação (de 1 a 10)', 0, 10, livro_para_editar.get('avaliacao', 0), key="avaliacao_editar")

                botao_salvar_edicao = st.form_submit_button('Salvar Edição')

                if botao_salvar_edicao:
                    salvar_arquivo(LIVROS_FILE, livros)  # Alterado de 'Livros' para 'livros'
                    st.success(f"Livro {livro_para_editar['titulo']} editado com sucesso!")

        # Lógica para excluir o livro
        if excluir_livro:
            livros.remove(livro_para_editar)
            salvar_arquivo(LIVROS_FILE, livros)  # Alterado de 'Livros' para 'livros'
            st.success(f"Livro {livro_para_editar['titulo']} excluído com sucesso!")
            st.rerun()  # Atualiza a página para refletir a exclusão

                    
# Página 7: Encontrar um livro
if pagina == "Encontrar um livro":
    st.title('Encontrar um livro')
    st.image("24.jpg", caption="", use_container_width=True)
    palavra_chave = st.text_input("Digite uma palavra-chave para buscar")
    if palavra_chave:
        livros_encontrados = buscar_livros(palavra_chave, livros)
        if livros_encontrados:
            for livro in livros_encontrados:
                st.write(f"*Título:* {livro['titulo']}")
                st.write(f"*Autor:* {livro['autor']}")
                st.write(f"*Anotações:* {livro['anotacoes']}")
                st.write(f"*Citações:* {livro['citacoes']}")
        else:
            st.write("Nenhum livro encontrado.")

# Página 8: Gráficos de Gêneros
if pagina == "Gráficos de Gêneros":
    st.title('Gráficos de Gêneros')
    st.image("bibli8.jpg", use_container_width=True)    

    # Contagem de gêneros
    generos = [livro['genero'] for livro in livros]
    genero_contagem = {}
    for genero in generos:
        if genero in genero_contagem:
            genero_contagem[genero] += 1
        else:
            genero_contagem[genero] = 1

    if genero_contagem:
        st.bar_chart(genero_contagem)
    else:
        st.write("Nenhum livro cadastrado.")

# Página 9: Emprestar Livro
if pagina == "Emprestar Livro":
    st.title('Emprestar Livro')
    st.image("4.jpg", use_container_width=True)

    # Verifica se há amigos cadastrados
    if not amigos:
        st.warning("Nenhum amigo cadastrado. Por favor, cadastre amigos antes de emprestar um livro.")
    else:
        # Cria uma lista com a opção em branco como primeira linha
        nomes_amigos = [""] + [amigo['nome'] for amigo in amigos]

        # Escolha do livro para emprestar
        livro_emprestado = st.selectbox("Escolha o livro para emprestar", [""] + [livro['titulo'] for livro in livros])

        # Escolha do amigo para emprestar
        nome_emprestado_para = st.selectbox('Emprestei para quem?', nomes_amigos, key="emprestado_para")
        nome_emprestado_de = st.selectbox('Peguei emprestado de quem?', nomes_amigos, key="emprestado_de")

        # Identifica os amigos selecionados, ou deixa como None se nenhum for selecionado
        amigo_para = next((amigo for amigo in amigos if amigo['nome'] == nome_emprestado_para), None)
        amigo_de = next((amigo for amigo in amigos if amigo['nome'] == nome_emprestado_de), None)

        # Registrar empréstimo
        if st.button('Registrar Empréstimo'):
            if livro_emprestado:
                emprestimos.append({
                    'livro': livro_emprestado,
                    'emprestado_para': amigo_para['nome'] if amigo_para else "",  # Deixa vazio se nenhum amigo for selecionado
                    'emprestado_de': amigo_de['nome'] if amigo_de else "",        # Deixa vazio se nenhum amigo for selecionado
                    'devolvido': False                                            # Adiciona o status para controle
                })
                salvar_arquivo(EMPRESTIMOS_FILE, emprestimos)
                st.success(f'Empréstimo do livro "{livro_emprestado}" registrado com sucesso!')
            else:
                st.error("Por favor, selecione um livro para emprestar.")

    # Exibir livros emprestados
    st.subheader("Livros Emprestados")
    livros_emprestados = [emprestimo for emprestimo in emprestimos if not emprestimo.get('devolvido', False)]

    if livros_emprestados:
        for idx, emprestimo in enumerate(livros_emprestados):
            st.write(f"**Livro:** {emprestimo['livro']}")
            st.write(f"**Emprestei para:** {emprestimo['emprestado_para'] or 'N/A'}")  # Exibe N/A se estiver vazio
            st.write(f"**Peguei emprestado de:** {emprestimo['emprestado_de'] or 'N/A'}")  # Exibe N/A se estiver vazio

            # Botão para marcar como devolvido
            if st.button('Marcar como devolvido', key=f"devolvido_{idx}"):
                emprestimos[idx]['devolvido'] = True
                salvar_arquivo(EMPRESTIMOS_FILE, emprestimos)
                st.success(f'O livro "{emprestimo["livro"]}" foi marcado como devolvido.')
            st.write("-----------")
    else:
        st.write("Nenhum livro emprestado no momento.")

# Página 10: Amigos
if pagina == "Amigos":
    st.title('Amigos')
    st.image("9.jpg", use_container_width=True)
    st.write("Lista de amigos com quem você pode compartilhar livros.")

    for amigo in amigos:
        if amigo['nome'] == amigo_logado:
            st.write(f"*Nome:* {amigo['nome']}")
            st.write(f"*Telefone:* {amigo['telefone']}")
            st.write("-----------")