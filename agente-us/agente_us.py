import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
import anthropic

load_dotenv()
CLIENT = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-haiku-4-5-20251001"

# ════════════════════════════════════════════════════════════
# UTILITÁRIOS DE TERMINAL
# ════════════════════════════════════════════════════════════

AZUL    = "\033[94m"
VERDE   = "\033[92m"
AMARELO = "\033[93m"
CINZA   = "\033[90m"
RESET   = "\033[0m"
BOLD    = "\033[1m"

def titulo(t):   print(f"\n{BOLD}{AZUL}{'═'*60}\n  {t}\n{'═'*60}{RESET}")
def secao(t):    print(f"\n{BOLD}{VERDE}── {t}{RESET}")
def info(t):     print(f"{CINZA}   {t}{RESET}")
def pergunta(t): return input(f"\n{AMARELO}▶  {t}{RESET} ").strip()
def ok(t):       print(f"{VERDE}   ✓ {t}{RESET}")
def aviso(t):    print(f"{AMARELO}   ⚠ {t}{RESET}")

# ════════════════════════════════════════════════════════════
# LEITURA DE DOCUMENTOS
# ════════════════════════════════════════════════════════════

def ler_documento(caminho: str) -> str:
    ext = Path(caminho).suffix.lower()
    if ext == ".txt":
        return Path(caminho).read_text(encoding="utf-8")
    elif ext == ".pdf":
        import fitz
        doc = fitz.open(caminho)
        return "\n".join(page.get_text() for page in doc)
    elif ext == ".docx":
        from docx import Document
        doc = Document(caminho)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    raise ValueError(f"Formato não suportado: {ext}. Use .docx, .pdf ou .txt")

def coletar_documentos() -> str:
    secao("Documentos de Entrada")
    info("Informe os caminhos dos documentos (ENTER em branco para finalizar).")
    info("Formatos aceitos: .docx · .pdf · .txt")
    textos = []
    idx = 1
    while True:
        caminho = pergunta(f"Documento {idx} (ou ENTER para continuar):").strip('"').strip("'")
        if not caminho:
            if not textos:
                aviso("Nenhum documento informado. Tente novamente.")
                continue
            break
        if not Path(caminho).exists():
            aviso(f"Arquivo não encontrado: {caminho}")
            continue
        try:
            texto = ler_documento(caminho)
            textos.append(f"=== DOCUMENTO {idx}: {Path(caminho).name} ===\n{texto}")
            ok(f"Lido: {Path(caminho).name} ({len(texto):,} caracteres)")
            idx += 1
        except Exception as e:
            aviso(f"Erro ao ler documento: {e}")
    return "\n\n".join(textos)

# ════════════════════════════════════════════════════════════
# PROMPTS
# ════════════════════════════════════════════════════════════

PROMPT_EXTRACAO = """
Você é um analista de requisitos sênior.
Analise os dados abaixo e extraia as informações relevantes para construção de um backlog Scrum.

Retorne APENAS um JSON válido, sem texto adicional, com esta estrutura exata:
{{
  "projeto": "nome do projeto",
  "descricao": "descrição resumida em 2-3 linhas",
  "atores": ["lista de perfis identificados"],
  "epicos": [
    {{
      "id": "EP01",
      "nome": "nome do épico",
      "descricao": "descrição do épico"
    }}
  ]
}}

DOCUMENTOS:
{dados}
"""

PROMPT_GERAR_US = """
Você é um analista de requisitos sênior especializado em Scrum.
Com base nos épicos e requisitos abaixo, gere as Histórias de Usuário (User Stories) detalhadas.

Regras obrigatórias:
- A saída deve ser um JSON válido contendo uma lista "user_stories".
- Formato da história: "Como [ator], quero [ação] para [benefício]".
- Cada US deve conter a lista "criterios_aceitacao" no formato:
  "Dado [condição], Quando [ação], Então [resultado]".
- NÃO adicione estimativas de pontos ou horas (será preenchido pela equipe na plataforma).

Retorne APENAS um JSON válido, sem texto adicional:
{{
  "user_stories": [
    {{
      "epico_id": "EP01",
      "titulo": "título curto da US",
      "historia": "Como [ator], quero [ação] para [benefício].",
      "criterios_aceitacao": ["Dado [condição], Quando [ação], Então [resultado]"],
      "dependencias": []
    }}
  ]
}}

PROJETO/ÉPICOS:
{requisitos}
"""

def chamar_claude(prompt: str) -> str:
    response = CLIENT.messages.create(
        model=MODEL,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def extrair_json(texto: str) -> dict:
    if not texto: return {}
    texto = re.sub(r"```json\s*", "", texto)
    texto = re.sub(r"```\s*", "", texto)
    inicio = texto.find("{")
    fim = texto.rfind("}") + 1
    if inicio == -1 or fim == 0:
        raise ValueError("JSON não encontrado na resposta.")
    return json.loads(texto[inicio:fim])

# ════════════════════════════════════════════════════════════
# FLUXO PRINCIPAL
# ════════════════════════════════════════════════════════════

def main():
    titulo("AGENTE DE US — GERADOR DE JSON")
    info("Lê documentos de requisitos e gera o JSON das User Stories.")
    info("O JSON gerado pode ser importado na Plataforma Web para gestão da equipe.\n")

    texto_entrada = coletar_documentos()

    secao("Analisando o projeto via IA...")
    resp_ext = chamar_claude(PROMPT_EXTRACAO.format(dados=texto_entrada))
    projeto_dados = extrair_json(resp_ext)

    ok(f"Projeto: {projeto_dados.get('projeto', 'Desconhecido')}")
    ok(f"Épicos encontrados: {len(projeto_dados.get('epicos', []))}")

    secao("Gerando User Stories e Critérios de Aceitação...")
    resp_us = chamar_claude(PROMPT_GERAR_US.format(requisitos=json.dumps(projeto_dados, ensure_ascii=False)))
    us_dados = extrair_json(resp_us)

    user_stories = us_dados.get("user_stories", [])
    ok(f"User Stories geradas: {len(user_stories)}")

    # Montar resultado final
    resultado_final = {
        "projeto": projeto_dados.get("projeto"),
        "descricao": projeto_dados.get("descricao"),
        "atores": projeto_dados.get("atores", []),
        "epicos": projeto_dados.get("epicos", []),
        "user_stories": user_stories
    }

    # Salvar JSON
    pasta_saida = Path("./backlog_json")
    pasta_saida.mkdir(parents=True, exist_ok=True)

    nome_proj = re.sub(r"[^a-zA-Z0-9_\-]", "_", resultado_final.get("projeto", "projeto").lower())
    caminho_arquivo = pasta_saida / f"{nome_proj}_backlog.json"

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=2)

    titulo("SUCESSO!")
    print(f"  {VERDE}JSON Gerado:{RESET} {caminho_arquivo}\n")
    info("Faça o upload deste arquivo na Plataforma Web para iniciar o Sprint Planning.")

if __name__ == "__main__":
    main()
