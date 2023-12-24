Certamente! Aqui está o texto sem os caracteres de formatação ```:

# Projeto CLI para Coleta e Manipulação de Dados do GBIF

Este é um projeto de linha de comando (CLI) desenvolvido em Python para coletar e manipular dados do GBIF (Global Biodiversity Information Facility), um site que disponibiliza um banco de dados de biodiversidade.

## Pré-requisitos

- Python 3.10 ou superior
- Poetry (para instalação de dependências)

## Instalação

Certifique-se de ter o Poetry instalado e, em seguida, execute o seguinte comando para instalar as dependências do projeto:

```
poetry install
```

## Utilização

Após a instalação bem-sucedida, você pode usar o seguinte comando no terminal:

```
python load_specie.py <Nome da espécie buscada> [--save-map]
```

Substitua `<Nome da espécie buscada>` pelo nome da espécie que você deseja pesquisar no GBIF.

### Opções

- `--save-map`: Esta opção salvará o mapa gerado usando o Folium em um arquivo HTML para consulta.

## Resultados

Os dados coletados serão salvos, por padrão, em uma planilha Excel localizada em `data/nome_da_especie.xlsx`. Além disso, se a opção `--save-map` for utilizada, os mapas gerados serão salvos na mesma pasta do script.

## Contribuições

Se você quiser contribuir para este projeto, sinta-se à vontade para abrir uma issue ou enviar um pull request. Toda contribuição é bem-vinda!

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
