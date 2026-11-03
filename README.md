# Guilherme Oliveira — Portfólio de TI

Portfólio profissional em português, com identidade escura, HTML semântico, CSS responsivo e JavaScript progressivo. Sem framework, backend, banco de dados, fontes remotas ou rastreamento.

Publicação existente: [GitHub Pages](https://gui71.github.io/GuilhermeOliveira_portfolio/). Esta sprint prepara uma futura hospedagem isolada na Oracle Cloud; nenhuma migração foi executada.

## Conteúdo

Projetos: automação de oposições e registros internos; plataforma de inscrições e sorteios; gestão de ambulatório multiprofissional (em desenvolvimento); MAVEN (acadêmico colaborativo, em produção); automação assistida de documentos de licitações (em desenvolvimento); este portfólio. Os textos distinguem uso interno, produção e desenvolvimento e descrevem a atuação em requisitos, integração, testes e entrega com apoio de ferramentas de IA.

A formação e a experiência seguem os dados confirmados pelo titular: Gestão de TI concluída em 2024, técnico em Redes concluído em abril de 2026 (1.000h), SENALBA com cargo formal de Assistente Administrativo e experiência anterior em almoxarifado. Tecnologias aplicadas e fundamentos de formação aparecem com contexto, sem alegação de especialidade ou certificação.

## Projetos pessoais adicionados

- **Nosso Infinito — Landing Page Pessoal Interativa:** presente de Dia dos Namorados com composição visual, responsividade e interações multimídia. HTML, CSS e JavaScript confirmados no código. [Acessar projeto](https://amor.matrix.com.br/) · [Repositório GitHub](https://github.com/Gui71/nossoinfinito).
- **Chá de Casa Nova — Aplicação Web de Lista de Presentes:** apresentação de itens, registro de escolhas e administração com Django, templates HTML, CSS e JavaScript. Experiência de implantação em Linux, Docker e Oracle Cloud conforme contexto fornecido pelo titular. [Acessar projeto](https://casanova.mavensec.com.br/) · [Repositório privado, com acesso restrito](https://github.com/Gui71/presentes), apresentado conforme orientação do titular, sem oferta pública de código-fonte.

Os repositórios foram consultados apenas como referência. Nenhuma fotografia, música, vídeo, dado de convidados ou configuração de produção foi copiada. O endereço HTTPS do Nosso Infinito deve ser preservado mesmo em caso de indisponibilidade temporária. A atualização mantém os projetos anteriores e não altera hospedagem, Docker, Nginx ou infraestrutura.

## Estrutura

- `index.html`, `styles.css`, `script.js`: página, apresentação e modal acessível da foto.
- `img/`: foto e favicons utilizados; mídias antigas permanecem no checkout.
- `scripts/export_site.py`: gera pacote estático com lista explícita de arquivos públicos.
- `tests/test_publication.py`: teste do limite de publicação.
- `_config.yml`: exclusões para o GitHub Pages usando Jekyll por branch.
- `Dockerfile`, `.dockerignore`, `compose.portfolio.yml`, `deploy/nginx.conf`: servidor estático isolado.
- `DEPLOY-ORACLE.md`: pré-check, publicação autorizada e rollback.
- `VALIDACAO.md`: verificações desta sprint e limitações.

## Revisão local segura

Requer Python 3 apenas como ferramenta local. Gere um diretório novo; a exportação recusa sobrescrever diretórios existentes:

```bash
python3 scripts/export_site.py dist/revisao-01
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist/revisao-01
```

Abra `http://127.0.0.1:8000`. Teste links do menu, Tab, Enter na foto, Tab dentro do modal, Escape, botão Fechar e viewport de 360px. Para testar a base do GitHub Pages, exporte para `dist/pages/GuilhermeOliveira_portfolio` e sirva `dist/pages`. Abra `/GuilhermeOliveira_portfolio/`. Não sirva a raiz do checkout: ela contém materiais locais que não pertencem à publicação.

```bash
python3 -m unittest discover -s tests -v
git diff --check
```

## Privacidade e publicação estática

Somente os 11 arquivos da lista `PUBLIC_FILES` entram no pacote exportado. O Docker usa a mesma seleção explícita. Currículos de referência, instruções locais, arquivos de ferramentas, documentos, `.env`, vídeos e screenshots de sistemas internos não são copiados. `.gitignore` impede a inclusão acidental dos materiais locais novos; **não retira arquivos já rastreados nem apaga histórico**.

Os vídeos e prints antigos não foram aprovados para republicação: o texto da versão anterior descrevia demonstrações de dados de participantes e funcionários. Permanecem no disco e no histórico, mas sem referência no novo HTML e fora da exportação, do contexto Docker e da saída Jekyll. A imagem histórica do portfólio também foi excluída da publicação para evitar conteúdo desatualizado. A foto de perfil foi inspecionada; os favicons existentes foram preservados. Nenhuma mídia interna deve voltar sem revisão humana integral. Esta alteração só produz efeito público depois da publicação autorizada; não remove cópias antigas já acessíveis.

Para Pages por branch, manter `_config.yml` e **não adicionar `.nojekyll`**, pois isso desativaria as exclusões. Antes de autorizar a publicação, confirmar nas configurações do repositório se Pages usa Jekyll por branch ou artefato personalizado. Se usar outro mecanismo, publicar apenas a saída de `export_site.py`; exclusões Jekyll não protegem um upload bruto do checkout. Não foi criado workflow de CI/CD. Caminhos relativos funcionam na raiz e na base do repositório; o container documentado serve na raiz.

LinkedIn anterior: validação bloqueada por HTTP 999; omitido da interface até confirmação do perfil pelo titular. Sem PDF público aprovado, não há botão de currículo. Repositórios antigos de sistemas internos não foram republicados: acessibilidade não equivaleria a aprovação de privacidade. E-mail preservado do site anterior; entrega de mensagens não foi testada. MAVEN respondeu HTTP 200 na verificação desta sprint; isso não é auditoria do sistema.

## Docker e Oracle Cloud

Copie `.env.example` para `.env`, defina uma porta **após conferir disponibilidade** e uma tag da versão revisada. A imagem usa a base oficial `nginx:alpine`, disponível para amd64 e arm64; o build nativo seleciona a arquitetura da máquina. Não houve teste ARM64 nesta máquina. Python e Node não fazem parte do runtime.

```bash
docker compose --env-file .env -f compose.portfolio.yml config
docker compose --env-file .env -f compose.portfolio.yml build portfolio
```

Subida, teste HTTP e configuração do proxy estão em [DEPLOY-ORACLE.md](DEPLOY-ORACLE.md). A porta é obrigatória e limitada a `127.0.0.1`; não existe porta padrão presumida. Nginx dentro do container serve arquivos; Nginx do host continua sendo o proxy central. O domínio sugerido ainda aguarda aprovação.

## Revisão e integração

Nenhum commit, push, PR, merge ou deploy é automático. Revise `git status`, `git diff --stat` e `git diff`. Após autorizar a publicação em branch/PR, adicione somente os arquivos desta sprint (nunca `git add -f` nos materiais privados), faça commit e envie a branch. Revise a lista de arquivos no PR antes de integrar. Validar o mecanismo de Pages e o pacote público antes do merge.

Para reverter uma versão publicada, prefira um novo commit com `git revert SHA_DO_COMMIT_DA_SPRINT` após revisão, seguido do fluxo normal de publicação. **A base antiga referencia mídias internas**: não restaure o HTML antigo publicamente sem revisar essas exposições. Para Docker, conserve a imagem da última versão segura e troque somente a tag do serviço do portfólio; procedimento completo no guia. Não use reset destrutivo nem limpeza global de imagens.

Após autorização para commit/push/PR, na branch atual, a sequência é:

```bash
git diff --check
python3 -m unittest discover -s tests -v
git add .gitignore .dockerignore .env.example _config.yml index.html styles.css script.js img/site.webmanifest Dockerfile compose.portfolio.yml deploy/nginx.conf scripts/export_site.py tests/test_publication.py README.md DEPLOY-ORACLE.md VALIDACAO.md
git diff --cached --stat
# Conferir a lista e o diff staged antes de continuar.
git diff --cached
git commit -m "Moderniza portfólio e prepara hospedagem estática isolada"
git push -u origin feat/portfolio-modernizacao-2026
gh pr create --base main --head feat/portfolio-modernizacao-2026 --fill
```

A criação do PR não autoriza merge nem implantação. Não inclua referências locais à força. O guia Oracle começa por verificações de ambiente e exige autorização para cada mudança de infraestrutura.
