import { useRef, useState } from "react";
import { Mic, Send, Square } from "lucide-react";
import { textCommand, voiceCommand } from "../api.js";
import ProductGrid from "../components/ProductGrid.jsx";
import { useCart } from "../state/CartContext.jsx";

export default function VoicePage() {
  const { setCart } = useCart();
  const recorderRef = useRef(null);
  const chunksRef = useRef([]);
  const [recording, setRecording] = useState(false);
  const [text, setText] = useState("Add two Dove shampoos to my cart");
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);

  async function runTextCommand(event) {
    event.preventDefault();
    setBusy(true);
    const data = await textCommand(text);
    setResult(data);
    if (data.cart) setCart(data.cart);
    setBusy(false);
  }

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    chunksRef.current = [];
    const recorder = new MediaRecorder(stream);
    recorderRef.current = recorder;
    recorder.ondataavailable = (event) => chunksRef.current.push(event.data);
    recorder.onstop = async () => {
      setBusy(true);
      const blob = new Blob(chunksRef.current, { type: "audio/webm" });
      const data = await voiceCommand(blob);
      setResult(data);
      if (data.cart) setCart(data.cart);
      setBusy(false);
      stream.getTracks().forEach((track) => track.stop());
    };
    recorder.start();
    setRecording(true);
  }

  function stopRecording() {
    recorderRef.current?.stop();
    setRecording(false);
  }

  return (
    <main className="mx-auto max-w-7xl px-4 py-8">
      <div className="grid gap-6 lg:grid-cols-[0.8fr_1.2fr]">
        <section className="card p-5">
          <h1 className="text-3xl font-black">Voice Shopping Assistant</h1>
          <p className="mt-2 text-slate-600">Speech is transcribed by Whisper, Gemini extracts JSON intent, and FastAPI performs the cart or search action.</p>

          <div className="mt-6 flex gap-3">
            {!recording ? (
              <button className="btn btn-primary" onClick={startRecording} disabled={busy}>
                <Mic size={18} />
                Start
              </button>
            ) : (
              <button className="btn btn-primary" onClick={stopRecording}>
                <Square size={18} />
                Stop
              </button>
            )}
          </div>

          <form onSubmit={runTextCommand} className="mt-6 space-y-3">
            <label className="text-sm font-bold" htmlFor="command">
              Typed command
            </label>
            <textarea
              id="command"
              className="input min-h-28 py-3"
              value={text}
              onChange={(event) => setText(event.target.value)}
              placeholder="Search for Oreo biscuits"
            />
            <button className="btn btn-primary" disabled={busy || !text.trim()}>
              <Send size={18} />
              Send
            </button>
          </form>
        </section>

        <section className="space-y-4">
          <div className="card p-5">
            <h2 className="text-xl font-black">Command Result</h2>
            {result ? (
              <div className="mt-3 space-y-2 text-sm">
                <p>
                  <span className="font-bold">Transcript:</span> {result.transcript}
                </p>
                <p>
                  <span className="font-bold">Intent JSON:</span> {JSON.stringify(result.intent)}
                </p>
                <p className="font-bold text-leaf">{result.message}</p>
              </div>
            ) : (
              <p className="mt-3 text-slate-500">No command sent yet.</p>
            )}
          </div>
          {result?.products?.length ? <ProductGrid products={result.products} /> : null}
        </section>
      </div>
    </main>
  );
}
