# 🤖 Agente de Backlog 

Script Python que lê documentos de requisitos (`.docx`, `.pdf`, `.txt`) e gera
automaticamente o backlog completo — com User Stories, critérios de aceitação,
distribuição em sprints semanais, documento Word formatado e planilha de acompanhamento
com Kanban.

O analista de requisitos entrega o documento → você roda o agente → backlog pronto para validar.

---

## O que o agente NÃO precisa

- ❌ Acesso ao banco de dados
- ❌ VPN ou rede interna

---

## Pré-requisitos

- Python 3.10+
- API Key da Anthropic → [console.anthropic.com](https://console.anthropic.com)

---

## Instalação

### 1. (Recomendado) Criar e ativar um ambiente virtual
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2. Instalar dependências Python
```bash
pip install -r requirements.txt
```

### 3. Configurar a chave da API
Copie o arquivo de exemplo e preencha com sua chave:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edite o `.env` e substitua `sk-ant-SUA_CHAVE_AQUI` pela sua chave real da Anthropic  
→ Obtenha em: [console.anthropic.com](https://console.anthropic.com)

> ⚠️ **NUNCA** versione o `.env`. Ele já está no `.gitignore` por padrão.

---

## Como usar

```bash
python backlog_agent.py
```

### Fluxo passo a passo

```
1. DOCUMENTOS
   Informe o caminho do documento de requisitos
   → Pode informar mais de um (ENTER em branco para encerrar)
   → Formatos aceitos: .docx · .pdf · .txt

2. EXTRAÇÃO AUTOMÁTICA
   O agente lê os documentos e extrai:
   → Épicos · Requisitos Funcionais · Regras de Negócio
   → Requisitos Não Funcionais · Atores · Fora de escopo
   Você revisa e confirma se os épicos estão corretos

3. USER STORIES
   O agente gera as User Stories com:
   → História: "Como [ator], quero [ação] para [benefício]"
   → Critérios de aceitação
   → Tela / contexto no sistema
   → Campos e elementos de tela
   → Dependências entre US
   Você revisa e confirma

4. ESTIMATIVA DE DIAS (sua participação)
   Para cada US o terminal pergunta: "Quantos dias úteis?"
   → Responda de 1 a 5
   → Se informar mais de 5, o agente sugere dividir a US em duas

5. DISTRIBUIÇÃO EM SPRINTS
   O agente distribui automaticamente:
   → 1 sprint = 1 semana = 5 dias úteis
   → Respeita dependências técnicas entre US
   → Agrupa US pequenas (1–2 dias) quando possível
   → Calcula o buffer de cada sprint explicitamente
   Você vê o resumo antes de gerar os arquivos

6. GERAÇÃO DOS ARQUIVOS
   Informe o nome do projeto e a pasta de saída
   → Backlog .docx gerado e formatado
   → Planilha .xlsx com Kanban, Sprints e Legenda
```

---

## Modelos disponíveis

Altere a variável `MODEL` no script conforme a necessidade:

| Modelo | Uso | Custo |
|--------|-----|-------|
| `claude-haiku-4-5-20251001` | Testes e validação do fluxo | Mais barato |
| `claude-sonnet-4-6` | Uso em produção | Melhor qualidade |

---

## Arquivos gerados

```
/backlog/
  Backlog_[projeto]_[data].docx
  Acompanhamento_[projeto]_[data].xlsx
```

### Backlog `.docx`
- Capa com nome do projeto, data e total de sprints
- Visão geral com épicos, atores e itens fora de escopo
- Cada sprint com objetivo, dias estimados, buffer e entrega
- Cada card com história, critérios de aceitação, tela, campos e dependências

### Planilha `.xlsx` — 4 abas

| Aba | Conteúdo |
|-----|----------|
| **Backlog** | Todos os cards com sprint, semana, dias, prioridade e dropdown de status |
| **Sprints** | Resumo dos sprints com totais calculados por fórmula |
| **Kanban** | Colunas To Do · In Progress · In Review · Done · Blocked |
| **Legenda** | Referência de cores por status e módulo |

---

## Kanban — Status

| Status | Quando usar |
|--------|-------------|
| **To Do** | Card ainda não iniciado |
| **In Progress** | Em desenvolvimento neste sprint |
| **In Review** | Entregue — aguardando validação / aprovação |
| **Done** | Validado e aceito |
| **Blocked** | Impedido por dependência ou dúvida externa |

---

## Regras Scrum adotadas

| Regra | Valor |
|-------|-------|
| Duração do sprint | 1 semana (5 dias úteis) |
| Máximo de dias por US | 5 dias úteis |
| Quem estima os dias | O DEV — durante a execução do agente |
| US com mais de 5 dias | Agente sugere divisão em 2 US |
| Review | Conforme disponibilidade do solicitante |
| Buffer | Calculado automaticamente por sprint |

---

## Estrutura de pastas sugerida

```
/projetos/
  /[NOME_PROJETO]/
    /entrada/       ← documentos da área + análise de requisitos
    /backlog/       ← outputs do backlog_agent.py
```

---

## Dúvidas frequentes

**Posso informar mais de um documento?**
Sim. Útil quando a área entrega o documento de requisitos e planilhas complementares.

**O agente substitui o analista de requisitos?**
Não. O analista continua responsável pela elicitação e pelo documento de requisitos.
O agente automatiza a transformação do documento em backlog.
A validação ainda é feita por você e pelo analista.

**Posso usar o agente para fases seguintes do mesmo projeto?**
Sim. Rode novamente com os documentos da nova fase e nomeie como `PROJETO_FASE2`.

**Posso alterar os prompts?**
Sim, diretamente no script. Os prompts `PROMPT_EXTRACAO_BASE` e `PROMPT_GERAR_US_BASE`
são texto livre — edite as instruções conforme necessário.
Atenção: mantenha as chaves duplas `{{` e `}}` no JSON de exemplo dentro dos prompts.

---

## Dependências Python

```
anthropic    — API Anthropic (Claude)
python-docx  — leitura e geração de .docx
openpyxl     — geração de .xlsx
pymupdf      — leitura de .pdf
python-dotenv — carregamento do .env
```
