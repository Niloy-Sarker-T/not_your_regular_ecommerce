import React from "react";
import { Link, NavLink, Route, Routes } from "react-router-dom";
import { ShoppingCart, Sparkles, Store } from "lucide-react";
import CartPage from "./pages/CartPage.jsx";
import HomePage from "./pages/HomePage.jsx";
import ProductDetailPage from "./pages/ProductDetailPage.jsx";
import VoicePage from "./pages/VoicePage.jsx";
import { CartProvider, useCart } from "./state/CartContext.jsx";

function Shell() {
  const { cart } = useCart();

  return (
    <div className="min-h-screen bg-mist text-ink">
      <header className="sticky top-0 z-30 border-b border-ink/10 bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
          <Link to="/" className="flex items-center gap-2 text-lg font-semibold">
            <span className="grid h-9 w-9 place-items-center rounded bg-leaf text-white">
              <Store size={20} />
            </span>
            Smart Grocery AI
          </Link>
          <nav className="flex items-center gap-2 text-sm font-medium">
            <NavLink className="nav-link" to="/">
              Shop
            </NavLink>
            <NavLink className="nav-link" to="/assistant">
              <Sparkles size={16} />
              Assistant
            </NavLink>
            <NavLink className="nav-link" to="/cart">
              <ShoppingCart size={16} />
              Cart {cart.item_count ? `(${cart.item_count})` : ""}
            </NavLink>
          </nav>
        </div>
      </header>

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/products/:id" element={<ProductDetailPage />} />
        <Route path="/assistant" element={<VoicePage />} />
        <Route path="/cart" element={<CartPage />} />
      </Routes>
    </div>
  );
}

export default function App() {
  return (
    <CartProvider>
      <Shell />
    </CartProvider>
  );
}
