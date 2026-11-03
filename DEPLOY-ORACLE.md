# Publicação isolada do portfólio na Oracle Cloud

Este é um procedimento para execução futura pelo proprietário ou após autorização específica. Nenhum SSH, DNS, TLS, alteração do proxy ou deploy foi realizado nesta sprint. O domínio sugerido `portfolio.mavensec.com.br` **não está aprovado**. Não copiar esse nome para a infraestrutura sem confirmação.

## 1. Confirmar o ambiente antes de executar

Contexto informado, ainda não inspecionado: Ubuntu 24.04 ARM64, Docker e Nginx no host compartilhando a VM com outras aplicações. Uma aplicação usa possivelmente `127.0.0.1:49171`; não alterar nem presumir disponibilidade de qualquer outra porta. Não tocar nos sites existentes, seus diretórios, redes ou containers.

Após autorização de acesso, executar somente leitura:

```bash
uname -m
lsb_release -ds
docker version
docker compose version
docker ps --format 'table {{.Names}}\t{{.Ports}}\t{{.Status}}'
docker compose ls
sudo ss -ltnp
sudo nginx -t
```

Inspecionar os server blocks existentes localmente, sem copiá-los para o repositório ou compartilhar saídas com segredos. Confirmar domínio aprovado, projeto Compose `guilherme-portfolio` ainda não utilizado, diretório exclusivo, recursos livres, backup e porta. Se houver conflito de nome, ajustar `name:` antes de usar. Não rodar comandos globais de limpeza/reinício ou `compose down`.

## 2. Revisão e backup

Publicar branch/PR somente com autorização; revisar conteúdo, arquivos ignorados e privacidade antes do merge. Confirmar SHA aprovado. No primeiro deploy, clonar em **novo diretório exclusivo** (exemplo abaixo usa `~/portfolio-publico`). Se já existir, inspecioná-lo antes de qualquer escrita. Não executar sobre checkout de outro serviço.

```bash
git clone https://github.com/Gui71/GuilhermeOliveira_portfolio.git ~/portfolio-publico
cd ~/portfolio-publico
git status --short
git fetch origin
# Substituir pelo SHA revisado que está no remoto:
git switch --detach SHA_APROVADO
```

Em atualizações: `git status --short` deve estar vazio antes de trocar versão. Use `git fetch origin` e `git switch --detach NOVO_SHA_APROVADO`; não usar pull que faça merge inesperado nem descartar alterações locais. Registrar fora do checkout: SHA atual, tag/digest da imagem anterior, porta, versão do Compose e backup protegido do `.env` (permissões 600). Antes de mudar o host, fazer backup **somente do server block do portfólio**. Na primeira instalação não existe versão anterior do portfólio no host.

## 3. Configuração e build

No diretório exclusivo do portfólio:

```bash
umask 077
cp .env.example .env
chmod 600 .env
```

Editar `.env` sem versionar:

```dotenv
PORTFOLIO_HOST_PORT=PORTA_LOCAL_VERIFICADA
PORTFOLIO_IMAGE_TAG=SHA_APROVADO
```

Os valores acima são marcadores: substituir a porta por número livre confirmado em `ss` e a tag pelo SHA. Não escolher 49172 ou outra por suposição. Não executar `source .env`; o Compose carrega o arquivo. Não reutilizar tag de uma versão já publicada.

```bash
docker compose --env-file .env -f compose.portfolio.yml config
docker compose --env-file .env -f compose.portfolio.yml build --pull portfolio
```

A imagem oficial `nginx:alpine` tem variantes ARM64/AMD64. Build nativo na VM ARM64; não forçar `platform: linux/amd64`. O uso de tag de base flutuante exige verificar atualizações; após o primeiro build aprovado, registrar o digest usado para rastreabilidade. Não é necessário registry ou workflow remoto. Contexto Docker e instruções COPY só permitem arquivos públicos. Revisar novamente antes do build se algum asset mudar.

## 4. Subida e teste local — só após autorização de deploy

Conferir novamente a porta e confirmar que nenhum projeto existente usa o nome escolhido:

```bash
docker compose --env-file .env -f compose.portfolio.yml up -d --no-deps --no-build portfolio
docker compose --env-file .env -f compose.portfolio.yml ps
docker compose --env-file .env -f compose.portfolio.yml logs --tail=30 portfolio
```

Substituir `PORTA_LOCAL_VERIFICADA` nos comandos abaixo; não publicar saídas privadas:

