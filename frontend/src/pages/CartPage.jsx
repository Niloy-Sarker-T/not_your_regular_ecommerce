import { Minus, Plus, Trash2 } from "lucide-react";
import { checkout } from "../api.js";
import { useCart } from "../state/CartContext.jsx";

export default function CartPage() {
  const { cart, setCart, update, remove } = useCart();

  async function handleCheckout() {
    const result = await checkout();
    setCart({ items: [], total: 0, item_count: 0 });
    alert(result.message);
  }

  return (
    <main className="mx-auto max-w-5xl px-4 py-8">
      <div className="mb-6 flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-black">Cart</h1>
          <p className="text-slate-500">{cart.item_count} items ready for mock checkout</p>
        </div>
        <p className="text-2xl font-black">${cart.total.toFixed(2)}</p>
      </div>

      <div className="space-y-3">
        {cart.items.map((item) => (
          <div className="card grid gap-4 p-4 sm:grid-cols-[88px_1fr_auto]" key={item.id}>
            <img src={item.product.image_url || "https://placehold.co/200x200?text=Product"} alt={item.product.name} className="h-20 w-20 object-contain" />
            <div>
              <p className="font-bold">{item.product.name}</p>
              <p className="text-sm text-slate-500">{item.product.brand}</p>
              <p className="mt-2 font-bold">${item.line_total.toFixed(2)}</p>
            </div>
            <div className="flex items-center gap-2">
              <button className="btn btn-ghost" onClick={() => update(item.product.id, item.quantity - 1)} title="Decrease">
                <Minus size={16} />
              </button>
              <span className="grid h-10 w-10 place-items-center rounded border border-ink/10 font-bold">{item.quantity}</span>
              <button className="btn btn-ghost" onClick={() => update(item.product.id, item.quantity + 1)} title="Increase">
                <Plus size={16} />
              </button>
              <button className="btn btn-ghost" onClick={() => remove(item.product.id)} title="Remove">
                <Trash2 size={16} />
              </button>
            </div>
          </div>
        ))}
      </div>

      {!cart.items.length && <div className="card p-8 text-center text-slate-500">Your cart is empty.</div>}

      <div className="mt-6 flex justify-end">
        <button className="btn btn-primary" disabled={!cart.items.length} onClick={handleCheckout}>
          Mock Checkout
        </button>
      </div>
    </main>
  );
}
