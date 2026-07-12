import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
});

export async function fetchProducts(params = {}) {
  const { data } = await api.get("/api/products", { params });
  return data;
}

export async function fetchProduct(id) {
  const { data } = await api.get(`/api/products/${id}`);
  return data;
}

export async function fetchCart() {
  const { data } = await api.get("/api/cart");
  return data;
}

export async function addToCart(productId, quantity = 1) {
  const { data } = await api.post("/api/cart", { product_id: productId, quantity });
  return data;
}

export async function updateCart(productId, quantity) {
  const { data } = await api.patch(`/api/cart/${productId}`, { quantity });
  return data;
}

export async function removeFromCart(productId) {
  const { data } = await api.delete(`/api/cart/${productId}`);
  return data;
}

export async function checkout() {
  const { data } = await api.post("/api/cart/checkout");
  return data;
}

export async function imageSearch(file) {
  const form = new FormData();
  form.append("file", file);
  const { data } = await api.post("/api/ai/image-search", form);
  return data;
}

export async function textCommand(text) {
  const { data } = await api.post("/api/ai/text-command", { text });
  return data;
}

export async function voiceCommand(blob, fallbackText = "") {
  const form = new FormData();
  if (blob) form.append("file", blob, "voice.webm");
  if (fallbackText) form.append("text", fallbackText);
  const { data } = await api.post("/api/ai/voice-command", form);
  return data;
}
