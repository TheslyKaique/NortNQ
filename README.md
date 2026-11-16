# Norte NQ (Etapa 1: candles automáticos)

Arquivos:
- `collector.py`: baixa os candles de 15 min do NQ (Yahoo Finance) e grava `data.json`.
- `.github/workflows/update.yml`: roda o coletor a cada 10 min em dias úteis e salva o `data.json` no repositório.
- `index.html`: o site. Lê `data.json` ao abrir (e a cada 5 min) e recalcula tudo.

## Colocar no ar (GitHub Pages)
1. Crie um repositório **público** no GitHub (repositórios privados têm limite de minutos de Actions) e envie estes arquivos, mantendo a pasta `.github/workflows`.
2. Em *Settings → Pages*, escolha *Deploy from a branch*, branch `main`, pasta `/ (root)`.
3. Em *Actions*, abra "Atualizar candles" e clique em *Run workflow* para gerar o primeiro `data.json`.
4. Abra o endereço do Pages. Pronto: a página atualiza sozinha.

## Testar no computador
    pip install -r requirements.txt
    python collector.py
    python -m http.server 8000    # abra http://localhost:8000

(Abrir o `index.html` com duplo clique não funciona: o navegador bloqueia a leitura do `data.json`.)

## Limites desta etapa
- O Yahoo tem atraso de cerca de 10 a 15 min e não é uma API oficial: pode mudar ou falhar. Se falhar, o `data.json` anterior é mantido e a página avisa que está defasado.
- O agendador do GitHub pode atrasar alguns minutos e roda no máximo a cada 5 min.
- Eventos do dia ainda são digitados na própria página (Etapa 2 traz `events.json`).
