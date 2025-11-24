# ⚓ AquaFiscal - Gerador de Notas Fiscais e Vendas

## 📖 Sobre o Projeto
O **AquaFiscal** é um sistema desktop desenvolvido em **Python** para gerenciamento de vendas e emissão de documentos fiscais simulados (DANFE, NFC-e, etc.) para uma empresa fictícia de embarcações, a **Aquavida**.  
O projeto demonstra o uso de interfaces gráficas nativas e a geração programática de arquivos PDF complexos, incluindo vetores, tabelas e códigos de barras.

---

## ✨ Funcionalidades

- **Interface Gráfica (GUI):** Formulários completos para entrada de dados usando Tkinter com suporte a rolagem (scroll).  
- **Carrinho de Compras:** Adição dinâmica de produtos com cálculo automático de totais.  
- **Cálculo de Impostos:** Estimativa automática de ICMS baseada no valor dos produtos.  
- **Geração de PDF (ReportLab):**
  - Layout desenhado *pixel-perfect* simulando uma DANFE.
  - Geração de Código de Barras (Code128) para a chave de acesso.
  - Canhoto de recebimento destacável.
  - Cabeçalho, dados do transportador e rodapé formatados.
- **Validações:** Verificação de campos vazios e tratamento de erros numéricos.

---

## 🛠️ Tecnologias Utilizadas

- **Python** – Linguagem principal  
- **Tkinter** – Interface gráfica  
- **ReportLab** – Geração de PDFs e gráficos vetoriais  

---

## 📸 Screenshots
*(Se possível, adicione aqui uma imagem da tela do programa rodando e uma imagem do PDF gerado)*

---

## 🚀 Como Executar

### Pré-requisitos
Você precisa ter o **Python** instalado em sua máquina.  
Além disso, é necessário instalar a biblioteca `reportlab`.

### Instalação

Clone o repositório:
```bash
git clone https://github.com/SEU-USUARIO/aquafiscal.git
```

Entre na pasta do projeto:
```bash
cd aquafiscal
```

Instale as dependências:
```bash
pip install reportlab
```

Execute o sistema:
```bash
python main.py
```
