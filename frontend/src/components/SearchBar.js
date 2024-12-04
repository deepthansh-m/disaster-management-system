import React, { useState } from "react";

function SearchBar() {
    const [query, setQuery] = useState("");

    const handleSearch = () => {
        console.log("Searching for:", query);
    };

    return (
        <div className="search-bar">
            <input
                type="text"
                placeholder="Search for location..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
            <button onClick={handleSearch}>Search</button>
        </div>
    );
}

export default SearchBar;
