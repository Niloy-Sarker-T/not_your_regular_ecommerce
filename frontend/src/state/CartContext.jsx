import { createContext, useContext, useEffect, useMemo, useState } from "react";
import * as api from "../api.js";

const CartContext = createContext(null);

const emptyCart = { items: [], total: 0, item_count: 0 };

export function CartProvider({ children }) {
  const [cart, setCart] = useState(emptyCart);

  async function refreshCart() {
    try {
      setCart(await api.fetchCart());
    } catch {
      setCart(emptyCart);
    }
  }

  useEffect(() => {
    refreshCart();
  }, []);

  const value = useMemo(
    () => ({
      cart,
      setCart,
      refreshCart,
      add: async (productId, quantity = 1) => setCart(await api.addToCart(productId, quantity)),
      update: async (productId, quantity) => setCart(await api.updateCart(productId, quantity)),
      remove: async (productId) => setCart(await api.removeFromCart(productId)),
    }),
    [cart]
  );

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  return useContext(CartContext);
}
