"""
Implementasi sederhana algoritma Apriori untuk Market Basket Analysis
"""
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd

def run_apriori(transactions, min_support=0.01, min_confidence=0.3):
    """
    Menjalankan algoritma Apriori untuk Market Basket Analysis
    
    Args:
        transactions: List of transactions [[item1, item2], [item3, item4], ...]
        min_support: Minimum support threshold (default 0.01)
        min_confidence: Minimum confidence threshold (default 0.3)
    
    Returns:
        DataFrame berisi association rules dengan kolom:
        - antecedents: produk premise
        - consequents: produk conclusion
        - support: nilai support
        - confidence: nilai confidence
        - lift: nilai lift ratio
    """
    if not transactions or len(transactions) == 0:
        return pd.DataFrame()
    
    # Step 1: Encode transactions ke format binary matrix
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    
    # Step 2: Generate frequent itemsets menggunakan Apriori
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    
    if frequent_itemsets.empty:
        return pd.DataFrame()
    
    # Step 3: Generate association rules
    rules = association_rules(
        frequent_itemsets, 
        metric="confidence", 
        min_threshold=min_confidence
    )
    
    if rules.empty:
        return pd.DataFrame()
    
    # Step 4: Filter rules dengan lift > 1 (positive association)
    rules = rules[rules['lift'] > 1.0]
    
    # Step 5: Sort by confidence descending
    rules = rules.sort_values('confidence', ascending=False)
    
    # Step 6: Select only required columns
    result = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].copy()
    
    return result

def format_itemset(itemset):
    """
    Format frozenset to readable string
    
    Args:
        itemset: frozenset of items
    
    Returns:
        Comma-separated string
    """
    return ', '.join(list(itemset))
