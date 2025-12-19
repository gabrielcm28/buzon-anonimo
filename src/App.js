import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [mensaje, setMensaje] = useState("");
  const [respuesta, setRespuesta] = useState("");
  const [mensajes, setMensajes] = useState([]);

  const enviarMensaje = async () => {
    if (!mensaje.trim()) return alert("El mensaje no puede estar vacío");

    try {
      const res = await fetch("http://localhost:8000/mensajes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mensaje }),
      });
      const data = await res.json();
      setRespuesta(data.status || "Mensaje enviado correctamente");
      setMensaje("");
      obtenerMensajes(); // Actualizar lista
    } catch (error) {
      console.error(error);
      setRespuesta("Error al enviar mensaje");
    }
  };

  const obtenerMensajes = async () => {
    try {
      const res = await fetch("http://localhost:8000/mensajes");
      const data = await res.json();
      setMensajes(data);
    } catch (error) {
      console.error(error);
    }
  };

  // Actualizar mensajes cada 5 segundos
  useEffect(() => {
    obtenerMensajes();
    const interval = setInterval(obtenerMensajes, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container">
      <h2>Enviar mensaje anónimo</h2>
      <textarea
        value={mensaje}
        onChange={(e) => setMensaje(e.target.value)}
        placeholder="Escribe tu mensaje..."
      />
      <button onClick={enviarMensaje}>Enviar</button>
      {respuesta && <div className="message">{respuesta}</div>}

      <h3>Mensajes recibidos (cifrados)</h3>
      <ul>
        {mensajes.map((m, i) => (
          <li key={i}>
            <strong>Mensaje:</strong> {m.mensaje} <br />
            <strong>Timestamp:</strong> {m.timestamp.toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;

