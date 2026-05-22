# Projeto Tech (RadarTech)

Aplicação desenvolvida para apresentação na **Expo Tech 2026 (Unifecaf)**, com foco em interface moderna, navegação por telas e simulação de fluxo de autenticação e gestão de interesse de usuários.

O projeto integra conteúdos de:
- Banco de Dados
- Programação Python
- Métodos Ágeis (Scrum e Kanban)

---

## Tecnologias Utilizadas

- **Linguagem:** Python
- **Framework de Interface:** Flet
- **Banco de dados (planejado):** MySQL Workbench
- **Métodos ágeis:** Scrum e Kanban

---

## Estrutura do Projeto

```text
projeto_tech/
├── README.md
└── radartech/
    ├── main.py
    ├── loginTech.py
    ├── cadastroTech.py
    ├── tendencia.py
    ├── perfil.py
    ├── estrategia.py
    ├── interesseTech.py
    ├── areaexclusiva.py
    ├── usuario.py
    ├── components/
    │   └── radar.py
    └── screens/
        ├── login.py
        ├── cadastro.py
        ├── tendencia.py
        ├── perfil.py
        ├── estrategia.py
        ├── interesse.py
        ├── area_exclusiva.py
        └── usuario.py
```

---

## Funcionalidades Principais

1. Tela inicial com loading animado
2. Tela de login
3. Tela de cadastro com validações e barra de progresso
4. Fluxo de recuperação de senha (simulado)
5. Tela de tendências com navegação para módulos do sistema
6. Componente visual de radar reutilizável em várias telas

---

## Como Executar

1. Instale as dependências principais:

```bash
pip install flet
```

2. Execute a aplicação:

```bash
python radartech/main.py
```

> A aplicação abre em modo navegador por causa da configuração em [`ft.app(target=main, view=ft.AppView.WEB_BROWSER)`](radartech/main.py:119).

---

## Explicação Detalhada dos Códigos

### 1) Arquivo de entrada: [`main.py`](radartech/main.py)

#### Função principal
- A função [`main(page: ft.Page)`](radartech/main.py:9) configura a janela (título, dimensões, alinhamento e cor de fundo).
- Em seguida, reutiliza o radar criado por [`criar_radar()`](radartech/components/radar.py:5).

#### Tela de loading
- Cria os componentes visuais:
  - Título da aplicação
  - Barra de progresso
  - Texto de percentual
- Esses itens são organizados em coluna no [`layout_loading = ft.Column(...)`](radartech/main.py:57).

#### Animação assíncrona
- A coroutine [`animar_loading()`](radartech/main.py:83) faz:
  1. Atualização gradual do valor da barra (`0` até `1`)
  2. Atualização do texto de porcentagem
  3. Rotação contínua do ponteiro do radar com [`ft.Rotate(...)`](radartech/main.py:102)
  4. Chamada de [`page.update()`](radartech/main.py:105) para redesenhar a UI
- Quando chega em 100%, chama [`show_login_screen(page)`](radartech/main.py:112).

#### Execução da aplicação
- A linha [`ft.app(...)`](radartech/main.py:119) é o bootstrap do app.

---

### 2) Tela de login: [`loginTech.py`](radartech/loginTech.py)

#### Estrutura da tela
- A função [`show_login_screen(page)`](radartech/loginTech.py:6) limpa a tela e monta a interface de login.
- Campos principais:
  - Usuário/email ([`ft.TextField(...)`](radartech/loginTech.py:18))
  - Senha ([`ft.TextField(password=True, ...)`](radartech/loginTech.py:26))

#### Validação de acesso
- Na função [`entrar(...)`](radartech/loginTech.py:39):
  - Lê usuário/senha simulados em [`USUARIO_TESTE_CADASTRO`](radartech/cadastroTech.py:7)
  - Compara com os valores digitados
  - Em sucesso: abre [`show_tendencia_screen(page, "RADARTECH")`](radartech/loginTech.py:48)
  - Em erro: exibe mensagens específicas

#### Navegação
- Botão “Criar conta” chama [`show_cadastro_screen(page)`](radartech/loginTech.py:63).

#### Recuperação de senha (simulada)
- Função [`abrir_recuperacao_senha(...)`](radartech/loginTech.py:82) abre um [`ft.AlertDialog(...)`](radartech/loginTech.py:99).
- Usuário informa telefone e escolhe canal (SMS/WhatsApp).
- Não há backend real aqui ainda; é feedback visual do fluxo.