```bash
curl -fsSI http://127.0.0.1:PORTA_LOCAL_VERIFICADA/
curl -fsSI http://127.0.0.1:PORTA_LOCAL_VERIFICADA/styles.css
curl -fsSI http://127.0.0.1:PORTA_LOCAL_VERIFICADA/img/Guilherme.jpeg
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:PORTA_LOCAL_VERIFICADA/rota-inexistente
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:PORTA_LOCAL_VERIFICADA/curriculo_referencia/
```

Esperado: 200 para página/assets, 404 para os dois caminhos ausentes. Verificar healthcheck, cabeçalhos `nosniff`, `DENY`, política de referência, cache de HTML revalidado e assets por 1h. Confirmar bind `127.0.0.1` em `docker compose ps` e `ss`. Se houver conflito, parar e selecionar outra porta sem mexer no serviço que a ocupa. O container serve em `/`; não há fallback de SPA para páginas inexistentes. A base `/GuilhermeOliveira_portfolio/` é atendida pelo Pages ou por um pacote colocado nesse subdiretório, não por alias automático no container.

## 5. Proxy do HOST — exemplo, requer aprovação específica

Somente depois do teste local, preparar um **novo** arquivo de site do portfólio, sem sobrescrever configurações existentes. Confirmar caminhos e convenção do Nginx da VM. O exemplo abaixo é deliberadamente um domínio reservado; substituir pelo domínio aprovado e pela porta inspecionada. Não adicionar `default_server`.

```nginx
server {
    listen 80;
    server_name portfolio.example.invalid;

    location / {
        proxy_pass http://127.0.0.1:PORTA_LOCAL_VERIFICADA;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

O arquivo `deploy/nginx.conf` do repositório pertence **ao container** e nunca deve substituir `nginx.conf` do host. Habilitar somente o novo site conforme a estrutura local e a aprovação recebida. Antes de aplicar:

```bash
sudo nginx -t
```

**Apenas após autorização explícita e teste válido**, executar reload controlado (`sudo systemctl reload nginx`). Não reiniciar Nginx/Docker globalmente. Após reload, conferir o novo host por `curl -H 'Host: DOMINIO_APROVADO' http://127.0.0.1/` e testar os sites existentes sem modificá-los. Se o teste falhar, não recarregar; corrigir ou retirar apenas a nova configuração preparada.

## 6. DNS, TLS e verificação pública

Confirmar nome aprovado e endereço público real da VM antes de criar registros DNS. Não inferir IP nem adicionar AAAA sem confirmar IPv6. Alterações de DNS e emissão de certificado exigem autorização própria. Inspecionar o mecanismo TLS já usado na VM e adicionar somente o novo domínio. Não instalar outro proxy ou emitir certificado para nomes existentes por conveniência. A porta do container permanece local; não abrir nova porta no firewall.

Depois de DNS e TLS validados, verificar certificado, redirecionamento HTTP→HTTPS, página, assets, âncoras, teclado e mobile na URL aprovada. Comparar os outros sites antes/depois. Manter GitHub Pages até migração validada; não remover ou redirecionar automaticamente. Não adicionar CI/CD nesta sprint.

## 7. Rollback somente do portfólio

Não remover imagens antigas nem fazer `docker system prune`. Preservar imagem da última versão segura e seu `.env` protegido antes de atualizar. Se a nova versão falhar:

1. Restaurar no `.env` a tag anterior e a mesma porta. Confirmar que a imagem ainda existe (`docker image inspect guilherme-portfolio:TAG_ANTERIOR`).
2. Executar apenas:

```bash
docker compose --env-file .env -f compose.portfolio.yml up -d --no-deps --no-build portfolio
docker compose --env-file .env -f compose.portfolio.yml ps
```

3. Repetir `curl` local e público. Se necessário, voltar o checkout ao SHA anterior aprovado com árvore limpa, sem reconstruir a tag anterior por cima.
4. Proxy geralmente não muda entre versões. Se tiver mudado, restaurar somente o server block próprio com backup, `nginx -t` e reload após autorização. Não restaurar arquivos globais de outros sites.
5. Na primeira implantação sem imagem anterior, `docker compose --env-file .env -f compose.portfolio.yml stop portfolio` interrompe somente este serviço. Desabilitar apenas o novo vhost, com aprovação, teste e reload. Pages continua disponível.

Para reverter o código no GitHub, criar commit de reversão revisado via PR; nunca force-push/reset destrutivo. A versão antiga pode conter referências a demonstrações internas: preferir a última versão segura e não restaurar mídia sensível publicamente. Não alterar DNS em rollback sem autorização específica.
