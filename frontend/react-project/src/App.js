import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./components/HomePage";
import Header from "./components/Header";
import NavBar from "./components/NavBar";
import Scanner from "./components/Scanner";
import Forum from "./components/Forum";
import Contact from "./components/Rewards";

function App() {
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
                  <HomePage />
                </section>
              }
            />
            <Route path="/scanner" element={<Scanner />} />
            <Route path="/forum" element={<Forum />} />
            <Route path="/rewards" element={<Contact />} />
          </Routes>	
          <h1 className="text-green-400">hello</h1>
          <footer></footer>
        </div>
      </div>
    </Router>
  );
}

export default App;
