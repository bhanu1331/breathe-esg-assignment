import { useEffect, useState } from "react";
import axios from "axios";

const API = import.meta.env.VITE_API_URL;

function App() {
  const [records, setRecords] = useState([]);
  const [file, setFile] = useState(null);
  const [source, setSource] = useState("sap");
  const [filter, setFilter] = useState("all");

  const fetchRecords = async () => {
    let url = `${API}/api/records/`;

    if (filter === "pending") {
      url = `${API}/api/records/pending/`;
    }

    if (filter === "suspicious") {
      url = `${API}/api/records/suspicious/`;
    }

    if (filter === "failed") {
      url = `${API}/api/records/failed/`;
    }

    const res = await axios.get(url);
    setRecords(res.data);
  };

  useEffect(() => {
    fetchRecords();
  }, [filter]);

  const uploadFile = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("tenant_id", 1);
    formData.append("uploaded_by", "bhanu");
    formData.append("file", file);

    await axios.post(
      `${API}/api/upload/${source}/`,
      formData
    );

    alert("Upload successful");
    setFile(null);
    fetchRecords();
  };

  const approveRecord = async (id) => {
    await axios.patch(`${API}/api/records/${id}/approve/`);
    fetchRecords();
  };

  const rejectRecord = async (id) => {
    await axios.patch(`${API}/api/records/${id}/reject/`);
    fetchRecords();
  };

  const lockRecord = async (id) => {
    await axios.patch(`${API}/api/records/${id}/lock/`);
    fetchRecords();
  };

  const badgeStyle = (status) => {
    if (status === "APPROVED") {
      return {
        backgroundColor: "#d1fae5",
        color: "#065f46",
        padding: "6px 12px",
        borderRadius: "20px",
        fontWeight: "bold",
      };
    }

    if (status === "REJECTED") {
      return {
        backgroundColor: "#fee2e2",
        color: "#991b1b",
        padding: "6px 12px",
        borderRadius: "20px",
        fontWeight: "bold",
      };
    }

    if (status === "LOCKED") {
      return {
        backgroundColor: "#dbeafe",
        color: "#1e40af",
        padding: "6px 12px",
        borderRadius: "20px",
        fontWeight: "bold",
      };
    }

    if (status === "FAILED") {
      return {
        backgroundColor: "#f3f4f6",
        color: "#111827",
        padding: "6px 12px",
        borderRadius: "20px",
        fontWeight: "bold",
      };
    }

    return {
      backgroundColor: "#fef3c7",
      color: "#92400e",
      padding: "6px 12px",
      borderRadius: "20px",
      fontWeight: "bold",
    };
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#f5f7fb",
        padding: "30px",
        fontFamily: "Arial",
      }}
    >
      <h1
        style={{
          textAlign: "center",
          marginBottom: "30px",
          color: "#1e293b",
        }}
      >
        Breathe ESG Analyst Review Dashboard
      </h1>

      <div
        style={{
          backgroundColor: "white",
          padding: "20px",
          borderRadius: "12px",
          boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
          marginBottom: "30px",
        }}
      >
        <h2>Upload ESG Source Data</h2>

        <div
          style={{
            display: "flex",
            gap: "15px",
            alignItems: "center",
            flexWrap: "wrap",
          }}
        >
          <select
            value={source}
            onChange={(e) => setSource(e.target.value)}
            style={{
              padding: "10px",
              borderRadius: "8px",
            }}
          >
            <option value="sap">SAP</option>
            <option value="utility">Utility</option>
            <option value="travel">Travel</option>
          </select>

          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button onClick={uploadFile}>
            Upload
          </button>

          <button onClick={() => setFilter("all")}>All</button>
          <button onClick={() => setFilter("pending")}>Pending</button>
          <button onClick={() => setFilter("suspicious")}>Suspicious</button>
          <button onClick={() => setFilter("failed")}>Failed</button>
        </div>
      </div>

      <div
        style={{
          backgroundColor: "white",
          padding: "20px",
          borderRadius: "12px",
          boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
          overflowX: "auto",
        }}
      >
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
          }}
        >
          <thead>
            <tr style={{ backgroundColor: "#e2e8f0" }}>
              <th>ID</th>
              <th>Activity</th>
              <th>Scope</th>
              <th>Value</th>
              <th>Unit</th>
              <th>Suspicious</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {records.map((record) => (
              <tr key={record.id}>
                <td>{record.id}</td>
                <td>{record.activity_type}</td>
                <td>{record.scope}</td>
                <td>{record.original_value}</td>
                <td>{record.original_unit}</td>
                <td>{record.suspicious ? "⚠ Yes" : "No"}</td>
                <td>
                  <span style={badgeStyle(record.status)}>
                    {record.status}
                  </span>
                </td>
                <td>
                  <button onClick={() => approveRecord(record.id)}>
                    Approve
                  </button>
                  <button onClick={() => rejectRecord(record.id)}>
                    Reject
                  </button>
                  <button onClick={() => lockRecord(record.id)}>
                    Lock
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;