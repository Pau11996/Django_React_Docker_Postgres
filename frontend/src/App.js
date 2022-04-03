import './App.css';

import React, { useState,useEffect} from 'react';
import axios from 'axios';


function App() {

    const [category, setCategory ] = useState( {} )
    // const id = match.params.id

    useEffect( () => {
        axios({
            method: 'GET',
            url: "http://127.0.0.1:8000/api/category/1"

        }).then(response => {
            setCategory(response.data)

        })

    }, [])

    return (
        <div className="App">
          <h1>Hi Django + React</h1>

            <div>
                    <p>{category.name}</p>

            </div>



    </div>
    )


}

export default App;
