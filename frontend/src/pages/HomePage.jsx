import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { fetchGraph } from "../lib/api";
import GraphView from "../components/GraphView";

export default function HomePage() {
  const { session, logout } = useAuth();
  const navigate = useNavigate();
  const [graph, setGraph] = useState(null);
  const [loading, setLoading] = useState(true);
  const [logoutError, setLogoutError] = useState("");

  useEffect(() => {
    if (!session) return;
    let cancelled = false;
    fetchGraph(session.access_token)
      .then((data) => {
        if (!cancelled) setGraph(data);
      })
      .catch(() => {
        if (!cancelled) setGraph({ nodes: [], edges: [] });
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [session]);

  const handleLogout = async () => {
    setLogoutError("");
    try {
      await logout();
      navigate("/login");
    } catch {
      setLogoutError("Logout failed. Please try again.");
    }
  };

  if (loading) {
    return <div className="spinner">Loading...</div>;
  }

  const isEmpty =
    !graph || (graph.nodes.length === 0 && graph.edges.length === 0);

  return (
    <div className="home-container">
      <header className="app-header">
        <h1>BJJ Game Graph</h1>
        <button onClick={handleLogout} className="logout-button">
          Log out
        </button>
      </header>
      {logoutError && <div className="error-message">{logoutError}</div>}
      <main className="graph-area">
        {isEmpty ? (
          <p className="empty-state">
            Click &apos;Add Position&apos; to add your first position
          </p>
        ) : (
          <GraphView nodes={graph.nodes} edges={graph.edges} />
        )}
      </main>
    </div>
  );
}
