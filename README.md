# 🤖 Agente de Backlog

Script Python que lê documentos de requisitos (`.docx`, `.pdf`, `.txt`) e gera
automaticamente o backlog completo — com User Stories, critérios de aceitação,
distribuição customizável em Sprints, documento Word formatado e planilha gerencial 
automatizada com Kanban e Dashboard Executivo.

O agente opera em **dois modos**:

| Modo | Quando usar | Saída |
|------|-------------|-------|
| **[1] Documento de Requisitos** | Projetos novos com análise formal | DOCX + XLSX |
| **[2] Mudanças / Melhorias** | Projetos legados sem documento | XLSX |

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

4. ESTIMATIVA DE HORAS (sua participação)
   Para cada US o terminal pergunta: "Quantas horas úteis de Dev e Teste?"
   → Responda com um número inteiro
   → Se transbordar o orçamento da sprint, você pode confirmar ou abortar

5. DISTRIBUIÇÃO EM SPRINTS
   O agente distribui automaticamente usando Horas Reais:
   → Baseado nas semanas configuráveis da sprint e carga horária/dia
   → Reserva um valor em horas fixado no fluxo para Deploy no fim do clico
   → Respeita dependências técnicas entre US

6. GERAÇÃO DOS ARQUIVOS
   Informe o nome do projeto e a pasta de saída
   → Backlog .docx gerado e formatado por Horas
   → Planilha .xlsx inteligente com Resumo Gerencial, Sprints com Status automático e Kanban dinâmico
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
- Cada sprint com objetivo, horas estimadas de esforço, horas de deploy estipuladas
- Cada card com história, critérios de aceitação, tela, campos, horas e dependências

### Planilha `.xlsx` — 5 abas

| Aba | Conteúdo |
|-----|----------|
| **Resumo** | Dashboard executivo com cálculo da Timeline do projeto e conversões macro de horas. |
| **Backlog** | Todos os cards com sprint, horas estimadas de esforço/teste, prioridade e status selecionável. |
| **Sprints** | Resumo dos sprints com totais de horas calculados, e Status interligado pela fórmula Backlog. |
| **Kanban** | Espelho dinâmico do Backlog em fluxo contínuo implementado com fórmulas de Matriz Automática. |
| **Legenda** | Referência de cores por status, siglas e módulo. |

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
| Duração do sprint | Personalizável na inicialização (Ex: 2 a 4 semanas) |
| Capacidade da sprint | Calculada via (Semanas) * (Carga Produtiva Horas/Dia) |
| Como estimar o esforço | Em **Horas Úteis** individualmente em Desenvolvimento e Validações de Teste |
| Deploy e Produção | Abstraído de cada História e reservado globalmente no cálculo da Sprint |
| Transbordo de Histórias | Agente avisa do transbordo de limite de horas se alocar o recurso individualmente |

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
