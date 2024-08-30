import "./App.css";
import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./components/HomePage";
import Header from "./components/Header";
import NavBar from "./components/NavBar";
import Scanner from "./components/Scanner";
import Forum from "./components/Forum";
import Rewards from "./components/Rewards";  // Renamed from Contact to Rewards
import FileDisplay from "./components/FileDisplay";

function App() {
  const [file, setFile] = useState(null);
  const [audioStream, setAudioStream] = useState(null);

  const isAudioAvailable = file || audioStream;

  function handleAudioReset() {
    setFile(null);
    setAudioStream(null);
  }

  return (
    <Router>
      <div className="w-full">
        <NavBar />
        <div className="flex flex-col px-4 lg:px-8">
          <Routes>
            <Route
              path="/"
              element={
                <section className="min-h-screen flex flex-col">
                  <Header />
                  {isAudioAvailable ? (
                    <FileDisplay
                      handleAudioReset={handleAudioReset}
                      file={file}
                      audioStream={audioStream}
                    />
                  ) : (
                    <HomePage setFile={setFile} setAudioStream={setAudioStream} />
                  )}
                </section>
              }
            />
            <Route path="/scanner" element={<Scanner />} />
            <Route path="/forum" element={<Forum />} />
            <Route path="/rewards" element={<Rewards />} />
          </Routes>
          <footer></footer>
        </div>
      </div>
    </Router>
  );
}

export default App;
