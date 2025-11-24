import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128 # Importando gerador de barras
from datetime import datetime
import os
import random # Para gerar números aleatórios

# --- PALETA DE CORES AQUAVIDA ---
COR_FUNDO = "#FFFFFF"       # Branco
COR_FRAME = "#FFFFFF"       # Branco para os frames
COR_TEXTO = "#01579B"       # Azul Marinho Escuro (para labels)
COR_INPUT = "#E1F5FE"       # Azul Claro (fundo dos campos)
COR_BOTAO = "#0288D1"       # Azul Médio (botões)
COR_BOTAO_TXT = "#FFFFFF"   # Texto do botão
COR_DESTAQUE = "#B3E5FC"    # Azul para bordas ou detalhes

class SistemaVendasBarcos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Vendas - Embarcações AQUAVIDA")
        self.root.geometry("1000x850")
        self.root.configure(bg=COR_FUNDO)

        # --- CONFIGURAÇÃO DE SCROLLBAR ---
        main_frame = tk.Frame(root, bg=COR_FUNDO)
        main_frame.pack(fill="both", expand=1)
        
        self.canvas_scroll = tk.Canvas(main_frame, bg=COR_FUNDO)
        self.canvas_scroll.pack(side="left", fill="both", expand=1)
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas_scroll.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.canvas_scroll.configure(yscrollcommand=scrollbar.set)
        self.canvas_scroll.bind('<Configure>', lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all")))
        
        self.content_frame = tk.Frame(self.canvas_scroll, bg=COR_FUNDO)
        self.canvas_scroll.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Estilos
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        style.map('Treeview', background=[('selected', '#0288D1')])
        style.configure("Treeview.Heading", background="#01579B", foreground="white", font=('Arial', 10, 'bold'))

        self.carrinho = []

        # =====================================================================
        # 1. DADOS DA OPERAÇÃO
        # =====================================================================
        frame_geral = tk.LabelFrame(self.content_frame, text="Dados da Operação", padx=10, pady=5, 
                                    bg=COR_FRAME, fg=COR_TEXTO, font=("Arial", 10, "bold"))
        frame_geral.pack(fill="x", padx=15, pady=10)

        # Linha 0 - Tipo de Documento
        self.criar_label(frame_geral, "Tipo de Documento:", 0, 0)
        tipos_doc = [
            "DANFE (NF-e)",
            "Nota Fiscal Eletrônica (NF-e)",
            "Nota Fiscal de Serviço (NFS-e)",
            "Nota Consumidor (NFC-e)",
            "Manifesto (MDF-e)",
            "Cupom Fiscal (CF-e)",
            "Nota Avulsa (NFA-e)"
        ]
        self.cb_tipo_doc = ttk.Combobox(frame_geral, values=tipos_doc, width=35)
        self.cb_tipo_doc.current(0)
        self.cb_tipo_doc.grid(row=0, column=1, padx=5, ipady=5)

        # Movimento (Entrada/Saída)
        self.criar_label(frame_geral, "Movimento:", 0, 2)
        self.cb_tipo_mov = ttk.Combobox(frame_geral, values=["1 - Saída", "0 - Entrada"], width=15)
        self.cb_tipo_mov.current(0) 
        self.cb_tipo_mov.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Linha 1
        self.criar_label(frame_geral, "Natureza da Operação:", 1, 0)
        self.cb_natureza = ttk.Combobox(frame_geral, values=["Venda de Mercadoria", "Prestação de Serviço", "Locação", "Outros"], width=35)
        self.cb_natureza.current(0)
        self.cb_natureza.grid(row=1, column=1, padx=5, ipady=5)

        self.criar_label(frame_geral, "Alíquota ICMS (%):", 1, 2)
        self.ent_imposto_perc = self.criar_input(frame_geral, width=10)
        self.ent_imposto_perc.insert(0, "18")
        self.ent_imposto_perc.grid(row=1, column=3, padx=5)

        # Linha 2 - NUMERO E SÉRIE
        self.criar_label(frame_geral, "Nº Nota:", 2, 0)
        self.ent_num_nf = self.criar_input(frame_geral, width=20)
        self.ent_num_nf.insert(0, "000.000.001")
        self.ent_num_nf.grid(row=2, column=1, padx=5, sticky="w", pady=5)

        self.criar_label(frame_geral, "Série:", 2, 2)
        self.ent_serie = self.criar_input(frame_geral, width=10)
        self.ent_serie.insert(0, "001")
        self.ent_serie.grid(row=2, column=3, padx=5, sticky="w")

        # =====================================================================
        # 2. DADOS DO CLIENTE
        # =====================================================================
        frame_cliente = tk.LabelFrame(self.content_frame, text="Dados do Cliente / Destinatário", padx=10, pady=5,
                                      bg=COR_FRAME, fg=COR_TEXTO, font=("Arial", 10, "bold"))
        frame_cliente.pack(fill="x", padx=15, pady=5)

        self.criar_label(frame_cliente, "Nome / Razão Social:", 0, 0)
        self.ent_nome = self.criar_input(frame_cliente, width=50)
        self.ent_nome.grid(row=0, column=1, columnspan=3, sticky="w", padx=5)

        self.criar_label(frame_cliente, "CNPJ/CPF:", 0, 4)
        self.ent_doc = self.criar_input(frame_cliente, width=20)
        self.ent_doc.grid(row=0, column=5, padx=5)

        self.criar_label(frame_cliente, "Endereço:", 1, 0)
        self.ent_endereco = self.criar_input(frame_cliente, width=40)
        self.ent_endereco.grid(row=1, column=1, columnspan=3, sticky="w", padx=5)
        
        self.criar_label(frame_cliente, "Bairro:", 1, 4)
        self.ent_bairro = self.criar_input(frame_cliente, width=20)
        self.ent_bairro.grid(row=1, column=5, padx=5)

        self.criar_label(frame_cliente, "Município:", 2, 0)
        self.ent_municipio = self.criar_input(frame_cliente, width=25)
        self.ent_municipio.grid(row=2, column=1, padx=5, sticky="w")

        self.criar_label(frame_cliente, "UF:", 2, 2)
        self.ent_uf = self.criar_input(frame_cliente, width=5)
        self.ent_uf.grid(row=2, column=3, padx=5, sticky="w")

        self.criar_label(frame_cliente, "CEP:", 2, 4)
        self.ent_cep = self.criar_input(frame_cliente, width=15)
        self.ent_cep.grid(row=2, column=5, padx=5, sticky="w")

        self.criar_label(frame_cliente, "Telefone:", 3, 0)
        self.ent_telefone = self.criar_input(frame_cliente, width=25)
        self.ent_telefone.grid(row=3, column=1, padx=5, sticky="w")

        # =====================================================================
        # 3. TRANSPORTADOR / VOLUMES
        # =====================================================================
        frame_transp = tk.LabelFrame(self.content_frame, text="Transportador / Volumes Transportados", padx=10, pady=5,
                                     bg=COR_FRAME, fg=COR_TEXTO, font=("Arial", 10, "bold"))
        frame_transp.pack(fill="x", padx=15, pady=5)

        # Linha 1
        self.criar_label(frame_transp, "Nome Transp.:", 0, 0)
        self.ent_transp_nome = self.criar_input(frame_transp, width=35)
        self.ent_transp_nome.grid(row=0, column=1, columnspan=2, sticky="w", padx=5)

        self.criar_label(frame_transp, "Frete:", 0, 3)
        self.cb_frete = ttk.Combobox(frame_transp, values=["0 - Remetente (CIF)", "1 - Destinatário (FOB)", "9 - Sem Frete"], width=20)
        self.cb_frete.current(0)
        self.cb_frete.grid(row=0, column=4, padx=5)

        # Linha 2
        self.criar_label(frame_transp, "Placa Veículo:", 1, 0)
        self.ent_transp_placa = self.criar_input(frame_transp, width=15)
        self.ent_transp_placa.grid(row=1, column=1, padx=5, sticky="w")

        self.criar_label(frame_transp, "UF Veículo:", 1, 2)
        self.ent_transp_placa_uf = self.criar_input(frame_transp, width=5)
        self.ent_transp_placa_uf.grid(row=1, column=3, padx=5, sticky="w")

        self.criar_label(frame_transp, "CNPJ/CPF Transp:", 1, 4)
        self.ent_transp_cnpj = self.criar_input(frame_transp, width=20)
        self.ent_transp_cnpj.grid(row=1, column=5, padx=5, sticky="w")

        # Linha 3
        self.criar_label(frame_transp, "Endereço Transp:", 2, 0)
        self.ent_transp_end = self.criar_input(frame_transp, width=35)
        self.ent_transp_end.grid(row=2, column=1, columnspan=2, padx=5, sticky="w")
        
        self.criar_label(frame_transp, "Município/UF:", 2, 3)
        self.ent_transp_mun = self.criar_input(frame_transp, width=20)
        self.ent_transp_mun.grid(row=2, column=4, padx=5, sticky="w")

        # Linha 4 - Volumes
        self.criar_label(frame_transp, "Qtd Volumes:", 3, 0)
        self.ent_vol_qtd = self.criar_input(frame_transp, width=10)
        self.ent_vol_qtd.grid(row=3, column=1, padx=5, sticky="w")

        self.criar_label(frame_transp, "Espécie:", 3, 2)
        self.ent_vol_esp = self.criar_input(frame_transp, width=15)
        self.ent_vol_esp.grid(row=3, column=3, padx=5, sticky="w")

        self.criar_label(frame_transp, "Peso Bruto (Kg):", 3, 4)
        self.ent_peso_b = self.criar_input(frame_transp, width=10)
        self.ent_peso_b.grid(row=3, column=5, padx=5, sticky="w")

        # =====================================================================
        # 4. PRODUTOS
        # =====================================================================
        frame_prod = tk.LabelFrame(self.content_frame, text="Adicionar Itens", padx=10, pady=5,
                                   bg=COR_FRAME, fg=COR_TEXTO, font=("Arial", 10, "bold"))
        frame_prod.pack(fill="x", padx=15, pady=10)

        self.criar_label(frame_prod, "Descrição:", 0, 0)
        self.ent_prod_desc = self.criar_input(frame_prod, width=30)
        self.ent_prod_desc.grid(row=0, column=1, padx=5)

        self.criar_label(frame_prod, "Qtd:", 0, 2)
        self.ent_qtd = self.criar_input(frame_prod, width=5)
        self.ent_qtd.grid(row=0, column=3, padx=5)

        self.criar_label(frame_prod, "Valor Unit:", 0, 4)
        self.ent_valor = self.criar_input(frame_prod, width=10)
        self.ent_valor.grid(row=0, column=5, padx=5)

        btn_add = tk.Button(frame_prod, text="Adicionar", command=self.adicionar_item, 
                            bg=COR_BOTAO, fg=COR_BOTAO_TXT, font=("Arial", 9, "bold"))
        btn_add.grid(row=0, column=6, padx=10)

        self.tree = ttk.Treeview(self.content_frame, columns=("Desc", "Qtd", "Unit", "Total"), show="headings", height=6)
        self.tree.heading("Desc", text="Descrição")
        self.tree.heading("Qtd", text="Qtd")
        self.tree.heading("Unit", text="Valor Unit.")
        self.tree.heading("Total", text="Total Item")
        self.tree.column("Desc", width=300)
        self.tree.column("Qtd", width=50)
        self.tree.column("Unit", width=100)
        self.tree.column("Total", width=100)
        self.tree.pack(padx=15, pady=5, fill='x')

        # =====================================================================
        # 5. DADOS ADICIONAIS
        # =====================================================================
        frame_adic = tk.LabelFrame(self.content_frame, text="Dados Adicionais (Info. Complementar)", padx=10, pady=5,
                                   bg=COR_FRAME, fg=COR_TEXTO, font=("Arial", 10, "bold"))
        frame_adic.pack(fill="x", padx=15, pady=5)
        
        self.txt_obs = tk.Text(frame_adic, height=4, width=80, bg=COR_INPUT, font=("Arial", 9))
        self.txt_obs.pack(padx=5, pady=5, fill="x")
        self.txt_obs.insert(1.0, "Documento emitido por ME ou EPP optante pelo Simples Nacional.")

        # RODAPÉ
        frame_footer = tk.Frame(self.content_frame, bg=COR_FUNDO)
        frame_footer.pack(fill="x", padx=15, pady=15)
        
        self.lbl_total = tk.Label(frame_footer, text="Total: R$ 0.00", font=("Arial", 14, "bold"), bg=COR_FUNDO, fg="#333")
        self.lbl_total.pack(side="left")

        btn_gerar = tk.Button(frame_footer, text="GERAR NOTA FISCAL (PDF)", command=self.gerar_pdf, 
                              bg="#00C853", fg="white", font=("Arial", 11, "bold"), padx=20, pady=5)
        btn_gerar.pack(side="right")

    # --- Funções Auxiliares ---
    def criar_label(self, parent, texto, r, c):
        lbl = tk.Label(parent, text=texto, bg=COR_FRAME, fg="#555", font=("Arial", 9))
        lbl.grid(row=r, column=c, sticky="w", pady=2)
        return lbl

    def criar_input(self, parent, width):
        return tk.Entry(parent, width=width, bg=COR_INPUT, relief="solid", borderwidth=1)

    def adicionar_item(self):
        desc = self.ent_prod_desc.get()
        qtd = self.ent_qtd.get()
        valor = self.ent_valor.get()

        if not desc or not qtd or not valor:
            messagebox.showwarning("Atenção", "Preencha os campos do produto.")
            return

        try:
            qtd = int(qtd)
            valor = float(valor.replace(",", "."))
            total = qtd * valor
            
            self.carrinho.append({"desc": desc, "qtd": qtd, "unit": valor, "total": total})
            self.tree.insert("", "end", values=(desc, qtd, f"R$ {valor:.2f}", f"R$ {total:.2f}"))
            
            total_geral = sum(i['total'] for i in self.carrinho)
            self.lbl_total.config(text=f"Total: R$ {total_geral:.2f}")

            self.ent_prod_desc.delete(0, tk.END)
            self.ent_qtd.delete(0, tk.END)
            self.ent_valor.delete(0, tk.END)
            self.ent_prod_desc.focus()
        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos.")

    def desenhar_caixa(self, c, x, y, w, h, titulo, conteudo):
        c.setLineWidth(0.5)
        c.rect(x, y, w, h)
        c.setFont("Helvetica-Oblique", 5)
        c.drawString(x + 2, y + h - 6, titulo)
        c.setFont("Helvetica-Bold", 7)
        if len(conteudo) * 4 > w: 
            conteudo = conteudo[:int(w/4)] + "..."
        c.drawString(x + 5, y + 4, conteudo)

    def gerar_pdf(self):
        if not self.carrinho:
            messagebox.showwarning("Vazio", "Adicione itens antes.")
            return

        try: perc_imposto = float(self.ent_imposto_perc.get().replace(",", "."))
        except: perc_imposto = 0.0

        natureza = self.cb_natureza.get()
        tipo_mov = self.cb_tipo_mov.get()[0] # '0' ou '1'
        selecao_doc = self.cb_tipo_doc.get()
        observacoes = self.txt_obs.get("1.0", tk.END).strip()
        num_nota = self.ent_num_nf.get()
        serie_nota = self.ent_serie.get()
        
        # --- LÓGICA DINÂMICA DE TIPO DE DOCUMENTO ---
        # Define o Título Central e a Sigla do Canhoto baseada na seleção
        if "DANFE" in selecao_doc or "NF-e" in selecao_doc:
            titulo_central = "DANFE"
            subtitulo_central = "Documento Auxiliar da Nota Fiscal Eletrônica"
            sigla_doc = "NF-e"
        elif "NFS-e" in selecao_doc:
            titulo_central = "NFS-e"
            subtitulo_central = "Nota Fiscal de Serviço Eletrônica"
            sigla_doc = "NFS-e"
        elif "NFA-e" in selecao_doc:
            titulo_central = "NFA-e"
            subtitulo_central = "Nota Fiscal Avulsa Eletrônica"
            sigla_doc = "NFA-e"
        elif "NFC-e" in selecao_doc:
            titulo_central = "NFC-e"
            subtitulo_central = "Nota Fiscal ao Consumidor Eletrônica"
            sigla_doc = "NFC-e"
        elif "MDF-e" in selecao_doc:
            titulo_central = "MDF-e"
            subtitulo_central = "Manifesto Eletrônico de Documentos Fiscais"
            sigla_doc = "MDF-e"
        else:
            titulo_central = "DOCUMENTO FISCAL"
            subtitulo_central = selecao_doc
            sigla_doc = "DOC"

        # --- GERAR CHAVE ALEATÓRIA PARA CADA NOTA (NOVO) ---
        chave_acesso = "".join([str(random.randint(0, 9)) for _ in range(30)])
        chave_formatada = " ".join([chave_acesso[i:i+4] for i in range(0, 30, 4)])

        nome_arquivo = f"NF_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        c = canvas.Canvas(nome_arquivo, pagesize=A4)
        w, h = A4
        y = h - 30

        # --- CANHOTO DE RECEBIMENTO ---
        c.setLineWidth(0.5)
        c.rect(20, y-25, 550, 25)
        c.line(120, y, 120, y-25)
        c.line(450, y, 450, y-25)
        
        c.setFont("Helvetica-Oblique", 5)
        c.drawString(22, y-8, "DATA DO RECEBIMENTO")
        c.drawString(122, y-8, "IDENTIFICAÇÃO E ASSINATURA DO RECEBEDOR")
        
        # SIGLA DINÂMICA NO CANHOTO
        c.setFont("Helvetica-Bold", 8)
        c.drawString(455, y-15, sigla_doc)
        c.setFont("Helvetica", 6)
        c.drawString(455, y-22, f"Nº {num_nota}")
        
        c.setFont("Helvetica", 6)
        c.drawString(20, y-32, "RECEBEMOS DE AQUAVIDA - RESGATE & TRANSPORTE OS PRODUTOS CONSTANTES DA NOTA FISCAL INDICADA AO LADO")
        c.setDash(3, 3)
        c.line(20, y-35, 570, y-35)
        c.setDash(1, 0)
        
        y -= 50

        # --- CABEÇALHO PRINCIPAL (MEIO) ---
        # Coluna da Esquerda (Emitente)
        c.rect(20, y-75, 270, 75) 
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, y-15, "AQUAVIDA - RESGATE & TRANSPORTE")
        c.setFont("Helvetica", 8)
        c.drawString(30, y-30, "Rua David Capistrano, 137")
        c.drawString(30, y-42, "Boa Viagem - Ceará")
        c.drawString(30, y-54, "CNPJ: 00.000.000/0001-00")
        c.drawString(30, y-66, f"Natureza: {natureza[:30]}")

        # Coluna do Meio (TITULO DINÂMICO)
        c.rect(290, y-75, 80, 75)
        
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(330, y-12, titulo_central) # Usa a variável dinâmica
        c.setFont("Helvetica", 5)
        # Quebra subtítulo se for longo
        if len(subtitulo_central) > 25:
            part1 = subtitulo_central[:25]
            part2 = subtitulo_central[25:]
            c.drawCentredString(330, y-20, part1)
            c.drawCentredString(330, y-26, part2)
        else:
            c.drawCentredString(330, y-20, subtitulo_central)
        
        # Box Entrada/Saída
        c.rect(300, y-48, 20, 18)
        c.setFont("Helvetica", 5)
        c.drawString(322, y-38, "0 - ENTRADA")
        c.drawString(322, y-45, "1 - SAÍDA")
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(310, y-45, tipo_mov)
        
        # Numero Serie Folha
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(330, y-58, f"Nº {num_nota}")
        c.drawCentredString(330, y-65, f"SÉRIE {serie_nota}")
        c.setFont("Helvetica", 6)
        c.drawCentredString(330, y-72, "FOLHA 1/1")

        # Coluna da Direita (Cod Barras - NOVO)
        c.rect(370, y-75, 200, 75)
        c.setFont("Helvetica", 7)
        c.drawString(380, y-15, "Chave de Acesso")
        
        # --- DESENHA O CÓDIGO DE BARRAS REAL ---
        # barHeight ajusta a altura das barras
        # barWidth ajusta a largura (0.9 cabe bem nessa caixa)
        barcode = code128.Code128(chave_acesso, barHeight=18, barWidth=0.8)
        barcode.drawOn(c, 375, y-45) 
        
        # Escreve o número formatado embaixo
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(470, y-55, chave_formatada)
        
        c.setFont("Helvetica", 6)
        c.drawCentredString(470, y-68, "Consulta de autenticidade no portal nacional")

        y -= 85

        # --- DESTINATÁRIO ---
        c.setFont("Helvetica-Bold", 8)
        c.drawString(20, y, "DESTINATÁRIO / REMETENTE")
        y -= 10
        
        self.desenhar_caixa(c, 20, y-25, 350, 25, "NOME / RAZÃO SOCIAL", self.ent_nome.get())
        self.desenhar_caixa(c, 370, y-25, 120, 25, "CNPJ / CPF", self.ent_doc.get())
        self.desenhar_caixa(c, 490, y-25, 80, 25, "DATA EMISSÃO", datetime.now().strftime("%d/%m/%Y"))
        y -= 25
        self.desenhar_caixa(c, 20, y-25, 300, 25, "ENDEREÇO", self.ent_endereco.get())
        self.desenhar_caixa(c, 320, y-25, 150, 25, "BAIRRO / DISTRITO", self.ent_bairro.get())
        self.desenhar_caixa(c, 470, y-25, 100, 25, "CEP", self.ent_cep.get())
        y -= 25
        self.desenhar_caixa(c, 20, y-25, 250, 25, "MUNICÍPIO", self.ent_municipio.get())
        self.desenhar_caixa(c, 270, y-25, 50, 25, "UF", self.ent_uf.get())
        self.desenhar_caixa(c, 320, y-25, 250, 25, "FONE / FAX", self.ent_telefone.get())
        y -= 35

        # --- CÁLCULO DO IMPOSTO ---
        c.setFont("Helvetica-Bold", 8)
        c.drawString(20, y, "CÁLCULO DO IMPOSTO")
        y -= 10
        total_prod = sum(i['total'] for i in self.carrinho)
        valor_imposto = total_prod * (perc_imposto / 100)
        
        col_w = 550 / 5
        self.desenhar_caixa(c, 20, y-25, col_w, 25, "BASE DE CÁLCULO ICMS", f"{total_prod:.2f}")
        self.desenhar_caixa(c, 20+col_w, y-25, col_w, 25, f"VALOR DO ICMS ({int(perc_imposto)}%)", f"{valor_imposto:.2f}")
        self.desenhar_caixa(c, 20+col_w*2, y-25, col_w, 25, "BASE CÁLC. ST", "0,00")
        self.desenhar_caixa(c, 20+col_w*3, y-25, col_w, 25, "VALOR TOTAL PRODUTOS", f"{total_prod:.2f}")
        self.desenhar_caixa(c, 20+col_w*4, y-25, col_w, 25, "VALOR TOTAL NOTA", f"R$ {total_prod:.2f}")
        y -= 40

        # --- TRANSPORTADOR ---
        c.setFont("Helvetica-Bold", 8)
        c.drawString(20, y, "TRANSPORTADOR / VOLUMES TRANSPORTADOS")
        y -= 10
        
        self.desenhar_caixa(c, 20, y-25, 250, 25, "NOME / RAZÃO SOCIAL", self.ent_transp_nome.get())
        self.desenhar_caixa(c, 270, y-25, 100, 25, "FRETE POR CONTA", self.cb_frete.get()[:15])
        self.desenhar_caixa(c, 370, y-25, 80, 25, "PLACA VEÍCULO", self.ent_transp_placa.get())
        self.desenhar_caixa(c, 450, y-25, 30, 25, "UF", self.ent_transp_placa_uf.get())
        self.desenhar_caixa(c, 480, y-25, 90, 25, "CNPJ/CPF", self.ent_transp_cnpj.get())
        y -= 25
        
        self.desenhar_caixa(c, 20, y-25, 250, 25, "ENDEREÇO", self.ent_transp_end.get())
        self.desenhar_caixa(c, 270, y-25, 200, 25, "MUNICÍPIO", self.ent_transp_mun.get())
        self.desenhar_caixa(c, 470, y-25, 100, 25, "INSCRIÇÃO ESTADUAL", "")
        y -= 25
        
        self.desenhar_caixa(c, 20, y-25, 60, 25, "QUANTIDADE", self.ent_vol_qtd.get())
        self.desenhar_caixa(c, 80, y-25, 100, 25, "ESPÉCIE", self.ent_vol_esp.get())
        self.desenhar_caixa(c, 180, y-25, 100, 25, "MARCA", "AQUAVIDA")
        self.desenhar_caixa(c, 280, y-25, 100, 25, "NUMERAÇÃO", "")
        self.desenhar_caixa(c, 380, y-25, 95, 25, "PESO BRUTO", self.ent_peso_b.get())
        self.desenhar_caixa(c, 475, y-25, 95, 25, "PESO LÍQUIDO", self.ent_peso_b.get())
        y -= 40

        # --- PRODUTOS ---
        c.setFont("Helvetica-Bold", 8)
        c.drawString(20, y, "DADOS DO PRODUTO / SERVIÇO")
        y -= 15

        c.setFillColorRGB(0.9, 0.9, 0.9) 
        c.rect(20, y-15, 550, 15, fill=1)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(25, y-10, "CÓD")
        c.drawString(60, y-10, "DESCRIÇÃO")
        c.drawString(300, y-10, "UN")
        c.drawString(330, y-10, "QTD")
        c.drawString(380, y-10, "V. UNIT")
        c.drawString(450, y-10, "V. TOTAL")
        y -= 15

        c.setFont("Helvetica", 7)
        for i, item in enumerate(self.carrinho):
            if y < 130: 
                c.showPage()
                y = h - 50
            c.rect(20, y-15, 550, 15)
            c.drawString(25, y-10, f"{i+1:02d}")
            c.drawString(60, y-10, item['desc'])
            c.drawString(300, y-10, "UN")
            c.drawString(330, y-10, str(item['qtd']))
            c.drawString(380, y-10, f"{item['unit']:.2f}")
            c.drawString(450, y-10, f"{item['total']:.2f}")
            y -= 15
        
        # --- DADOS ADICIONAIS (RODAPÉ) ---
        if y > 160: y = 160 
        else: y -= 30

        c.setFont("Helvetica-Bold", 8)
        c.drawString(20, y, "DADOS ADICIONAIS")
        y -= 5
        
        c.rect(20, y-60, 350, 60)
        c.setFont("Helvetica-Oblique", 6)
        c.drawString(22, y-8, "INFORMAÇÕES COMPLEMENTARES")
        
        text_obj = c.beginText(25, y-20)
        text_obj.setFont("Helvetica", 7)
        for linha in observacoes.split('\n'):
            text_obj.textLine(linha)
        c.drawText(text_obj)
        
        c.rect(370, y-60, 200, 60)
        c.setFont("Helvetica-Oblique", 6)
        c.drawString(372, y-8, "RESERVADO AO FISCO")
        
        c.save()
        messagebox.showinfo("Sucesso", f"Nota gerada!\nArquivo: {nome_arquivo}")
        try: os.startfile(nome_arquivo)
        except: pass

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaVendasBarcos(root)
    root.mainloop()
