# ILMJ Buscador de Vagas

## Descrição

O Buscador de Vagas é uma solução autoral da ILMJ que coleta automaticamente as vagas publicadas nos ATS (Applicant Tracking Systems) de clientes parceiros e as exibe nos respectivos sites de carreira. O objetivo é centralizar as oportunidades, reduzindo a evasão dos usuários e aumentando o engajamento dos candidatos.

---

## Funcionalidades principais

- Coleta automática das vagas e seus links diretamente dos ATS.
- API REST com endpoint `/vagas` para disponibilização das vagas em formato JSON.
- Atualização periódica das vagas, removendo as que não estão mais disponíveis e adicionando novas oportunidades.
- Separação das vagas por empresa para facilitar personalizações e comercialização.
- Implantação via Docker para portabilidade e facilidade de hospedagem.

---

## Tecnologias

- Python
- Selenium (para automação e extração de dados dos ATS)
- FastAPI (API REST)
- Docker (containerização)
- WordPress + Elementor (front-end integrado)

---

## Como executar

### Requisitos

- Python 3.8+
- Docker (opcional, mas recomendado)
- Navegador Chrome (para Selenium)

### Passos para execução local

1. Clone o repositório:
```bash
git clone https://github.com/seuusuario/ilmj-buscador-vagas.git
cd ilmj-buscador-vagas
