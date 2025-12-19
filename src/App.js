import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [mensaje, setMensaje] = useState("");
  const [mensajes, setMensajes] = useState([]);
  const [status, setStatus] = useState("");

  const enviarMensaje = async () => {
    if (!mensaje.trim()) {
      setStatus("Mensaje vacío");
      return;
    }

    const res = await fetch("http://127.0.0.1:8000/mensajes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mensaje }),
    });

    const data = await res.json();
    setStatus(data.status);
    setMensaje("");
    obtenerMensajes();
  };

  const obtenerMensajes = async () => {
    const res = await fetch("http://127.0.0.1:8000/mensajes");
    const data = await res.json();
    setMensajes(data);
  };

  useEffect(() => {
    obtenerMensajes();
  }, []);

  return (
    <div className="App">
      <h1>Buzón Anónimo</h1>

      <div style={{ marginBottom: "20px" }}>
        <input
          value={mensaje}
          onChange={(e) => setMensaje(e.target.value)}
          placeholder="Escribe tu mensaje..."
          style={{ width: "250px", padding: "8px" }}
        />
        <button onClick={enviarMensaje} style={{ marginLeft: "10px" }}>
          Enviar
        </button>
      </div>

      <p>{status}</p>

      <h2>Mensajes almacenados:</h2>
      <ul>
        {mensajes.map((m, i) => (
          <li key={i}>
            <strong>Cifrado:</strong> {m.mensaje}
            <br />
            <small>Timestamp (ruidoso): {m.timestamp}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;


