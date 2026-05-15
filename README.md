# 🤖 Agente de US — Gerador de JSON

Script Python que lê documentos de requisitos (`.docx`, `.pdf`, `.txt`) e gera automaticamente
o backlog estruturado em formato **JSON**, com épicos, User Stories e critérios de aceitação prontos
para importação na Plataforma Web de gestão ágil.

> [!WARNING]
> **Este projeto utiliza um modelo de linguagem (LLM) para análise e geração de conteúdo.**
> LLMs cometem erros — podem interpretar mal requisitos, gerar critérios incompletos ou
> organizar épicos de forma inadequada ao contexto real do projeto.
> **Toda análise gerada deve ser revisada e validada pelo analista de requisitos
> antes de ser utilizada como base para o desenvolvimento.**

---

## O que o agente faz

1. **Lê** um ou mais documentos de requisitos (`.docx`, `.pdf`, `.txt`)
2. **Extrai** via LLM: nome do projeto, descrição, atores e épicos
3. **Gera** as User Stories com critérios de aceitação no padrão Gherkin
4. **Salva** um arquivo `.json` pronto para ser importado na Plataforma Web

---

## Pré-requisitos

- Python 3.10+
- API Key da Anthropic → [console.anthropic.com](https://console.anthropic.com)

---

## Instalação

### 1. Criar e ativar um ambiente virtual (recomendado)
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar a chave da API
```bash
cp .env.example .env
```
Edite o `.env` e substitua `sk-ant-SUA_CHAVE_AQUI` pela sua chave real.  
→ Obtenha em: [console.anthropic.com](https://console.anthropic.com)

> ⚠️ **NUNCA** versione o `.env`. Ele já está no `.gitignore`.

---

## Como usar

```bash
python agente_us.py
```

### Fluxo passo a passo

```
1. DOCUMENTOS
   Informe o caminho de cada documento de requisitos
   → Pode informar mais de um (ENTER em branco para encerrar)
   → Formatos aceitos: .docx · .pdf · .txt

2. EXTRAÇÃO
   O agente envia os documentos ao LLM e extrai:
   → Nome do projeto · Descrição · Atores · Épicos

3. GERAÇÃO DE US
   Para cada épico, o agente gera as User Stories com:
   → História no formato "Como [ator], quero [ação] para [benefício]"
   → Critérios de aceitação no formato Gherkin (Dado/Quando/Então)
   → Dependências entre US

4. JSON GERADO
   O arquivo é salvo em ./backlog_json/<nome_projeto>_backlog.json
   → Faça o upload na Plataforma Web para iniciar o Sprint Planning
```

---

## Arquivo de saída

```
./backlog_json/
  <nome_projeto>_backlog.json
```

### Estrutura do JSON

```json
{
  "projeto": "Nome do Projeto",
  "descricao": "Descrição resumida do projeto.",
  "atores": ["Usuário Final", "Administrador"],
  "epicos": [
    {
      "id": "EP01",
      "nome": "Nome do Épico",
      "descricao": "Descrição do épico."
    }
  ],
  "user_stories": [
    {
      "epico_id": "EP01",
      "titulo": "Título curto da US",
      "historia": "Como Usuário Final, quero realizar X para Y.",
      "criterios_aceitacao": [
        "Dado que estou na tela X, Quando aciono Y, Então vejo Z."
      ],
      "dependencias": []
    }
  ]
}
```

---

## Modelos disponíveis

Altere a variável `MODEL` no script conforme a necessidade:

| Modelo | Uso | Custo |
|--------|-----|-------|
| `claude-haiku-4-5-20251001` | Testes e validação do fluxo | Mais barato |
| `claude-sonnet-4-6` | Uso em produção | Melhor qualidade |

---

## Dúvidas frequentes

**Posso informar mais de um documento?**  
Sim. O agente concatena todos antes de enviar ao LLM. Útil quando a área entrega o documento de requisitos e planilhas complementares.

**O agente substitui o analista de requisitos?**  
Não. O analista continua responsável pela elicitação e pelo documento de requisitos.
O agente automatiza a transformação do documento em backlog estruturado.
A validação ainda é feita por você e pelo analista.

**Posso alterar os prompts?**  
Sim, diretamente no script. Os prompts `PROMPT_EXTRACAO` e `PROMPT_GERAR_US` são texto livre.
Atenção: mantenha as chaves duplas `{{` e `}}` no JSON de exemplo dentro dos prompts.

---

## Dependências Python

```
anthropic      — API Anthropic (Claude)
pymupdf        — leitura de .pdf
python-dotenv  — carregamento do .env
```
