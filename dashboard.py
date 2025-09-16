
import pandas as pd
import matplotlib.pyplot as plt
import os

def validate(df):
    errors = []
    for idx,row in df.iterrows():
        if pd.isna(row['user']):
            errors.append((row['id'], 'Missing user'))
        try:
            amt = float(row['amount'])
            if amt < 0:
                errors.append((row['id'], 'Negative amount'))
        except:
            errors.append((row['id'], 'Invalid amount'))
    return errors

def generate_reports():
    df = pd.read_csv('transactions.csv')
    errors = validate(df)
    print("Validation Errors:", errors)
    # Clean data
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna(subset=['user','amount'])
    df = df[df['amount'] >= 0]
    # Summary
    summary = df.groupby('user')['amount'].sum().reset_index()
    os.makedirs('results', exist_ok=True)
    summary.to_csv('results/summary.csv', index=False)
    print("Summary report saved at results/summary.csv")
    # Visualization
    plt.bar(summary['user'], summary['amount'])
    plt.xlabel('User')
    plt.ylabel('Total Amount')
    plt.title('Transaction Summary')
    plt.savefig('results/summary.png')
    print("Visualization saved at results/summary.png")

if __name__ == '__main__':
    generate_reports()
