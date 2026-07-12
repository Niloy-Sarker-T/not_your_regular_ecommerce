import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, Plus } from "lucide-react";
import { fetchProduct } from "../api.js";
import { useCart } from "../state/CartContext.jsx";

export default function ProductDetailPage() {
  const { id } = useParams();
  const { add } = useCart();
  const [product, setProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    fetchProduct(id).then(setProduct);
  }, [id]);

  if (!product) return <main className="mx-auto max-w-7xl px-4 py-10">Loading product...</main>;

  return (
    <main className="mx-auto max-w-7xl px-4 py-8">
      <Link className="mb-5 inline-flex items-center gap-2 text-sm font-bold text-leaf" to="/">
        <ArrowLeft size={16} />
        Back to shop
      </Link>
      <section className="grid gap-8 lg:grid-cols-2">
        <div className="rounded-lg bg-white p-6">
          <img src={product.image_url || "https://placehold.co/700x700?text=Product"} alt={product.name} className="mx-auto h-[420px] max-w-full object-contain" />
        </div>
        <div className="py-2">
          <p className="text-sm font-black uppercase tracking-wide text-leaf">{product.brand}</p>
          <h1 className="mt-2 text-4xl font-black">{product.name}</h1>
          <p className="mt-3 text-slate-600">{product.description}</p>
          <div className="mt-6 flex items-end justify-between border-y border-ink/10 py-5">
            <div>
              <p className="text-3xl font-black">${product.price.toFixed(2)}</p>
              <p className="text-sm text-slate-500">{product.stock} available</p>
            </div>
            <span className="rounded bg-citrus/25 px-3 py-1 text-sm font-bold">{product.category}</span>
          </div>
          <div className="mt-6 flex max-w-sm gap-3">
            <input className="input max-w-24" type="number" min="1" max="99" value={quantity} onChange={(event) => setQuantity(Number(event.target.value))} />
            <button className="btn btn-primary flex-1" onClick={() => add(product.id, quantity)}>
              <Plus size={18} />
              Add to Cart
            </button>
          </div>
        </div>
      </section>
    </main>
  );
}
