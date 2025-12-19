const API_URL = "https://buzon-anonimo.onrender.com";


export async function sendMessage(texto) {
  const res = await fetch(`${API_URL}/mensajes`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ mensaje: texto })
  });

  return res.json();
}

export async function getMessages() {
  const res = await fetch(`${API_URL}/mensajes/procesados`);
  return res.json();
}
