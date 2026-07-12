import { useEffect, useState } from "react";
import { Camera, Search } from "lucide-react";
import { fetchProducts, imageSearch } from "../api.js";
import ProductGrid from "../components/ProductGrid.jsx";

const categories = ["All", "Personal Care", "Snacks", "Beverages", "Biscuits", "Noodles", "Dairy", "Cooking Oil"];

export default function HomePage() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("All");
  const [products, setProducts] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [imageStatus, setImageStatus] = useState("");

  async function loadProducts(nextQuery = query, nextCategory = category) {
    setLoading(true);
    const params = { q: nextQuery || undefined, category: nextCategory === "All" ? undefined : nextCategory, limit: 48 };
    const data = await fetchProducts(params);
    setProducts(data.items);
    setTotal(data.total);
    setLoading(false);
  }

  useEffect(() => {
    loadProducts();
  }, []);

  async function submitSearch(event) {
    event.preventDefault();
    await loadProducts();
  }

  async function handleImage(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    setImageStatus("Identifying product from image...");
    const data = await imageSearch(file);
    setProducts(data.products);
    setTotal(data.products.length);
    setImageStatus(`Image search identified: ${data.identified_product}`);
  }

  return (
    <main>
      <section className="bg-white">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 py-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
          <div>
            <h1 className="max-w-3xl text-4xl font-black leading-tight text-ink md:text-5xl">Shop groceries with image and voice AI</h1>
            <p className="mt-4 max-w-2xl text-lg text-slate-600">
              Browse a local SQLite catalog, upload a product image, or ask the assistant to update your cart.
            </p>
            <form onSubmit={submitSearch} className="mt-6 flex max-w-2xl gap-2">
              <input className="input" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search shampoo, biscuits, cola..." />
              <button className="btn btn-primary" type="submit">
                <Search size={18} />
                Search
              </button>
            </form>
          </div>
          <div className="rounded-lg border border-ink/10 bg-mist p-5">
            <label className="flex min-h-52 cursor-pointer flex-col items-center justify-center rounded-md border-2 border-dashed border-leaf/40 bg-white p-6 text-center hover:border-leaf">
              <Camera size={34} className="text-leaf" />
              <span className="mt-3 font-bold">Upload a product image</span>
              <span className="mt-1 text-sm text-slate-500">Gemini Vision identifies it, then the backend searches SQLite.</span>
              <input className="sr-only" type="file" accept="image/*" onChange={handleImage} />
            </label>
            {imageStatus && <p className="mt-3 text-sm font-medium text-leaf">{imageStatus}</p>}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-6">
        <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap gap-2">
            {categories.map((item) => (
              <button
                key={item}
                className={`btn ${category === item ? "btn-primary" : "btn-ghost"}`}
                onClick={() => {
                  setCategory(item);
                  loadProducts(query, item);
                }}
              >
                {item}
              </button>
            ))}
          </div>
          <p className="text-sm text-slate-500">{loading ? "Loading..." : `${total} products`}</p>
        </div>
        <ProductGrid products={products} />
      </section>
    </main>
  );
}
