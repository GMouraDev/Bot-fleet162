# 🚛 Bot Fleet162 - Exportador Automático de Dados

> **Automatize a exportação de notificações e multas do sistema Frota162 com scripts Python inteligentes e seguros.**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Produção-brightgreen.svg)]()

---

## 📖 Sobre o Projeto

O **Bot Fleet162** é uma solução de automação que simplifica a exportação e consolidação de dados do sistema de gestão de frota. Ele permite:

- 🔐 **Login automático** no sistema Frota162
- 📊 **Exportação automática** de notificações e multas
- 🔄 **Consolidação inteligente** de dados (sem duplicatas)
- 💾 **Armazenamento organizado** em arquivos Excel
- 🛡️ **Segurança** com credenciais em variáveis de ambiente

---

## 🚀 Começando Rápido

### Pré-requisitos
- **Python 3.7+** instalado
- **Acesso ao sistema Frota162**
- **Credenciais válidas** (usuário e senha)

### Instalação em 3 Passos

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd Bot-fleet162

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure suas credenciais
# Edite o arquivo config.env com seu usuário e senha
```

---

## ⚙️ Configuração

### 1. Arquivo de Configuração

Crie/edite o arquivo `config.env` na raiz do projeto:

```env
# Suas credenciais do Frota162
FROTA162_USERNAME=seu_usuario_aqui
FROTA162_PASSWORD=sua_senha_aqui

# URLs do sistema (não altere)
FROTA162_LOGIN_URL=https://sistema.frota162.com.br/login
FROTA162_NOTIFICACOES_EXPORT_URL=https://sistema.frota162.com.br/notificacoes/export?trashed=0&order_by=indication_limit_date,asc
FROTA162_MULTAS_EXPORT_URL=https://sistema.frota162.com.br/multas/export?paid=all&trashed=0&order_by=due_date,desc
```

### 2. Estrutura de Pastas

```
Bot-fleet162/
├── 📁 bot/                    # Scripts principais
│   ├── 📄 ExportMulta.py     # Exporta multas
│   └── 📄 ExportNotificação.py # Exporta notificações
├── 📁 Resources/              # Pasta criada automaticamente
│   ├── 📊 Multas162.xlsx     # Dados consolidados de multas
│   └── 📊 Notificacao162.xlsx # Dados consolidados de notificações
├── ⚙️ config.env             # Suas credenciais
├── 📋 requirements.txt        # Dependências Python
└── 📖 README.md              # Este arquivo
```

---

## 🎯 Como Usar

### Exportar Multas

```bash
python bot/ExportMulta.py
```

**O que acontece:**
1. 🔐 Faz login automático no sistema
2. 📥 Baixa dados de multas
3. 🔄 Combina com dados existentes (se houver)
4. 🗑️ Remove duplicatas baseado no campo "AIT"
5. 💾 Salva arquivo consolidado em `Resources/Multas162.xlsx`

### Exportar Notificações

```bash
python bot/ExportNotificação.py
```

**O que acontece:**
1. 🔐 Faz login automático no sistema
2. 📥 Baixa dados de notificações
3. 🔄 Combina com dados existentes (se houver)
4. 🗑️ Remove duplicatas baseado no campo "AIT"
5. 💾 Salva arquivo consolidado em `Resources/Notificacao162.xlsx`

---

## ✨ Funcionalidades Principais

### 🔒 Segurança
- **Credenciais protegidas** em arquivo de configuração
- **Sessões HTTP seguras** com cookies automáticos
- **Token CSRF** capturado automaticamente

### 🧠 Inteligência
- **Deduplicação automática** baseada no campo "AIT"
- **Consolidação inteligente** de dados históricos
- **Validação de dados** antes do processamento

### 🚀 Performance
- **Processamento em memória** (sem arquivos temporários)
- **Barra de progresso visual** com TQDM
- **Feedback em tempo real** de cada etapa

### 🛡️ Robustez
- **Tratamento de erros** com mensagens claras
- **Criação automática** de pastas necessárias
- **Validação de permissões** e conectividade

---

## 📊 Exemplo de Saída

```
🚀 Iniciando processo de exportação de multas...
📁 Criando pasta Resources...
✅ Pasta Resources criada com sucesso!
🔐 Acessando página de login...
✅ Token CSRF capturado com sucesso!
🔐 Realizando login...
✅ Login realizado com sucesso!
📥 Exportando dados de multas...
✅ Arquivo de exportação baixado com sucesso!
🔄 Processando dados...
████████████████████████████████████████ 100%
✅ Processo concluído! Novas multas importadas: 15
📊 Total de registros únicos: 1,247
```

---

## 🐛 Solução de Problemas

### Erros Comuns e Soluções

| ❌ Erro | 🔍 Causa | ✅ Solução |
|---------|-----------|------------|
| `Credenciais não encontradas` | Arquivo `config.env` não existe ou está vazio | Verifique se o arquivo existe e tem as credenciais corretas |
| `Token CSRF não encontrado` | Sistema Frota162 com problemas ou mudança na estrutura | Verifique se o sistema está funcionando |
| `Login falhou` | Usuário ou senha incorretos | Verifique as credenciais no `config.env` |
| `Coluna 'AIT' não encontrada` | Formato de exportação mudou | Verifique se o sistema alterou a estrutura dos dados |
| `Pasta Resources não pode ser criada` | Permissões insuficientes | Execute como administrador ou verifique permissões |

### Logs de Debug

Para mais detalhes sobre erros, verifique:
- **Status HTTP** das respostas
- **Conteúdo das páginas** de erro
- **Permissões de arquivo** na pasta do projeto

---

## 🔧 Dependências

| Biblioteca | Versão | Propósito |
|------------|--------|-----------|
| `requests` | 2.31.0 | Requisições HTTP e sessões |
| `pandas` | 2.1.4 | Manipulação de dados Excel |
| `beautifulsoup4` | 4.12.2 | Parsing HTML para token CSRF |
| `openpyxl` | 3.1.2 | Leitura/escrita de arquivos Excel |
| `python-dotenv` | 1.0.0 | Carregamento de variáveis de ambiente |
| `tqdm` | 4.66.1 | Barras de progresso visuais |

---

## 🚧 Limitações Atuais

- **Execução manual** (não automatizada)
- **Um sistema por vez** (Frota162)
- **Formato fixo** de exportação (Excel)
- **Campo único** para deduplicação (AIT)

---

## 🚀 Roadmap

### Próximas Versões
- [ ] **Agendamento automático** de execução
- [ ] **Interface gráfica** simples (GUI)
- [ ] **Suporte a múltiplos sistemas** de frota
- [ ] **Notificações** por email/telegram
- [ ] **Dashboard web** para visualização
- [ ] **API REST** para integração

### Melhorias Técnicas
- [ ] **Refatoração** para classes (eliminar duplicação)
- [ ] **Testes automatizados** (unitários e integração)
- [ ] **Logging estruturado** com arquivos de log
- [ ] **Configuração via YAML/JSON**
- [ ] **Docker** para fácil deploy

---

## 🤝 Contribuindo

### Como Contribuir
1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Padrões de Código
- **Python PEP 8** para estilo
- **Docstrings** para funções
- **Type hints** quando possível
- **Tratamento de erros** robusto
---

## 🙏 Agradecimentos

- **Equipe Frota162** pelo sistema
- **Comunidade Python** pelas bibliotecas
- **Contribuidores** do projeto

---

<div align="center">

**⭐ Se este projeto te ajudou, considere dar uma estrela! ⭐**

*Feito com ❤️ para automatizar tarefas repetitivas*

</div>
