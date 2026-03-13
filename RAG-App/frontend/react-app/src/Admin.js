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
    const res = await fetch(`${API}/admin/documents`);
    const data = await res.json();
    setDocs(data.documents || []);
  };

  const loadStats = async () => {
    const res = await fetch(`${API}/admin/stats`);
    const data = await res.json();
    setStats(data);
  };

  useEffect(() => {
    loadStats();
    loadDocs();
  }, []);

  const uploadDoc = async () => {
    const res = await fetch(`${API}/admin/upload`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        file_path: filePath.trim().replace(/^['"]|['"]$/g, ""),
        file_type: fileType,
        replace,
      }),
    });
    const data = await res.json();
    alert(data.result || data.error || "Done");
    setFilePath("");
    await loadStats();
    await loadDocs();
  };

  const deleteDoc = async (source) => {
    if (!window.confirm("Delete this document from ChromaDB?")) return;

    const res = await fetch(`${API}/admin/documents`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source }),
    });
    const data = await res.json();
    alert(`Deleted. Collection size: ${data.collection_size}`);
    await loadStats();
    await loadDocs();
  };

  return (
    <div className="admin-page">
      <div className="admin-header">
        <h2>Admin</h2>
        <button onClick={logoutAction}>Logout</button>
      </div>

      <section>
        <h3>ChromaDB Stats</h3>
        {stats ? (
          <ul>
            <li>Collection: {stats.collection_name}</li>
            <li>Unique documents: {stats.unique_documents}</li>
            <li>Total chunks: {stats.total_chunks}</li>
          </ul>
        ) : (
          <p>Loading stats…</p>
        )}
      </section>

      <section>
        <h3>Upload Document</h3>
        <div className="admin-upload">
          <input
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
          <label style={{ display: "flex", gap: 6, alignItems: "center" }}>
            <input
              type="checkbox"
              checked={replace}
              onChange={(e) => setReplace(e.target.checked)}
            />
            Replace if exists
          </label>
          <button onClick={uploadDoc}>Upload</button>
        </div>
      </section>

      <section>
        <h3>Documents in ChromaDB</h3>
        <button onClick={() => { loadStats(); loadDocs(); }}>Refresh</button>

        <table style={{ width: "100%", marginTop: 10 }}>
          <thead>
            <tr>
              <th align="left">Name</th>
              <th align="left">Uploaded</th>
              <th align="left">Source Path</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {docs.map((d) => (
              <tr key={d.source}>
                <td>{d.display_name}</td>
                <td>{d.uploaded_at || "(unknown)"}</td>
                <td style={{ fontFamily: "monospace", fontSize: 12 }}>{d.source}</td>
                <td>
                  <button onClick={() => deleteDoc(d.source)}>Delete</button>
                </td>
              </tr>
            ))}
            {docs.length === 0 && (
              <tr>
                <td colSpan={4}>No documents found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </section>
    </div>
  );
};

export default Admin;