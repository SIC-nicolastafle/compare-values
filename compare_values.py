#!/usr/bin/env python3
"""
CSV Value Comparator - Compara VALORES de colunas comuns entre duas tabelas
Usa a primeira tabela como ORIGINAL (a correta)
"""

import csv
import sys
import os
from datetime import datetime


def normalize_value(value):
    """Normaliza valor para comparação"""
    if value is None or value == "":
        return ""
    return str(value).strip()


def load_csv(filename, key_column):
    """Carrega CSV usando coluna como chave"""
    records = {}

    if not os.path.exists(filename):
        print(f"❌ ERRO: Ficheiro '{filename}' não encontrado!")
        return None, None

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames

            if not headers:
                print(f"❌ ERRO: Ficheiro vazio!")
                return None, None

            if key_column not in headers:
                print(f"❌ ERRO: Coluna '{key_column}' não existe!")
                print(f"   Colunas disponíveis: {', '.join(headers)}")
                return None, None

            for row in reader:
                key = normalize_value(row[key_column])
                if key:
                    records[key] = row

        return records, headers

    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        return None, None


def find_common_columns(headers1, headers2, key_column):
    """Encontra colunas comuns (exceto a chave)"""
    common = set(headers1) & set(headers2)
    common.discard(key_column)  # Remover a coluna chave
    return sorted(list(common))


def compare_values(original_records, new_records, common_columns, key_column):
    """Compara valores das colunas comuns"""
    differences = []

    for key in original_records:
        if key not in new_records:
            continue  # Não existe na nova, não comparamos valores

        original_row = original_records[key]
        new_row = new_records[key]

        row_differences = {}
        has_difference = False

        for column in common_columns:
            original_val = normalize_value(original_row.get(column, ""))
            new_val = normalize_value(new_row.get(column, ""))

            if original_val != new_val:
                has_difference = True
                row_differences[column] = {
                    'original': original_val,
                    'nova': new_val
                }

        if has_difference:
            differences.append({
                'key': key,
                'key_column': key_column,
                'differences': row_differences
            })

    return differences


def main():
    print("\n" + "=" * 80)
    print("CSV VALUE COMPARATOR - COMPARAR VALORES DE COLUNAS")
    print("=" * 80 + "\n")

    # Verificar argumentos
    if len(sys.argv) < 4:
        print("COMO USAR:")
        print("-" * 80)
        print(f"  python {sys.argv[0]} <original.csv> <nova.csv> <coluna_chave> [output.csv]")
        print("\nEXEMPLOS:")
        print(f"  python {sys.argv[0]} produtos_prod.csv produtos_nova.csv Nome")
        print(f"  python {sys.argv[0]} dados1.csv dados2.csv id diferencas.csv")
        print("\nNOTA:")
        print("  - A primeira tabela é considerada a ORIGINAL (correta)")
        print("  - Compara apenas colunas que existem em AMBOS os ficheiros")
        print("  - A coluna_chave é usada para fazer o match entre registos")
        print("=" * 80)
        sys.exit(1)

    file_original = sys.argv[1]
    file_nova = sys.argv[2]
    key_column = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) > 4 else None

    print(f"📂 Ficheiro ORIGINAL (correto): {file_original}")
    print(f"📂 Ficheiro NOVA (a validar): {file_nova}")
    print(f"🔑 Coluna de comparação: {key_column}\n")

    # Carregar dados
    print("📖 A carregar ficheiro original...")
    original_records, headers_original = load_csv(file_original, key_column)
    if original_records is None:
        sys.exit(1)

    print("📖 A carregar ficheiro nova...")
    new_records, headers_nova = load_csv(file_nova, key_column)
    if new_records is None:
        sys.exit(1)

    print("\n✅ Ficheiros carregados!\n")

    # Encontrar colunas comuns
    common_columns = find_common_columns(headers_original, headers_nova, key_column)

    print(f"📊 ESTATÍSTICAS:")
    print("-" * 80)
    print(f"   Registos na original: {len(original_records)}")
    print(f"   Registos na nova: {len(new_records)}")
    print(f"   Colunas comuns a comparar: {len(common_columns)}")

    if common_columns:
        print(f"\n   Colunas: {', '.join(common_columns)}")
    else:
        print("\n⚠️  AVISO: Nenhuma coluna comum encontrada (além da chave)!")
        sys.exit(0)

    # Comparar valores
    print("\n🔍 A comparar valores...")
    differences = compare_values(original_records, new_records, common_columns, key_column)

    # Resultados
    print(f"\n📊 RESULTADOS:")
    print("-" * 80)
    print(f"   🔴 Registos com diferenças: {len(differences)}")
    print(f"   ✅ Registos iguais: {len(original_records) - len(differences)}")

    if not differences:
        print("\n✅ Parabéns! Todos os registos são iguais!")
        sys.exit(0)

    # Mostrar exemplos
    print(f"\n📝 DIFERENÇAS ENCONTRADAS (primeiros 10):")
    print("-" * 80)

    for i, diff in enumerate(differences[:10], 1):
        print(f"\n{i}. {key_column}: {diff['key']}")
        for col, values in diff['differences'].items():
            print(f"   {col}:")
            print(f"      Original: {values['original'] if values['original'] else '(vazio)'}")
            print(f"      Nova:     {values['nova'] if values['nova'] else '(vazio)'}")

    if len(differences) > 10:
        print(f"\n   ... e mais {len(differences) - 10} registos com diferenças")

    # Guardar resultados
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"diferencas_{timestamp}.csv"

    print(f"\n💾 A guardar resultados em: {output_file}")

    # Criar CSV com diferenças
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        # Headers: chave + todas as colunas com sufixo _original e _nova
        fieldnames = [key_column]
        for col in common_columns:
            fieldnames.append(f"{col}_ORIGINAL")
            fieldnames.append(f"{col}_NOVA")
            fieldnames.append(f"{col}_DIFERENTE")

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for diff in differences:
            key = diff['key']
            original_row = original_records[key]
            new_row = new_records[key]

            row_data = {key_column: key}

            for col in common_columns:
                original_val = normalize_value(original_row.get(col, ""))
                new_val = normalize_value(new_row.get(col, ""))
                is_different = original_val != new_val

                row_data[f"{col}_ORIGINAL"] = original_val
                row_data[f"{col}_NOVA"] = new_val
                row_data[f"{col}_DIFERENTE"] = "SIM" if is_different else ""

            writer.writerow(row_data)

    print(f"\n✅ CONCLUÍDO!")
    print("-" * 80)
    print(f"📁 Ficheiro criado: {output_file}")
    print(f"\nO ficheiro contém {len(differences)} registos com diferenças.")
    print("Para cada coluna, tens 3 colunas no output:")
    print("  - [COLUNA]_ORIGINAL: Valor correto (da original)")
    print("  - [COLUNA]_NOVA: Valor atual (da nova)")
    print("  - [COLUNA]_DIFERENTE: 'SIM' se os valores diferem")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()