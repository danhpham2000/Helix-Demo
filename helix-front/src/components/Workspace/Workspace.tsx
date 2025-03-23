import { useEffect, useState } from "react";
import "./Workspace.css";

export default function Workspace() {
  const [steps, setSteps] = useState([
    {
      id: 1,
      description:
        "Step 1: Research Identify your target audience and gather information about them.",
    },
    {
      id: 2,
      description:
        "Step 2: Research Identify your target audience and gather information about them.",
    },
    {
      id: 3,
      description:
        "Step 3: Research Identify your target audience and gather information about them.",
    },
  ]);

  // update the sequence
  const handleUpdate = async () => {};

  const fetchSequence = async () => {
    const response = await fetch("http://localhost:5000/api/sequences", {
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();

    console.log(data);
  };

  useEffect(() => {
    fetchSequence();
  }, []);

  const [editingId, setEditingId] = useState(null);
  const [editText, setEditText] = useState("");

  const handleEdit = (step: any) => {
    setEditingId(step.id);
    setEditText(step.description);
  };

  const handleSave = () => {
    setSteps(
      steps.map((step) =>
        step.id === editingId ? { ...step, description: editText } : step
      )
    );
    setEditingId(null);
  };

  const handleCancel = () => {
    setEditingId(null);
  };

  return (
    <div className="workspace-container">
      <h4 className="workspace-header">Workspace</h4>

      <div className="step-container">
        {steps.map((step) => (
          <div className="card" key={step.id}>
            {editingId === step.id ? (
              <div className="edit-container">
                <textarea
                  className="edit-textarea"
                  value={editText}
                  onChange={(e) => setEditText(e.target.value)}
                />
                <div className="edit-buttons">
                  <button className="save-button" onClick={handleSave}>
                    Save
                  </button>
                  <button className="cancel-button" onClick={handleCancel}>
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <>
                <p className="step-description">{step.description}</p>
                <button
                  className="edit-button"
                  onClick={() => handleEdit(step)}
                >
                  Edit
                </button>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
