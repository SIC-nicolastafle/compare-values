# 🔍 CSV Value Comparator - Comparador de Valores Simples

## 📋 O Que Faz

Compara os **VALORES** das colunas comuns entre duas tabelas CSV e lista apenas os registos que têm diferenças.

**Conceito:** A primeira tabela é sempre considerada a **ORIGINAL (correta)**, e comparamos a segunda com ela.

## 🚀 Como Usar

### Sintaxe Básica

```bash
python3 compare_values.py <original.csv> <nova.csv> <coluna_chave> [output.csv]
```

### Parâmetros

1. **original.csv** - Ficheiro original (considerado correto)
2. **nova.csv** - Ficheiro nova (a validar contra a original)
3. **coluna_chave** - Coluna usada para fazer match entre registos (ex: Nome, id, Código)
4. **output.csv** (opcional) - Nome do ficheiro de saída (default: diferencas_[timestamp].csv)

## 📊 O Que Recebes

### Console (Terminal)
O script mostra:
- ✅ Estatísticas (quantos registos, quantas colunas comuns)
- 📝 Lista das primeiras 10 diferenças encontradas
- 🔴 Total de registos com diferenças

### Ficheiro CSV
Um ficheiro com estrutura assim:

```csv
Nome,Custo_ORIGINAL,Custo_NOVA,Custo_DIFERENTE,Preco_ORIGINAL,Preco_NOVA,Preco_DIFERENTE
Produto B,20.00,22.00,SIM,25.00,25.00,
Produto C,15.75,15.75,,20.00,22.00,SIM
```

**Explicação:**
- Para cada coluna comparada, tens 3 colunas no output:
  - `[COLUNA]_ORIGINAL` - Valor correto (da tabela original)
  - `[COLUNA]_NOVA` - Valor atual (da tabela nova)
  - `[COLUNA]_DIFERENTE` - "SIM" se os valores são diferentes

## ⚙️ Como Funciona Internamente

1. **Carrega ambos os ficheiros**
2. **Identifica colunas comuns** (que existem em ambos)
3. **Para cada registo:**
   - Faz match usando a coluna chave (ex: Nome)
   - Compara VALORES de todas as colunas comuns
   - Se encontrar diferença, adiciona à lista
4. **Gera ficheiro** apenas com registos que têm diferenças

## ⚠️ Notas Importantes

- **Só compara registos que existem em AMBAS as tabelas**
  - Se um produto existe só na original ou só na nova, não aparece no resultado

- **A coluna chave deve ser única**
  - Se tiver duplicados, só o primeiro será comparado

- **Comparação case-insensitive e sem espaços**
  - "10.50" == "10.5" (são considerados diferentes por causa do trailing)
  - " Texto " == "Texto" (espaços removidos)

- **Colunas com nomes diferentes não são comparadas**
  - Se uma tabela tem "Custo" e outra "standard_price", não serão comparadas
  - Só compara colunas com o MESMO nome
