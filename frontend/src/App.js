import { useEffect, useState } from "react";
import API from "./api";

function App() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    API.get("books/")
      .then((res) => setBooks(res.data.results))
      .catch((err) => console.log(err));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>📚 Bibliothèque</h1>

      {books.map((book) => (
        <div key={book.id}>
          <h3>{book.title}</h3>
          <p>{book.author}</p>
        </div>
      ))}
    </div>
  );
}

export default App;