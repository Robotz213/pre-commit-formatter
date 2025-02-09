# Pre-Commit Formatter

Este projeto é projetado para executar hooks de pré-commit e formatar os resultados em um arquivo HTML para visualização fácil.

## Como Funciona

1. **Executar Hooks de Pré-Commit**: A classe `PreCommitParser` executa os hooks de pré-commit usando o comando `pre-commit run --all-files`.
2. **Analisar Saída**: A saída dos hooks de pré-commit é analisada para extrair informações relevantes, como caminhos de arquivos, números de linha, números de coluna e mensagens de erro.
3. **Gerar HTML**: As informações analisadas são então formatadas em um arquivo HTML usando templates Jinja2. O arquivo HTML inclui links para as linhas relevantes no código-fonte e referências à documentação dos erros.

## Instalação

Para usar este projeto, você precisa ter Python e `pre-commit` instalados. Você pode instalar as dependências necessárias usando pip:

```sh
poetry install
```

## Uso

Para executar o formatter de pré-commit, execute o seguinte comando:

```sh
python -m pre_commit_formatter
```

Isso gerará um arquivo HTML chamado `result_pre_commit.html` no diretório do projeto.

## Estrutura do Projeto

- `pre_commit_formatter/__main__.py`: Contém a função principal para executar o formatter de pré-commit.
- `pre_commit_formatter/__init__.py`: Contém a classe `PreCommitParser`, que lida com a execução dos hooks de pré-commit e a formatação da saída.
- `site/templates/`: Contém os templates Jinja2 usados para gerar o arquivo HTML.

## Templates

O projeto usa templates Jinja2 para formatar a saída HTML. Os templates estão localizados no diretório `site/templates/` e incluem:

- `code_part.jinja`: Template para formatar partes do código.
- `code_error.jinja`: Template para formatar erros de código.
- `html_content.jinja`: Template para o conteúdo geral do HTML.

## Exemplo

Aqui está um exemplo de como a saída HTML pode parecer:

```html
<h3>Arquivo: <a href="./path/to/file.py:10:5">path/to/file.py:10:5</a></h3>
<p>
  Erro: <a href="https://docs.astral.sh/ruff/rules/#E123">E123</a> Alguma
  mensagem de erro
</p>
<pre>
    | Alguma parte do código |
</pre>
```

## Licença

Este projeto é licenciado sob a Licença MIT.
