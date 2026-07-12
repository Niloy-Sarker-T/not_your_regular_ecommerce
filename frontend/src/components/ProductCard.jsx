import { Link } from "react-router-dom";
import { Plus } from "lucide-react";
import { useCart } from "../state/CartContext.jsx";

export default function ProductCard({ product }) {
  const { add } = useCart();

  return (
    <article className="card flex h-full flex-col overflow-hidden">
      <Link to={`/products/${product.id}`} className="block bg-white">
        <div className="aspect-square w-full overflow-hidden bg-slate-100">
          <img
            src={product.image_url || "https://placehold.co/600x600?text=Product"}
            alt={product.name}
            className="h-full w-full object-contain p-4"
            loading="lazy"
          />
        </div>
      </Link>
      <div className="flex flex-1 flex-col gap-3 p-4">
        <div>
          <p className="text-xs font-bold uppercase tracking-wide text-leaf">{product.brand}</p>
          <Link to={`/products/${product.id}`} className="mt-1 line-clamp-2 min-h-12 font-semibold hover:text-leaf">
            {product.name}
          </Link>
          <p className="mt-1 text-sm text-slate-500">{product.category}</p>
        </div>
        <div className="mt-auto flex items-center justify-between gap-3">
          <div>
            <p className="text-lg font-bold">${product.price.toFixed(2)}</p>
            <p className="text-xs text-slate-500">{product.stock} in stock</p>
          </div>
          <button className="btn btn-primary" onClick={() => add(product.id, 1)} title="Add to cart">
            <Plus size={18} />
          </button>
        </div>
      </div>
    </article>
  );
}
