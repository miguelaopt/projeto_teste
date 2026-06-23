import time
from typing import List, Dict

# 🚨 ISCO 1: "Mutable Default Argument" - O erro mais clássico de Python.
# A lista 'cart' vai ser partilhada entre todos os utilizadores que chamarem a função!
def add_to_cart(item_name: str, price: float, cart: List[Dict] = []):
    cart.append({"name": item_name, "price": price})
    return cart

def apply_discount(price: float, discount_percent: float) -> float:
    final_price = price - (price * (discount_percent / 100))
    # 🚨 ISCO 2: Lógica de negócio fraca. E se o desconto for 150%? O preço fica negativo e a loja perde dinheiro.
    return final_price

def process_checkout(cart_items: List[Dict]):
    # 🚨 ISCO 3: Falta de validação. E se a lista estiver vazia? Cobra 0€ e gera um recibo?
    total = sum(item["price"] for item in cart_items)
    
    # 🚨 ISCO 4: Código síncrono bloqueante (time.sleep).
    # Numa API FastAPI, isto bloqueia a thread inteira e derruba o servidor se houver muitos acessos.
    print("A processar pagamento via Stripe...")
    time.sleep(5) 
    
    return {"status": "success", "amount_charged": total}
    #cart system? 