#### Animação contínua
- [`animar_ponteiro_login()`](radartech/loginTech.py:186) mantém a rotação do ponteiro do radar em background.

---

### 3) Cadastro: [`cadastroTech.py`](radartech/cadastroTech.py)

Agora o projeto separa responsabilidades:
1. Componente visual do radar em [`criar_radar()`](radartech/components/radar.py:5)
2. Fluxo da tela de cadastro em [`show_cadastro_screen(page)`](radartech/cadastroTech.py:40)

#### Persistência temporária (simulada)
- [`USUARIO_TESTE_CADASTRO`](radartech/cadastroTech.py:7) é um dicionário global para guardar usuário/senha em memória.
- Serve apenas para demonstração, sem banco real.

#### Componente reutilizável do radar
- A função [`criar_radar()`](radartech/components/radar.py:5) monta um [`ft.Stack`](radartech/components/radar.py:53) com:
  - Círculos/bordas
  - Linhas angulares (geradas por list comprehension)
  - Ponteiro central rotativo
- Retorna **dois elementos**: radar e ponteiro, para que cada tela controle a animação.

#### Tela de cadastro
- A função [`show_cadastro_screen(page)`](radartech/cadastroTech.py:40) cria campos de:
  - Nome
  - E-mail
  - DDD + telefone
  - Senha + confirmação
  - Aceite de termos LGPD

#### Validações
- Função [`validar_campos()`](radartech/cadastroTech.py:74):
  - Nome com ao menos 2 partes
  - E-mail com `@`
  - DDD com 2 dígitos
  - Telefone com tamanho mínimo
  - Senha forte para usuários comuns
  - Regra especial para e-mails que começam com “radar”
  - Senhas iguais
  - Termos aceitos

#### Barra de progresso de cadastro
- [`atualizar_progresso(...)`](radartech/cadastroTech.py:111) calcula percentual com base nas validações.
- Quando chega em 100%:
  - Salva os dados em [`USUARIO_TESTE_CADASTRO`](radartech/cadastroTech.py:130)
  - Dispara [`processar_redirecionamento()`](radartech/cadastroTech.py:136)

#### Redirecionamento por perfil
- Em [`processar_redirecionamento()`](radartech/cadastroTech.py:136):
  - E-mail prefixo “radar” → tenta abrir módulo de interesse
  - Fluxo comum → volta para login

---

### 4) Tela de tendências: [`tendencia.py`](radartech/tendencia.py)

#### Construção da tela
- A função [`show_tendencia_screen(...)`](radartech/tendencia.py:6) limpa a página e aplica estilo visual padrão.

#### Métricas visuais
- Usa uma lista [`valores_barras = [...]`](radartech/tendencia.py:17) para construir barras em layout vertical.
- Cada barra é um [`ft.Container`](radartech/tendencia.py:19) com altura proporcional ao valor.

#### Navegação interna
- Botões da barra de navegação:
  - Tendências (tela atual)
  - Perfis → [`show_perfil_screen(...)`](radartech/tendencia.py:37)
  - Estratégia → [`show_estrateguia_screen(...)`](radartech/tendencia.py:41)

#### Animação do radar
- [`animar_ponteiro()`](radartech/tendencia.py:89) faz rotação contínua do ponteiro.

---

## Fluxo Geral da Aplicação

1. Inicialização em [`main.py`](radartech/main.py)
2. Loading animado
3. Login em [`show_login_screen()`](radartech/loginTech.py:6)
4. Cadastro em [`show_cadastro_screen()`](radartech/cadastroTech.py:40), se necessário
5. Tendências em [`show_tendencia_screen()`](radartech/tendencia.py:6)

---

## Situação Atual do Projeto

**Status:** Em desenvolvimento.

Próximas evoluções esperadas:
- Integração real com banco de dados MySQL
- Persistência de usuários e autenticação segura
- Integração de recuperação de senha com serviço real
- Separação por camadas (UI, serviços, dados)

---

## Observações Técnicas

- O projeto foi reorganizado com separação entre telas ([`radartech/screens/`](radartech/screens)) e componentes reutilizáveis ([`radartech/components/`](radartech/components)).
- O uso de [`page.run_task(...)`](radartech/main.py:115) permite animações assíncronas sem travar interface.
- O dicionário global de cadastro é útil para protótipo, mas deve ser substituído por persistência real em produção.
