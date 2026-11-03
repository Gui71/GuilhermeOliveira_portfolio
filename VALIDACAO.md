# Validação da sprint — 01/11/2026

## Base e escopo

Branch examinada: `feat/portfolio-modernizacao-2026`. Commit inicial: `525546b1163011dbc033a17acf1633ba9489caaf`. Remoto: `https://github.com/Gui71/GuilhermeOliveira_portfolio`. Antes da implementação havia apenas materiais locais não rastreados; nenhum arquivo rastreado modificado. Não houve commit, push, merge, deploy, SSH, mudança de domínio, proxy ou serviço existente.

Os dois currículos locais foram consultados sem reproduzir dados privados em logs ou documentação. O conteúdo público segue o contexto confirmado na sprint. O plano e os scripts auxiliares de navegador ficaram fora do versionamento. `AGENTS.md`, referências de currículo e diretórios de ferramentas estão ignorados; nenhum deles integra os pacotes estáticos.

## Comandos e resultados

- `python3 -m unittest discover -s tests -v`: **1 teste passou**. O teste foi executado antes da implementação do exportador e falhou por ausência dele; após implementação, passou. Verifica que a saída contém a página/foto/JS e exclui documentos, referências, ferramentas e mídias internas.
- `git diff --check`: passou, sem erro de whitespace.
- Parser `html5lib.HTMLParser().parse(...)` sobre `index.html`: **zero erros HTML5**. Conferência complementar de IDs únicos e todos os alvos de âncora.
- `PORTFOLIO_HOST_PORT=58329 PORTFOLIO_IMAGE_TAG=validacao docker compose -f compose.portfolio.yml config`: passou; bind renderizado `127.0.0.1:58329:80`, projeto próprio, sem rede host. Porta apenas de teste local; não representa disponibilidade na VM.
- `docker version`: CLI 26.1.5; acesso ao daemon negado, inclusive após execução fora do sandbox. `docker compose version`: 2.26.1-4.
- `docker build -t guilherme-portfolio:validacao-local .`: **não conseguiu iniciar o build** por `permission denied` no socket do daemon. Imagem, healthcheck, sintaxe Nginx em execução, HTTP do container e ARM64 **não foram validados**. Nenhum container foi iniciado.
- `python3 scripts/export_site.py dist/preview` e `python3 scripts/export_site.py dist/pages/GuilhermeOliveira_portfolio`: 11 arquivos públicos em cada pacote. Folha CSS posteriormente reformatada, sem alteração dos tokens, e recopiada para os dois pacotes antes da verificação final.
- Servidores temporários: `python3 -m http.server 58329 --bind 127.0.0.1 --directory dist/preview` e servidor 58331 com `--directory dist/pages`.
- `/tmp/portfolio-http-check.py`: HTTP 200 para página e todos os recursos referenciados em `/` e `/GuilhermeOliveira_portfolio/`. HTTP 404 para instruções locais, referências privadas, vídeo antigo, print interno, `.env` e caminho inexistente. Todos os alvos das âncoras existem; IDs únicos.
- Chromium headless com perfil temporário, CDP em loopback e `/tmp/portfolio-browser-check.py`: larguras **320, 360, 390, 768, 1024 e 1440px**, sem overflow horizontal; itens de navegação dentro da viewport. Página com um h1, seis cards, foto carregada, sem falhas de recursos nem erros de console/exceções. Inspeção visual dos screenshots desktop e mobile.
- Teclado no Chromium: Enter abre a foto; Tab permanece no diálogo; Escape e botão Fechar encerram o modal; foco retorna ao link. `prefers-reduced-motion: reduce` aplica `scroll-behavior: auto`. Sem JavaScript, texto, âncoras e link direto da foto permanecem disponíveis. Uma espera inicial do teste pela imagem lazy oculta foi corrigida no próprio teste; a página não exigiu correção por esse motivo.
- URLs: `curl -IL --max-time 20` fora da restrição de rede obteve **200** para GitHub e MAVEN. O repositório do portfólio também foi acessível pela ferramenta web. LinkedIn retornou **999**; perfil omitido da interface, sem supor substituto. Não houve teste de envio de e-mail, login ou funções do MAVEN.
- `git check-ignore` confirmou exclusão de instruções locais, currículos, `.env` e diretório de ferramentas. Busca de padrões de segredos nos arquivos textuais candidatos à entrega sem reproduzir possíveis valores em logs.
- Revisão independente de código somente leitura: **sem achados materiais**. Revisou os arquivos novos e alterados, limites de publicação, configurações Docker, modal e documentação.

## Limitações e pendências

- Sem build/runtime Docker por permissão do daemon; executar os comandos do guia em ambiente autorizado. A configuração Nginx foi revisada, mas `nginx -t` não foi executado localmente, pois Nginx não está instalado fora da imagem.
- Sem linter dedicado CSS/JS instalado; o CSS e o JS foram carregados/executados no Chromium. Isso não equivale a auditoria WCAG ou testes em Safari/Firefox, leitor de tela e aparelhos físicos.
- O teste da base Pages usa arquivos exportados sob subdiretório. O build Jekyll e as configurações reais da hospedagem não foram inspecionados. Confirmar Jekyll por branch antes de depender de `_config.yml`; em publicação por artefato, usar somente a exportação por allowlist.
- Vídeos e prints internos não foram aprovados para republicação nem auditados quadro a quadro. Permanecem no disco/histórico e podem continuar acessíveis na versão publicada anterior até intervenção autorizada. Não foram apagados nem alterados.
- Falta confirmar LinkedIn e eventual PDF público. Referências locais não constituem autorização para oferecer download dos currículos.
- Domínio, porta livre, arquitetura real, recursos, proxy, DNS e TLS na VM continuam pendentes de inspeção e autorização. O domínio sugerido não é a URL final.
- Rollback público deve preservar a política de privacidade: a base antiga referencia demonstrações internas. Preferir última imagem/versão segura, sem restaurar essas exposições.

Revisão local, sequência de branch/PR e rollback de código: `README.md`. Deploy e rollback isolado do container: `DEPLOY-ORACLE.md`.
