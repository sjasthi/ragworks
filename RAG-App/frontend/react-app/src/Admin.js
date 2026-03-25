import React, { useEffect, useState } from "react";
import "./Admin.css";

const API = "http://127.0.0.1:5000";

const Admin = ({ logoutAction }) => {
  const [docs, setDocs] = useState([]);
  const [stats, setStats] = useState(null);

  const [filePath, setFilePath] = useState("");
  const [fileType, setFileType] = useState("pdf");
  const [replace, setReplace] = useState(false);

  const loadDocs = async () => {
    try {
      const res = await fetch(`${API}/admin/documents`);

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Documents request failed: ${res.status} ${res.statusText} - ${text}`);
      }

      const data = await res.json();
      setDocs(data.documents || []);
    } catch (err) {
      console.error("loadDocs error:", err);
      alert(`Could not load documents: ${err.message}`);
      setDocs([]);
    }
  };

  const loadStats = async () => {
    try {
      const res = await fetch(`${API}/admin/stats`);

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Stats request failed: ${res.status} ${res.statusText} - ${text}`);
      }

      const data = await res.json();
      setStats(data);
    } catch (err) {
      console.error("loadStats error:", err);
      alert(`Could not load stats: ${err.message}`);
      setStats(null);
    }
  };

  useEffect(() => {
    loadStats();
    loadDocs();
  }, []);


const uploadDoc = async () => {
  try {
    const cleanedPath = filePath.trim().replace(/^['"]|['"]$/g, "");

    const res = await fetch(`${API}/admin/upload`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        file_path: cleanedPath,
        file_type: fileType,
        replace,
      }),
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Upload failed: ${res.status} ${res.statusText} - ${text}`);
    }

    const data = await res.json();
    alert(data.result || data.error || "Done");
    setFilePath("");
    await loadStats();
    await loadDocs();
  } catch (err) {
    console.error("Upload error:", err);
    alert(`Upload failed: ${err.message}`);
  }
};
  const deleteDoc = async (source) => {
    if (!window.confirm("Delete this document from ChromaDB?")) return;

    try {
      const res = await fetch(`${API}/admin/documents`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Delete failed: ${res.status} ${res.statusText} - ${text}`);
      }

      const data = await res.json();
      alert(`Deleted. Collection size: ${data.collection_size}`);
      await loadStats();
      await loadDocs();
    } catch (err) {
      console.error("Delete error:", err);
      alert(`Delete failed: ${err.message}`);
    }
  };

  // HTML structure of the admin page
  // UI developments occur here, but all backend interactions are handled by the functions defined above.
  // Update visuals below as needed, but keep backend calls in their respective functions to maintain separation of concerns. 
  // Styles are in Admin.css.
  return (
    <div className="admin-page">
      <div className="admin-header">
        <h2>Admin Dashboard</h2>
        <button onClick={logoutAction}>Logout</button>
      </div>

      {/* Stats */}
      <div className="admin-card">
        <h3>ChromaDB Stats</h3>
        {stats ? (
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-label">Collection</div>
              <div className="stat-name">{stats.collection_name}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Unique Documents</div>
              <div className="stat-value">{stats.unique_documents}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Total Chunks</div>
              <div className="stat-value">{stats.total_chunks}</div>
            </div>
          </div>
        ) : (
          <p style={{ color: "var(--muted)", margin: 0 }}>Loading stats…</p>
        )}
      </div>

      {/* Upload */}
      <div className="admin-card">
        <h3>Upload Document</h3>
        <div className="admin-upload">
          <input
            type="text"
            placeholder="Enter full file path (e.g. C:\...\file.pdf)"
            value={filePath}
            onChange={(e) => setFilePath(e.target.value)}
          />
          <select value={fileType} onChange={(e) => setFileType(e.target.value)}>
            <option value="pdf">pdf</option>
            <option value="pptx">pptx</option>
            <option value="docx">docx</option>
            <option value="txt">txt</option>
            <option value="html">html</option>
          </select>
          <label>
            <input
              type="checkbox"
              checked={replace}
              onChange={(e) => setReplace(e.target.checked)}
            />
            Replace if exists
          </label>
          <button className="btn-primary" onClick={uploadDoc}>Upload</button>
        </div>
      </div>

      {/* Documents table */}
      <div className="admin-card">
        <h3>Documents in ChromaDB</h3>
        <div className="docs-toolbar">
          <button className="refresh-btn" onClick={() => { loadStats(); loadDocs(); }}>
            ↻ Refresh
          </button>
        </div>
        <table className="docs-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Uploaded</th>
              <th>Source Path</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {docs.map((d) => (
              <tr key={d.source}>
                <td className="doc-name">{d.display_name}</td>
                <td>{d.uploaded_at ? new Date(d.uploaded_at).toLocaleString() : "—"}</td>
                <td><span className="doc-path">{d.source}</span></td>
                <td>
                  <button className="btn-danger" onClick={() => deleteDoc(d.source)}>Delete</button>
                </td>
              </tr>
            ))}
            {docs.length === 0 && (
              <tr className="empty-row">
                <td colSpan={4}>No documents found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Admin;