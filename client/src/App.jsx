import { useState, useEffect } from 'react'
import './App.css'
import axios from 'axios'
import ConsultaOllama from './ConsultaOllama'

function App() {
  const [count, setCount] = useState(0)
  const [array, setArray] = useState([])

  const fetchAPI = async () => {
    const response = await axios.get("http://127.0.0.1:5000/")
    setArray(response)
  }

  useEffect(() => {
    fetchAPI()
  },[])

  return (
    <div>
      <ConsultaOllama />
    </div>
  )
}

export default App
