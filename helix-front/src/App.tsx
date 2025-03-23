import Workspace from "./components/Workspace/Workspace";
import "./App.css";
import ChatBot from "./components/Chat/Chat";

function App() {
  return (
    <div className="container">
      <ChatBot />
      <Workspace />
    </div>
  );
}

export default App;
