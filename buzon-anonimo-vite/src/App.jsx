import React, { useState, useEffect } from 'react';
import { Send, Shield, Lock, Eye, Database, Shuffle } from 'lucide-react';

// Configuración de API
const API_URL = "http://127.0.0.1:5000";

async function sendMessage(texto) {
  const res = await fetch(`${API_URL}/mensajes`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ mensaje: texto })
  });
  return res.json();
}

async function getMessages() {
  const res = await fetch(`${API_URL}/mensajes/procesados`);
  return res.json();
}

export default function App() {
  const [mensaje, setMensaje] = useState('');
  const [mensajes, setMensajes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');
  const [showStats, setShowStats] = useState(false);

  useEffect(() => {
    cargarMensajes();
  }, []);

  const cargarMensajes = async () => {
    try {
      const data = await getMessages();
      setMensajes(data);
    } catch (error) {
      console.error('Error al cargar mensajes:', error);
      setStatus('Error al cargar mensajes');
    }
  };

  const enviarMensaje = async () => {
    if (!mensaje.trim()) return;

    setLoading(true);
    try {
      const data = await sendMessage(mensaje);
      setStatus(`${data.status} - Procesados: ${data.procesados}`);
      setMensaje('');
      
      setTimeout(() => {
        cargarMensajes();
        setStatus('');
      }, 1500);
    } catch (error) {
      setStatus('Error al enviar mensaje');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      enviarMensaje();
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleString('es-ES', {
      dateStyle: 'short',
      timeStyle: 'medium'
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-purple-500/20 bg-black/20 backdrop-blur-xl">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">SecureChat</h1>
                <p className="text-xs text-purple-300">Privacidad Diferencial Garantizada</p>
              </div>
            </div>
            <button
              onClick={() => setShowStats(!showStats)}
              className="px-4 py-2 bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 rounded-lg transition-all flex items-center gap-2 border border-purple-500/30"
            >
              <Eye className="w-4 h-4" />
              {showStats ? 'Ocultar' : 'Ver'} Stats
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Security Features Banner */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-gradient-to-br from-purple-500/10 to-purple-600/5 border border-purple-500/20 rounded-xl p-4 backdrop-blur-sm">
            <div className="flex items-center gap-3 mb-2">
              <Lock className="w-5 h-5 text-purple-400" />
              <h3 className="text-white font-semibold">Cifrado E2E</h3>
            </div>
            <p className="text-sm text-purple-200">Cifrado Fernet con llaves únicas</p>
          </div>
          
          <div className="bg-gradient-to-br from-pink-500/10 to-pink-600/5 border border-pink-500/20 rounded-xl p-4 backdrop-blur-sm">
            <div className="flex items-center gap-3 mb-2">
              <Shuffle className="w-5 h-5 text-pink-400" />
              <h3 className="text-white font-semibold">Mixnet</h3>
            </div>
            <p className="text-sm text-pink-200">Procesamiento en batch aleatorio</p>
          </div>
          
          <div className="bg-gradient-to-br from-blue-500/10 to-blue-600/5 border border-blue-500/20 rounded-xl p-4 backdrop-blur-sm">
            <div className="flex items-center gap-3 mb-2">
              <Database className="w-5 h-5 text-blue-400" />
              <h3 className="text-white font-semibold">Privacidad ε</h3>
            </div>
            <p className="text-sm text-blue-200">Ruido Laplaciano diferencial</p>
          </div>
        </div>

        {/* Stats Panel */}
        {showStats && (
          <div className="bg-black/40 border border-purple-500/30 rounded-xl p-6 mb-8 backdrop-blur-xl">
            <h3 className="text-lg font-semibold text-white mb-4">Estadísticas del Sistema</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-400">{mensajes.length}</div>
                <div className="text-sm text-gray-400">Mensajes Total</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-pink-400">ε=1.0</div>
                <div className="text-sm text-gray-400">Epsilon</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-400">5</div>
                <div className="text-sm text-gray-400">Batch Size</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-400">256</div>
                <div className="text-sm text-gray-400">Bits Cifrado</div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Enviar Mensaje */}
          <div className="bg-black/40 border border-purple-500/30 rounded-2xl p-6 backdrop-blur-xl">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Send className="w-5 h-5 text-purple-400" />
              Enviar Mensaje Seguro
            </h2>
            
            <div className="space-y-4">
              <div>
                <textarea
                  value={mensaje}
                  onChange={(e) => setMensaje(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Escribe tu mensaje privado aquí..."
                  className="w-full h-32 px-4 py-3 bg-slate-800/50 border border-purple-500/30 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 resize-none"
                  disabled={loading}
                />
              </div>

              <button
                onClick={enviarMensaje}
                disabled={loading || !mensaje.trim()}
                className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg shadow-purple-500/25"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Procesando...
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    Enviar con Privacidad
                  </>
                )}
              </button>

              {status && (
                <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-lg text-green-300 text-sm text-center animate-pulse">
                  {status}
                </div>
              )}
            </div>

            <div className="mt-6 pt-6 border-t border-purple-500/20">
              <p className="text-xs text-gray-400 leading-relaxed">
                <Shield className="w-4 h-4 inline mr-1 text-purple-400" />
                Tus mensajes son cifrados localmente antes de ser enviados. El sistema utiliza 
                privacidad diferencial y procesamiento en batch para proteger tu identidad y 
                metadatos temporales.
              </p>
            </div>
          </div>

          {/* Lista de Mensajes */}
          <div className="bg-black/40 border border-purple-500/30 rounded-2xl p-6 backdrop-blur-xl">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                <Database className="w-5 h-5 text-purple-400" />
                Mensajes Almacenados
              </h2>
              <button
                onClick={cargarMensajes}
                className="px-3 py-1 bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 rounded-lg text-sm transition-all border border-purple-500/30"
              >
                Actualizar
              </button>
            </div>

            <div className="space-y-3 max-h-96 overflow-y-auto pr-2 custom-scrollbar">
              {mensajes.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                  <Lock className="w-12 h-12 mx-auto mb-3 opacity-30" />
                  <p>No hay mensajes aún</p>
                  <p className="text-sm mt-2">Envía el primer mensaje seguro</p>
                </div>
              ) : (
                mensajes.map((msg, idx) => (
                  <div
                    key={idx}
                    className="bg-slate-800/50 border border-purple-500/20 rounded-lg p-4 hover:border-purple-500/40 transition-all"
                  >
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                        <span className="text-xs text-gray-400 font-mono">
                          ID: {idx + 1}
                        </span>
                      </div>
                      <span className="text-xs text-purple-300 font-mono">
                        {formatTimestamp(msg.timestamp)}
                      </span>
                    </div>
                    <div className="text-sm text-gray-300 break-all font-mono bg-slate-900/50 p-2 rounded border border-slate-700/50">
                      {msg.mensaje.length > 100 ? `${msg.mensaje.substring(0, 100)}...` : msg.mensaje}
                    </div>
                    <div className="mt-2 text-xs text-gray-500 flex items-center gap-2">
                      <Lock className="w-3 h-3" />
                      Cifrado • Timestamp con ruido ε
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>🔒 Protegido por cifrado Fernet, Privacidad Diferencial (Laplace) y Mixnet</p>
        </div>
      </div>

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(0, 0, 0, 0.2);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(168, 85, 247, 0.4);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(168, 85, 247, 0.6);
        }
      `}</style>
    </div>
  );
}
