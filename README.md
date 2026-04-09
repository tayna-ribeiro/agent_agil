# 🤖 Agente de Backlog

Script Python que lê documentos de requisitos (`.docx`, `.pdf`, `.txt`) e gera
automaticamente o backlog completo — com User Stories, critérios de aceitação,
distribuição customizável em Sprints, documento Word formatado e planilha gerencial
automatizada com Kanban, Cronograma de fases e Testes de Aceitação.

> [!WARNING]
> **Este projeto utiliza um modelo de linguagem (LLM) para análise e geração de conteúdo.**
> LLMs cometem erros — podem interpretar mal requisitos, gerar critérios incompletos ou
> organizar épicos de forma inadequada ao contexto real do projeto.
> **Toda análise gerada deve ser revisada e validada pelo analista de requisitos
> antes de ser utilizada como base para o desenvolvimento.**

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

## Scripts disponíveis

| Script | Descrição |
|--------|-----------|
| `backlog_agent.py` | Fluxo completo: extrai requisitos, gera US, distribui sprints e gera DOCX + XLSX |
| `gerar_testes.py` | Script standalone: lê um Excel já existente e adiciona (ou atualiza) a aba de Testes de Aceitação |

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

### Backlog completo (projetos novos ou mudanças)

```bash
python backlog_agent.py
```

#### Fluxo passo a passo

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
   → Reserva um valor em horas fixado no fluxo para Deploy no fim do ciclo
   → Respeita dependências técnicas entre US

6. TESTES DE ACEITAÇÃO
   Para cada US, o agente gera os testes de aceitação via LLM:
   → Usa critérios de aceitação como base (quando disponíveis)
   → Formato: "Dado [contexto], quando [ação], então [resultado mensurável]"
   → Apenas os testes realmente necessários — sem redundância

7. GERAÇÃO DOS ARQUIVOS
   Informe o nome do projeto e a pasta de saída
   → Backlog .docx gerado e formatado por Horas
   → Planilha .xlsx com 7 abas (ver detalhes abaixo)
```

---

### Testes de aceitação para Excel já existente

Use este script para adicionar (ou regenerar) a aba de testes em planilhas já criadas:

```bash
python gerar_testes.py
```

O script lê a aba **Backlog** do Excel, gera os testes via LLM e adiciona a aba
**Testes de Aceitação** sem alterar nenhuma outra aba do arquivo.

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
  Backlog_[projeto]_[data].docx       ← apenas Modo 1
  Acompanhamento_[projeto]_[data].xlsx
```

### Backlog `.docx`
- Capa com nome do projeto, data e total de sprints
- Visão geral com épicos, atores e itens fora de escopo
- Cada sprint com objetivo, horas estimadas de esforço, horas de deploy estipuladas
- Cada card com história, critérios de aceitação, tela, campos, horas e dependências

### Planilha `.xlsx` — 7 abas

| Aba | Conteúdo |
|-----|----------|
| **Resumo** | Dashboard executivo com Timeline do projeto e conversões macro de horas. |
| **Backlog** | Todos os cards com sprint, horas estimadas, prioridade e status selecionável. |
| **Sprints** | Resumo dos sprints com totais de horas e Status interligado ao Backlog. |
| **Kanban** | Espelho dinâmico do Backlog em fluxo contínuo com fórmulas de Matriz Automática. |
| **Legenda** | Referência de cores por status, siglas e módulo. |
| **Cronograma** | Datas-limite de cada fase por sprint: Desenvolvimento → Teste de Aceitação → Apresentação → Homologação → Deploy. Sprints apertadas são destacadas em laranja. |
| **Testes de Aceitação** | Lista de testes gerada por LLM para cada US. O analista de requisitos preenche o resultado (✅ Passou / ❌ Falhou / 🔄 Reteste) após cada entrega do dev. |

---

## Aba Testes de Aceitação — como usar

Após cada entrega do desenvolvedor, o analista de requisitos preenche:

| Coluna | O que preencher |
|--------|-----------------|
| **F — Resultado** | `⬜ Não executado` / `✅ Passou` / `❌ Falhou` / `🔄 Reteste necessário` |
| **G — Observação** | Detalhes do comportamento observado ou descrição da falha |
| **H — Data** | Data em que o teste foi executado |
| **I — Testador** | Nome do analista responsável |

Use o **filtro da coluna F** para acompanhar o status dos testes por sprint.

---

## Kanban — Status

| Status | Quando usar |
|--------|-------------|
| **To Do** | Card ainda não iniciado |
| **In Progress** | Em desenvolvimento neste sprint |
| **In Acceptance Test** | Em teste de aceitação pelo analista de requisitos |
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
O agente automatiza a transformação do documento em backlog estruturado.
A validação ainda é feita por você e pelo analista.

**Os testes de aceitação gerados são definitivos?**  
Não. São uma sugestão inicial gerada por LLM com base nas User Stories.
O analista de requisitos deve revisá-los e adaptá-los ao contexto real do sistema
antes de executar.

**Posso usar o agente para fases seguintes do mesmo projeto?**  
Sim. Rode novamente com os documentos da nova fase e nomeie como `PROJETO_FASE2`.

**Posso regenerar apenas a aba de testes sem rodar o fluxo completo?**  
Sim. Use o `gerar_testes.py` apontando para o Excel já existente.

**Posso alterar os prompts?**  
Sim, diretamente no script. Os prompts `PROMPT_EXTRACAO_BASE`, `PROMPT_GERAR_US_BASE`
e os prompts de testes são texto livre — edite as instruções conforme necessário.
Atenção: mantenha as chaves duplas `{{` e `}}` no JSON de exemplo dentro dos prompts.

---

## Dependências Python

```
anthropic     — API Anthropic (Claude)
python-docx   — leitura e geração de .docx
openpyxl      — geração de .xlsx
pymupdf       — leitura de .pdf
python-dotenv — carregamento do .env
```
