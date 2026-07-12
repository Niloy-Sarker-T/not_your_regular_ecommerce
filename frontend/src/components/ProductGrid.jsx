import ProductCard from "./ProductCard.jsx";

export default function ProductGrid({ products, emptyText = "No products found." }) {
  if (!products.length) {
    return <div className="rounded border border-dashed border-ink/20 bg-white p-8 text-center text-slate-500">{emptyText}</div>;
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
